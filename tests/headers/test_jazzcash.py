from hashlib import sha256

from src.raqm_core.headers.jazzcash import generate_secure_hash


def test_generate_secure_hash_pass_standard():
    hash_key = "secret_key"
    params = {"b_param": "value2", "a_param": "value1"}

    expected_hash = sha256(b"secret_key&value1&value2").hexdigest()
    assert generate_secure_hash(hash_key, params) == expected_hash


def test_generate_secure_hash_pass_empty_params():
    hash_key = "secret_key"
    params = {}

    expected_hash = sha256(b"secret_key&").hexdigest()
    assert generate_secure_hash(hash_key, params) == expected_hash


def test_generate_secure_hash_fail_includes_keys():
    hash_key = "secret_key"
    params = {"a": "1", "b": "2"}

    wrong_expected_hash = sha256(b"secret_key&a=1&b=2").hexdigest()
    assert generate_secure_hash(hash_key, params) != wrong_expected_hash


def test_generate_secure_hash_fail_wrong_sort_assumption():
    hash_key = "secret_key"
    params = {"z": "last", "a": "first"}

    wrong_expected_hash = sha256(b"secret_key&last&first").hexdigest()
    assert generate_secure_hash(hash_key, params) != wrong_expected_hash
