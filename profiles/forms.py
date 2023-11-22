from django.forms import FileInput, ImageField, ModelForm
from django.utils.html import format_html

from profiles.models import Profile
from profiles.services import save_avatar_profile


class ImagePreviewInputWidget(FileInput):
    """Custom input widget that renders an image preview when a value is present."""

    def render(self, name, value, attrs=None, renderer=None):
        """Render the image preview input widget with an image preview if a value is present."""
        output = []
        if value is not None:
            output.append(
                format_html(
                    f'<div><img src="{value.url}" alt="Image" width="150" height="150"/><div/>'
                )
            )
        output.append(super().render(name, value, attrs, renderer))
        return format_html("\n".join(output))


class ProfileAdminForm(ModelForm):
    """Form for managing user profile data in the admin panel."""

    avatar_preview_download = ImageField(
        label="Avatar", widget=ImagePreviewInputWidget, required=False
    )

    class Meta:
        model = Profile
        fields = ("avatar_preview_download", "fullName", "phone", "balance")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance is not None:
            self.fields["avatar_preview_download"].initial = instance.avatar.src

    def save(self, commit=True):
        """Save user profile data and handle avatar changes."""
        profile = super().save(commit=commit)
        avatar = profile.avatar
        avatar_download = self.cleaned_data.get("avatar_preview_download")

        if avatar and avatar_download:
            save_avatar_profile(
                avatar=avatar,
                new_avatar=avatar_download,
                full_name=profile.fullName,
            )
        return profile
