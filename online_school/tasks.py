from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from online_school.models import Course
from users.models import User


@shared_task
def send_updated_info(pk):
    course = Course.objects.get(pk=pk)
    subscriptions = course.subscriptions.filter(is_active=True)
    emails = [sub.user.email for sub in subscriptions]
    message_header = f'Обновление курса {course.name}'
    message_body = 'Курс был обновлён'

    send_mail(message_header, message_body, settings.EMAIL_HOST_USER, emails)


@shared_task(name='check_last_login')
def check_last_login():
    users = User.objects.all()
    for user in users:
        if user.last_login:
            if timezone.now() > user.last_login + timedelta(days=30):
                user.is_active = False
                user.save()
