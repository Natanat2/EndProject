from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Post, Response


@receiver(post_save, sender = Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        mail = User.objects.values_list('email', flat = True)
        send_mail(
            'Новое объявление',
            f'Вышло новое объявление {instance.title}',
            'natanat2@yandex.ru',
            list(mail),
            fail_silently = False,
        )


@receiver(post_save, sender = Response)
def response_created(sender, instance, created, **kwargs):
    if instance.approve:
        mail = instance.responseUser.email
        send_mail(
            'Ваш отклик приняли',
            f'Ваш отклик на пост {instance.responsePost} приняли',
            'natanat2@yandex.ru',
            [mail],
            fail_silently = False,
        )
    mail = instance.responsePost.responseUser.email
    send_mail(
        'Пришел новый отклик',
        f'На ваш пост {instance.responsePost} пришел новый отклик',
        'natanat2@yandex.ru',
        [mail],
        fail_silently = False,
    )
