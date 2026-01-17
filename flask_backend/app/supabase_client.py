import os
from typing import Optional

from supabase import Client, create_client


def _get_env(name: str) -> Optional[str]:
    """Internal helper to fetch environment variables safely."""
    value = os.getenv(name)
    if value is not None:
        value = value.strip()
    return value or None


# PUBLIC_INTERFACE
def get_supabase_client() -> Client:
    """Create and return a Supabase client using environment variables.

    Required env vars:
      - SUPABASE_URL
      - SUPABASE_SERVICE_ROLE_KEY

    Returns:
        supabase.Client: Initialized client instance.

    Raises:
        RuntimeError: If required env vars are not set.
    """
    url = _get_env("SUPABASE_URL")
    key = _get_env("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Supabase is not configured. Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )
    return create_client(url, key)
