from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Response


@receiver(post_save, sender = Response)
def response_created(instance, created, **kwargs):
    if created and instance.approve:
        mail_subject = 'Ваш отклик принят'
        message = f'Ваш отклик на пост "{instance.responsePost}" был принят.'
        to_email = instance.responseUser.email
        send_notification_email(mail_subject, message, to_email)

    elif created and not instance.approve:
        mail_subject = 'Новый отклик на ваш пост'
        message = f'На ваш пост "{instance.responsePost}" пришел новый отклик.'
        to_email = instance.responsePost.postAuthor.email
        send_notification_email(mail_subject, message, to_email)


@receiver(post_delete, sender = Response)
def response_deleted(instance, **kwargs):
    mail_subject = 'Ваш отклик отклонен'
    message = f'Ваш отклик на пост "{instance.responsePost}" был отклонен.'
    to_email = instance.responseUser.email
    send_notification_email(mail_subject, message, to_email)


def send_notification_email(mail_subject, message, to_email):
    from_email = 'natanat2@yandex.ru'
    msg = EmailMultiAlternatives(mail_subject, message, from_email, [to_email])
    msg.send()
