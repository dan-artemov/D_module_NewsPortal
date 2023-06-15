from celery import shared_task

# import time
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from news.models import *
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)

@shared_task
def weekly_news_send_mail():
    subscriptions = Subscriber.objects.select_related('category', 'user')
    for subscription in subscriptions:
        category_name = subscription.category
        user = subscription.user
        user_email = user.email

        last_notification_date = timezone.now() - timedelta(days=7)

        new_posts = set(
            Post.objects.filter(data_create__gt=last_notification_date, categories=category_name))
        articles = []

        for article in new_posts:
            post_header = article.post_header
            data_create = article.data_create
            preview = article.preview()
            pk = article.pk
            # title = article.post_header
            link = f"http://127.0.0.1:8000/news/{pk}"

            articles.append({
                'text': preview,
                'link': link,
                'header': post_header,
                'data': data_create,
            })

        html_content = render_to_string(
            'daily_posts.html',
            {
                'articles': articles,
                'category': category_name,

            }
        )

        subject = "Новые статьи на портале"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        send_mail(subject, '', from_email, recipient_list, html_message=html_content)

@shared_task
def send_new_post_to_subscribers(text_content, html_content, subscribers_email, subject):

    for email in subscribers_email:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
