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
from pathlib import Path
from typing import Any

from scripts import (
    generated_artifacts_sync as sync,
    generated_artifacts_writeback as writeback,
)

ROOT = sync.ROOT
REPO_NAME_RE = re.compile(r"^[^/\s]+/[^/\s]+$")


class ProducerError(RuntimeError):
    """Producer payload 생성 또는 경계 검증에 실패할 때 발생한다."""


def _run_git(root: Path, *args: str) -> bytes:
    env = os.environ.copy()
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    try:
        result = subprocess.run(
            [
                "git",
                "-c",
                f"core.hooksPath={os.devnull}",
                "-c",
                "credential.helper=",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.autocrlf=false",
                *args,
            ],
            cwd=root,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        err = exc.stderr.decode("utf-8", errors="replace").strip()
        raise ProducerError(f"Git 명령 실행 실패 ({args[0]}): {err}") from exc
    return result.stdout


def _require_regular_generated_output(root: Path, path: str) -> None:
    target = root / path
    relative = target.relative_to(root)
    try:
        for parent in reversed(relative.parents[:-1]):
            directory = (root / parent).lstat()
            if (
                not stat.S_ISDIR(directory.st_mode)
                or getattr(directory, "st_reparse_tag", 0)
                == stat.IO_REPARSE_TAG_MOUNT_POINT
            ):
                raise ProducerError(
                    f"생성 출력의 상위 경로가 일반 디렉터리가 아닙니다: {parent}"
                )
        if not stat.S_ISREG(target.lstat().st_mode):
            raise ProducerError(f"생성 출력이 일반 파일이 아닙니다: {path}")
    except OSError as exc:
        raise ProducerError(f"생성 출력 파일을 읽을 수 없습니다: {path}") from exc


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
        elif status in {"M", "A"}:
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
        if not writeback.is_allowed_generated_output(path):
            raise ProducerError(f"허용된 생성 출력 외 파일이 변경되었습니다: {path}")

    final_deleted = sorted(deleted_set - changed_set)
    for path in final_deleted:
        if path in writeback.PROTECTED_CORE_OUTPUTS:
            raise ProducerError(f"핵심 생성 출력 파일이 삭제되었습니다: {path}")

    for path in sorted(changed_set):
        _require_regular_generated_output(root, path)

    return sorted(changed_set), final_deleted


def _require_positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ProducerError(f"{name}은(는) 양의 정수여야 합니다: {value!r}")
    return value


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
    repo_id = _require_positive_int(repository_id, "repository_id")
    run_id = _require_positive_int(producer_run_id, "producer_run_id")
    run_attempt = _require_positive_int(producer_run_attempt, "producer_run_attempt")

    if not REPO_NAME_RE.fullmatch(repository_full_name):
        raise ProducerError(
            f"유효하지 않은 repository 이름입니다: {repository_full_name!r}"
        )
    if not branch or branch == "main" or branch.startswith("refs/"):
        raise ProducerError(f"유효하지 않은 source branch입니다: {branch!r}")
    if not writeback.HEX_SHA_RE.fullmatch(head_sha):
        raise ProducerError(f"유효하지 않은 head_sha입니다: {head_sha!r}")

    actual_head = _run_git(root, "rev-parse", "HEAD").decode("utf-8").strip()
    if actual_head != head_sha:
        raise ProducerError(
            f"작업 트리 HEAD가 기대 SHA와 다릅니다: {actual_head} != {head_sha}"
        )

    changed_paths, deleted_paths = collect_generated_changes(root)
    if len(changed_paths) + len(deleted_paths) > writeback.MAX_FILE_COUNT:
        raise ProducerError("변경된 생성 출력 수가 artifact 제한을 초과했습니다.")
    if output_dir.is_symlink() or output_dir.is_junction():
        raise ProducerError(f"출력 디렉터리가 링크입니다: {output_dir}")
    resolved_output = output_dir.resolve()
    resolved_root = root.resolve()
    if resolved_output.is_relative_to(resolved_root) or resolved_root.is_relative_to(
        resolved_output
    ):
        raise ProducerError("Artifact와 원본 작업 트리는 별도 디렉터리여야 합니다.")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_entries: list[dict[str, Any]] = []
    total_bytes = 0
    if changed_paths:
        files_root = output_dir / "files"
        for rel_path in changed_paths:
            src = root / rel_path
            with src.open("rb") as handle:
                raw_bytes = handle.read(writeback.MAX_FILE_BYTES + 1)
            if len(raw_bytes) > writeback.MAX_FILE_BYTES:
                raise ProducerError(
                    f"생성 출력 크기가 artifact 제한을 초과했습니다: {rel_path}"
                )
            total_bytes += len(raw_bytes)
            if total_bytes > writeback.MAX_TOTAL_PAYLOAD_BYTES:
                raise ProducerError(
                    "생성 출력의 총 크기가 artifact 제한을 초과했습니다."
                )
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
        "schema_version": writeback.SCHEMA_VERSION,
        "repository_id": repo_id,
        "repository_full_name": repository_full_name,
        "branch": branch,
        "head_sha": head_sha,
        "producer_run_id": run_id,
        "producer_run_attempt": run_attempt,
        "changed": changed,
        "files": file_entries,
        "deleted": deleted_paths,
    }
    encoded = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    if len(encoded) > writeback.MAX_METADATA_BYTES:
        raise ProducerError("metadata.json 크기가 artifact 제한을 초과했습니다.")
    (output_dir / "metadata.json").write_bytes(encoded)
    return metadata


def _parse_ascii_positive_int(raw: str, name: str) -> int:
    if not (raw.isascii() and raw.isdigit()):
        raise ProducerError(f"유효한 양의 정수가 아닙니다: {name}={raw!r}")
    value = int(raw)
    if value <= 0:
        raise ProducerError(f"유효한 양의 정수가 아닙니다: {name}={raw!r}")
    return value


def _resolve_env_provenance() -> dict[str, Any]:
    if os.environ.get("GITHUB_EVENT_NAME") != "push":
        raise ProducerError("브랜치 push 이벤트만 처리합니다.")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise ProducerError("GITHUB_EVENT_PATH가 필요합니다.")
    try:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProducerError(f"GITHUB_EVENT_PATH 파싱 실패: {exc}") from exc
    if not isinstance(event, dict) or event.get("deleted") is not False:
        raise ProducerError("삭제되지 않은 브랜치 push 이벤트가 필요합니다.")
    event_repo = event.get("repository")
    if not isinstance(event_repo, dict):
        raise ProducerError("push 이벤트에 repository 정보가 필요합니다.")

    repo_full_name = os.environ.get("GITHUB_REPOSITORY", "")
    repo_id = _parse_ascii_positive_int(
        os.environ.get("GITHUB_REPOSITORY_ID", ""), "GITHUB_REPOSITORY_ID"
    )
    event_repo_id = _require_positive_int(event_repo.get("id"), "repository.id")
    if event_repo_id != repo_id or event_repo.get("full_name") != repo_full_name:
        raise ProducerError("GitHub 환경과 push 이벤트의 repository가 다릅니다.")

    github_ref = os.environ.get("GITHUB_REF", "")
    if not github_ref.startswith("refs/heads/"):
        raise ProducerError(f"브랜치 push ref가 아닙니다: {github_ref!r}")
    head_sha = os.environ.get("GITHUB_SHA", "")
    if event.get("ref") != github_ref or event.get("after") != head_sha:
        raise ProducerError("GitHub 환경과 push 이벤트의 ref 또는 SHA가 다릅니다.")

    run_id = _parse_ascii_positive_int(
        os.environ.get("GITHUB_RUN_ID", ""), "GITHUB_RUN_ID"
    )
    run_attempt = _parse_ascii_positive_int(
        os.environ.get("GITHUB_RUN_ATTEMPT", ""), "GITHUB_RUN_ATTEMPT"
    )

    return {
        "repository_id": repo_id,
        "repository_full_name": repo_full_name,
        "branch": github_ref.removeprefix("refs/heads/"),
        "head_sha": head_sha,
        "producer_run_id": run_id,
        "producer_run_attempt": run_attempt,
    }


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
        print(
            f"producer: changed={metadata['changed']} "
            f"files={len(metadata['files'])} deleted={len(metadata['deleted'])}"
        )
        return 0
    except ProducerError as exc:
        msg = f"FAIL {exc}\n".encode("utf-8", errors="replace").decode("utf-8")
        print(msg, end="", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
