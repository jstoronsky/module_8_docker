from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class User(AbstractUser):
    """
    модель пользователя
    """
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    is_active = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар пользователя', **NULLABLE)
    city = models.CharField(max_length=40, verbose_name='город', **NULLABLE)
    phone_number = models.CharField(max_length=15, verbose_name='номер телефона', **NULLABLE)
    verification_key = models.CharField(max_length=4, verbose_name='ключ для верификации', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
