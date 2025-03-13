# api/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
import redis
import json
from .models import StudySession

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@shared_task
def update_leaderboards():
    """
    Update leaderboards every 30 minutes and save to Redis
    """
    # Get current time
    now = timezone.now()
    today = date.today()

    # Calculate start dates for current week and month
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Calculate next update time
    next_update = (now + timedelta(minutes=30)).replace(minute=now.minute // 30 * 30, second=0, microsecond=0)
    if now.minute % 30 == 0:
        next_update += timedelta(minutes=30)

    # Save next update time to Redis
    redis_client.set('leaderboard:next_update', next_update.timestamp())

    # Get data and create leaderboards
    # 1. Today's leaderboard
    today_leaderboard = generate_daily_leaderboard(today)

    # 2. This week's leaderboard
    weekly_leaderboard = generate_date_range_leaderboard(start_of_week, today)

    # 3. This month's leaderboard
    monthly_leaderboard = generate_date_range_leaderboard(start_of_month, today)

    # Save leaderboards to Redis with 35 minute expiration
    redis_client.setex('leaderboard:today', 60 * 35, json.dumps(today_leaderboard))
    redis_client.setex('leaderboard:week', 60 * 35, json.dumps(weekly_leaderboard))
    redis_client.setex('leaderboard:month', 60 * 35, json.dumps(monthly_leaderboard))


def generate_daily_leaderboard(target_date):
    """
    Generate leaderboard for a specific day
    """
    # Get total study time for each user in the day
    study_sessions = StudySession.objects.filter(date=target_date)

    user_times = {}
    for session in study_sessions:
        username = session.user.username
        if username in user_times:
            user_times[username] += session.total_time
        else:
            user_times[username] = session.total_time

    # Create leaderboard
    leaderboard = [{"username": username, "total_time": time} for username, time in user_times.items()]

    # Sort by time in descending order
    leaderboard.sort(key=lambda x: x["total_time"], reverse=True)

    # Add ranking
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1

    return leaderboard


def generate_date_range_leaderboard(start_date, end_date):
    """
    Generate leaderboard for a date range
    """
    # Get total study time for each user in the date range
    study_sessions = StudySession.objects.filter(date__gte=start_date, date__lte=end_date)

    user_times = {}
    for session in study_sessions:
        username = session.user.username
        if username in user_times:
            user_times[username] += session.total_time
        else:
            user_times[username] = session.total_time

    # Create leaderboard
    leaderboard = [{"username": username, "total_time": time} for username, time in user_times.items()]

    # Sort by time in descending order
    leaderboard.sort(key=lambda x: x["total_time"], reverse=True)

    # Add ranking
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1

    return leaderboard