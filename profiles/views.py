import json

from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from profiles.services import save_avatar_profile


class SignInApiView(APIView):
    """User sign-in API view."""

    def post(self, request) -> Response:
        """Handle user sign-in."""
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpApiView(APIView):
    """User sign-up API view."""

    def post(self, request) -> Response:
        """Register a new user."""
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutApiView(APIView):
    """User logout API view."""

    permission_classes = (IsAuthenticated,)

    def post(self, request) -> Response:
        """Handle user logout."""
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileApiView(RetrieveUpdateAPIView):
    """User profile API view."""

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs) -> Response:
        """Update user profile."""
        with transaction.atomic():
            user_serializer = UserSerializer(
                request.user,
                data={"email": request.data.get("email")},
                partial=True,
            )
            if user_serializer.is_valid():
                user_serializer.save()

            return self.partial_update(request, *args, **kwargs)

    def get_object(self) -> Profile:
        return Profile.objects.get(user=self.request.user)


class AvatarUploadApiView(APIView):
    """User avatar upload API view."""

    parser_classes = [MultiPartParser]

    def post(self, request) -> Response:
        """Handle user's avatar upload."""
        avatar = request.user.profile.avatar
        if avatar and request.FILES.get("avatar"):
            save_avatar_profile(
                avatar=avatar,
                new_avatar=request.FILES["avatar"],
                full_name=request.user.profile.fullName,
            )
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfilePasswordApiView(APIView):
    """User password change API view."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Handle user's password change."""
        form = PasswordChangeForm(
            user=request.user,
            data={
                "old_password": request.data.get("currentPassword"),
                "new_password1": request.data.get("newPassword"),
                "new_password2": request.data.get("newPassword"),
            },
        )
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
