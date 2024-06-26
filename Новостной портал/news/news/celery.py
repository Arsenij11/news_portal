import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_last_news': {
        'task': 'news_bd.tasks.last_news',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}