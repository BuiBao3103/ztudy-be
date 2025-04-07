broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
accept_content = ['pickle']
task_serializer = 'pickle'
result_serializer = 'pickle'
timezone = 'Asia/Ho_Chi_Minh'
imports = (
    'scheduler.leaderboard_tasks',
    'scheduler.monthly_tasks',
)
task_routes = {
    'scheduler.leaderboard_tasks.update_leaderboards': {'queue': 'celery'},
    'scheduler.monthly_tasks.reset_monthly_study_time': {'queue': 'celery'},
} 