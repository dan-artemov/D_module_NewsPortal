import logging
from datetime import timedelta
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import *

logger = logging.getLogger(__name__)


def my_job():
    subscriptions = Subscriber.objects.select_related('category', 'user')
    for subscription in subscriptions:
        category_name = subscription.category
        user = subscription.user
        user_email = user.email

        last_notification_date = timezone.now() - timedelta(days=7)

        new_posts = set(
            Post.objects.filter(data_create__gt=last_notification_date, categories=category_name))
        articles = []

        for article in new_posts:
            post_header = article.post_header
            data_create = article.data_create
            preview = article.preview()
            pk = article.pk
            # title = article.post_header
            link = f"http://127.0.0.1:8000/news/{pk}"

            articles.append({
                'text': preview,
                'link': link,
                'header': post_header,
                'data': data_create,
            })

        html_content = render_to_string(
            'daily_posts.html',
            {
                'articles': articles,
                'category': category_name,

            }
        )

        subject = "Новые статьи на портале"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        send_mail(subject, '', from_email, recipient_list, html_message=html_content)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique day_of_week="sun", hour="16", minute="25"
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")