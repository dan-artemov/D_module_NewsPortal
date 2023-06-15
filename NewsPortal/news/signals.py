# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import post_save

from django.db.models.signals import m2m_changed
# from django.template.loader import render_to_string
# from django.conf import settings

from django.dispatch import receiver
from .tasks import send_new_post_to_subscribers
from .models import *


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':


        categories = instance.categories.all()

        subscribers_email = []

        for cat in categories:
            subscribers = Subscriber.objects.filter(category=cat)

            for sub in subscribers:
                subscribers_email += [sub.user.email]
        # Для удаления дубликатов из списка преобразуем полученный список в множество, а затем снова в список
        subscribers_email = list(set(subscribers_email))

        subject = f'Новая статья в категориях, на которые вы подписаны'

        text_content = (
            f'Заголовок: {instance.post_header}\n'
            f'Краткое содержание: {instance.preview()}\n\n'
            f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}')
        html_content = (
            f'Заголовок: {instance.post_header}<br>'
            f'Краткое содержание: {instance.post_text[:124]}+ "..."<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на статью</a>')
        # Вызываем tasks для отправки сообщения пользователям
        send_new_post_to_subscribers.delay(text_content, html_content, subscribers_email, subject)

