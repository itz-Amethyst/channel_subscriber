from rest_framework import serializers
from core.models.user import User
from core.models.profile import Profile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name"]

    def validate_password(self, password):
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

    def create(self, validated_data):
        # Validate password
        password = validated_data.get("password")
        self.validate_password(password)

        # Create user with the given data
        user = User(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=make_password(password),  # Hash the password
        )
        user.save()

        # Create a profile for the newly created user
        profile = Profile(user=user)
        profile.save()

        return user  # Return the created user




    