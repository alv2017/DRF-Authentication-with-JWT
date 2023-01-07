from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Personal Account",
        operation_description="Shows account details of the logged in user",
    )
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

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Retrieve Account by User ID",
        operation_description="Retrieves user account by user ID",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


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

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Create Account",
        operation_description="Creates user account",
        responses={
            status.HTTP_201_CREATED: AccountPreviewSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountListView(generics.ListAPIView):
    name = "account_list"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = AccountPreviewSerializer

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Accounts List",
        operation_description="Displays a list of existing user accounts",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Account Update",
        operation_description="Updates user account data, full account data needs to be provided",
        responses={
            status.HTTP_200_OK: AccountPreviewSerializer,
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Partial Account Update",
        operation_description="Updates user account, accepts partial account update data",
        responses={
            status.HTTP_200_OK: AccountPreviewSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AccountDestroyView(generics.DestroyAPIView):
    name = "account_destroy"
    queryset = AccountUser.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = AccountSerializer

    @swagger_auto_schema(
        tags=["account"],
        operation_summary="Delete Account",
        operation_description="Delete user account by provided user ID",
        responses={
            status.HTTP_204_NO_CONTENT: "",
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
