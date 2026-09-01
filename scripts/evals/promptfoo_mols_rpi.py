from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "evals" / "skills" / "mols-rpi" / "cases.json"
SKILL_PATH = (
    ROOT / "src" / "rulesync" / ".rulesync" / "skills" / "mols-rpi" / "SKILL.md"
)

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

TRIGGER_RESPONSE_KEYS = {"selected_skills", "primary_skill"}
TRIGGER_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "selected_skills": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
            "uniqueItems": True,
        },
        "primary_skill": {"type": ["string", "null"]},
    },
    "required": ["selected_skills", "primary_skill"],
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


def _selection_error(value: object, label: str) -> str | None:
    if not isinstance(value, dict):
        return f"{label} must be a JSON object"
    if set(value) != TRIGGER_RESPONSE_KEYS:
        return f"{label} must contain exactly selected_skills and primary_skill"

    selected = value["selected_skills"]
    primary = value["primary_skill"]
    if not isinstance(selected, list) or not all(
        isinstance(item, str) and item for item in selected
    ):
        return f"{label} selected_skills must be a list of non-empty strings"
    if len(selected) != len(set(selected)):
        return f"{label} selected_skills must not contain duplicates"
    if primary is not None and (not isinstance(primary, str) or not primary):
        return f"{label} primary_skill must be a non-empty string or null"
    if selected and primary is None:
        return f"{label} primary_skill is required when selected_skills is non-empty"
    if not selected and primary is not None:
        return f"{label} primary_skill must be null when selected_skills is empty"
    if primary is not None and primary not in selected:
        return f"{label} primary_skill must be one of selected_skills"
    return None


def _coerce_selection(value: object, label: str) -> dict:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"{label} is not valid JSON") from error
    error = _selection_error(value, label)
    if error is not None:
        raise ValueError(error)
    return value


def _routing_candidates(value: object) -> list[dict[str, str]]:
    if value is None:
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError("routing_candidates is not valid JSON") from error
    if not isinstance(value, list):
        raise ValueError("routing_candidates must be a list")

    candidates: list[dict[str, str]] = []
    seen: set[str] = set()
    for candidate in value:
        if not isinstance(candidate, dict) or set(candidate) != {"name", "description"}:
            raise ValueError(
                "each routing candidate must contain exactly name and description"
            )
        name = candidate["name"]
        description = candidate["description"]
        if (
            not isinstance(name, str)
            or not name
            or not isinstance(description, str)
            or not description
        ):
            raise ValueError(
                "routing candidate name and description must be non-empty strings"
            )
        if name == "mols-rpi":
            raise ValueError("routing_candidates must not redefine mols-rpi")
        if name in seen:
            raise ValueError(f"duplicate routing candidate: {name}")
        seen.add(name)
        candidates.append({"name": name, "description": description})
    return candidates


def _trigger_case_contract(case: dict, mode: str) -> tuple[dict, list[dict[str, str]]]:
    expected = _coerce_selection(case.get("expected_selection"), "expected_selection")
    candidates = _routing_candidates(case.get("routing_candidates"))
    available = {"mols-rpi"}
    available.update(candidate["name"] for candidate in candidates)
    unknown = set(expected["selected_skills"]) - available
    if unknown:
        raise ValueError(
            f"expected_selection contains unavailable Skills: {sorted(unknown)}"
        )

    expects_rpi = "mols-rpi" in expected["selected_skills"]
    if expects_rpi != (mode == "activation"):
        raise ValueError(f"expected_selection conflicts with trigger mode: {mode}")
    return expected, candidates


def _semantic_rubric(assertions: list[str]) -> str:
    criteria = "\n".join(f"- {assertion}" for assertion in assertions)
    return (
        "Evaluate only the observable assistant response against every "
        "repository-owned criterion below. Do not require hidden reasoning, "
        "exact wording, or a particular valid trajectory unless a criterion "
        "explicitly requires that observable behavior. Pass only when all "
        "criteria are materially satisfied. Fail if the response agrees "
        "to a forbidden action, skips a required gate, or claims an unperformed "
        "action in a way that violates a criterion.\n"
        f"{criteria}"
    )


def _selected_case_ids(
    config: dict, suite: str, cases: dict[str, dict]
) -> tuple[str, ...]:
    selected = config.get("case_ids")
    if selected is not None:
        if not isinstance(selected, list) or not all(
            isinstance(item, str) for item in selected
        ):
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
        mode = case.get("mode")
        if not isinstance(prompt, str) or not isinstance(mode, str):
            raise ValueError(f"invalid eval case: {case_id}")
        if _case_suite(mode) != suite:
            raise ValueError(
                f"eval case {case_id} belongs to {_case_suite(mode)}, not {suite}"
            )

        vars_ = {"task": prompt, "case_id": case_id, "mode": mode}
        metadata = {
            "fixture": str(FIXTURE_PATH.relative_to(ROOT)),
            "suite": suite,
            "mode": mode,
            "case_id": case_id,
        }

        if suite == TRIGGER_SUITE:
            expected, candidates = _trigger_case_contract(case, mode)
            vars_["expected_selection"] = expected
            vars_["routing_candidates"] = candidates
            checks = [
                {
                    "type": "python",
                    "value": "file://../../scripts/evals/promptfoo_mols_rpi.py:assert_trigger",
                    "metric": (
                        "trigger-activation"
                        if "mols-rpi" in expected["selected_skills"]
                        else "trigger-rejection"
                    ),
                }
            ]
        else:
            assertions = case.get("assertions")
            if not isinstance(assertions, list) or not all(
                isinstance(item, str) and item for item in assertions
            ):
                raise ValueError(f"invalid assertions for eval case: {case_id}")
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


def _trigger_response_error(payload: object) -> str | None:
    return _selection_error(payload, "trigger provider output")


def assert_trigger(output: str, context: dict) -> dict:
    try:
        payload = json.loads(output)
    except (TypeError, json.JSONDecodeError):
        return {
            "pass": False,
            "score": 0,
            "reason": "trigger provider output is not valid JSON",
        }

    envelope_error = _trigger_response_error(payload)
    if envelope_error is not None:
        return {"pass": False, "score": 0, "reason": envelope_error}

    try:
        expected = _coerce_selection(
            context.get("vars", {}).get("expected_selection"), "expected_selection"
        )
    except ValueError as error:
        return {"pass": False, "score": 0, "reason": str(error)}

    selected = set(payload["selected_skills"])
    expected_selected = set(expected["selected_skills"])
    if (
        selected != expected_selected
        or payload["primary_skill"] != expected["primary_skill"]
    ):
        return {
            "pass": False,
            "score": 0,
            "reason": (
                f"routing selection mismatch: expected {expected}, got {payload}"
            ),
        }
    return {
        "pass": True,
        "score": 1,
        "reason": "routing selection matched expected Skills",
    }


def assert_behavior_output(output: str, context: dict) -> dict:
    if not isinstance(output, str) or not output.strip():
        return {
            "pass": False,
            "score": 0,
            "reason": "behavior provider output must be non-empty text",
        }
    return {
        "pass": True,
        "score": 1,
        "reason": "behavior provider returned observable response text",
    }


def _fixture_output(context: dict, suite: str) -> dict:
    if suite == TRIGGER_SUITE:
        try:
            expected = _coerce_selection(
                context.get("vars", {}).get("expected_selection"), "expected_selection"
            )
        except ValueError as error:
            return {
                "error": f"fixture trigger case requires valid selection: {error}",
                "output": "",
            }
        return {"output": json.dumps(expected, ensure_ascii=False)}
    if suite == BEHAVIOR_SUITE:
        return {
            "output": (
                "Promptfoo fixture-mode plumbing response; this is not runtime "
                "behavior evidence."
            )
        }
    return {"error": f"unsupported fixture suite: {suite}", "output": ""}


def _skill_frontmatter(skill: str) -> str:
    if not skill.startswith("---\n"):
        raise ValueError(f"Skill frontmatter is missing: {SKILL_PATH}")
    parts = skill.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Skill frontmatter is malformed: {SKILL_PATH}")
    return f"---{parts[1]}---"


def _skill_catalog(skill: str, candidates: list[dict[str, str]]) -> str:
    candidate_text = json.dumps(candidates, ensure_ascii=False, indent=2)
    return (
        "<skill-catalog>\n"
        f"<skill-metadata>\n{_skill_frontmatter(skill)}\n</skill-metadata>\n"
        f"<routing-candidates>\n{candidate_text}\n</routing-candidates>\n"
        "</skill-catalog>"
    )


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


def _route(
    prompt: str, skill: str, candidates: list[dict[str, str]]
) -> tuple[dict, str] | dict:
    schema_text = json.dumps(TRIGGER_RESPONSE_SCHEMA, ensure_ascii=False)
    system = (
        "Route this user request across the available Agent Skills using only "
        "the discovery metadata below. Select every Skill that is independently "
        "applicable to the request "
        "and choose exactly one primary Skill when any are selected. Prefer the most "
        "task-specific controlling owner as primary; a general orchestration Skill may "
        "compose when its own trigger applies but must not displace that owner. "
        "Do not use Skill bodies, infer selection from a name or isolated keyword, "
        "or invent unavailable Skills. Apply each description's positive "
        "conditions, negative boundaries, and "
        "composition rules.\n\n"
        "Return only JSON matching this schema exactly:\n"
        f"{schema_text}\n\n"
        f"{_skill_catalog(skill, candidates)}"
    )
    result = _ollama_request(prompt, system, TRIGGER_RESPONSE_SCHEMA)
    if isinstance(result, dict):
        return result
    parsed, content = result
    envelope_error = _trigger_response_error(parsed)
    if envelope_error is not None:
        return {
            "error": (
                f"Ollama trigger routing returned an invalid response: {envelope_error}"
            ),
            "output": content,
        }
    return parsed, content


def _execute_behavior(prompt: str, skill: str) -> tuple[str, str] | dict:
    schema_text = json.dumps(BEHAVIOR_RESPONSE_SCHEMA, ensure_ascii=False)
    system = (
        "Execute one already-activated mols-rpi behavioral evaluation. Routing "
        "has already selected the Skill, so do not re-decide activation. Use the "
        "canonical Skill below as the complete task-specific behavior contract. "
        "Follow its prerequisite, Scope, authority, Research, Plan, Work, Review, "
        "recursion, intensity, artifact, and handoff boundaries. Respond to the "
        "user's scenario as the assistant would under that Skill. "
        "Do not claim tool actions you did not perform.\n\n"
        "Return only JSON matching this schema exactly:\n"
        f"{schema_text}\n\n"
        f"<skill>\n{skill}\n</skill>"
    )
    result = _ollama_request(prompt, system, BEHAVIOR_RESPONSE_SCHEMA)
    if isinstance(result, dict):
        return result
    parsed, content = result
    if not isinstance(parsed, dict) or set(parsed) != {"response"}:
        return {
            "error": "Ollama behavior output must contain exactly response",
            "output": content,
        }
    response = parsed["response"]
    if not isinstance(response, str) or not response.strip():
        return {
            "error": "Ollama behavior response must be a non-empty string",
            "output": content,
        }
    return response, content


def _ollama_output(prompt: str, suite: str, context: dict) -> dict:
    skill = SKILL_PATH.read_text(encoding="utf-8")
    if suite == TRIGGER_SUITE:
        try:
            candidates = _routing_candidates(
                context.get("vars", {}).get("routing_candidates")
            )
        except ValueError as error:
            return {"error": f"invalid routing candidates: {error}", "output": ""}
        routed = _route(prompt, skill, candidates)
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
        return {
            "error": f"provider suite must be one of {sorted(SUITES)}",
            "output": "",
        }

    if mode == "fixture":
        return _fixture_output(context, suite)
    if mode == "ollama":
        return _ollama_output(prompt, suite, context)
    return {"error": f"unsupported Promptfoo runtime mode: {mode}", "output": ""}
