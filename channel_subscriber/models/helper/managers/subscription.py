from django.db import models

# Manager for the Subscription model
class SubscriptionManager(models.Manager):
    def get_subscriptions_with_users(self):
        # Use select_related to fetch subscribers and targets efficiently
        return self.select_related('subscriber', 'target')

    def get_subscriptions_with_channels(self):
        # Prefetch related channels for subscribers
        return self.prefetch_related('subscriber__subscriptions')