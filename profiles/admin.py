from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from profiles.forms import ProfileAdminForm
from profiles.models import Profile


class ProfileInline(admin.StackedInline):
    """Inline profile for UserAdmin."""

    model = Profile
    form = ProfileAdminForm


class CustomUserAdmin(UserAdmin):
    """Custom UserAdmin class for managing user profiles."""

    inlines = (ProfileInline,)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        """Override to hide the ProfileInline if no profile exists."""
        if obj is not None:
            return super().get_inline_instances(request, obj)
        return []

    def save_model(self, request, obj, form, change):
        """Override to create a profile for the user if it doesn't exist."""
        super().save_model(request, obj, form, change)
        if not hasattr(obj, "profile"):
            Profile.objects.create(user=obj, fullName=obj.username)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
