import json

import pytest
from httpx import AsyncClient

invalid_update_values = [
    ["lname", "a" * 2],
    ["lname", "a" * 51],
    ["fname", "a" * 2],
    ["fname", "a" * 51],
    ["mname", "a" * 2],
    ["mname", "a" * 51],
    ["dob", "15.12.2004"],
    ["dob", "2004.12.02"],
    ["dob", "2015-12-02"],
    ["dob", "2004-13-02"],
    ["dob", "2004-02-30"],
    ["dob", "notdate"],
    ["dob", 228],
    ["schedule_id", "3"],
    ["schedule_id", "sdf"],
    ["schedule_id", -1],
    ["schedule_id", 3],
    ["role_id", 0],
    ["role_id", "asdasd"],
    ["role_id", 4],
    ["departments", [0, 1]],
    ["departments", ["0", 1]],
    ["departments", ["0", "1"]],
    ["departments", ["asda", "asdas"]],
    ["departments", [{"id": 0, "office": "office"}, {"id": "1", "office": 5}]],
    ["departments", [{"id": 0, "office": "office"}, {"id": "1"}]],
    ["departments", [{"id": 0, "office": "office"}, {"id": "sdf", "office": "office"}]],
    ["departments", {"id": 0, "office": "office"}],
    ["phone", "8" + "0" * 10],
    ["phone", "7" + "0" * 10],
    ["phone", "+7" + "0" * 9],
    ["phone", "+7" + "0" * 11],
    ["email", "just_a_string"],
    ["email", "@"],
    ["email", "@@@"],
    ["email", "poopa@loopa"],
    ["email", "string@"],
    ["email", "string@.ru"],
    ["email", "@assd.ru"],
    ["password", "ordinallettersonly"],
    ["password", "CAPITALLETTERSONLY"],
    ["password", "tooshort"],
    ["password", "toolong" * 7],
    ["password", "/.," * 5],
    ["password", "AAAAAAAAAaaaaaaaaa"],
    ["password", "AAAAAAAAAAaaaaaaa23"],
    ["password", "AAAAAAAAAaaaaaaa..."],
    ["password", "31415926535"],
]


class EmployeeRequester:

    path = "employees"

    @classmethod
    def all(cls) -> dict:
        return {"url": f"/{cls.path}/all/"}

    @classmethod
    def get_by_id(cls, uid) -> dict:
        return {"url": f"/{cls.path}/get_by_id/", "params": {"id": uid}}

    @classmethod
    def update(cls, id, **kwargs):
        return {
            "url": f"/{cls.path}/update/",
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            "content": json.dumps({"id": id, **kwargs}),
        }

    @classmethod
    def calendar_mine_today(cls):
        return {"url": f"/{cls.path}/calendar/mine/today/"}

    @classmethod
    def calendar_mine(cls, tdate):
        return {
            "url": f"/{cls.path}/calendar/mine/",
            "params": {"date": tdate},
        }

    @classmethod
    def calendar_mine_range(cls, start_date, end_date):
        return {
            "url": f"/{cls.path}/calendar/mine/range/",
            "params": {"start_date": start_date, "end_date": end_date},
        }


@pytest.mark.asyncio
class TestEmployees:

    requester = EmployeeRequester()
    update = {
        "lname": "lastname",
        "fname": "firstname",
        "mname": "midname",
        "dob": "2000-01-02",
        "schedule_id": 1,
        "position": "worker",
        "role_id": 1,
        "departments": [{"id": 0, "office": "office1"}],
        "phone": "+78005553535",
        "email": "workersemail@gmail.com",
        "password": "CAPITALordinal123.",
    }

    @classmethod
    async def test_get_all(cls, async_client_as_executor: AsyncClient):
        response = await async_client_as_executor.get(**cls.requester.all())

        assert response.status_code == 200
        assert len(response.json()) == 3

    @classmethod
    @pytest.mark.parametrize("user_id", [0, 1, 2])
    async def test_get_by_id(cls, user_id, async_client_as_executor: AsyncClient):
        response = await async_client_as_executor.get(
            **cls.requester.get_by_id(user_id)
        )

        assert response.status_code == 200

    @pytest.mark.parametrize("user_id", [-1, 100, 3])
    async def test_get_by_id_on_no_existent(
        cls, user_id, async_client_as_executor: AsyncClient
    ):
        response = await async_client_as_executor.get(
            **cls.requester.get_by_id(user_id)
        )

        assert response.status_code == 404

    @pytest.mark.parametrize("user_id", ["VasyaPoopkin", object()])
    async def test_get_by_id_with_uprocessible_input(
        cls, user_id, async_client_as_executor: AsyncClient
    ):
        response = await async_client_as_executor.get(
            **cls.requester.get_by_id(user_id)
        )

        assert response.status_code == 422

    @classmethod
    async def test_update(cls, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.put(
            **cls.requester.update(2, **cls.update)
        )
        assert response.status_code == 200

    @classmethod
    @pytest.mark.parametrize("field, value", invalid_update_values)
    async def test_update_validation(
        cls, field, value, async_client_as_admin: AsyncClient
    ):
        response = await async_client_as_admin.put(
            **cls.requester.update(2, **{**cls.update, field: value})
        )

        assert response.status_code == 422

    @classmethod
    async def test_calendar_mine_today(cls, async_client_as_admin):
        response = await async_client_as_admin.get(
            **cls.requester.calendar_mine_today()
        )

        assert response.status_code == 200

    @classmethod
    @pytest.mark.parametrize("tdate", ["2026-01-15", "2026-01-16"])
    async def test_calendar_mine(cls, tdate, async_client_as_admin):
        response = await async_client_as_admin.get(**cls.requester.calendar_mine(tdate))

        assert response.status_code == 200
        assert response.json()["timesheet"][0][0] == "16:00:00"

    @classmethod
    async def test_calendar_mine_range(cls, async_client_as_admin):
        response = await async_client_as_admin.get(
            **cls.requester.calendar_mine_range("2026-01-15", "2026-01-17")
        )

        assert response.status_code == 200
        response = response.json()
        assert len(response[0]["timesheet"]) == 1
        assert len(response[1]["timesheet"]) == 1
        assert len(response[2]["timesheet"]) == 0
