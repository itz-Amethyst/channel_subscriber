from channel_subscriber.models import Channel
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class ChannelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["title", "content", "url"]  # The fields that can be updated

    def validate(self, data):
        # Custom validation to avoid creating duplicate titles for the same owner
        instance = self.instance  # The existing Channel instance
        request = self.context.get("request")
        owner = request.user if request else None

        if "title" in data and Channel.objects.filter(owner=owner, title=data["title"]).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"title": _("Another channel with this title already exists for this owner.")})

        return data