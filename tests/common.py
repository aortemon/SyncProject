import json

import pytest
from httpx import AsyncClient


class DefaultRequester:

    def __init__(self, _base_url: str):
        self.base_route: str = _base_url

    def all(self) -> dict:
        return {
            "url": f"/{self.base_route}/all/",
            "headers": {"accept": "application/json"},
        }

    def get_by_id(self, id: int) -> dict:
        return {
            "url": f"/{self.base_route}/get_by_id/?id={id}",
            "headers": {"accept": "application/json"},
        }

    def add(self, **kwargs) -> dict:
        return {
            "url": f"/{self.base_route}/add/",
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            "content": json.dumps(kwargs),
        }

    def update(self, id: int | None, **kwargs) -> dict:
        return {
            "url": f"/{self.base_route}/update/",
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            "content": json.dumps({"id": id, **kwargs}),
        }


class BaseTest:

    def _config(
        self,
    ):
        self.suite_name = ""
        self.route = ""
        self.requester = DefaultRequester(self.route)
        self.existent_ids = []
        self.no_existent_ids = []
        self.add_values = {}
        self.update_values = {}

    def __postconfig(self):
        if not hasattr(self, "no_existent_ids"):
            self.no_existent_ids = list(range(10000, 10006))
        self.requester = DefaultRequester(self.route)

    @pytest.fixture(autouse=True)
    def _setup(self):
        self._config()
        self.__postconfig()

        yield

    async def test_all(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.get(**self.requester.all())
        assert response.status_code == 200, f"In {self.suite_name}"
        assert len(response.json()) == len(self.existent_ids), f"In {self.suite_name}"

    @pytest.mark.parametrize("_", range(5))
    async def test_get_by_id(self, _, async_client_as_executor: AsyncClient):
        if _ >= len(self.existent_ids):
            return

        response = await async_client_as_executor.get(
            **self.requester.get_by_id(self.existent_ids[_])
        )

        assert (
            response.status_code == 200
        ), f"Error on ID = existent_ids[{_}]={self.existent_ids[_]} in {self.suite_name}"

    async def test_add(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.post(
            **self.requester.add(**self.add_values)
        )
        assert (
            response.status_code == 200
        ), f"In {self.suite_name}In {self.suite_name} with response.json() = \n{response.json()}"
        assert response.json() == {
            "msg": "Successfully added!"
        }, f"In {self.suite_name} with response.json() = \n{response.json()}"

    async def test_update(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.put(
            **self.requester.update(**self.update_values)
        )
        assert response.status_code == 200, f"In {self.suite_name}"

    async def test_update_requires_id(self, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.put(
            **self.requester.update(id=None, **dict([self.update_values.popitem()]))
        )

        assert response.status_code == 422, f"In {self.suite_name}"

    async def test_update_required_at_least_one_unreqiured_field(
        self, async_client_as_admin: AsyncClient
    ):
        response = await async_client_as_admin.put(**self.requester.update(id=1))

        assert response.status_code == 405, f"In {self.suite_name}"

    @pytest.mark.parametrize("_", range(6))
    async def test_cant_get_no_existent_ids(
        self, _, async_client_as_executor: AsyncClient
    ):
        if _ >= len(self.no_existent_ids):
            return
        response = await async_client_as_executor.get(
            **self.requester.get_by_id(self.no_existent_ids[_])
        )

        assert (
            response.status_code == 404
        ), f"Error on ID = no_existent_ids[{_}]={self.no_existent_ids[_]} in {self.suite_name}"

    async def _test_fields_length_on_add(self, field, value, client: AsyncClient):
        request = self.requester.add(**{**self.add_values, field: value})
        response = await client.post(**request)
        assert (
            response.status_code == 422
        ), f'In {self.suite_name} with field="{field}". Get status_code={response.status_code} and body={response.json()}'

    async def _test_fields_length_on_update(self, field, value, client: AsyncClient):
        response = await client.put(
            **self.requester.update(id=None, **dict([self.update_values.popitem()]))
        )

        request = self.requester.update(id=1, **{field: value})
        response = await client.put(**request)
        assert (
            response.status_code == 422
        ), f'In {self.suite_name} with field="{field}". Get status_code={response.status_code} and body={response.json()}'
