from django.db import models

# Manager for the Channel model
class ChannelManager(models.Manager):
    def get_channels_with_owners(self):
        # Use select_related to optimize queries that need owner details
        return self.get_queryset().select_related('owner')

    def get_channels_with_subscriptions(self):
        # Prefetch subscriptions related to the channel
        return self.get_queryset().prefetch_related('subscriptions')