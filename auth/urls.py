from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import LogoutAllView, LogoutView, TokenVerificationView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerificationView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="logout_user"),
    path("logout_all/", LogoutAllView.as_view(), name="logout_all_user_devices"),
]
