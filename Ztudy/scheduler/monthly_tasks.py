from celery import shared_task
from django.utils import timezone
import logging
from core.models import User

logger = logging.getLogger(__name__)


class MonthlyTasks:
    def _reset_monthly_study_time(self):
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


# Define the task at module level
@shared_task(name='scheduler.monthly_tasks.reset_monthly_study_time')
def reset_monthly_study_time():
    """
    Reset monthly study time và level cho tất cả users vào đầu tháng
    """
    print("Starting monthly study time reset task...")
    tasks = MonthlyTasks()
    tasks._reset_monthly_study_time()
