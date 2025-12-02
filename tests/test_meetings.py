import pytest
from httpx import AsyncClient

from .common import BaseTest

pytestmark = pytest.mark.usefixtures("auto_async_client")

invalid_data = [
    ["name", "a" * 31],
    ["name", "a" * 2],
    ["description", "a" * 501],
    ["date", "notdatestr"],
    ["date", "20-08-2004"],
    ["date", 254565],
    ["link", "a" * 257],
    ["employees", "invalid_id"],
    ["employees", ["invalid_id_1", "invalid_id_2"]],
]


@pytest.mark.asyncio()
class TestWorkhours(BaseTest):

    def _config(self):
        self.suite_name = "meetings"
        self.route = "meetings"
        self.existent_ids = [0, 1, 2]
        self.add_values = {
            "name": "string",
            "description": "string",
            "date": "2026-01-12 14:30:00",
            "link": "string",
            "employees": [0, 1, 2],
        }
        self.update_values = {"id": 1, "employees": [0, 1]}

    @pytest.mark.parametrize("field, value", invalid_data)
    async def test_fields_length_on_add(
        self, field, value, async_client_as_admin: AsyncClient
    ):
        await self._test_fields_length_on_add(field, value, async_client_as_admin)

    @pytest.mark.parametrize("field, value", invalid_data)
    async def test_fields_length_on_update(
        self, field, value, async_client_as_admin: AsyncClient
    ):
        await self._test_fields_length_on_update(field, value, async_client_as_admin)
