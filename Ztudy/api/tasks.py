from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
import redis
import logging
from django.conf import settings
from .models import StudySession, User, MonthlyLevel  # Giả định model đã định nghĩa

# Thiết lập logging
logger = logging.getLogger(__name__)

# Kết nối Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@shared_task
def update_leaderboards():
    """
    Cập nhật leaderboards mỗi 30 phút và lưu vào Redis
    """
    logger.info("Starting leaderboard update at %s", timezone.now())
    now = timezone.now()
    today = date.today()

    # Tính toán ngày bắt đầu
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Thời gian cập nhật tiếp theo
    reset_interval = getattr(settings, 'LEADERBOARD_RESET_INTERVAL', 30)  # Mặc định 30 phút
    next_update = now + timedelta(minutes=reset_interval)

    # Acquire lock với SETNX
    lock_acquired = redis_client.setnx('leaderboard:updating:lock', 'true')
    if not lock_acquired:
        logger.warning("Another process is updating leaderboard")
        return

    try:
        redis_client.expire('leaderboard:updating:lock', 300)
        redis_client.set('leaderboard:updating', 'true', ex=300)
        redis_client.set('leaderboard:next_update', next_update.timestamp())

        # Xóa ZSET cũ
        redis_client.delete('leaderboard:today:zset')
        redis_client.delete('leaderboard:week:zset')
        redis_client.delete('leaderboard:month:zset')

        # Cập nhật leaderboards
        update_daily_leaderboard(today)
        update_date_range_leaderboard(start_of_week, today, 'leaderboard:week')
        update_date_range_leaderboard(start_of_month, today, 'leaderboard:month')

        # Đặt thời gian hết hạn
        expiration_time = int((reset_interval + 5) * 60)
        for key in ['leaderboard:today:zset', 'leaderboard:week:zset', 'leaderboard:month:zset']:
            redis_client.expire(key, expiration_time)
        logger.info("Leaderboard update completed successfully")
    except Exception as e:
        logger.error(f"Error updating leaderboard: {str(e)}")
        raise
    finally:
        redis_client.delete('leaderboard:updating')
        redis_client.delete('leaderboard:updating:lock')


def update_daily_leaderboard(target_date):
    """Cập nhật bảng xếp hạng hàng ngày"""
    offset = 0
    batch_size = 1000
    has_data = False
    
    while True:
        sessions = StudySession.objects.filter(date=target_date).values(
            'user_id', 'total_time'
        )[offset:offset + batch_size]
        logger.info(f"Fetched {len(sessions)} daily sessions at offset {offset}")

        if not sessions:
            break

        has_data = True
        for session in sessions:
            scaled_time = int(session['total_time'] * 10)
            redis_client.zincrby('leaderboard:today:zset', scaled_time, session['user_id'])
        offset += batch_size

    # Nếu không có data, tạo ZSET với một dummy entry và xóa nó ngay
    if not has_data:
        redis_client.zadd('leaderboard:today:zset', {'dummy': 0})
        redis_client.zrem('leaderboard:today:zset', 'dummy')
        logger.info("Created empty daily leaderboard")


def update_date_range_leaderboard(start_date, end_date, key_name):
    """Cập nhật bảng xếp hạng theo khoảng thời gian"""
    offset = 0
    batch_size = 1000
    has_data = False
    
    while True:
        sessions = StudySession.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('user_id', 'total_time')[offset:offset + batch_size]
        logger.info(f"Fetched {len(sessions)} sessions for {key_name} at offset {offset}")

        if not sessions:
            break

        has_data = True
        user_times = {}
        for session in sessions:
            user_id = session['user_id']
            user_times[user_id] = user_times.get(user_id, 0) + session['total_time']

        for user_id, time_value in user_times.items():
            scaled_time = int(time_value * 10)
            redis_client.zincrby(f'{key_name}:zset', scaled_time, user_id)
        offset += batch_size

    # Nếu không có data, tạo ZSET với một dummy entry và xóa nó ngay
    if not has_data:
        redis_client.zadd(f'{key_name}:zset', {'dummy': 0})
        redis_client.zrem(f'{key_name}:zset', 'dummy')
        logger.info(f"Created empty leaderboard for {key_name}")


@shared_task
def reset_monthly_study_time():
    """Reset monthly study time và level cho tất cả users vào đầu tháng"""
    try:
        # Reset monthly_study_time về 0 và level về MEMBER
        updated_count = User.objects.all().update(
            monthly_study_time=0,
        )
        
        logger.info(
            f"Successfully reset monthly stats for {updated_count} users at {timezone.now()}"
        )
        return f"Reset completed for {updated_count} users"
    except Exception as e:
        logger.error(f"Error resetting monthly stats: {str(e)}")
        raise
