"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import WelcomeView

api_version = settings.API_VERSION

api_info = openapi.Info(
    title=settings.API_NAME,
    default_version=settings.API_VERSION,
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Django Admin Views
    path("admin/", admin.site.urls),
    # API Schema
    path(
        f"api/{api_version}/swagger/ui/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Welcome View
    path(f"api/{api_version}/", WelcomeView.as_view(), name="api_welcome_view"),
    # Authentication Views
    path(f"api/{api_version}/auth/", include("auth.urls")),
    # Account Management
    path(f"api/{api_version}/account/", include("account.urls")),
]
