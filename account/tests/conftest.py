import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def regular_user_data():
    return {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "password": "super_secret_password",
        "is_staff": False,
        "is_superuser": False,
    }


@pytest.fixture()
def admin_user_data():
    return {
        "username": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": "super_secret_password",
        "is_staff": True,
        "is_superuser": False,
    }


@pytest.fixture()
def super_user_data():
    return {
        "username": "superuser",
        "first_name": "Super",
        "last_name": "User",
        "email": "super@example.com",
        "password": "super_secret_password",
        "is_staff": True,
        "is_superuser": True,
    }


@pytest.fixture
def user_api_client(api_client, django_user_model, regular_user_data):
    client = api_client
    user = django_user_model.objects.create_user(**regular_user_data)
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def admin_api_client(api_client, django_user_model, admin_user_data):
    client = api_client
    admin_user = django_user_model.objects.create_user(**admin_user_data)
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def super_api_client(api_client, django_user_model, super_user_data):
    client = api_client
    super_user = django_user_model.objects.create_user(**super_user_data)
    refresh = RefreshToken.for_user(super_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
