from django.contrib.auth.models import User
from django.db import models


def get_profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    """Return the directory path for storing profile avatars."""
    return f"profiles/avatars/profile_{instance.pk}/{filename}"


class Avatar(models.Model):
    """Model for storing the user's avatar"""

    src = models.ImageField(
        upload_to=get_profile_avatar_directory_path,
        default="profiles/avatars/default.png",
    )
    alt = models.CharField(max_length=128)

    class Meta:
        db_table = "profiles_avatars"


class Profile(models.Model):
    """User profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128)
    phone = models.CharField(max_length=20, blank=True, null=False)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    avatar = models.OneToOneField(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    class Meta:
        db_table = "profiles"

    def __str__(self) -> str:
        """String representation of the user profile."""
        return self.fullName

    def save(self, *args, **kwargs):
        """Save the user profile with a default avatar if one is not set."""
        if not hasattr(self, "avatar"):
            avatar = Avatar.objects.create(alt="default avatar")
            self.avatar = avatar
        super().save(*args, **kwargs)
