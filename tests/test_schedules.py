import pytest

from .common import BaseTest
from httpx import AsyncClient

pytestmark = pytest.mark.usefixtures("auto_async_client")

invalid_data = [[name, value] for name in ['sun_id', 'mon_id', 'tue_id', 'wed_id', 'thu_id', 'fri_id', 'sat_id'] for value in [-1, 'a']]


@pytest.mark.asyncio()
class TestSchedules(BaseTest):

    def _config(self):
        self.suite_name = "schedules"
        self.route = "schedules"
        self.existent_ids = [0, 1, 2]
        self.add_values = {
            "sun_id": 0,
            "mon_id": 0,
            "tue_id": 0,
            "wed_id": 0,
            "thu_id": 0,
            "fri_id": 0,
            "sat_id": 0,
        }
        self.update_values = {"id": 1, "wed_id": "1"}

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

