"""Shared helpers for iDoklad read-only and prepare-only scripts."""

from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request


TIMEOUT_SECONDS = 20
DEFAULT_ENV_FILES = [".env.idoklad", ".env.local", ".env"]


def load_env_file() -> None:
    for candidate in DEFAULT_ENV_FILES:
        path = Path(candidate)
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key or key in os.environ:
                continue
            os.environ[key] = value
        return


def getenv_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def post_form(url: str, data: dict[str, str]) -> dict:
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"POST {url} failed with {exc.code}: {body}") from exc


def get_json(url: str, token: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {url} failed with {exc.code}: {body}") from exc


def get_access_token() -> tuple[str, int | None]:
    load_env_file()
    application_id = getenv_required("IDOKLAD_APPLICATION_ID")
    client_id = getenv_required("IDOKLAD_CLIENT_ID")
    client_secret = getenv_required("IDOKLAD_CLIENT_SECRET")
    auth_url = getenv_required("IDOKLAD_AUTH_URL").rstrip("/")
    scope = os.environ.get("IDOKLAD_SCOPE", "idoklad_api").strip()

    token_payload = post_form(
        f"{auth_url}/server/v2/connect/token",
        {
            "grant_type": "client_credentials",
            "application_id": application_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        },
    )
    access_token = token_payload.get("access_token")
    expires_in = token_payload.get("expires_in")
    if not access_token:
        raise RuntimeError("Token response did not include access_token")
    return access_token, expires_in


def get_api_url() -> str:
    load_env_file()
    return getenv_required("IDOKLAD_API_URL").rstrip("/")


def api_get(path: str, token: str, query: dict[str, str | int] | None = None) -> dict:
    api_url = get_api_url()
    query_string = ""
    if query:
        query_string = "?" + urllib.parse.urlencode(query)
    return get_json(f"{api_url}{path}{query_string}", token)
