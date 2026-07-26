from typing import Any


def req(t: type = str, **kwargs: Any) -> dict[str, Any]:
    return {"type": t, "required": True, **kwargs}


def opt(t: type = str, default: Any = "", **kwargs: Any) -> dict[str, Any]:
    return {"type": t, "required": False, "default": default, **kwargs}


SUMMARY_SCHEMA: dict[str, Any] = {
    "frontmatter": {
        "title": req(),
        "date": req(),
        "type": req(default="code-review-summary"),
    },
    "sections": ("Summary", "Findings Details"),
}

FINDING_SCHEMA: dict[str, Any] = {
    "frontmatter": {
        "title": req(),
        "description": opt(),
        "type": req(default="code-review-finding"),
        "priority": opt(
            default="p4",
            allowed_values=("p0", "p1", "p2", "p3", "p4"),
        ),
    },
    "sections": (
        "Summary",
        "Observation",
        "Impact",
        "Recommendation",
        "Verification",
    ),
}

TEMPLATE_SCHEMAS: dict[str, dict[str, Any]] = {
    "code-review-summary": SUMMARY_SCHEMA,
    "code-review-finding": FINDING_SCHEMA,
}
