from rest_framework import serializers
from core.models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # todo
    class Meta:
        model = Profile
        fields = ["user", "subscriber_count", "subscription_count", "bio"]