import json
from pathlib import Path
from io import BytesIO

import pytest
from httpx import AsyncClient


class TaskRequester:

    path = "tasks"

    @classmethod
    def all(cls):
        return {"url": f"/{cls.path}/all/"}

    @classmethod
    def my_drafts(cls):
        return {"url": f"/{cls.path}/my_drafts"}

    @classmethod
    def my_tasks(cls):
        return {"url": f"/{cls.path}/my_tasks"}

    @classmethod
    def get_by_id(cls, task_id):
        return {"url": f"/{cls.path}/get_by_id/", "params": {"id": task_id}}

    @classmethod
    def add(cls, values: dict = {}):
        return {
            "url": f"/{cls.path}/add/",
            "headers": {
                "accept": "application/json",
            },
            "data": {
                **{
                    "executor_id": 2,
                    "start_date": "2026-01-01",
                    "end_date": "2026-01-30",
                    "name": "Taskname",
                    "description": "descript",
                    "status_id": 1,
                    "project_id": 0,
                    **values,
                }
            },
            "files": {
                "file_field": (
                    "test.txt",
                    BytesIO(b"Some text content"),
                    "text/plain",
                )
            },
        }

    @classmethod
    def update(cls, task_id, field, value):
        return {
            "url": f"/{cls.path}/update/",
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            "content": json.dumps({"id": task_id, field: value}),
        }


@pytest.mark.asyncio
class TestTasks:

    requester = TaskRequester()

    @classmethod
    async def test_all(cls, async_client_as_admin):
        response = await async_client_as_admin.get(**cls.requester.all())

        assert response.status_code == 200
        assert len(response.json()) == 5

    @classmethod
    async def test_my_drafts(cls, async_client_as_manager):
        response = await async_client_as_manager.get(**cls.requester.my_drafts())

        assert response.status_code == 200
        assert len(response.json()) == 2

    @classmethod
    async def test_my_tasks(cls, async_client_as_manager):
        response = await async_client_as_manager.get(**cls.requester.my_tasks())

        assert response.status_code == 200
        assert len(response.json()) == 5

    @classmethod
    @pytest.mark.parametrize("task_id", range(1, 6))
    async def test_get_by_id(cls, task_id, async_client_as_executor):
        response = await async_client_as_executor.get(
            **cls.requester.get_by_id(task_id)
        )

        assert response.status_code == 200

    @classmethod
    @pytest.mark.parametrize("task_id", range(-6, 1))
    async def test_get_by_id_with_no_existent(cls, task_id, async_client_as_executor):
        response = await async_client_as_executor.get(
            **cls.requester.get_by_id(task_id)
        )

        assert response.status_code == 404

    @classmethod
    async def test_add(cls, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.post(**cls.requester.add())

        assert response.status_code == 200

    @classmethod
    async def test_update(cls, async_client_as_admin: AsyncClient):
        response = await async_client_as_admin.put(
            **cls.requester.update(1, "name", "asdfsadf")
        )

        assert response.json()
