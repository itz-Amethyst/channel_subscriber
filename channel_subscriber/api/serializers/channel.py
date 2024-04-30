from rest_framework import serializers
from channel_subscriber.models.channel import Channel
class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # Display owner's name or related field

    class Meta:
        model = Channel
        fields = ["id", "owner", "title", "content", "url", "created_at"]  # Include additional metadata fields if needed