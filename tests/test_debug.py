import pytest
import cdnauth


@pytest.fixture
def client():
    with cdnauth.app.test_client() as client:
        yield client


def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 200
    assert b"pong" in res.data


def test_debug(client):
    res = client.get("/debug/")
    assert res.status_code == 302
    assert b"/saml/?sso=True&amp;next=http://localhost/" in res.data


def test_debug_with_session(client):
    with client.session_transaction() as session:
        session["samlNameId"] = "yo@example.com"
        session["samlUserdata"] = "fakeuserdata"

    res = client.get("/debug/")
    assert res.status_code == 200
