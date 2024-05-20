from flask import current_app

import pytest
import cdnauth


@pytest.fixture
def client():
    with cdnauth.app.test_client() as client:
        yield client


# we need to test all routes with no session to confirm we redirect
# we also need to test all routes with a valid session["samlNameId"]
# to confirm the expected behavior


def test_root_no_download_url_no_session(client):
    res = client.get("/")
    assert res.status_code == 302
    assert b"/saml/?sso=True&amp;next=http://localhost/" in res.data


def test_root_no_download_url_with_session(client):
    with client.session_transaction() as session:
        session["samlNameId"] = "yo@example.com"

    res = client.get("/")
    assert res.status_code == 200
    assert b"No download URL present" in res.data


def test_invalid_download_url_no_session(client):
    res = client.get("/?cdn_resource=http://example.com")
    assert res.status_code == 302
    assert b"/saml/?sso=True&amp;next=http://localhost/" in res.data


def test_invalid_download_url_with_session(client):
    with client.session_transaction() as session:
        session["samlNameId"] = "yo@example.com"

    res = client.get("/?cdn_resource=http://example.com")
    assert res.status_code == 200
    assert b"Invalid redirect URL" in res.data


def test_valid_download_url_no_session(client):
    res = client.get("/?cdn_resource=http://cdn.libraries.mit.edu/restricted/stuff.zip")
    assert res.status_code == 302
    assert b"/saml/?sso=True&amp;next=http://localhost/" in res.data


def test_valid_download_url_with_session(client):
    with client.session_transaction() as session:
        session["samlNameId"] = "yo@example.com"

    res = client.get("/?cdn_resource=http://cdn.libraries.mit.edu/restricted/stuff.zip")
    assert res.status_code == 200
    assert b"MIT authentication successful: " in res.data
    assert b"your download should start shortly." in res.data
    assert b"Close this window/tab to return to your search." not in res.data


def test_valid_download_url_with_session_timdexui_flag(client):
    with client.session_transaction() as session:
        session["samlNameId"] = "yo@example.com"

    res = client.get("/?cdn_resource=http://cdn.libraries.mit.edu/restricted/stuff.zip?timdexui=true")
    assert res.status_code == 200
    assert b"MIT authentication successful: " in res.data
    assert b"your download should start shortly." in res.data
    assert b"Close this window/tab to return to your search." in res.data


def test_valid_request_sets_cookie(client):
    with client.session_transaction() as session:
        session["samlNameId"] = "yo@example.com"

    res = client.get("/?cdn_resource=http://cdn.libraries.mit.edu/restricted/stuff.zip")
    assert res.status_code == 200
    cookie_header = res.headers["Set-Cookie"]
    assert current_app.config["COOKIE_NAME"] in cookie_header
    assert f'Domain={current_app.config["COOKIE_DOMAIN"]}' in cookie_header


def test_metadata(client):
    res = client.get("/saml/metadata/")
    assert res.status_code == 200
