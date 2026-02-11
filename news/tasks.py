from celery import shared_task
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from django.contrib.auth.models import User

@shared_task
def send_notifications_task(preview, pk, title, subscribers_emails):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def weekly_newsletter():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    if not posts:
        return

    subscribers = User.objects.filter(categories__isnull=False).distinct()
    for user in subscribers:
        user_categories = user.categories.all()
        user_posts = posts.filter(categories__in=user_categories).distinct()
        if user_posts:
            html_content = render_to_string(
                'weekly_newsletter.html',
                {
                    'link': settings.SITE_URL,
                    'posts': user_posts,
                    'user': user,
                }
            )
            msg = EmailMultiAlternatives(
                subject='Новости за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()