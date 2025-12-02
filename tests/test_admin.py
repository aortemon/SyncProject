import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAdmin:

    @pytest.mark.parametrize(
        "compress, include_data",
        [[False, False], [False, True], [True, False], [True, True]],
    )
    async def test_db_bump(
        self,
        compress,
        include_data,
        async_client_as_admin: AsyncClient,
        setup_test_db_dumper,
    ):
        request = await async_client_as_admin.post(
            url=f"/admin/db_dump/?compress={compress}&include_data={include_data}",
            headers={"accept": "application/json"},
        )

        assert request.status_code == 200
