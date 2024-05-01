from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from channel_subscriber.models import Subscription
from core.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # When a new user is created, create a corresponding profile
        profile = Profile.objects.create(user=instance)

        # Calculate subscription-related counts and update the profile
        profile.subscriber_count = Subscription.objects.filter(target=instance).count()
        profile.subscription_count = Subscription.objects.filter(subscriber=instance).count()

        profile.save()

@receiver(post_save, sender=Subscription)
def update_profile_on_subscription_created(sender, instance, created, **kwargs):
    if created:
        # Subscription was created, update the subscriber's and target's profiles
        subscriber_profile = Profile.objects.get(user=instance.subscriber)
        target_profile = Profile.objects.get(user=instance.target)

        # Increment the counts
        subscriber_profile.subscription_count += 1
        target_profile.subscriber_count += 1

        # Save the updated profiles
        subscriber_profile.save()
        target_profile.save()

@receiver(post_delete, sender=Subscription)
def update_profile_on_subscription_deleted(sender, instance, **kwargs):
    # Subscription was deleted, update the subscriber's and target's profiles
    subscriber_profile = Profile.objects.get(user=instance.subscriber)
    target_profile = Profile.objects.get(user=instance.target)

    # Decrement the counts
    subscriber_profile.subscription_count -= 1
    target_profile.subscriber_count -= 1

    # Save the updated profiles
    subscriber_profile.save()
    target_profile.save()
