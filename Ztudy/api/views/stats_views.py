import logging
import time

import redis
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils.timezone import now, timedelta
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import StudySession, User, MonthlyLevel
from ..pagination import CustomPagination
from ..serializers import LeaderboardUserSerializer

# Thiết lập logging
logger = logging.getLogger(__name__)


class StudyTimeStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        # Lấy study time
        daily_study = StudySession.objects.filter(user=user, date=today).aggregate(
            total=Sum('total_time')
        )['total'] or 0

        weekly_study = StudySession.objects.filter(user=user, date__gte=week_start).aggregate(
            total=Sum('total_time')
        )['total'] or 0

        monthly_study = StudySession.objects.filter(user=user, date__gte=month_start).aggregate(
            total=Sum('total_time')
        )['total'] or 0

        # Lấy rank từ Redis
        today_rank = "unranked"
        week_rank = "unranked"
        month_rank = "unranked"

        # Kiểm tra rank today
        if redis_client.exists('leaderboard:today:zset'):
            today_rank_pos = redis_client.zrevrank(
                'leaderboard:today:zset', user.id)
            if today_rank_pos is not None:
                today_rank = today_rank_pos + 1

        # Kiểm tra rank week
        if redis_client.exists('leaderboard:week:zset'):
            week_rank_pos = redis_client.zrevrank(
                'leaderboard:week:zset', user.id)
            if week_rank_pos is not None:
                week_rank = week_rank_pos + 1

        # Kiểm tra rank month
        if redis_client.exists('leaderboard:month:zset'):
            month_rank_pos = redis_client.zrevrank(
                'leaderboard:month:zset', user.id)
            if month_rank_pos is not None:
                month_rank = month_rank_pos + 1

        return Response({
            "study": {
                "today": round(daily_study, 1),
                "week": round(weekly_study, 1),
                "month": round(monthly_study, 1)
            },
            "rank": {
                "today": today_rank,
                "week": week_rank,
                "month": month_rank
            },
            "current_monthly_level": {
                "level": MonthlyLevel.get_role_from_time(monthly_study),
                "next_level": MonthlyLevel.next_level(MonthlyLevel.get_role_from_time(float(monthly_study))),
                "progress": round(MonthlyLevel.progress(MonthlyLevel.get_role_from_time(monthly_study), monthly_study), 1),
                "time_to_next_level": round(MonthlyLevel.time_to_next_level(MonthlyLevel.get_role_from_time(monthly_study), monthly_study), 1)
            }
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
            date_range = [
                week_start + timedelta(days=i) for i in range((today - week_start).days + 1)]
        elif filter_type == "this_month":
            date_range = [
                month_start + timedelta(days=i) for i in range((today - month_start).days + 1)]
        else:
            return Response({"error": "Invalid filter type"}, status=400)

        study_data = (
            StudySession.objects.filter(
                user=user, date__gte=date_range[0], date__lte=today)
            .annotate(study_date=TruncDate("date"))
            .values("study_date")
            .annotate(total_study=Sum("total_time"))
        )

        study_dict = {item["study_date"].strftime(
            "%Y-%m-%d"): round(item["total_study"], 2) for item in study_data}

        response_data = [
            {"date": date.strftime(
                "%Y-%m-%d"), "total_study": study_dict.get(date.strftime("%Y-%m-%d"), 0)}
            for date in date_range
        ]

        return Response({"data": response_data})


# Kết nối Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


class LeaderboardView(generics.ListAPIView):
    """
    API để lấy leaderboards với cập nhật gần thời gian thực và phân trang
    """
    pagination_class = CustomPagination
    serializer_class = LeaderboardUserSerializer

    def get(self, request, period):
        if period not in ['today', 'week', 'month']:
            return Response({"error": "Invalid period. Use: today, week, month"}, status=status.HTTP_400_BAD_REQUEST)

        current_time = time.time()
        next_update_timestamp = redis_client.get('leaderboard:next_update')
        is_updating = redis_client.get('leaderboard:updating')
        zset_key = f'leaderboard:{period}:zset'
        zset_exists = redis_client.exists(zset_key)

        # Tính thời gian đến lần cập nhật tiếp theo
        if next_update_timestamp:
            next_update_timestamp = float(next_update_timestamp)
            time_until_next_update = next_update_timestamp - current_time
            if time_until_next_update < 0:
                time_until_next_update = 0
        else:
            time_until_next_update = 0

        # Nếu đang cập nhật
        if is_updating:
            logger.info(f"Leaderboard {period} is being updated")
            return Response({
                'leaderboard': {
                    'page': 1,
                    'totalPages': 1,
                    'totalItems': 0,
                    'results': []
                },
                'message': "Leaderboard is being updated, please try again in a few seconds",
                'next_update_timestamp': next_update_timestamp,
                'seconds_until_next_update': 0
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Nếu ZSET không tồn tại
        if not zset_exists:
            logger.warning(f"Leaderboard {period} ZSET does not exist")
            return Response({
                'leaderboard': {
                    'page': 1,
                    'totalPages': 1,
                    'totalItems': 0,
                    'results': []
                },
                'message': "Leaderboard is being prepared or not ready, please try again shortly",
                'next_update_timestamp': next_update_timestamp,
                'seconds_until_next_update': int(time_until_next_update)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Lấy dữ liệu từ Redis
        total_users = redis_client.zcard(zset_key)
        paginator = self.pagination_class()
        page_size = paginator.get_page_size(request)
        page_number = request.query_params.get(paginator.page_query_param, 1)

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size - 1

        leaderboard_tuples = redis_client.zrevrange(
            zset_key, start_idx, end_idx, withscores=True)
        if not leaderboard_tuples:
            return Response({
                'leaderboard': {
                    'page': page_number,
                    'totalPages': 1,
                    'totalItems': total_users,
                    'results': []
                },
                'next_update_timestamp': next_update_timestamp,
                'seconds_until_next_update': int(time_until_next_update)
            })

        user_ids = []
        user_data_map = {}
        for i, (user_id, score) in enumerate(leaderboard_tuples):
            user_id_int = int(user_id.decode() if isinstance(
                user_id, bytes) else user_id)
            user_ids.append(user_id_int)
            user_data_map[user_id_int] = {
                'rank': start_idx + i + 1,
                'total_time': round(score / 10, 1)
            }

        users = User.objects.filter(id__in=user_ids)
        user_data_list = []
        for user in users:
            if user.id in user_data_map:
                user_dict = {
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar.url if hasattr(user, 'avatar') and user.avatar else None,
                    'rank': user_data_map[user.id]['rank'],
                    'total_time': user_data_map[user.id]['total_time']
                }
                user_data_list.append(user_dict)

        user_data_list.sort(key=lambda x: x['rank'])

        # Response cuối cùng
        response_data = {
            'leaderboard': {
                'page': page_number,
                'totalPages': (total_users + page_size - 1) // page_size,
                'totalItems': total_users,
                'results': user_data_list
            },
            'next_update_timestamp': next_update_timestamp,
            'seconds_until_next_update': int(time_until_next_update)
        }
        return Response(response_data)
