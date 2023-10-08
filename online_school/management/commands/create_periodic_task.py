from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        interval = IntervalSchedule.objects.create(every=1, period='days')
        PeriodicTask.objects.create(
            name='check last login', task='check_last_login',
            interval=interval,
            start_time=timezone.now()
        )
