# ztudy/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ztudy.settings')

app = Celery('Ztudy')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cấu hình celery sử dụng JSON cho task mới, nhưng vẫn chấp nhận pickle cho task cũ
app.conf.accept_content = ['json', 'pickle']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'

app.autodiscover_tasks()