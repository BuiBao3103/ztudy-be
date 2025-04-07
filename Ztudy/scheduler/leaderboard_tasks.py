from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
import redis
from django.conf import settings
from core.models import StudySession


class LeaderboardTasks:
    LOCK_KEY = 'leaderboard:updating:lock'
    TODAY_ZSET = 'leaderboard:today:zset'
    WEEK_ZSET = 'leaderboard:week:zset'
    MONTH_ZSET = 'leaderboard:month:zset'
    WEEK_KEY = 'leaderboard:week'
    MONTH_KEY = 'leaderboard:month'

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def update_daily_leaderboard(self, target_date):
        """Cập nhật bảng xếp hạng hàng ngày"""
        offset = 0
        batch_size = 1000
        has_data = False

        while True:
            sessions = StudySession.objects.filter(date=target_date).values(
                'user_id', 'total_time'
            )[offset:offset + batch_size]
            print(f"Fetched {len(sessions)} daily sessions at offset {offset}")

            if not sessions:
                break

            has_data = True
            for session in sessions:
                scaled_time = int(session['total_time'] * 10)
                self.redis_client.zincrby(
                    self.TODAY_ZSET, scaled_time, session['user_id'])
            offset += batch_size

        if not has_data:
            self.redis_client.zadd(self.TODAY_ZSET, {'dummy': 0})
            self.redis_client.zrem(self.TODAY_ZSET, 'dummy')
            print("Created empty daily leaderboard")

    def update_date_range_leaderboard(self, start_date, end_date, key_name):
        """Cập nhật bảng xếp hạng theo khoảng thời gian"""
        offset = 0
        batch_size = 1000
        has_data = False

        while True:
            sessions = StudySession.objects.filter(
                date__gte=start_date,
                date__lte=end_date
            ).values('user_id', 'total_time')[offset:offset + batch_size]
            print(f"Fetched {len(sessions)} sessions for {key_name} at offset {offset}")

            if not sessions:
                break

            has_data = True
            user_times = {}
            for session in sessions:
                user_id = session['user_id']
                user_times[user_id] = user_times.get(
                    user_id, 0) + session['total_time']

            for user_id, time_value in user_times.items():
                scaled_time = int(time_value * 10)
                self.redis_client.zincrby(
                    f'{key_name}:zset', scaled_time, user_id)
            offset += batch_size

        if not has_data:
            self.redis_client.zadd(f'{key_name}:zset', {'dummy': 0})
            self.redis_client.zrem(f'{key_name}:zset', 'dummy')
            print(f"Created empty leaderboard for {key_name}")

    def _update_leaderboards(self):
        """
        Internal method to update leaderboards
        """
        print(f"Starting leaderboard update at {timezone.now()}")
        now = timezone.now()
        today = date.today()

        # Tính toán ngày bắt đầu
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        # Thời gian cập nhật tiếp theo
        reset_interval = getattr(settings, 'LEADERBOARD_RESET_INTERVAL', 30)
        next_update = now + timedelta(minutes=reset_interval)

        # Acquire lock với SETNX
        lock_acquired = self.redis_client.setnx(
            self.LOCK_KEY, 'true')
        if not lock_acquired:
            print("Another process is updating leaderboard")
            return

        try:
            self.redis_client.expire(self.LOCK_KEY, 300)
            self.redis_client.set('leaderboard:updating', 'true', ex=300)
            self.redis_client.set(
                'leaderboard:next_update', next_update.timestamp())

            # Xóa ZSET cũ
            self.redis_client.delete(self.TODAY_ZSET)
            self.redis_client.delete(self.WEEK_ZSET)
            self.redis_client.delete(self.MONTH_ZSET)

            # Cập nhật leaderboards
            self.update_daily_leaderboard(today)
            self.update_date_range_leaderboard(
                start_of_week, today, self.WEEK_KEY)
            self.update_date_range_leaderboard(
                start_of_month, today, self.MONTH_KEY)

            # Đặt thời gian hết hạn
            expiration_time = int((reset_interval + 5) * 60)
            for key in [self.TODAY_ZSET, self.WEEK_ZSET, self.MONTH_ZSET]:
                self.redis_client.expire(key, expiration_time)
            print("Leaderboard update completed successfully")
        except Exception as e:
            print(f"Error updating leaderboard: {str(e)}")
            raise
        finally:
            self.redis_client.delete('leaderboard:updating')
            self.redis_client.delete(self.LOCK_KEY)


# Define the task at module level
@shared_task(name='scheduler.leaderboard_tasks.update_leaderboards')
def update_leaderboards():
    """
    Cập nhật leaderboards mỗi 30 phút và lưu vào Redis
    """
    print("Starting leaderboard update task...")
    tasks = LeaderboardTasks()
    tasks._update_leaderboards()
