from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_notifications_task

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    # 'post_add' срабатывает, когда через админку или форму добавили категории к посту
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        subscribers_emails = list(set(subscribers_emails))

        if subscribers_emails:
            # Вызываем задачу Celery. Сама функция отработает в фоне
            send_notifications_task.delay(
                instance.preview(),
                instance.pk,
                instance.title,
                subscribers_emails
            )