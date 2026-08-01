from __future__ import annotations

from pathlib import Path

from .model import ValidationResult

CACHE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tmp",
    "node_modules",
    "dist",
    "build",
}
PLACEHOLDER_NAMES = {"example", "sample", "placeholder", "todo", "untitled"}
RESOURCE_DIRS = ("references", "templates", "assets")


def _documentation_files(root: Path) -> list[Path]:
    return [
        path for path in root.rglob("*.md") if path.is_file() and not path.is_symlink()
    ]


def validate_structure(
    root: Path,
    *,
    tests_root: Path | None = None,
    fail_on_generated: bool = False,
) -> ValidationResult:
    result = ValidationResult()
    if not root.is_dir():
        result.error("skill root must be a directory")
        return result

    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if path.is_symlink():
            result.error(f"symlink is not allowed: {rel}")
            continue
        if any(part in CACHE_DIRS for part in rel.parts):
            if fail_on_generated:
                result.error(f"generated or cache path is not allowed: {rel}")
            continue
        if path.is_dir() and not any(path.iterdir()):
            result.error(f"empty directory is not allowed: {rel}")
        if path.is_file() and path.stat().st_size == 0:
            result.error(f"zero-byte resource is not allowed: {rel}")
        if path.name == "SKILL.md" and path != root / "SKILL.md":
            result.error(f"nested discoverable SKILL.md is not allowed: {rel}")
        if path.stem.lower() in PLACEHOLDER_NAMES:
            result.warn(f"placeholder-like release filename: {rel}")

    documentation_files = _documentation_files(root)
    for directory in RESOURCE_DIRS:
        resource_root = root / directory
        if not resource_root.is_dir():
            continue
        for path in resource_root.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            rel = path.relative_to(root).as_posix()
            documentation = "\n".join(
                item.read_text(encoding="utf-8")
                for item in documentation_files
                if item != path
            )
            if rel not in documentation and path.name not in documentation:
                result.warn(f"potentially orphaned resource: {rel}")

    documentation = "\n".join(
        item.read_text(encoding="utf-8") for item in documentation_files
    )
    scripts = root / "scripts"
    if scripts.is_dir():
        test_text = ""
        if tests_root and tests_root.exists():
            test_text = "\n".join(
                path.read_text(encoding="utf-8", errors="ignore")
                for path in tests_root.rglob("*.py")
                if path.is_file()
            )
        for path in scripts.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            if (
                'if __name__ == "__main__"' not in text
                and "if __name__ == '__main__'" not in text
            ):
                continue
            if path.name not in documentation:
                result.warn(
                    "executable script missing from operation documentation: "
                    f"scripts/{path.name}"
                )
            if tests_root and path.name not in test_text:
                result.warn(
                    f"executable script has no named test evidence: scripts/{path.name}"
                )
    return result
