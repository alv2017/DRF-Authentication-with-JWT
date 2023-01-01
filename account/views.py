from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User as AccountUser
from .permissions import IsSuperUser
from .serializers import (
    AccountPreviewSerializer,
    AccountSerializer,
    PersonalAccountSerializer,
)


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
    serializer_class = AccountPreviewSerializer


class AccountCreateView(generics.CreateAPIView):
    name = "account_create"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_serializer = AccountPreviewSerializer(account)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AccountListView(generics.ListCreateAPIView):
    name = "account_list"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = AccountPreviewSerializer


class AccountUpdateView(generics.UpdateAPIView):
    name = "account_update"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response_serializer = AccountPreviewSerializer(account)

        return Response(response_serializer.data)


class AccountDestroyView(generics.DestroyAPIView):
    name = "account_destroy"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer
