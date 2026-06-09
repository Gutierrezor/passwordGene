import string
import pytest

from src.password_generator import generate_password


def test_length_and_types_all_enabled():
    pwd = generate_password(12, True, True, True)
    assert len(pwd) == 12
    assert any(c.islower() for c in pwd)
    assert any(c.isupper() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in string.punctuation for c in pwd)


def test_disable_all_optional_types():
    pwd = generate_password(10, False, False, False)
    assert len(pwd) == 10
    assert all(c.islower() for c in pwd)


def test_length_too_small_raises():
    # Requires at least 4 characters when all options on (lower + upper + digits + special)
    with pytest.raises(ValueError):
        generate_password(2, True, True, True)


def test_zero_or_negative_length_raises():
    with pytest.raises(ValueError):
        generate_password(0)
    with pytest.raises(ValueError):
        generate_password(-5)
