import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from backend.app.core.config import settings

ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16
)


def get_password_hash(password: str) -> str:
    """Hashes a password using Argon2id."""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against an Argon2id hash."""
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


def generate_public_reference() -> str:
    """Generates a secure, human-readable random public reference ID like REF-2026-9842."""
    year = datetime.now().year
    alphabet = string.ascii_uppercase + string.digits
    suffix = "".join(secrets.choice(alphabet) for _ in range(4))
    return f"REF-{year}-{suffix}"


def generate_tracking_secret() -> str:
    """Generates a high-entropy secret token for report status tracking."""
    token = secrets.token_urlsafe(24)
    return f"TRK-{token}"


def hash_tracking_secret(secret: str) -> str:
    """Hashes a tracking secret before storage in database."""
    return ph.hash(secret)


def verify_tracking_secret(plain_secret: str, hashed_secret: str) -> bool:
    """Verifies a tracking secret against its stored Argon2id hash."""
    try:
        return ph.verify(hashed_secret, plain_secret)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Creates a signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """Decodes and validates a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
