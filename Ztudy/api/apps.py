from django.apps import AppConfig
import os
import sys
from django.db.models.signals import post_migrate


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Import here to avoid circular imports
        from scheduler.tasks import update_leaderboards

        def schedule_leaderboard_update(sender, **kwargs):
            if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
                try:
                    update_leaderboards.delay()  # Use .delay() for Celery task
                    print("Leaderboard update scheduled on server startup!")
                except Exception as e:
                    print(f"Error scheduling update_leaderboards: {e}")

        post_migrate.connect(schedule_leaderboard_update, sender=self)