import os
import secrets
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from flask import request

# In-memory token store (MVP). For production, use a persistent store or JWT.
_TOKENS: Dict[str, "TokenInfo"] = {}


@dataclass(frozen=True)
class TokenInfo:
    """Represents an issued admin token."""

    username: str
    issued_at: int


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    if value is None:
        return None
    value = value.strip()
    return value or None


# PUBLIC_INTERFACE
def validate_admin_credentials(username: str, password: str) -> bool:
    """Validate admin credentials against environment variables.

    Env vars:
      - ADMIN_USERNAME
      - ADMIN_PASSWORD

    Returns:
        bool: True if credentials match, else False.
    """
    expected_user = _env("ADMIN_USERNAME", "admin")
    expected_pass = _env("ADMIN_PASSWORD")
    if not expected_pass:
        # Explicitly require password to be set; avoids accidental open admin.
        return False
    return username == expected_user and password == expected_pass


# PUBLIC_INTERFACE
def issue_admin_token(username: str) -> str:
    """Issue a new admin bearer token (in-memory).

    Returns:
        str: The bearer token value.
    """
    token = secrets.token_urlsafe(32)
    _TOKENS[token] = TokenInfo(username=username, issued_at=int(time.time()))
    return token


# PUBLIC_INTERFACE
def get_bearer_token_from_request() -> Optional[str]:
    """Extract Bearer token from the Authorization header.

    Returns:
        Optional[str]: token if present, otherwise None.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        return None
    parts = auth_header.split(" ", 1)
    if len(parts) != 2:
        return None
    scheme, token = parts[0].strip().lower(), parts[1].strip()
    if scheme != "bearer" or not token:
        return None
    return token


# PUBLIC_INTERFACE
def require_admin_token() -> Tuple[bool, Optional[str]]:
    """Validate the current request has a valid admin bearer token.

    Returns:
        Tuple[bool, Optional[str]]:
            (is_valid, username_if_valid)
    """
    token = get_bearer_token_from_request()
    if not token:
        return False, None
    info = _TOKENS.get(token)
    if not info:
        return False, None
    return True, info.username
