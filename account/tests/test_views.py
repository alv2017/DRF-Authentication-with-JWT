from django.urls import reverse, reverse_lazy

from account.views import (AccountCreateView, AccountDestroyView,
                           AccountListView, AccountRetrieveView,
                           AccountUpdateView, PersonalAccountView)


class TestPersonalAccountView:
    view = PersonalAccountView

    def view_url(self):
        return reverse_lazy(self.view.name)

    def test_authentication_required(self, client):
        view_url = self.view_url()
        response = client.get(view_url)
        # 401: unauthorized request
        assert response.status_code == 401
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_authenticated"

    def test_authenticated_valid_request(self, user_api_client, regular_user_data):
        view_url = self.view_url()
        client = user_api_client
        response = client.get(view_url)
        assert response.status_code == 200

    def test_valid_request_password_is_not_displayed(self, user_api_client):
        view_url = self.view_url()
        client = user_api_client
        response = client.get(view_url)
        # 200: request succeeded
        assert response.status_code == 200
        assert "password" not in response.data


class TestAccountRetrieveView:
    view = AccountRetrieveView

    def view_url(self, user_id: int = 1):
        return reverse(self.view.name, kwargs={"pk": user_id})

    def test_authentication_required(self, client):
        view_url = self.view_url()
        response = client.get(view_url)
        # 401: unauthorized request
        assert response.status_code == 401
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_authenticated"

    def test_authenticated_regular_user_has_no_permission(self, user_api_client):
        view_url = self.view_url()
        client = user_api_client
        response = client.get(view_url)
        # 403: request is forbidden
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_admin_request_with_valid_data(
        self,
        admin_api_client,
    ):
        view_url = self.view_url()
        client = admin_api_client
        response = client.get(view_url)
        # 200: request succeeded
        assert response.status_code == 200

    def test_admin_request_with_non_existent_user_data(self, admin_api_client):
        view_url = self.view_url(2)
        client = admin_api_client
        response = client.get(view_url)
        # 404: requested item is not found
        assert response.status_code == 404
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_found"


class TestAccountListView:
    view = AccountListView

    def view_url(self):
        return reverse_lazy(self.view.name)

    def test_authentication_required(self, client):
        view_url = self.view_url()
        response = client.get(view_url)
        # 401: unauthorized request
        assert response.status_code == 401
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_authenticated"

    def test_authenticated_regular_user_has_no_permission(self, user_api_client):
        view_url = self.view_url()
        client = user_api_client
        response = client.get(view_url)
        # 403: request is forbidden
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_admin_request_with_valid_data(
        self,
        admin_api_client,
    ):
        view_url = self.view_url()
        client = admin_api_client
        response = client.get(view_url)
        # 200: request succeeded
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) == 1


class TestAccountCreateView:
    view = AccountCreateView

    def view_url(self):
        return reverse_lazy(self.view.name)

    def test_authentication_required(self, client):
        view_url = self.view_url()
        response = client.post(view_url, {})
        # 401: unauthorized request
        assert response.status_code == 401
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_authenticated"

    def test_authenticated_regular_user_has_no_permission(self, user_api_client):
        view_url = self.view_url()
        client = user_api_client
        response = client.post(view_url, {})
        # 403: forbidden request
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_authenticated_admin_user_has_no_permission(self, admin_api_client):
        view_url = self.view_url()
        client = admin_api_client
        response = client.post(view_url, {})
        # 403: forbidden request
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_superuser_request_with_valid_data(
        self, regular_user_data, super_api_client
    ):
        view_url = self.view_url()
        client = super_api_client
        expected_username = regular_user_data["username"]
        response = client.post(view_url, regular_user_data)
        # 201: request item created
        assert response.status_code == 201
        assert response.data["id"] == 2
        assert response.data["username"] == expected_username

    def test_superuser_request_with_weak_password(
        self, regular_user_data, super_api_client
    ):
        view_url = self.view_url()
        client = super_api_client
        regular_user_data["password"] = "password"
        response = client.post(view_url, regular_user_data)
        # 400: bad request
        assert response.status_code == 400
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "invalid_password"


class TestAccountUpdateView:
    view = AccountUpdateView

    def view_url(self, user_id: int = 1):
        return reverse(self.view.name, kwargs={"pk": user_id})

    def test_patch_authentication_required(self, client):
        view_url = self.view_url()
        response = client.patch(view_url, {})
        assert response.status_code == 401
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_authenticated"

    def test_authenticated_regular_user_has_no_permission(self, user_api_client):
        view_url = self.view_url()
        client = user_api_client
        response = client.patch(view_url, {})
        # 403: request is forbidden
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_authenticated_admin_user_has_no_permission(self, admin_api_client):
        view_url = self.view_url()
        client = admin_api_client
        response = client.patch(view_url, {})
        # 403: request is forbidden
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_valid_superuser_request(self, super_api_client):
        view_url = self.view_url()
        client = super_api_client
        first_name = "John"
        last_name = "Doe"
        response = client.patch(
            view_url, {"first_name": first_name, "last_name": last_name}
        )
        assert response.status_code == 200
        assert response.data["first_name"] == first_name
        assert response.data["last_name"] == last_name

    def test_superuser_request_with_non_existent_user_data(self, super_api_client):
        view_url = self.view_url(2)
        client = super_api_client
        response = client.patch(view_url, {})
        # 404: requested item is not found
        assert response.status_code == 404
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_found"


class TestAccountDestroyView:
    view = AccountDestroyView

    def view_url(self, user_id: int = 1):
        return reverse(self.view.name, kwargs={"pk": user_id})

    def test_authentication_required(self, client):
        view_url = self.view_url()
        response = client.delete(view_url)
        # 401: unauthorized request
        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_authenticated_regular_user_has_no_permission(self, user_api_client):
        view_url = self.view_url()
        client = user_api_client
        response = client.delete(view_url)
        # 403: request is forbidden
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_authenticated_admin_user_has_no_permission(self, admin_api_client):
        view_url = self.view_url()
        client = admin_api_client
        response = client.delete(view_url)
        # 403: request is forbidden
        assert response.status_code == 403
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "permission_denied"

    def test_superuser_request_with_valid_data(
        self, regular_user_data, super_api_client
    ):
        view_url = self.view_url()
        client = super_api_client
        response = client.delete(view_url)

        assert response.status_code == 204

    def test_superuser_request_with_non_existent_user_data(self, super_api_client):
        view_url = self.view_url(2)
        client = super_api_client
        response = client.delete(view_url)
        # 204: requested item deleted
        assert response.status_code == 404
        # response contains errors
        assert "detail" in response.data
        assert response.data["detail"].code == "not_found"
