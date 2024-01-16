import os
import pytest
import cdnauth


@pytest.fixture
def client():
    os.environ["FLASK_ENV"] = "testing"
    with cdnauth.app.test_client() as client:
        yield client


def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 200
    assert b"pong" in res.data


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
