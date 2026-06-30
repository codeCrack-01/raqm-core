import pytest

from src.headers.easypaisa import generate_auth_header


def test_auth_header_success():
    result = generate_auth_header(username="admin", password="123")
    assert result == "Basic YWRtaW46MTIz"


def test_auth_header_failed():
    result = generate_auth_header(username="admin", password="321")
    assert result != "Basic YWRtaW46MTIz"
