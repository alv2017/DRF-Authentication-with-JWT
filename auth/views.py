from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.views import TokenBlacklistView, TokenVerifyView

from .serializers import TokenVerificationSerializer


class TokenVerificationView(TokenVerifyView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = TokenVerificationSerializer


class LogoutView(TokenBlacklistView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user_id = request.user.id
        tokens = OutstandingToken.objects.filter(user_id=user_id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
