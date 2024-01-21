from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Response
from django.core.mail import send_mail


@receiver(post_save, sender = Response)
def response_created(sender, instance, created, **kwargs):
    if instance.approve is True:
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
