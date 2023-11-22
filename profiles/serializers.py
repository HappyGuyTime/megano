from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import Avatar, Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = ["email"]


class AvatarSerializer(serializers.ModelSerializer):
    """Serializer for the Avatar model."""

    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj) -> str:
        """Get the URL of the avatar image."""
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    avatar = AvatarSerializer(read_only=True)
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    def get_email(self, obj) -> str:
        """Get the email associated with the user's profile."""
        return obj.user.email
