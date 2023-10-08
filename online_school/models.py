from django.db import models
from users.models import NULLABLE
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    added_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='добавил', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='lesson/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    video_link = models.CharField(max_length=250, verbose_name='ссылка', **NULLABLE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    added_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='добавил', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    CASH = "Наличные"
    DEBIT_CARD = "Безналичные"

    PAYMENT_CHOICES = [
        (CASH, "Наличные"),
        (DEBIT_CARD, "Безналичные"),
    ]

    sum_of_payment = models.IntegerField(verbose_name='cумма платежа')
    date_of_payment = models.DateField(verbose_name='дата платежа')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='оплаченный курс')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='способ оплаты')
    payment_url = models.CharField(max_length=500, verbose_name='ссылка на оплату', **NULLABLE)

    def __str__(self):
        return f'{self.date_of_payment} - {self.sum_of_payment}'

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс',
                               related_name='subscriptions', **NULLABLE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь',
                             related_name='subscriptions', **NULLABLE)
    is_active = models.BooleanField(verbose_name='активна ли подписка? ', **NULLABLE)

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
