import pytest
from httpx import AsyncClient
from .common import BaseTest

pytestmark = pytest.mark.usefixtures("auto_async_client")

invalid_data = [
    ['status_id', -1],
    ['status_id', 'string'],
    ['release_id', '-1'],
    ['release_id', 'string'],
    ['name', 'a'*2],
    ['name', 'a'*31]
]

@pytest.mark.asyncio()
class TestProjects(BaseTest):

    def _config(self):
        self.suite_name = "projects"
        self.route = "projects"
        self.existent_ids = [
            0,
            1,
            2,
        ]
        self.add_values = {
            "name": "dep1",
            "description": "description",
            "status_id": 1,
            "release_id": 2,
        }
        self.update_values = {"id": 1, "name": "NewNameForDepartment"}

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
