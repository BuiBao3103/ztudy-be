from django.utils.timezone import now, timedelta
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import StudySession


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
