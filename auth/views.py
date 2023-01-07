from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import (
    TokenBlacklistResponseSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerificationResponseSerializer,
    TokenVerificationSerializer,
)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Obtain Tokens Pair",
        operation_description="Obtain tokens pair: authentication token and refresh token",
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Refresh Token",
        operation_description="Refresh access token",
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerificationView(TokenVerifyView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = TokenVerificationSerializer

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Verify Token",
        operation_description="Verify token",
        responses={
            status.HTTP_200_OK: TokenVerificationResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(TokenBlacklistView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Logout User",
        operation_description="Logs out the user by blacklisting user's refresh token",
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        tags=["auth"],
        operation_summary="Logout All User Connections",
        operation_description="Logs out the user by blacklisting all existing user's refresh tokens",
        responses={
            status.HTTP_205_RESET_CONTENT: "",
        },
    )
    def get(self, request):
        user_id = request.user.id
        tokens = OutstandingToken.objects.filter(user_id=user_id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
