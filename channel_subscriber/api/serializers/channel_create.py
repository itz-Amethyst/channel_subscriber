from rest_framework import serializers
from channel_subscriber.models.channel import Channel
from channel_subscriber.models.helper.constraint.url_path_validator_reg import youtube_channel_validator
from django.utils.translation import gettext_lazy as _
class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["title", "content", "url"]  #todo No 'owner' field; it should be set by the backend
        extra_kwargs = {
            'url': {
                'validators': [youtube_channel_validator]  # Ensure the URL starts with 'https://youtube.com/channel/'
            }
        }

    def validate(self, data):
        # Example validation to check if the title is unique for a given owner
        # todo parse the request
        request = self.context.get("request")
        owner = request.user if request else None

        if Channel.objects.filter(owner=owner, title=data["title"]).exists():
            raise serializers.ValidationError({"title": _("A channel with this title already exists for this owner.")})

        return data


    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"error": "User must be authenticated."})

        # Set the owner to the current authenticated user
        validated_data["owner"] = request.user

        return super().create(validated_data)