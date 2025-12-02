import pytest

from .conftest import auto_async_client

pytestmark = pytest.mark.usefixtures("auto_async_client")


@pytest.mark.asyncio
class TestRoot:

    async def test_root(self, auto_async_client):
        response = await auto_async_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "OK"}

    @pytest.mark.parametrize("path", ["notfound", "not_existing_route", "aabracadabra"])
    async def test_notfound(self, auto_async_client, path):
        response = await auto_async_client.get(f"/{path}")
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "method, route",
        [
            ["GET", "/auth/login/"],
            ["GET", "/auth/register/"],
            ["GET", "/auth/logout/"],
            ["POST", "/auth/me/"],
            ["POST", "/auth/is_token_correct/"],
            ["PUT", "/admin/db_dump/"],
            ["POST", "/employees/all/"],
            ["DELETE", "/employees/calendar/mine/"],
            ["GET", "/statuses/update/"],
            ["GET", "/vacations/delete_past/"],
            ["DELETE", "/notifications/my/"],
        ],
    )
    async def test_incorrect_methods_on_existent_routes(
        self, async_client_as_admin, method, route
    ):

        if method == "GET":
            action = async_client_as_admin.get
        elif method == "POST":
            action = async_client_as_admin.post
        elif method == "PUT":
            action = async_client_as_admin.put
        elif method == "DELETE":
            action = async_client_as_admin.delete

        response = await action(route)
        assert response.status_code in [405, 404]
