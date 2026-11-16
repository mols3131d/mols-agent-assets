"""읽기 전용 Producer의 생성 출력 변경 수집 및 artifact payload 패키징을 수행한다."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from scripts import generated_artifacts_sync as sync

ROOT = sync.ROOT
SCHEMA_VERSION = 1
HEX_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PROTECTED_CORE_OUTPUTS = frozenset(
    {
        "docs/INDEX.tsv",
        "catalog/INDEX.tsv",
        "route/routes.jsonl",
        ".agents/route/routes.jsonl",
        ".agents/route/all.jsonl",
        ".agents/route/uncategorized.jsonl",
    }
)


class ProducerError(RuntimeError):
    """Producer payload 생성 또는 경계 검증에 실패할 때 발생한다."""


def is_safe_relative_posix_path(path: str) -> bool:
    """경로 순회나 제어 문자가 없는 순수 POSIX 상대 경로인지 검사한다."""
    if not path or "\\" in path or path.startswith("/") or path.endswith("/"):
        return False
    if "//" in path:
        return False
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in path):
        return False
    parts = path.split("/")
    if any(part in {"", ".", "..", ".git"} for part in parts):
        return False
    return PurePosixPath(path).as_posix() == path


def is_allowed_generated_output(path: str) -> bool:
    """저장소 `PROJECTIONS`가 소유하는 생성 출력 경로인지 확인한다."""
    if not is_safe_relative_posix_path(path):
        return False
    if not any(projection.output_matches(path) for projection in sync.PROJECTIONS):
        return False

    posix = PurePosixPath(path)
    if path.startswith(("docs/", "catalog/")):
        return posix.name == "INDEX.tsv"
    if path.startswith("route/"):
        return (
            posix.parent == PurePosixPath("route")
            and posix.suffix == ".jsonl"
            and bool(posix.stem)
        )
    if path.startswith(".agents/route/"):
        return (
            posix.parent == PurePosixPath(".agents/route")
            and posix.suffix == ".jsonl"
            and bool(posix.stem)
        )
    return False


def _run_git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", f"core.hooksPath={os.devnull}", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def collect_generated_changes(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """HEAD 대비 작업 트리의 생성 출력 변경·추가·삭제 목록을 수집한다."""
    raw_diff = _run_git(
        root, "diff", "--name-status", "--no-renames", "-z", "HEAD", "--"
    )
    tokens = [
        item.decode("utf-8", errors="surrogateescape") for item in raw_diff.split(b"\0")
    ]
    if tokens and tokens[-1] == "":
        tokens.pop()
    if len(tokens) % 2 != 0:
        raise ProducerError("git diff --name-status 출력 형식이 올바르지 않습니다.")

    changed_set: set[str] = set()
    deleted_set: set[str] = set()
    for idx in range(0, len(tokens), 2):
        status = tokens[idx]
        path = tokens[idx + 1]
        if status == "D":
            deleted_set.add(path)
        elif status in {"M", "A", "T"}:
            changed_set.add(path)
        else:
            raise ProducerError(f"지원하지 않는 git diff 상태입니다: {status} ({path})")

    raw_untracked = _run_git(
        root, "ls-files", "--others", "--exclude-standard", "-z", "--"
    )
    for item in raw_untracked.split(b"\0"):
        if item:
            changed_set.add(item.decode("utf-8", errors="surrogateescape"))

    for path in sorted(changed_set | deleted_set):
        if not is_allowed_generated_output(path):
            raise ProducerError(f"허용된 생성 출력 외 파일이 변경되었습니다: {path}")

    for path in sorted(deleted_set):
        if path in PROTECTED_CORE_OUTPUTS:
            raise ProducerError(f"핵심 생성 출력 파일이 삭제되었습니다: {path}")

    for path in sorted(changed_set):
        target = root / path
        try:
            mode = os.lstat(target).st_mode
        except OSError as exc:
            raise ProducerError(f"생성 출력 파일을 읽을 수 없습니다: {path}") from exc
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise ProducerError(f"생성 출력이 일반 파일이 아닙니다: {path}")

    return sorted(changed_set), sorted(deleted_set - changed_set)


def package_payload(
    *,
    root: Path = ROOT,
    output_dir: Path,
    repository_id: int,
    repository_full_name: str,
    branch: str,
    head_sha: str,
    producer_run_id: int,
    producer_run_attempt: int = 1,
) -> dict[str, Any]:
    """생성 출력 변경분을 metadata.json + files/ payload 디렉터리로 패키징한다."""
    if repository_id <= 0 or producer_run_id <= 0 or producer_run_attempt <= 0:
        raise ProducerError("저장소 ID와 run ID는 양의 정수여야 합니다.")
    if not repository_full_name or "/" not in repository_full_name:
        raise ProducerError(
            f"유효하지 않은 repository 이름입니다: {repository_full_name!r}"
        )
    if not branch or branch == "main" or branch.startswith("refs/"):
        raise ProducerError(f"유효하지 않은 source branch입니다: {branch!r}")
    if not HEX_SHA_RE.fullmatch(head_sha):
        raise ProducerError(f"유효하지 않은 head_sha입니다: {head_sha!r}")

    actual_head = _run_git(root, "rev-parse", "HEAD").decode("utf-8").strip()
    if actual_head != head_sha:
        raise ProducerError(
            f"작업 트리 HEAD가 기대 SHA와 다릅니다: {actual_head} != {head_sha}"
        )

    changed_paths, deleted_paths = collect_generated_changes(root)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_entries: list[dict[str, Any]] = []
    if changed_paths:
        files_root = output_dir / "files"
        for rel_path in changed_paths:
            src = root / rel_path
            raw_bytes = src.read_bytes()
            dest = files_root / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw_bytes)
            file_entries.append(
                {
                    "path": rel_path,
                    "sha256": hashlib.sha256(raw_bytes).hexdigest(),
                    "size": len(raw_bytes),
                }
            )

    changed = bool(file_entries or deleted_paths)
    metadata: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "repository_id": repository_id,
        "repository_full_name": repository_full_name,
        "branch": branch,
        "head_sha": head_sha,
        "producer_run_id": producer_run_id,
        "producer_run_attempt": producer_run_attempt,
        "changed": changed,
        "files": file_entries,
        "deleted": deleted_paths,
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return metadata


def _resolve_env_provenance() -> dict[str, Any]:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    event: dict[str, Any] = {}
    if event_path and Path(event_path).is_file():
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))

    repo_full_name = os.environ.get("GITHUB_REPOSITORY", "")
    event_repo = (
        event.get("repository") if isinstance(event.get("repository"), dict) else {}
    )
    if (
        event_repo.get("full_name")
        and repo_full_name
        and event_repo["full_name"] != repo_full_name
    ):
        raise ProducerError(
            "GITHUB_REPOSITORY와 이벤트 repository.full_name이 다릅니다."
        )

    raw_repo_id = os.environ.get("GITHUB_REPOSITORY_ID", "")
    repo_id = int(raw_repo_id) if raw_repo_id.isdigit() else event_repo.get("id")
    if isinstance(repo_id, bool) or not isinstance(repo_id, int) or repo_id <= 0:
        raise ProducerError("유효한 repository ID를 확인할 수 없습니다.")

    github_ref = os.environ.get("GITHUB_REF", "")
    if not github_ref.startswith("refs/heads/"):
        raise ProducerError(f"브랜치 push ref가 아닙니다: {github_ref!r}")
    branch = github_ref.removeprefix("refs/heads/")

    head_sha = os.environ.get("GITHUB_SHA", "")
    raw_run_id = os.environ.get("GITHUB_RUN_ID", "")
    raw_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    if not raw_run_id.isdigit() or not raw_attempt.isdigit():
        raise ProducerError("유효한 GITHUB_RUN_ID/GITHUB_RUN_ATTEMPT가 필요합니다.")

    return {
        "repository_id": repo_id,
        "repository_full_name": repo_full_name or str(event_repo.get("full_name", "")),
        "branch": branch,
        "head_sha": head_sha,
        "producer_run_id": int(raw_run_id),
        "producer_run_attempt": int(raw_attempt),
    }


def _write_github_output(changed: bool) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changed else 'false'}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    package_cmd = subparsers.add_parser(
        "package", help="Package generated output delta into artifact directory"
    )
    package_cmd.add_argument("--output-dir", type=Path, required=True)
    package_cmd.add_argument("--root", type=Path, default=ROOT)

    args = parser.parse_args(argv)
    try:
        provenance = _resolve_env_provenance()
        metadata = package_payload(
            root=args.root,
            output_dir=args.output_dir,
            **provenance,
        )
        _write_github_output(bool(metadata["changed"]))
        print(
            f"producer: changed={metadata['changed']} "
            f"files={len(metadata['files'])} deleted={len(metadata['deleted'])}"
        )
        return 0
    except ProducerError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
