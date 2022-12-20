from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class WelcomeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        welcome = {"name": "My Awesome API", "api_version": "v1", "message": "Welcome!"}
        return Response(welcome, status=status.HTTP_200_OK)
