from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
import redis
import json
import time
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudySession, User  # Giả định User và StudySession đã được định nghĩa
from .serializers import LeaderboardUserSerializer  # Giả định serializer đã được định nghĩa
from .pagination import CustomPagination  # Giả định pagination đã được định nghĩa

# Kết nối Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


# Task để cập nhật leaderboards
@shared_task
def update_leaderboards():
    """
    Cập nhật leaderboards mỗi 30 phút và lưu vào Redis
    """
    now = timezone.now()
    today = date.today()

    # Tính toán ngày bắt đầu
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Tính toán thời điểm cập nhật tiếp theo
    reset_interval = settings.LEADERBOARD_RESET_INTERVAL  # Giả định giá trị trong settings
    next_update = (now + timedelta(minutes=reset_interval)).replace(
        minute=(now.minute // reset_interval) * reset_interval,
        second=0,
        microsecond=0
    )
    if now.minute % reset_interval == 0:
        next_update += timedelta(minutes=reset_interval)

    # Acquire lock với SETNX
    lock_acquired = redis_client.setnx('leaderboard:updating:lock', 'true')
    if not lock_acquired:
        return  # Đã có process khác đang cập nhật

    try:
        # Đặt khóa với thời gian hết hạn dài hơn (300 giây thay vì 60)
        redis_client.expire('leaderboard:updating:lock', 300)
        redis_client.set('leaderboard:updating', 'true', ex=300)
        redis_client.set('leaderboard:next_update', next_update.timestamp())

        # Xóa ZSET cũ ngay lập tức để tránh trả về dữ liệu cũ
        redis_client.delete('leaderboard:today:zset')
        redis_client.delete('leaderboard:week:zset')
        redis_client.delete('leaderboard:month:zset')

        # Tạo leaderboards bằng ZSETs
        update_daily_leaderboard(today)
        update_date_range_leaderboard(start_of_week, today, 'leaderboard:week')
        update_date_range_leaderboard(start_of_month, today, 'leaderboard:month')

        # Đặt thời gian hết hạn cho tất cả leaderboards
        expiration_time = int((reset_interval + 5) * 60)
        for key in ['leaderboard:today:zset', 'leaderboard:week:zset', 'leaderboard:month:zset']:
            redis_client.expire(key, expiration_time)
    finally:
        # Xóa trạng thái cập nhật
        redis_client.delete('leaderboard:updating')
        redis_client.delete('leaderboard:updating:lock')


def update_daily_leaderboard(target_date):
    # Xử lý theo batch để tránh vấn đề bộ nhớ
    offset = 0
    batch_size = 1000

    while True:
        sessions = StudySession.objects.filter(date=target_date).values(
            'user_id', 'total_time'
        )[offset:offset + batch_size]

        if not sessions:
            break

        # Thêm vào Redis ZSET - lưu user_id thay vì username
        for session in sessions:
            scaled_time = int(session['total_time'] * 10)  # Lưu thời gian với 1 chữ số thập phân
            redis_client.zincrby(
                'leaderboard:today:zset',
                scaled_time,
                session['user_id']
            )

        offset += batch_size


def update_date_range_leaderboard(start_date, end_date, key_name):
    # Xử lý theo batch
    offset = 0
    batch_size = 1000

    while True:
        sessions = StudySession.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('user_id', 'total_time')[offset:offset + batch_size]

        if not sessions:
            break

        # Tổng hợp thời gian theo user trước khi thêm vào Redis
        user_times = {}
        for session in sessions:
            user_id = session['user_id']
            user_times[user_id] = user_times.get(user_id, 0) + session['total_time']

        # Thêm vào Redis ZSET với user_id và thời gian đã scale
        for user_id, time_value in user_times.items():
            scaled_time = int(time_value * 10)
            redis_client.zincrby(key_name + ':zset', scaled_time, user_id)

        offset += batch_size