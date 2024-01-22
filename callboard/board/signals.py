from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from .models import Post, Response


@receiver(post_save, sender = Post)
def post_created(instance, created, **kwargs):
    if created:
        emails = User.objects.filter(subscriptions__category = instance.postCategory).values_list('email', flat = True)
        subject = 'Новое объявление'
        text_content = (
            f'Вышло новое объявление {instance.title}\n'
            f'Ссылка на новое объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Вышло новое объявление {instance.title}<br>'
            f'Ссылка на новое объявление: <a href= "http://127.0.0.1:8000{instance.get_absolute_url()}">Подробнее</a>'

        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@receiver(post_save, sender = Response)
def response_created(instance, created, **kwargs):
    if instance.approve:
        mail = instance.responseUser.email
        msg = EmailMultiAlternatives(
            'Ваш отклик приняли',
            f'Ваш отклик на пост {instance.responsePost} приняли',
            'natanat2@yandex.ru',
            [mail],
        )
        msg.send()
    mail = instance.responsePost.postAuthor.email
    msg = EmailMultiAlternatives(
        'Пришел новый отклик',
        f'На ваш пост {instance.responsePost} пришел новый отклик',
        'natanat2@yandex.ru',
        [mail],
    )
    msg.send()
