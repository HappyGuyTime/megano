def save_avatar_profile(avatar, new_avatar, full_name) -> None:
    """Update the user's avatar with a new image."""
    if avatar.src.url != "/media/profiles/avatars/default.png":
        avatar.src.delete(save=False)

    avatar.src = new_avatar
    avatar.alt = f"Avatar {full_name}"
    avatar.save()
