import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news_bd.models import Post, Category
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from news.settings import DEFAULT_FROM_EMAIL
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(type_post='AR') & Post.objects.filter(time_post__gte = last_week)
    text = '\n\n'.join(['{} - {}'.format(p.title, p.preview()) for p in posts])
    html_content = '<br><br>'.join(['<b>{}</b> - {} <a href="http://127.0.0.1:8000/news/{}">Читать продолжение в источнике</a>'.format(p.title, p.preview(), p.id) for p in posts])
    categories = posts.values_list('category__category_name', flat=True)
    subscribers = Category.objects.filter(category_name__in = categories).values_list('subscribers__email', flat=True)
    for email in subscribers:
        msg = EmailMultiAlternatives(subject="Новые статьи!", body=text, from_email=DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()




# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour=18, minute=0),
            id="my_job",  # The `id` assigned to each job MUST be unique
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