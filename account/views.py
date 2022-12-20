from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User as AccountUser
from .permissions import IsSuperUser
from .serializers import AccountSerializer, PersonalAccountSerializer


class PersonalAccountView(APIView):
    name = "personal_account"
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, request):
        user_id = request.user.id
        try:
            return AccountUser.objects.get(pk=user_id)
        except AccountUser.DoesNotExist:
            raise NotFound(detail="Account not found.", code="account_not_found")

    def get(self, request):
        account = self.get_object(request)
        serializer = PersonalAccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountRetrieveView(generics.RetrieveAPIView):
    name = "account_retrieve"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = AccountSerializer


class AccountCreateView(generics.CreateAPIView):
    name = "account_create"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer


class AccountListView(generics.ListCreateAPIView):
    name = "account_list"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = AccountSerializer


class AccountUpdateView(generics.UpdateAPIView):
    name = "account_update"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer


class AccountDestroyView(generics.DestroyAPIView):
    name = "account_destroy"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer
