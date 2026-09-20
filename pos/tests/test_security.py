from datetime import timedelta

from app.services.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing_and_verification():
    password = "secretpassword"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_token_generation_decoding_and_expiration():
    token = create_access_token({"sub": "admin_user"})
    assert decode_access_token(token)["sub"] == "admin_user"

    expired = create_access_token(
        {"sub": "admin_user"}, expires_delta=timedelta(seconds=-1)
    )
    assert decode_access_token(expired) is None
