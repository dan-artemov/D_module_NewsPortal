import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_news_send_mail': {
        'task': 'news.tasks.weekly_news_send_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': ()
    },
}
# crontab(hour=8, minute=0, day_of_week='monday')
# crontab(hour=8, minute=0, day_of_week='thursday')