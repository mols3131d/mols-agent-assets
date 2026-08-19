from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "src" / "rulesync"


def rulesync_command() -> list[str]:
    npx = shutil.which("npx")
    if npx is None:
        raise RuntimeError("npx is required to run Rulesync")
    return [npx, "--yes", "rulesync@latest"]


def run(args: list[str], cwd: Path) -> None:
    subprocess.run([*rulesync_command(), *args], cwd=cwd, check=True)


def markdown_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return text.strip()
    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise AssertionError(f"unclosed frontmatter: {path}") from exc
    return "\n".join(lines[end + 1 :]).strip()


def relative_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def assert_skill_projection(workspace: Path, output_dir: Path) -> None:
    source_dir = workspace / ".rulesync" / "skills"
    source_names = {
        path.name
        for path in source_dir.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    output_names = {path.name for path in output_dir.iterdir() if path.is_dir()}
    assert output_names == source_names, (
        f"Skill projection set mismatch for {output_dir}: "
        f"expected {sorted(source_names)}, got {sorted(output_names)}"
    )

    for name in source_names:
        source = source_dir / name
        output = output_dir / name
        source_files = relative_files(source)
        output_files = relative_files(output)
        assert output_files == source_files, (
            f"Skill package shape mismatch for {output}: "
            f"expected {sorted(source_files)}, got {sorted(output_files)}"
        )
        assert markdown_body(output / "SKILL.md") == markdown_body(source / "SKILL.md"), (
            f"Skill body changed during projection: {name}"
        )
        for relative_path in source_files - {"SKILL.md"}:
            assert (output / relative_path).read_bytes() == (
                source / relative_path
            ).read_bytes(), f"Skill supporting file changed during projection: {name}/{relative_path}"


def assert_projection(workspace: Path) -> None:
    source = workspace / ".rulesync"

    root_rule = source / "rules" / "overview.md"
    for output in (
        workspace / ".github" / "copilot-instructions.md",
        workspace / "AGENTS.md",
    ):
        assert output.is_file(), f"missing projected root Rule: {output}"
        assert markdown_body(output) == markdown_body(root_rule), (
            f"root Rule body changed during projection: {output}"
        )

    assert_skill_projection(workspace, workspace / ".github" / "skills")
    assert_skill_projection(workspace, workspace / ".agents" / "skills")

    source_agents = {
        path.stem for path in (source / "subagents").glob("*.md") if path.is_file()
    }
    copilot_agents = {
        path.name.removesuffix(".agent.md")
        for path in (workspace / ".github" / "agents").glob("*.agent.md")
    }
    antigravity_agents = {
        path.stem for path in (workspace / ".agents" / "agents").glob("*.md")
    }
    assert copilot_agents == source_agents, "Copilot subagent projection set mismatch"
    assert antigravity_agents == source_agents, "Antigravity subagent projection set mismatch"

    for name in source_agents:
        source_body = markdown_body(source / "subagents" / f"{name}.md")
        assert markdown_body(
            workspace / ".github" / "agents" / f"{name}.agent.md"
        ) == source_body, f"Copilot subagent body changed during projection: {name}"
        assert markdown_body(
            workspace / ".agents" / "agents" / f"{name}.md"
        ) == source_body, f"Antigravity subagent body changed during projection: {name}"


def doctor() -> None:
    run(["doctor", "--strict"], WORKSPACE)


def preview() -> None:
    run(["generate", "--dry-run"], WORKSPACE)


def validate() -> None:
    with tempfile.TemporaryDirectory(prefix="rulesync-validate-") as temp_dir:
        workspace = Path(temp_dir) / "rulesync"
        shutil.copytree(WORKSPACE, workspace)
        run(["doctor", "--strict"], workspace)
        run(["generate"], workspace)
        assert_projection(workspace)
        run(["generate", "--check"], workspace)


def main() -> None:
    commands = {
        "doctor": doctor,
        "preview": preview,
        "validate": validate,
    }
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        expected = "|".join(commands)
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <{expected}>")
    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
