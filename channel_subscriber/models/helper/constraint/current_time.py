from django.utils import timezone


def get_current_time():
    return timezone.now()