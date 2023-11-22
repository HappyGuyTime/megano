from django.urls import path

from profiles.views import (AvatarUploadApiView, LogoutApiView, ProfileApiView,
                            ProfilePasswordApiView, SignInApiView,
                            SignUpApiView)

app_name = "profiles"

urlpatterns = [
    path("sign-in/", SignInApiView.as_view(), name="login"),
    path("sign-up/", SignUpApiView.as_view(), name="register"),
    path("sign-out/", LogoutApiView.as_view(), name="logout"),
    path("profile/", ProfileApiView.as_view(), name="profile"),
    path("profile/avatar/", AvatarUploadApiView.as_view(), name="avatar_upload"),
    path("profile/password/", ProfilePasswordApiView.as_view(), name="password"),
]
