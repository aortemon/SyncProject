import pytest

from .common import BaseTest
from httpx import AsyncClient

pytestmark = pytest.mark.usefixtures("auto_async_client")

invalid_data = [
    ['alias', 'a'*2],
    ['alias', 'a'*16]
]

@pytest.mark.asyncio()
class TestStatuses(BaseTest):

    def _config(self):
        self.suite_name = "statuses"
        self.route = "statuses"
        self.existent_ids = [0, 1, 2]
        self.add_values = {"alias": "another_status"}
        self.update_values = {"id": 1, "alias": "Newalias"}
        
    

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

