from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email=input('Введите почту(логин): '),
            first_name=input('Введите имя: '),
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        superuser.set_password(input('Введите пароль: '))
        superuser.save()
