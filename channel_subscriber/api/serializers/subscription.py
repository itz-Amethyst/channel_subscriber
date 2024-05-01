from rest_framework import serializers
from channel_subscriber.models import Subscription , Channel
from django.utils.translation import gettext_lazy as _


# Serializer for creating a new Subscription (subscribing to a channel)
class SubscriptionCreateSerializer(serializers.ModelSerializer):
    channel_id = serializers.PrimaryKeyRelatedField(
        queryset=Channel.objects.all(),
        source='target',  # Target is the owner of the channel
        help_text=_("The ID of the channel to subscribe to."),
    )

    class Meta:
        model = Subscription
        fields = ["channel_id"]

    def validate(self, data):
        request = self.context.get("request")
        subscriber = request.user if request else None

        if not subscriber:
            raise serializers.ValidationError({"subscriber": _("Subscriber is required.")})

        channel = data["target"]  # `target` maps from `channel_id`

        if channel.owner == subscriber:
            # Validate that the subscriber isn't trying to subscribe to their own channel
            raise serializers.ValidationError(
                {"channel_id": _("You can only subscribe to channels owned by other users.")}
            )

        # Validate that the subscription doesn't already exist
        if Subscription.objects.filter(subscriber=subscriber, target=channel.owner).exists():
            raise serializers.ValidationError(
                {"channel_id": _("You are already subscribed to this channel.")}
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        subscriber = request.user if request else None

        subscription = Subscription(
            subscriber=subscriber,
            target=validated_data["target"].owner  # The target is the channel's owner
        )
        subscription.save()
        return subscription