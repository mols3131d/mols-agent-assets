from __future__ import annotations

import math
from collections.abc import Mapping

DEFAULT_RUNTIME_MODEL = "qwen2.5"
DEFAULT_GRADER_PROVIDER = f"ollama:chat:{DEFAULT_RUNTIME_MODEL}"
DEFAULT_REQUEST_TIMEOUT_MS = 120_000


def setting(env: Mapping[str, str], name: str, default: str) -> str:
    return env.get(name, "").strip() or default


def request_timeout_ms(env: Mapping[str, str]) -> int:
    native = env.get("REQUEST_TIMEOUT_MS", "").strip()
    if native:
        try:
            milliseconds = int(native)
        except ValueError:
            raise ValueError(
                "REQUEST_TIMEOUT_MS must be a positive integer in milliseconds"
            ) from None
        if milliseconds <= 0:
            raise ValueError(
                "REQUEST_TIMEOUT_MS must be a positive integer in milliseconds"
            )
        return milliseconds

    legacy = env.get("PROMPTFOO_RUNTIME_TIMEOUT_SECONDS", "").strip()
    if not legacy:
        return DEFAULT_REQUEST_TIMEOUT_MS
    try:
        milliseconds = float(legacy) * 1000
    except ValueError:
        milliseconds = math.nan
    if not math.isfinite(milliseconds) or milliseconds < 1:
        raise ValueError(
            "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS must be finite "
            "and at least 0.001 seconds"
        )
    return int(milliseconds)
