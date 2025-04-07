from django.apps import AppConfig
import threading
import time
import os


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'
    _task_scheduled = False

    def ready(self):
        # Only run in the main process, not in auto-reloader
        if os.environ.get('RUN_MAIN') != 'true':
            return

        # Ensure task is only scheduled once
        if SchedulerConfig._task_scheduled:
            return

        # Schedule the initial leaderboard update with a delay
        def delayed_leaderboard_update():
            # Wait for 5 seconds to ensure the app is fully loaded
            time.sleep(5)
            try:
                from .leaderboard_tasks import update_leaderboards
                print("Scheduling initial leaderboard update...")
                update_leaderboards()
                print("Leaderboard update scheduled successfully!")
            except Exception as e:
                print(f"Error scheduling update_leaderboards: {e}")

        # Start a thread to run the task after a delay
        thread = threading.Thread(target=delayed_leaderboard_update)
        thread.daemon = True  # Thread will exit when the main program exits
        thread.start()
        
        # Mark task as scheduled
        SchedulerConfig._task_scheduled = True
