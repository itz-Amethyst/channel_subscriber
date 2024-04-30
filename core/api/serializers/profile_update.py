from rest_framework import serializers
from core.models.profile import Profile

class UpdateProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required = True, write_only = True, allow_null = True)
    class Meta:
        model = Profile
        fields = ["bio",]