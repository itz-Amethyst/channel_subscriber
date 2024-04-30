from rest_framework import serializers
from channel_subscriber.models import Subscription, Channel
from django.utils.translation import gettext_lazy as _

class SubscriptionDeleteSerializer(serializers.Serializer):
    channel_id = serializers.PrimaryKeyRelatedField(
        queryset=Channel.objects.all(),
        help_text=_("The ID of the channel to unsubscribe from."),
    )

    def validate(self, data):
        request = self.context.get("request")
        subscriber = request.user if request else None

        if not subscriber:
            raise serializers.ValidationError({"subscriber": _("Subscriber is required.")})

        # Get the target (channel owner) from the specified channel_id
        channel = data["channel_id"]
        target = channel.owner

        # Ensure that the subscription exists
        if not Subscription.objects.filter(subscriber=subscriber, target=target).exists():
            raise serializers.ValidationError(
                {"channel_id": _("You are not subscribed to this channel.")}
            )

        return data