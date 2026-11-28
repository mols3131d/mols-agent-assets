from __future__ import annotations

import math
from collections.abc import Mapping
from urllib.parse import urlsplit

DEFAULT_REQUEST_TIMEOUT_MS = 120_000
MAX_TIMEOUT_MS = 2_147_483_647


def ollama_base_url(env: Mapping[str, str]) -> str:
    value = env.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    try:
        url = urlsplit(value)
        url.port
        if (
            value != value.strip()
            or any(char.isspace() for char in value)
            or url.scheme not in {"http", "https"}
            or not url.hostname
            or url.username is not None
            or url.password is not None
            or url.query
            or url.fragment
        ):
            raise ValueError
    except ValueError:
        raise ValueError(
            "OLLAMA_BASE_URL must be an HTTP(S) base URL without credentials"
        ) from None
    return value.rstrip("/")


def positive_timeout(value: str, name: str) -> int:
    try:
        milliseconds = int(value)
        if 1 <= milliseconds <= MAX_TIMEOUT_MS:
            return milliseconds
    except ValueError:
        pass
    raise ValueError(
        f"{name} must be a positive integer in milliseconds (at most {MAX_TIMEOUT_MS})"
    )


def codex_timeout_ms(env: Mapping[str, str]) -> int:
    value = env.get("PROMPTFOO_CODEX_TIMEOUT_MS")
    if value is None:
        return DEFAULT_REQUEST_TIMEOUT_MS
    return positive_timeout(value, "PROMPTFOO_CODEX_TIMEOUT_MS")


def request_timeout_ms(env: Mapping[str, str]) -> int:
    native = env.get("REQUEST_TIMEOUT_MS", "").strip()
    if native:
        return positive_timeout(native, "REQUEST_TIMEOUT_MS")

    legacy = env.get("PROMPTFOO_RUNTIME_TIMEOUT_SECONDS", "").strip()
    if not legacy:
        return DEFAULT_REQUEST_TIMEOUT_MS
    try:
        milliseconds = float(legacy) * 1000
    except ValueError:
        milliseconds = math.nan
    if not math.isfinite(milliseconds) or not 1 <= milliseconds <= MAX_TIMEOUT_MS:
        raise ValueError(
            "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS must be finite "
            f"and yield between 1 and {MAX_TIMEOUT_MS} milliseconds"
        )
    return int(milliseconds)
