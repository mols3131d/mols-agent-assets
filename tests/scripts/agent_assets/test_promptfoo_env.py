import pytest

from scripts.agent_assets import promptfoo_env as config


@pytest.mark.parametrize(
    "env, expected",
    [
        ({}, 120000),
        ({"REQUEST_TIMEOUT_MS": "9000"}, 9000),
        ({"PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "75"}, 75000),
        ({"PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "0.125"}, 125),
        ({"PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "0.001"}, 1),
        ({"REQUEST_TIMEOUT_MS": " 9000 "}, 9000),
        ({"REQUEST_TIMEOUT_MS": "", "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "2"}, 2000),
        ({"REQUEST_TIMEOUT_MS": " ", "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": " "}, 120000),
        (
            {
                "REQUEST_TIMEOUT_MS": "9000",
                "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "invalid-unused-legacy-value",
            },
            9000,
        ),
    ],
)
def test_request_timeout_resolves_native_then_legacy_then_default(env, expected):
    assert config.request_timeout_ms(env) == expected


@pytest.mark.parametrize("value", ["invalid", "0", "-1", "1.5", "nan", "inf"])
def test_request_timeout_rejects_invalid_native_value_without_legacy_fallback(value):
    with pytest.raises(
        ValueError, match="REQUEST_TIMEOUT_MS must be a positive integer"
    ):
        config.request_timeout_ms(
            {"REQUEST_TIMEOUT_MS": value, "PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": "120"}
        )


@pytest.mark.parametrize(
    "value", ["invalid", "0", "-1", "0.0001", "nan", "inf", "1e999"]
)
def test_request_timeout_rejects_invalid_legacy_value(value):
    with pytest.raises(
        ValueError, match="PROMPTFOO_RUNTIME_TIMEOUT_SECONDS must be finite"
    ):
        config.request_timeout_ms({"PROMPTFOO_RUNTIME_TIMEOUT_SECONDS": value})


@pytest.mark.parametrize("value", ["", "0", "abc", "2147483648"])
def test_invalid_codex_timeout_is_rejected(value):
    with pytest.raises(ValueError, match="PROMPTFOO_CODEX_TIMEOUT_MS"):
        config.codex_timeout_ms({"PROMPTFOO_CODEX_TIMEOUT_MS": value})


def test_codex_timeout_does_not_use_ollama_timeout():
    assert config.codex_timeout_ms({"REQUEST_TIMEOUT_MS": "5"}) == 120000


@pytest.mark.parametrize(
    "value",
    ["", "file:///tmp/model", "http://user:key@localhost", "http://localhost:abc"],
)
def test_invalid_ollama_endpoint_is_rejected(value):
    with pytest.raises(ValueError, match="OLLAMA_BASE_URL"):
        config.ollama_base_url({"OLLAMA_BASE_URL": value})
