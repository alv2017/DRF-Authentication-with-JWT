from django.urls import path

from .views import (AccountCreateView, AccountDestroyView, AccountListView,
                    AccountRetrieveView, AccountUpdateView,
                    PersonalAccountView)

urlpatterns = [
    path("", PersonalAccountView.as_view(), name=PersonalAccountView.name),
    path("management/", AccountListView.as_view(), name=AccountListView.name),
    path(
        "management/create/", AccountCreateView.as_view(), name=AccountCreateView.name
    ),
    path(
        "management/<int:pk>/",
        AccountRetrieveView.as_view(),
        name=AccountRetrieveView.name,
    ),
    path(
        "management/<int:pk>/update/",
        AccountUpdateView.as_view(),
        name=AccountUpdateView.name,
    ),
    path(
        "management/<int:pk>/delete/",
        AccountDestroyView.as_view(),
        name=AccountDestroyView.name,
    ),
]
