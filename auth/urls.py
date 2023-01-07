from django.urls import path

from .views import (
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    DecoratedTokenVerificationView,
    LogoutAllView,
    LogoutView,
)

urlpatterns = [
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path(
        "token/verify/", DecoratedTokenVerificationView.as_view(), name="token_verify"
    ),
    path("logout/", LogoutView.as_view(), name="logout_user"),
    path("logout_all/", LogoutAllView.as_view(), name="logout_all_user_devices"),
]
