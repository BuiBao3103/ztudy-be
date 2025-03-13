from django.apps import AppConfig
import os
import sys

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Chỉ chạy trong tiến trình chính của runserver, không chạy trong StatReloader
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            try:
                from api.tasks import update_leaderboards
                update_leaderboards()
                print("Leaderboard updated on server startup!")
            except Exception as e:
                print(f"Error running update_leaderboards: {e}")