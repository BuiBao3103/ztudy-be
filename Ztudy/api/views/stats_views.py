from django.db.models.functions import TruncDate
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from ..models import StudySession
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
import redis
import json
import time


class StudyTimeStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        daily_study = StudySession.objects.filter(user=user, date=today).aggregate(
            total=Sum('total_time')
        )['total'] or 0

        weekly_study = StudySession.objects.filter(user=user, date__gte=week_start).aggregate(
            total=Sum('total_time')
        )['total'] or 0

        monthly_study = StudySession.objects.filter(user=user, date__gte=month_start).aggregate(
            total=Sum('total_time')
        )['total'] or 0

        all_time = StudySession.objects.filter(user=user).aggregate(total=Sum('total_time'))['total'] or 0

        return Response({
            "daily_study": round(daily_study, 2),
            "weekly_study": round(weekly_study, 2),
            "monthly_study": round(monthly_study, 2),
            "all_time": round(all_time, 2)
        })


class StudyTimeChartView(APIView):
    permission_classes = [IsAuthenticated]

    filter_param = openapi.Parameter(
        'filter', openapi.IN_QUERY, description="Filter by time range: today, this_week, this_month",
        type=openapi.TYPE_STRING, enum=["today", "this_week", "this_month"]
    )

    @swagger_auto_schema(manual_parameters=[filter_param])
    def get(self, request):
        user = request.user
        filter_type = request.GET.get("filter", "this_week")
        today = now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        if filter_type == "today":
            date_range = [today]
        elif filter_type == "this_week":
            date_range = [week_start + timedelta(days=i) for i in range((today - week_start).days + 1)]
        elif filter_type == "this_month":
            date_range = [month_start + timedelta(days=i) for i in range((today - month_start).days + 1)]
        else:
            return Response({"error": "Invalid filter type"}, status=400)

        study_data = (
            StudySession.objects.filter(user=user, date__gte=date_range[0], date__lte=today)
            .annotate(study_date=TruncDate("date"))
            .values("study_date")
            .annotate(total_study=Sum("total_time"))
        )

        study_dict = {item["study_date"].strftime("%Y-%m-%d"): round(item["total_study"], 2) for item in study_data}

        response_data = [
            {"date": date.strftime("%Y-%m-%d"), "total_study": study_dict.get(date.strftime("%Y-%m-%d"), 0)}
            for date in date_range
        ]

        return Response({"data": response_data})


class LeaderboardView(APIView):
    """
    API to retrieve leaderboards
    """

    def get(self, request, period):
        # Connect to Redis
        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Check if period is valid
        if period not in ['today', 'week', 'month']:
            return Response({"error": "Period must be one of: today, week, month"}, status=400)

        # Get leaderboard from Redis
        leaderboard_data = redis_client.get(f'leaderboard:{period}')

        # Get next update time
        next_update_timestamp = redis_client.get('leaderboard:next_update')

        if next_update_timestamp:
            next_update_timestamp = float(next_update_timestamp)
            # Calculate seconds until next update (for backwards compatibility)
            time_until_next_update = next_update_timestamp - time.time()
        else:
            # If no data about update time
            next_update_timestamp = None
            time_until_next_update = 0

        if leaderboard_data:
            leaderboard = json.loads(leaderboard_data)
            return Response({
                "leaderboard": leaderboard,
                "next_update_timestamp": next_update_timestamp,
                "seconds_until_next_update": max(0, int(time_until_next_update))
            })
        else:
            # If no data in Redis, return pending status
            return Response({
                "message": "Creating leaderboard, please try again later",
                "next_update_timestamp": next_update_timestamp,
                "seconds_until_next_update": max(0, int(time_until_next_update))
            })
