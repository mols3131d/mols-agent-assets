from __future__ import annotations

from pathlib import Path

from .github_agent import validate_agent
from .github_hooks import validate_hooks_file
from .github_mcp import validate_github_mcp
from .model import ValidationResult
from .openai_interface import validate_openai_interface
from .skill import validate_skill
from .vscode_instruction import validate_instruction
from .vscode_prompt import validate_prompt

PROFILES = {
    "agent-skill",
    "openai-skill",
    "openai-interface",
    "agent",
    "github-agent",
    "vscode-agent",
    "vscode-instruction",
    "agents-md",
    "copilot-instructions",
    "vscode-prompt",
    "github-hooks",
    "vscode-hooks",
    "github-mcp",
}


def detect_profile(path: Path) -> str:
    if path.is_dir() and (path / "SKILL.md").is_file():
        return "agent-skill"
    name = path.name
    normalized = path.as_posix()
    if name == "openai.yaml" and path.parent.name == "agents":
        return "openai-interface"
    if name == "AGENTS.md":
        return "agents-md"
    if name == "copilot-instructions.md":
        return "copilot-instructions"
    if name.endswith(".instructions.md"):
        return "vscode-instruction"
    if name.endswith(".prompt.md"):
        return "vscode-prompt"
    if name.endswith(".agent.md") or "/.github/agents/" in normalized:
        return "agent"
    if name.endswith(".json") and "/.github/hooks/" in normalized:
        return "github-hooks"
    if name in {"mcp.json", ".mcp.json", "mcp-config.json"}:
        return "github-mcp"
    raise ValueError(f"cannot infer validation profile for {path}")


def validate_target(
    path: Path,
    *,
    profile: str,
    strict: bool,
    boundary: Path | None = None,
) -> ValidationResult:
    path = path.resolve()
    if profile == "auto":
        try:
            profile = detect_profile(path)
        except ValueError as exc:
            result = ValidationResult()
            result.error(str(exc))
            return result
    if profile not in PROFILES:
        result = ValidationResult()
        result.error(f"unknown profile: {profile}")
        return result
    resolved_boundary = (boundary or (path if path.is_dir() else Path.cwd())).resolve()
    if profile in {"agent-skill", "openai-skill"}:
        return validate_skill(path, strict=strict, profile=profile)
    if profile == "openai-interface":
        skill_root = path.parent.parent
        return validate_openai_interface(path, skill_root, strict=strict)
    if profile in {"agent", "github-agent", "vscode-agent"}:
        return validate_agent(path, resolved_boundary, strict=strict, profile=profile)
    if profile in {"vscode-instruction", "agents-md", "copilot-instructions"}:
        return validate_instruction(
            path, resolved_boundary, strict=strict, profile=profile
        )
    if profile == "vscode-prompt":
        return validate_prompt(path, resolved_boundary, strict=strict)
    if profile in {"github-hooks", "vscode-hooks"}:
        return validate_hooks_file(path, strict=strict, profile=profile)
    if profile == "github-mcp":
        return validate_github_mcp(path, strict=strict)
    result = ValidationResult()
    result.error(f"unhandled profile: {profile}")
    return result
