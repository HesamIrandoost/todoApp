# core/celery.py
import os 
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()    

app.conf.beat_schedule = {
    'delete-done-tasks-every-10-min': {
        'task': 'todo.tasks.delete_done_tasks',  # مسیر درست
        'schedule': crontab(minute='*/20'), 
    },
}