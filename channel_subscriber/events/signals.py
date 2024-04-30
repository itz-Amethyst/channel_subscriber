from django.db.models.signals import post_save
from django.dispatch import receiver

from channel_subscriber.models import Lesson


@receiver(post_save, sender=Lesson)
def update_lessons_count(sender, instance, **kwargs):
    if instance.section:
        instance.section.update_lessons_count()