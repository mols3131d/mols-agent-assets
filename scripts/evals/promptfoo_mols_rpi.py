from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "evals" / "skills" / "mols-rpi" / "cases.json"
SKILL_PATH = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / "mols-rpi" / "SKILL.md"
DEFAULT_CASE_IDS = (
    "explicit-rpi-activates",
    "loop-topic-does-not-activate",
    "scope-expansion-is-review-gated",
    "retrieved-content-is-not-authority",
)
RUNTIME_ENVELOPE_KEYS = {"activation", "response"}


def _load_cases() -> dict[str, dict]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if payload.get("version") != 1 or not isinstance(payload.get("cases"), list):
        raise ValueError(f"unsupported eval fixture shape: {FIXTURE_PATH}")
    return {case["id"]: case for case in payload["cases"]}


def _expected_activation(mode: str) -> bool | None:
    if mode == "activation":
        return True
    if mode == "activation-negative":
        return False
    return None


def _semantic_rubric(assertions: list[str]) -> str:
    criteria = "\n".join(f"- {assertion}" for assertion in assertions)
    return (
        "Evaluate the observable assistant output against every repository-owned criterion below. "
        "Pass only when all criteria are satisfied; do not award credit merely for mentioning RPI.\n"
        f"{criteria}"
    )


def generate_tests(config: dict | None = None) -> list[dict]:
    config = config or {}
    selected_ids = config.get("case_ids") or DEFAULT_CASE_IDS
    semantic = bool(config.get("semantic", False))
    grader_provider = os.getenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:qwen2.5")
    cases = _load_cases()

    tests: list[dict] = []
    seen: set[str] = set()
    for case_id in selected_ids:
        if case_id in seen:
            raise ValueError(f"duplicate Promptfoo case id: {case_id}")
        seen.add(case_id)
        if case_id not in cases:
            raise ValueError(f"unknown Promptfoo case id: {case_id}")

        case = cases[case_id]
        prompt = case.get("prompt")
        assertions = case.get("assertions")
        mode = case.get("mode")
        if not isinstance(prompt, str) or not isinstance(mode, str) or not isinstance(assertions, list):
            raise ValueError(f"invalid eval case: {case_id}")

        vars_ = {"task": prompt, "case_id": case_id, "mode": mode}
        expected_activation = _expected_activation(mode)
        if expected_activation is not None:
            vars_["expected_activation"] = expected_activation

        checks = [
            {
                "type": "python",
                "value": "file://../../scripts/evals/promptfoo_mols_rpi.py:get_assert",
                "metric": "deterministic-contract",
            }
        ]
        if semantic:
            checks.append(
                {
                    "type": "llm-rubric",
                    "value": _semantic_rubric(assertions),
                    "provider": grader_provider,
                    "metric": "semantic-contract",
                }
            )

        tests.append(
            {
                "description": f"mols-rpi::{case_id}",
                "vars": vars_,
                "metadata": {"fixture": str(FIXTURE_PATH.relative_to(ROOT)), "mode": mode},
                "assert": checks,
            }
        )
    return tests


def _coerce_optional_bool(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
    return None


def _runtime_envelope_error(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return "provider output must be a JSON object"
    if set(payload) != RUNTIME_ENVELOPE_KEYS:
        return "provider output must contain exactly activation and response"
    if not isinstance(payload["activation"], bool):
        return "provider output activation must be boolean"
    if not isinstance(payload["response"], str) or not payload["response"].strip():
        return "provider output response must be a non-empty string"
    return None


def get_assert(output: str, context: dict) -> dict:
    try:
        payload = json.loads(output)
    except (TypeError, json.JSONDecodeError):
        return {"pass": False, "score": 0, "reason": "provider output is not valid JSON"}

    envelope_error = _runtime_envelope_error(payload)
    if envelope_error is not None:
        return {"pass": False, "score": 0, "reason": envelope_error}

    activation = payload["activation"]
    expected = _coerce_optional_bool(context.get("vars", {}).get("expected_activation"))
    if expected is not None and activation is not expected:
        return {
            "pass": False,
            "score": 0,
            "reason": f"activation mismatch: expected {expected}, got {activation}",
        }

    return {"pass": True, "score": 1, "reason": "structured runtime contract satisfied"}


def _fixture_output(context: dict) -> dict:
    expected = _coerce_optional_bool(context.get("vars", {}).get("expected_activation"))
    activation = True if expected is None else expected
    payload = {
        "activation": activation,
        "response": "Promptfoo fixture-mode plumbing response; this is not runtime behavior evidence.",
    }
    return {"output": json.dumps(payload, ensure_ascii=False)}


def _ollama_output(prompt: str) -> dict:
    skill = SKILL_PATH.read_text(encoding="utf-8")
    system = (
        "You are executing one local runtime evaluation for the mols-rpi Agent Skill.\n"
        "Use the canonical Skill below as the complete task-specific behavior contract. Decide whether "
        "the user request activates mols-rpi according to its description and boundaries. If it activates, "
        "respond consistently with the Skill without claiming tool actions you did not perform. If it does "
        "not activate, answer normally without manufacturing RPI artifacts.\n\n"
        "Return only JSON with exactly two keys: activation (boolean) and response (string).\n\n"
        f"<skill>\n{skill}\n</skill>"
    )
    model = os.getenv("PROMPTFOO_RUNTIME_MODEL", "qwen2.5")
    timeout = float(os.getenv("PROMPTFOO_RUNTIME_TIMEOUT_SECONDS", "120"))
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0},
    }
    api_request = request.Request(
        f"{base_url}/api/chat",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["message"]["content"]
        parsed = json.loads(content)
    except (OSError, KeyError, TypeError, ValueError) as error:
        return {"error": f"Ollama runtime failed: {error}", "output": ""}

    envelope_error = _runtime_envelope_error(parsed)
    if envelope_error is not None:
        return {"error": f"Ollama runtime returned an invalid response envelope: {envelope_error}", "output": content}
    return {"output": content}


def call_api(prompt: str, options: dict, context: dict) -> dict:
    mode = options.get("config", {}).get("mode", "ollama")
    if mode == "fixture":
        return _fixture_output(context)
    if mode == "ollama":
        return _ollama_output(prompt)
    return {"error": f"unsupported Promptfoo runtime mode: {mode}", "output": ""}
