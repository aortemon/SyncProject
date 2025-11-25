import pytest
from fastapi import status


class TestMainEndpoints:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "OK"}
