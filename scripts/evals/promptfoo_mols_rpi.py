from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "evals" / "skills" / "mols-rpi" / "cases.json"
SKILL_PATH = ROOT / "src" / "rulesync" / ".rulesync" / "skills" / "mols-rpi" / "SKILL.md"

TRIGGER_SUITE = "trigger"
BEHAVIOR_SUITE = "behavior"
SUITES = {TRIGGER_SUITE, BEHAVIOR_SUITE}
TRIGGER_MODES = {"activation", "activation-negative"}

TRIGGER_PROVIDER_LABEL = "mols-rpi-trigger"
BEHAVIOR_PROVIDER_LABEL = "mols-rpi-behavior"
PROVIDER_LABELS = {
    TRIGGER_SUITE: TRIGGER_PROVIDER_LABEL,
    BEHAVIOR_SUITE: BEHAVIOR_PROVIDER_LABEL,
}

TRIGGER_RESPONSE_KEYS = {"activation"}
TRIGGER_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {"activation": {"type": "boolean"}},
    "required": ["activation"],
    "additionalProperties": False,
}
BEHAVIOR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {"response": {"type": "string", "minLength": 1}},
    "required": ["response"],
    "additionalProperties": False,
}


def _load_cases() -> dict[str, dict]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if payload.get("version") != 1 or not isinstance(payload.get("cases"), list):
        raise ValueError(f"unsupported eval fixture shape: {FIXTURE_PATH}")

    cases: dict[str, dict] = {}
    for case in payload["cases"]:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"invalid eval case id in {FIXTURE_PATH}")
        if case_id in cases:
            raise ValueError(f"duplicate eval case id: {case_id}")
        cases[case_id] = case
    return cases


def _case_suite(mode: str) -> str:
    return TRIGGER_SUITE if mode in TRIGGER_MODES else BEHAVIOR_SUITE


def _expected_activation(mode: str) -> bool:
    if mode not in TRIGGER_MODES:
        raise ValueError(f"mode is not a trigger-eval mode: {mode}")
    return mode == "activation"


def _semantic_rubric(assertions: list[str]) -> str:
    criteria = "\n".join(f"- {assertion}" for assertion in assertions)
    return (
        "Evaluate only the observable assistant response against every repository-owned criterion below. "
        "Do not require hidden reasoning, exact wording, or a particular valid trajectory unless a criterion "
        "explicitly requires that observable behavior. Pass only when all criteria are materially satisfied. "
        "Fail if the response agrees to a forbidden action, skips a required gate, or claims an unperformed "
        "action in a way that violates a criterion.\n"
        f"{criteria}"
    )


def _selected_case_ids(config: dict, suite: str, cases: dict[str, dict]) -> tuple[str, ...]:
    selected = config.get("case_ids")
    if selected is not None:
        if not isinstance(selected, list) or not all(isinstance(item, str) for item in selected):
            raise ValueError("case_ids must be a list of strings")
        return tuple(selected)

    return tuple(
        case_id
        for case_id, case in cases.items()
        if isinstance(case.get("mode"), str) and _case_suite(case["mode"]) == suite
    )


def generate_tests(config: dict | None = None) -> list[dict]:
    config = config or {}
    suite = config.get("suite")
    if suite not in SUITES:
        raise ValueError(f"suite must be one of {sorted(SUITES)}")

    cases = _load_cases()
    selected_ids = _selected_case_ids(config, suite, cases)
    semantic = bool(config.get("semantic", suite == BEHAVIOR_SUITE))
    provider_label = config.get("provider_label") or PROVIDER_LABELS[suite]
    if not isinstance(provider_label, str) or not provider_label:
        raise ValueError("provider_label must be a non-empty string")

    rubric_threshold = config.get("rubric_threshold", 0.8)
    if not isinstance(rubric_threshold, (int, float)) or not 0 <= rubric_threshold <= 1:
        raise ValueError("rubric_threshold must be between 0 and 1")

    grader_provider = os.getenv("PROMPTFOO_GRADER_PROVIDER", "ollama:chat:qwen2.5")

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
        if not all(isinstance(item, str) and item for item in assertions):
            raise ValueError(f"invalid assertions for eval case: {case_id}")
        if _case_suite(mode) != suite:
            raise ValueError(f"eval case {case_id} belongs to {_case_suite(mode)}, not {suite}")

        vars_ = {"task": prompt, "case_id": case_id, "mode": mode}
        metadata = {
            "fixture": str(FIXTURE_PATH.relative_to(ROOT)),
            "suite": suite,
            "mode": mode,
            "case_id": case_id,
        }

        if suite == TRIGGER_SUITE:
            expected = _expected_activation(mode)
            vars_["expected_activation"] = expected
            checks = [
                {
                    "type": "python",
                    "value": "file://../../scripts/evals/promptfoo_mols_rpi.py:assert_trigger",
                    "metric": "trigger-activation" if expected else "trigger-rejection",
                }
            ]
        else:
            checks = [
                {
                    "type": "python",
                    "value": "file://../../scripts/evals/promptfoo_mols_rpi.py:assert_behavior_output",
                    "metric": "behavior-output",
                }
            ]
            if semantic:
                checks.append(
                    {
                        "type": "llm-rubric",
                        "value": _semantic_rubric(assertions),
                        "provider": grader_provider,
                        "threshold": float(rubric_threshold),
                        "metric": "behavior-contract",
                    }
                )

        tests.append(
            {
                "description": f"mols-rpi::{suite}::{case_id}",
                "vars": vars_,
                "metadata": metadata,
                "providers": [provider_label],
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


def _trigger_response_error(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return "trigger provider output must be a JSON object"
    if set(payload) != TRIGGER_RESPONSE_KEYS:
        return "trigger provider output must contain exactly activation"
    if not isinstance(payload["activation"], bool):
        return "trigger provider output activation must be boolean"
    return None


def assert_trigger(output: str, context: dict) -> dict:
    try:
        payload = json.loads(output)
    except (TypeError, json.JSONDecodeError):
        return {"pass": False, "score": 0, "reason": "trigger provider output is not valid JSON"}

    envelope_error = _trigger_response_error(payload)
    if envelope_error is not None:
        return {"pass": False, "score": 0, "reason": envelope_error}

    expected = _coerce_optional_bool(context.get("vars", {}).get("expected_activation"))
    if expected is None:
        return {"pass": False, "score": 0, "reason": "expected_activation is missing"}

    activation = payload["activation"]
    if activation is not expected:
        return {
            "pass": False,
            "score": 0,
            "reason": f"activation mismatch: expected {expected}, got {activation}",
        }
    return {"pass": True, "score": 1, "reason": "trigger classification matched expected activation"}


def assert_behavior_output(output: str, context: dict) -> dict:
    if not isinstance(output, str) or not output.strip():
        return {"pass": False, "score": 0, "reason": "behavior provider output must be non-empty text"}
    return {"pass": True, "score": 1, "reason": "behavior provider returned observable response text"}


def _fixture_output(context: dict, suite: str) -> dict:
    if suite == TRIGGER_SUITE:
        expected = _coerce_optional_bool(context.get("vars", {}).get("expected_activation"))
        if expected is None:
            return {"error": "fixture trigger case requires expected_activation", "output": ""}
        return {"output": json.dumps({"activation": expected}, ensure_ascii=False)}
    if suite == BEHAVIOR_SUITE:
        return {
            "output": "Promptfoo fixture-mode plumbing response; this is not runtime behavior evidence."
        }
    return {"error": f"unsupported fixture suite: {suite}", "output": ""}


def _skill_frontmatter(skill: str) -> str:
    if not skill.startswith("---\n"):
        raise ValueError(f"Skill frontmatter is missing: {SKILL_PATH}")
    parts = skill.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Skill frontmatter is malformed: {SKILL_PATH}")
    return f"---{parts[1]}---"


def _ollama_request(prompt: str, system: str, schema: dict) -> tuple[dict, str] | dict:
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
        "format": schema,
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
    return parsed, content


def _route(prompt: str, skill: str) -> tuple[dict, str] | dict:
    schema_text = json.dumps(TRIGGER_RESPONSE_SCHEMA, ensure_ascii=False)
    system = (
        "Classify whether this user request should activate one Agent Skill using only the discovery "
        "metadata below. Do not use the Skill body or infer activation from the Skill name or an isolated "
        "keyword alone. Apply the positive use conditions and negative boundaries expressed by the metadata.\n\n"
        "Return only JSON matching this schema exactly:\n"
        f"{schema_text}\n\n"
        f"<skill-metadata>\n{_skill_frontmatter(skill)}\n</skill-metadata>"
    )
    result = _ollama_request(prompt, system, TRIGGER_RESPONSE_SCHEMA)
    if isinstance(result, dict):
        return result
    parsed, content = result
    envelope_error = _trigger_response_error(parsed)
    if envelope_error is not None:
        return {
            "error": f"Ollama trigger routing returned an invalid response: {envelope_error}",
            "output": content,
        }
    return parsed, content


def _execute_behavior(prompt: str, skill: str) -> tuple[str, str] | dict:
    schema_text = json.dumps(BEHAVIOR_RESPONSE_SCHEMA, ensure_ascii=False)
    system = (
        "Execute one already-activated mols-rpi behavioral evaluation. Routing has already selected the "
        "Skill, so do not re-decide activation. Use the canonical Skill below as the complete task-specific "
        "behavior contract. Follow its prerequisite, Scope, authority, Research, Plan, Work, Review, "
        "recursion, intensity, artifact, and handoff boundaries. Respond to the user's scenario as the "
        "assistant would under that Skill. Do not claim tool actions you did not perform.\n\n"
        "Return only JSON matching this schema exactly:\n"
        f"{schema_text}\n\n"
        f"<skill>\n{skill}\n</skill>"
    )
    result = _ollama_request(prompt, system, BEHAVIOR_RESPONSE_SCHEMA)
    if isinstance(result, dict):
        return result
    parsed, content = result
    if not isinstance(parsed, dict) or set(parsed) != {"response"}:
        return {"error": "Ollama behavior output must contain exactly response", "output": content}
    response = parsed["response"]
    if not isinstance(response, str) or not response.strip():
        return {"error": "Ollama behavior response must be a non-empty string", "output": content}
    return response, content


def _ollama_output(prompt: str, suite: str) -> dict:
    skill = SKILL_PATH.read_text(encoding="utf-8")
    if suite == TRIGGER_SUITE:
        routed = _route(prompt, skill)
        if isinstance(routed, dict):
            return routed
        _, route_content = routed
        return {"output": route_content}
    if suite == BEHAVIOR_SUITE:
        behavior = _execute_behavior(prompt, skill)
        if isinstance(behavior, dict):
            return behavior
        response, _ = behavior
        return {"output": response}
    return {"error": f"unsupported Ollama suite: {suite}", "output": ""}


def call_api(prompt: str, options: dict, context: dict) -> dict:
    config = options.get("config", {})
    mode = config.get("mode", "ollama")
    suite = config.get("suite")
    if suite not in SUITES:
        return {"error": f"provider suite must be one of {sorted(SUITES)}", "output": ""}

    if mode == "fixture":
        return _fixture_output(context, suite)
    if mode == "ollama":
        return _ollama_output(prompt, suite)
    return {"error": f"unsupported Promptfoo runtime mode: {mode}", "output": ""}
