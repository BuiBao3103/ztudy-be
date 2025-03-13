from django.db.models.functions import TruncDate
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import StudySession, User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
import redis
import time

from ..pagination import CustomPagination
from ..serializers import LeaderboardUserSerializer


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


redis_client = redis.Redis(host='localhost', port=6379, db=0)


class LeaderboardView(generics.ListAPIView):
    """
    API để lấy leaderboards với cập nhật gần thời gian thực và phân trang
    """
    pagination_class = CustomPagination
    serializer_class = LeaderboardUserSerializer

    def get(self, request, period):
        if period not in ['today', 'week', 'month']:
            return Response({"error": "Period must be one of: today, week, month"}, status=400)

        current_time = time.time()
        next_update_timestamp = redis_client.get('leaderboard:next_update')
        is_updating = redis_client.get('leaderboard:updating')
        zset_key = f'leaderboard:{period}:zset'
        zset_exists = redis_client.exists(zset_key)

        # Tính toán thời gian đến lần cập nhật tiếp theo
        if next_update_timestamp:
            next_update_timestamp = float(next_update_timestamp)
            time_until_next_update = next_update_timestamp - current_time
        else:
            time_until_next_update = 0

        # Nếu đang cập nhật, trả về thông báo ngay lập tức
        if is_updating:
            return Response({
                "message": "Leaderboard is being updated, please try again in a few seconds",
                "next_update_timestamp": next_update_timestamp,
                "seconds_until_next_update": 0
            }, status=503)

        # Nếu ZSET không tồn tại hoặc thời gian cập nhật đã hết, thông báo đang chuẩn bị
        if not zset_exists or time_until_next_update <= 0:
            return Response({
                "message": "Leaderboard is being prepared or not ready, please try again shortly",
                "next_update_timestamp": next_update_timestamp,
                "seconds_until_next_update": max(0, int(time_until_next_update))
            }, status=503)

        # Chỉ trả về dữ liệu nếu ZSET tồn tại và không đang cập nhật
        if zset_exists and not is_updating:
            # Lấy tổng số user để phân trang
            total_users = redis_client.zcard(zset_key)

            # Tạo instance phân trang
            paginator = self.pagination_class()
            page_size = paginator.get_page_size(request)

            # Lấy số trang từ request
            page_number = request.query_params.get(paginator.page_query_param, 1)
            try:
                page_number = int(page_number)
            except ValueError:
                page_number = 1

            # Tính toán chỉ số Redis
            start_idx = (page_number - 1) * page_size
            end_idx = start_idx + page_size - 1

            # Lấy dữ liệu từ Redis ZSET với xếp hạng
            leaderboard_tuples = redis_client.zrevrange(zset_key, start_idx, end_idx, withscores=True)

            if not leaderboard_tuples:
                return Response({
                    "leaderboard": {
                        "count": total_users,
                        "next": None,
                        "previous": None,
                        "results": []
                    },
                    "next_update_timestamp": next_update_timestamp,
                    "seconds_until_next_update": max(0, int(time_until_next_update))
                })

            # Trích xuất user IDs và ánh xạ rank/score
            user_ids = []
            user_data_map = {}
            for i, (user_id, score) in enumerate(leaderboard_tuples):
                user_id_int = int(user_id.decode()) if isinstance(user_id, bytes) else int(user_id)
                user_ids.append(user_id_int)
                user_data_map[user_id_int] = {
                    'rank': start_idx + i + 1,
                    'total_time': round(score / 10, 1)  # Chuyển từ scaled score về 1 chữ số thập phân
                }

            # Lấy thông tin user từ database
            users = User.objects.filter(id__in=user_ids)

            # Tạo danh sách dữ liệu user để serialize
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

            # Sắp xếp theo rank
            user_data_list.sort(key=lambda x: x['rank'])

            # Tạo thông tin phân trang
            base_url = request.build_absolute_uri().split('?')[0]
            next_page = page_number + 1 if (page_number * page_size) < total_users else None
            previous_page = page_number - 1 if page_number > 1 else None

            # Phản hồi với dữ liệu phân trang
            response_data = {
                "leaderboard": {
                    "count": total_users,
                    "next": f"{base_url}?page={next_page}" if next_page else None,
                    "previous": f"{base_url}?page={previous_page}" if previous_page else None,
                    "results": user_data_list
                },
                "next_update_timestamp": next_update_timestamp,
                "seconds_until_next_update": max(0, int(time_until_next_update))
            }

            return Response(response_data)

        # Trường hợp dự phòng (không nên xảy ra với logic trên)
        return Response({
            "message": "Waiting for next leaderboard update",
            "next_update_timestamp": next_update_timestamp,
            "seconds_until_next_update": max(0, int(time_until_next_update))
        }, status=503)
