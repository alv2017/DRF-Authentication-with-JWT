from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class WelcomeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        operation_summary="API Info",
        operation_description="Returns API Info",
        tags=["api"],
    )
    def get(self, request):
        welcome = {
            "api": settings.API_NAME,
            "version": settings.API_VERSION,
            "description": settings.API_DESCRIPTION,
            "message": "Welcome!",
        }
        return Response(welcome, status=status.HTTP_200_OK)
