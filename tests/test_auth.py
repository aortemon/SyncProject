import base64
import json

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.usefixtures("auto_async_client")


class AuthRequester:
    def me(self):
        return {"url": "/auth/me/", "headers": {"accept": "application/json"}}

    def is_token_correct(self):
        return {
            "url": "/auth/is_token_correct/",
            "headers": {"accept": "application/json"},
        }

    def register(self, email: str, password: str, dob: str = "1995-08-10"):
        return {
            "url": "/auth/register/",
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            "content": json.dumps(
                {
                    "lname": "test",
                    "fname": "test",
                    "mname": "test",
                    "dob": dob,
                    "schedule_id": 0,
                    "position": "test",
                    "role_id": 3,
                    "departments": [
                        {"id": 0, "office": "office1"},
                        {"id": 1, "office": "office2"},
                    ],
                    "phone": "+79607495028",
                    "email": email,
                    "password": password,
                }
            ),
        }

    def login(self, username: str, password: str) -> dict:
        return {
            "url": "/auth/login/",
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            "data": {"username": f"{username}", "password": f"{password}"},
        }


@pytest.mark.asyncio()
class TestAuth:

    requester = AuthRequester()

    async def test_login_as_existent_user(self, auto_async_client: AsyncClient):
        response = await auto_async_client.post(
            **self.requester.login("admin@admin.admin", "temikadmin")
        )
        assert response.status_code == 200
        assert "access_token" in response.json() and "token_type" in response.json()
        assert response.json()["token_type"] == "Bearer"

        JWT_headers = {"alg": "HS256", "typ": "JWT"}
        JWT_token_beginning = (
            base64.urlsafe_b64encode(
                json.dumps(JWT_headers, separators=(",", ":")).encode()
            )
            .decode()
            .rstrip("=")
        )

        assert response.json()["access_token"].startswith(JWT_token_beginning)

    async def test_login_as_existent_user_invalid_password(
        self, auto_async_client: AsyncClient
    ):
        response = await auto_async_client.post(
            **self.requester.login("admin@admin.admin", "incorrectpassword")
        )

        assert response.status_code == 401

    async def test_login_as_no_existent_user(self, auto_async_client: AsyncClient):
        response = await auto_async_client.post(
            **self.requester.login("noexistent@user.ru", "temikadmin")
        )

        assert response.status_code == 401

    async def test_auth_me_as_unloggined_user(self, auto_async_client: AsyncClient):
        response = await auto_async_client.get(url="/auth/me")

        assert response != 200

    async def test_auth_me_as_admin(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.get(**self.requester.me())

        assert response.status_code == 200
        assert "mname" in response.json()
        assert response.json()["mname"] == "admin"

    async def test_auth_me_as_manager(self, async_client_as_manager: AsyncClient):
        response = await async_client_as_manager.get(**self.requester.me())

        assert response.status_code == 200
        assert "mname" in response.json()
        assert response.json()["mname"] == "manager"

    async def test_auth_me_as_executor(self, async_client_as_executor: AsyncClient):
        response = await async_client_as_executor.get(**self.requester.me())

        assert response.status_code == 200
        assert "mname" in response.json()
        assert response.json()["mname"] == "exec"

    async def test_is_token_correct_with_correct_token(
        self, async_client_as_admin: AsyncClient
    ):
        response = await async_client_as_admin.get(**self.requester.is_token_correct())
        assert response.status_code == 200

    async def test_is_token_correct_with_incorrect_token(
        self, async_client_as_admin: AsyncClient
    ):
        async_client_as_admin.headers.update({"Authorization": "Bearer invalid token"})
        response = await async_client_as_admin.get(**self.requester.is_token_correct())
        assert response.status_code != 200

    async def test_adding_user_as_admin(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.post(
            **self.requester.register("email@email.ru", "PasdasdasAS12.")
        )

        assert response.status_code == 200
        assert response.json() == {"msg": "Registered successfully"}

    @pytest.mark.parametrize(
        "password",
        ["Aa2.", "hsdhsdhsdjfsdjhf2.", "54654654654654.A", "dfsdfsdfsdfsd+1221"],
    )
    async def test_adding_user_as_admin_unsafe_password(
        self, password: str, async_client_as_admin: AsyncClient
    ):
        response = await async_client_as_admin.post(
            **self.requester.register("emailaaa@email.ru", password)
        )

        assert response.status_code == 422

    async def test_adding_user_with_email_already_exists(
        self, async_client_as_admin: AsyncClient
    ):
        response = await async_client_as_admin.post(
            **self.requester.register("admin@admin.admin", "KAJSDksdllksdlk15.")
        )

        assert response.status_code == 409

    async def test_adding_user_which_is_child(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.post(
            **self.requester.register(
                "admin@admin.admin", "KAJSDksdllksdlk15.", dob="2015-10-11"
            )
        )

        assert response.status_code == 422

    async def test_adding_user_with_incorrect_email(
        self, async_client_as_admin: AsyncClient
    ):
        response = await async_client_as_admin.post(
            **self.requester.register("adminadmin.admin", "KAJSDksdllksdlk15.")
        )

        assert response.status_code == 422

    async def test_adding_user_not_as_admin(
        self,
        async_client_as_executor: AsyncClient,
        async_client_as_manager: AsyncClient,
    ):
        for client in [async_client_as_executor, async_client_as_manager]:
            response = await client.post(
                **self.requester.register("emasail@email.ru", "PasdasdasAS12.")
            )

            assert response.status_code == 403
            assert response.json() == {
                "detail": "403: Access denied due to unsufficient privileges",
                "type": "http_err",
            }
