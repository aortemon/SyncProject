import pytest

from .common import BaseTest
from httpx import AsyncClient

pytestmark = pytest.mark.usefixtures("auto_async_client")

invalid_data = [
    [field, value] for field in ['starttime', 'endtime', 'lunchbreak_start', 'lunchbreak_end'] for value in ['asdasd', 123123, '2025-11-10', '00.00.00']
]

@pytest.mark.asyncio()
class TestVacations(BaseTest):

    def _config(self):
        self.suite_name = "workhours"
        self.route = "workhours"
        self.existent_ids = [0, 1, 2, 3]
        self.add_values = {
            "starttime": "12:00:00",
            "endtime": "21:00:00",
            "lunchbreak_start": "13:00:00",
            "lunchbreak_end": "13:30:00",
        }
        self.update_values = {"id": 1, "starttime": "06:00:00"}
        

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

