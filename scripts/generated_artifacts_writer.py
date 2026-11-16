"""신뢰된 기본 브랜치 Writer의 provenance·artifact·diff 검증과 App push를 수행한다."""

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
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from scripts import generated_artifacts_sync as sync

EXPECTED_PRODUCER_NAME = "Sync Generated Artifacts"
EXPECTED_PRODUCER_PATH = ".github/workflows/generated-sync.yml"
EXPECTED_ARTIFACT_NAME = "generated-sync-payload"
DEFAULT_API_URL = "https://api.github.com"
DEFAULT_SERVER_URL = "https://github.com"
COMMIT_MESSAGE = "chore(generated): sync indexes and routes"

MAX_METADATA_BYTES = 1 * 1024 * 1024
MAX_FILE_COUNT = 500
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_PAYLOAD_BYTES = 20 * 1024 * 1024
MAX_ARTIFACT_ARCHIVE_BYTES = 25 * 1024 * 1024

HEX_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
APP_SLUG_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-]*$")
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
FORBIDDEN_BRANCH_TOKENS = ("..", "@{", "//", "~", "^", ":", "?", "*", "[", "\\")


class WriterSecurityError(RuntimeError):
    """신뢰 경계, provenance 또는 artifact 계약 위반 시 발생한다."""


@dataclass(frozen=True)
class Provenance:
    """검증된 workflow_run 이벤트 출처 정보."""

    repository_id: int
    repository_full_name: str
    default_branch: str
    branch: str
    head_sha: str
    run_id: int
    run_attempt: int


@dataclass(frozen=True)
class PayloadFile:
    """Artifact에 포함된 단일 생성 파일 메타데이터."""

    path: str
    sha256: str
    size: int


@dataclass(frozen=True)
class ValidatedPayload:
    """검증을 통과한 Producer payload."""

    changed: bool
    files: tuple[PayloadFile, ...]
    deleted: tuple[str, ...]
    artifact_dir: Path


@dataclass(frozen=True)
class Decision:
    """Writer 단계의 계속 진행 또는 안전 중단 판단."""

    proceed: bool
    reason: str


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
    """기본 브랜치 `PROJECTIONS`가 소유한 생성 출력 경로인지 확인한다."""
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


def validate_source_branch(branch: str, default_branch: str = "main") -> str:
    """원본 브랜치 이름이 안전한 non-default 브랜치인지 검증한다."""
    if not branch or branch in {default_branch, "main", "HEAD"}:
        raise WriterSecurityError(f"허용되지 않는 대상 브랜치입니다: {branch!r}")
    if branch.startswith(("refs/", "-", "/")) or branch.endswith(("/", ".", ".lock")):
        raise WriterSecurityError(f"안전하지 않은 브랜치 이름 형식입니다: {branch!r}")
    if any(ord(ch) < 32 or ord(ch) == 127 or ch.isspace() for ch in branch):
        raise WriterSecurityError(
            f"브랜치 이름에 제어/공백 문자가 있습니다: {branch!r}"
        )
    if any(token in branch for token in FORBIDDEN_BRANCH_TOKENS):
        raise WriterSecurityError(
            f"브랜치 이름에 금지된 Git ref 토큰이 있습니다: {branch!r}"
        )
    if any(
        part.startswith(".") or part.endswith(".lock") for part in branch.split("/")
    ):
        raise WriterSecurityError(
            f"브랜치 세그먼트 형식이 올바르지 않습니다: {branch!r}"
        )
    return branch


def is_branch_allowed(branch: str, allowed_spec: str) -> bool:
    """승인된 브랜치 allowlist에 포함되는지 fail-closed로 판정한다."""
    tokens = [
        item.strip() for item in re.split(r"[\s,]+", allowed_spec) if item.strip()
    ]
    if not tokens:
        return False
    if "*" in tokens:
        return True
    return branch in tokens


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise WriterSecurityError(
            f"유효하지 않은 양의 정수 필드입니다: {name}={value!r}"
        )
    return value


def _require_nonempty_str(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise WriterSecurityError(f"유효하지 않은 문자열 필드입니다: {name}={value!r}")
    return value


def verify_workflow_run_event(
    event: dict[str, Any],
    *,
    github_repository: str,
    github_repository_id: str,
    github_ref: str,
    enabled: str,
    allowed_branches: str,
) -> tuple[Decision, Provenance | None]:
    """`workflow_run` 이벤트와 활성화 스위치를 검증한다."""
    if enabled != "true":
        return Decision(False, "disabled"), None

    repo = event.get("repository")
    run = event.get("workflow_run")
    if not isinstance(repo, dict) or not isinstance(run, dict):
        raise WriterSecurityError(
            "workflow_run 이벤트 payload 구조가 올바르지 않습니다."
        )

    default_branch = _require_nonempty_str(
        repo.get("default_branch"), "repository.default_branch"
    )
    expected_ref = f"refs/heads/{default_branch}"
    if github_ref != expected_ref:
        raise WriterSecurityError(
            f"Trusted Writer는 기본 브랜치({expected_ref})에서만 "
            f"실행할 수 있습니다: {github_ref}"
        )

    expected_repo_id = _require_int(
        int(github_repository_id) if github_repository_id.isdigit() else None,
        "GITHUB_REPOSITORY_ID",
    )
    event_repo_id = _require_int(repo.get("id"), "repository.id")
    event_repo_name = _require_nonempty_str(
        repo.get("full_name"), "repository.full_name"
    )
    if event_repo_id != expected_repo_id or event_repo_name != github_repository:
        raise WriterSecurityError(
            "실행 저장소와 이벤트 repository 메타데이터가 일치하지 않습니다."
        )

    workflow = event.get("workflow")
    workflow_path = run.get("path") or (
        workflow.get("path") if isinstance(workflow, dict) else None
    )
    if (
        run.get("name") != EXPECTED_PRODUCER_NAME
        or workflow_path != EXPECTED_PRODUCER_PATH
    ):
        raise WriterSecurityError(
            "신뢰된 Producer 워크플로가 아닙니다: "
            f"name={run.get('name')!r}, path={workflow_path!r}"
        )
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        raise WriterSecurityError(
            "Producer 실행이 성공 완료 상태가 아닙니다: "
            f"status={run.get('status')!r}, conclusion={run.get('conclusion')!r}"
        )
    if run.get("event") != "push":
        raise WriterSecurityError(
            f"허용된 Producer 트리거 이벤트(push)가 아닙니다: {run.get('event')!r}"
        )

    run_repo = run.get("repository")
    head_repo = run.get("head_repository")
    if not isinstance(run_repo, dict) or not isinstance(head_repo, dict):
        raise WriterSecurityError("workflow_run repository 출처 정보가 누락되었습니다.")
    if (
        run_repo.get("id") != expected_repo_id
        or run_repo.get("full_name") != github_repository
        or head_repo.get("id") != expected_repo_id
        or head_repo.get("full_name") != github_repository
    ):
        raise WriterSecurityError(
            "외부 저장소 또는 fork에서 온 workflow_run은 거부됩니다."
        )

    head_branch = validate_source_branch(
        _require_nonempty_str(run.get("head_branch"), "workflow_run.head_branch"),
        default_branch=default_branch,
    )
    head_sha = _require_nonempty_str(run.get("head_sha"), "workflow_run.head_sha")
    if not HEX_SHA_RE.fullmatch(head_sha):
        raise WriterSecurityError(f"유효하지 않은 head_sha입니다: {head_sha!r}")

    run_id = _require_int(run.get("id"), "workflow_run.id")
    run_attempt = _require_int(run.get("run_attempt") or 1, "workflow_run.run_attempt")

    provenance = Provenance(
        repository_id=expected_repo_id,
        repository_full_name=github_repository,
        default_branch=default_branch,
        branch=head_branch,
        head_sha=head_sha,
        run_id=run_id,
        run_attempt=run_attempt,
    )

    if not is_branch_allowed(head_branch, allowed_branches):
        return Decision(False, "branch_not_allowed"), provenance

    return Decision(True, "ok"), provenance


def make_github_api_requester(
    token: str,
    api_url: str = DEFAULT_API_URL,
) -> Callable[[str], tuple[int, dict[str, Any]]]:
    """Read-only GitHub REST API JSON 호출기를 만든다."""
    base = api_url.rstrip("/")

    def request(path: str) -> tuple[int, dict[str, Any]]:
        url = f"{base}/{path.lstrip('/')}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "mols-generated-artifacts-writer",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                body = resp.read().decode("utf-8")
                return resp.status, json.loads(body) if body else {}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body) if body else {}
            except json.JSONDecodeError:
                parsed = {"message": body}
            return exc.code, parsed

    return request


def verify_single_artifact(
    requester: Callable[[str], tuple[int, dict[str, Any]]],
    repo: str,
    run_id: int,
) -> dict[str, Any]:
    """Producer run에 기대된 단일 artifact만 존재하는지 확인한다."""
    status, data = requester(f"repos/{repo}/actions/runs/{run_id}/artifacts")
    if status != 200:
        raise WriterSecurityError(
            f"artifact 목록 조회 실패 (HTTP {status}): run_id={run_id}"
        )
    artifacts = data.get("artifacts")
    total_count = data.get("total_count")
    if not isinstance(artifacts, list) or total_count != 1 or len(artifacts) != 1:
        raise WriterSecurityError(
            f"Producer artifact는 정확히 1개여야 합니다: total_count={total_count!r}"
        )
    artifact = artifacts[0]
    if not isinstance(artifact, dict) or artifact.get("name") != EXPECTED_ARTIFACT_NAME:
        raise WriterSecurityError(f"예상하지 않은 artifact 이름입니다: {artifact!r}")
    if artifact.get("expired") is True:
        raise WriterSecurityError("만료된 artifact는 사용할 수 없습니다.")
    size = artifact.get("size_in_bytes")
    if (
        isinstance(size, bool)
        or not isinstance(size, int)
        or size <= 0
        or size > MAX_ARTIFACT_ARCHIVE_BYTES
    ):
        raise WriterSecurityError(f"허용 범위를 벗어난 artifact 크기입니다: {size!r}")
    return artifact


def get_branch_head_sha(
    requester: Callable[[str], tuple[int, dict[str, Any]]],
    repo: str,
    branch: str,
) -> str | None:
    """원격 브랜치의 현재 HEAD commit SHA를 조회한다."""
    quoted = urllib.parse.quote(branch, safe="")
    status, data = requester(f"repos/{repo}/git/ref/heads/{quoted}")
    if status == 404:
        return None
    if status != 200:
        raise WriterSecurityError(
            f"브랜치 HEAD 조회 실패 (HTTP {status}): branch={branch}"
        )
    obj = data.get("object")
    if not isinstance(obj, dict) or obj.get("type") != "commit":
        raise WriterSecurityError(f"브랜치 ref가 commit을 가리키지 않습니다: {data!r}")
    sha = obj.get("sha")
    if not isinstance(sha, str) or not HEX_SHA_RE.fullmatch(sha):
        raise WriterSecurityError(f"유효하지 않은 원격 HEAD SHA입니다: {sha!r}")
    return sha


def get_bot_identity(
    requester: Callable[[str], tuple[int, dict[str, Any]]],
    app_slug: str,
) -> tuple[str, str]:
    """App slug로부터 실제 GitHub App bot의 Git author name/email을 조회한다."""
    if not APP_SLUG_RE.fullmatch(app_slug):
        raise WriterSecurityError(f"유효하지 않은 GitHub App slug입니다: {app_slug!r}")
    login = f"{app_slug}[bot]"
    quoted = urllib.parse.quote(login, safe="")
    status, data = requester(f"users/{quoted}")
    if status != 200:
        raise WriterSecurityError(
            f"GitHub App bot 사용자 조회 실패 (HTTP {status}): {login}"
        )
    bot_id = _require_int(data.get("id"), "bot.id")
    if data.get("type") != "Bot" or data.get("login") != login:
        raise WriterSecurityError(f"예상한 Bot 계정이 아닙니다: {data!r}")
    return login, f"{bot_id}+{login}@users.noreply.github.com"


def _scan_artifact_tree(root: Path) -> set[str]:
    """Symlink와 비정규 파일을 거부하며 artifact 내부 파일 목록을 수집한다."""
    if root.is_symlink() or not root.is_dir():
        raise WriterSecurityError(f"유효하지 않은 artifact 루트 디렉터리입니다: {root}")

    found_files: set[str] = set()

    def walk(directory: Path) -> None:
        entries = sorted(directory.iterdir(), key=lambda p: p.name)
        for entry in entries:
            mode = os.lstat(entry).st_mode
            if stat.S_ISLNK(mode):
                raise WriterSecurityError(
                    f"Artifact 내 symlink는 허용되지 않습니다: {entry}"
                )
            if stat.S_ISDIR(mode):
                walk(entry)
                continue
            if not stat.S_ISREG(mode):
                raise WriterSecurityError(
                    f"Artifact 내 비정규 파일은 허용되지 않습니다: {entry}"
                )
            rel = entry.relative_to(root).as_posix()
            if not is_safe_relative_posix_path(rel):
                raise WriterSecurityError(
                    f"안전하지 않은 artifact 상대 경로입니다: {rel!r}"
                )
            found_files.add(rel)

    walk(root)
    return found_files


def validate_artifact_payload(
    artifact_dir: Path, provenance: Provenance
) -> ValidatedPayload:
    """다운로드된 Producer artifact의 무결성·provenance·허용 경로를 검증한다."""
    all_entries = _scan_artifact_tree(artifact_dir)
    if "metadata.json" not in all_entries:
        raise WriterSecurityError("Artifact에 metadata.json이 없습니다.")

    top_levels = {entry.split("/", 1)[0] for entry in all_entries}
    unexpected_top = top_levels - {"metadata.json", "files"}
    if unexpected_top:
        raise WriterSecurityError(
            f"허용되지 않은 최상위 artifact 항목입니다: {sorted(unexpected_top)}"
        )

    metadata_path = artifact_dir / "metadata.json"
    if metadata_path.stat().st_size > MAX_METADATA_BYTES:
        raise WriterSecurityError("metadata.json 크기가 제한을 초과했습니다.")

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WriterSecurityError(f"metadata.json 파싱 실패: {exc}") from exc

    if not isinstance(metadata, dict):
        raise WriterSecurityError("metadata.json 최상위는 JSON object여야 합니다.")

    expected_keys = {
        "schema_version",
        "repository_id",
        "repository_full_name",
        "branch",
        "head_sha",
        "producer_run_id",
        "producer_run_attempt",
        "changed",
        "files",
        "deleted",
    }
    if set(metadata.keys()) != expected_keys:
        raise WriterSecurityError(
            f"metadata.json 키 집합이 일치하지 않습니다: {sorted(metadata.keys())}"
        )

    if isinstance(metadata["schema_version"], bool) or metadata["schema_version"] != 1:
        raise WriterSecurityError(
            f"지원하지 않는 schema_version입니다: {metadata['schema_version']!r}"
        )
    if (
        metadata["repository_id"] != provenance.repository_id
        or metadata["repository_full_name"] != provenance.repository_full_name
    ):
        raise WriterSecurityError(
            "metadata 저장소 정보가 workflow_run과 일치하지 않습니다."
        )
    if (
        metadata["branch"] != provenance.branch
        or metadata["head_sha"] != provenance.head_sha
    ):
        raise WriterSecurityError(
            "metadata 브랜치/커밋 SHA가 workflow_run과 일치하지 않습니다."
        )
    if (
        metadata["producer_run_id"] != provenance.run_id
        or metadata["producer_run_attempt"] != provenance.run_attempt
    ):
        raise WriterSecurityError(
            "metadata Producer run 정보가 workflow_run과 일치하지 않습니다."
        )

    changed = metadata["changed"]
    if not isinstance(changed, bool):
        raise WriterSecurityError("metadata.changed는 boolean이어야 합니다.")

    raw_files = metadata["files"]
    raw_deleted = metadata["deleted"]
    if not isinstance(raw_files, list) or not isinstance(raw_deleted, list):
        raise WriterSecurityError(
            "metadata.files와 metadata.deleted는 배열이어야 합니다."
        )

    actual_payload_files = {
        entry.removeprefix("files/")
        for entry in all_entries
        if entry.startswith("files/")
    }
    if not changed:
        if (
            raw_files
            or raw_deleted
            or actual_payload_files
            or (artifact_dir / "files").exists()
        ):
            raise WriterSecurityError(
                "changed=false인데 파일 목록이나 files 디렉터리가 존재합니다."
            )
        return ValidatedPayload(
            changed=False, files=(), deleted=(), artifact_dir=artifact_dir
        )

    if not raw_files and not raw_deleted:
        raise WriterSecurityError(
            "changed=true인데 files와 deleted가 모두 비어 있습니다."
        )
    if len(raw_files) + len(raw_deleted) > MAX_FILE_COUNT:
        raise WriterSecurityError("변경 파일 수가 허용 제한을 초과했습니다.")

    parsed_files: list[PayloadFile] = []
    seen_files: set[str] = set()
    total_bytes = 0
    for item in raw_files:
        if not isinstance(item, dict) or set(item.keys()) != {"path", "sha256", "size"}:
            raise WriterSecurityError(f"잘못된 payload file 항목입니다: {item!r}")
        rel_path = item["path"]
        digest = item["sha256"]
        size = item["size"]
        if not isinstance(rel_path, str) or not is_allowed_generated_output(rel_path):
            raise WriterSecurityError(
                f"허용되지 않은 생성 파일 경로입니다: {rel_path!r}"
            )
        if rel_path in seen_files:
            raise WriterSecurityError(f"중복된 payload 파일 경로입니다: {rel_path}")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise WriterSecurityError(f"유효하지 않은 sha256 형식입니다: {rel_path}")
        if (
            isinstance(size, bool)
            or not isinstance(size, int)
            or size < 0
            or size > MAX_FILE_BYTES
        ):
            raise WriterSecurityError(
                f"허용 범위를 벗어난 파일 크기입니다: {rel_path}={size!r}"
            )
        seen_files.add(rel_path)
        total_bytes += size
        parsed_files.append(PayloadFile(path=rel_path, sha256=digest, size=size))

    if total_bytes > MAX_TOTAL_PAYLOAD_BYTES:
        raise WriterSecurityError("전체 payload 크기가 허용 제한을 초과했습니다.")

    seen_deleted: list[str] = []
    seen_deleted_set: set[str] = set()
    for rel_path in raw_deleted:
        if not isinstance(rel_path, str) or not is_allowed_generated_output(rel_path):
            raise WriterSecurityError(f"허용되지 않은 삭제 경로입니다: {rel_path!r}")
        if rel_path in PROTECTED_CORE_OUTPUTS:
            raise WriterSecurityError(f"핵심 생성 출력 삭제는 거부됩니다: {rel_path}")
        if rel_path in seen_files or rel_path in seen_deleted_set:
            raise WriterSecurityError(f"중복 또는 충돌하는 삭제 경로입니다: {rel_path}")
        seen_deleted_set.add(rel_path)
        seen_deleted.append(rel_path)

    if actual_payload_files != seen_files:
        missing = sorted(seen_files - actual_payload_files)
        extra = sorted(actual_payload_files - seen_files)
        raise WriterSecurityError(
            "Artifact 파일 목록과 metadata가 불일치합니다: "
            f"missing={missing}, extra={extra}"
        )

    for entry in parsed_files:
        file_path = artifact_dir / "files" / entry.path
        raw_bytes = file_path.read_bytes()
        if len(raw_bytes) != entry.size:
            raise WriterSecurityError(f"파일 크기 불일치: {entry.path}")
        if hashlib.sha256(raw_bytes).hexdigest() != entry.sha256:
            raise WriterSecurityError(f"파일 SHA-256 불일치: {entry.path}")
        try:
            raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise WriterSecurityError(
                f"생성 출력이 유효한 UTF-8 텍스트가 아닙니다: {entry.path}"
            ) from exc

    return ValidatedPayload(
        changed=True,
        files=tuple(parsed_files),
        deleted=tuple(seen_deleted),
        artifact_dir=artifact_dir,
    )


def _run_git(
    repo_dir: Path,
    *args: str,
    env_overrides: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    return subprocess.run(
        ["git", "-c", f"core.hooksPath={os.devnull}", *args],
        cwd=repo_dir,
        env=env,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _git_askpass_env(token: str, temp_dir: Path) -> dict[str, str]:
    """토큰을 argv나 .git/config에 노출하지 않는 일회성 GIT_ASKPASS 환경을 구성한다."""
    responder = temp_dir / "askpass_responder.py"
    responder.write_text(
        "import os, sys\n"
        "prompt = sys.argv[1].lower() if len(sys.argv) > 1 else ''\n"
        "token = os.environ['GENERATED_SYNC_ASKPASS_TOKEN']\n"
        "print('x-access-token' if 'username' in prompt else token)\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        launcher = temp_dir / "askpass.cmd"
        launcher.write_text(
            f'@echo off\r\n"{sys.executable}" "{responder}" %*\r\n', encoding="utf-8"
        )
    else:
        launcher = temp_dir / "askpass.sh"
        launcher.write_text(
            f'#!/bin/sh\nexec "{sys.executable}" "{responder}" "$@"\n', encoding="utf-8"
        )
        launcher.chmod(0o700)

    return {
        "GIT_ASKPASS": str(launcher),
        "GIT_TERMINAL_PROMPT": "0",
        "GCM_INTERACTIVE": "never",
        "GENERATED_SYNC_ASKPASS_TOKEN": token,
    }


def checkout_source_commit(
    remote_url: str,
    target_dir: Path,
    head_sha: str,
    *,
    read_token: str = "",
) -> None:
    """신뢰된 기본 브랜치 코드와 분리된 디렉터리에 대상 커밋을 clean checkout한다."""
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True)

    _run_git(target_dir, "init", "-q")
    _run_git(target_dir, "remote", "add", "origin", remote_url)

    with tempfile.TemporaryDirectory() as tmp:
        env_overrides = (
            _git_askpass_env(read_token, Path(tmp))
            if read_token
            else {"GIT_TERMINAL_PROMPT": "0"}
        )
        _run_git(
            target_dir,
            "fetch",
            "--depth=1",
            "--no-tags",
            "origin",
            head_sha,
            env_overrides=env_overrides,
        )

    _run_git(target_dir, "checkout", "--detach", "-q", head_sha)
    actual_sha = (
        _run_git(target_dir, "rev-parse", "HEAD").stdout.decode("utf-8").strip()
    )
    if actual_sha != head_sha:
        raise WriterSecurityError(
            f"체크아웃한 HEAD가 기대 SHA와 다릅니다: {actual_sha} != {head_sha}"
        )


def _ensure_no_symlink_components(root: Path, rel_path: str) -> None:
    current = root
    for part in PurePosixPath(rel_path).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            rel = current.relative_to(root).as_posix()
            raise WriterSecurityError(f"대상 저장소 경로에 symlink가 있습니다: {rel}")


def _git_z_paths(repo_dir: Path, *args: str) -> list[str]:
    result = _run_git(repo_dir, *args)
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def apply_payload(target_dir: Path, payload: ValidatedPayload) -> list[str]:
    """검증된 payload를 clean 대상 checkout에 적용하고 staged diff를 검증한다."""
    if not payload.changed:
        return []

    dirty = _git_z_paths(target_dir, "status", "--porcelain=v1", "-z", "--")
    if dirty:
        raise WriterSecurityError("대상 checkout 디렉터리가 clean 상태가 아닙니다.")

    declared_paths = {entry.path for entry in payload.files} | set(payload.deleted)

    for entry in payload.files:
        _ensure_no_symlink_components(target_dir, entry.path)
        dest = target_dir / entry.path
        dest.parent.mkdir(parents=True, exist_ok=True)
        src = payload.artifact_dir / "files" / entry.path
        shutil.copyfile(src, dest)

    for rel_path in payload.deleted:
        _ensure_no_symlink_components(target_dir, rel_path)
        dest = target_dir / rel_path
        tracked = _run_git(
            target_dir, "ls-files", "--error-unmatch", "--", rel_path, check=False
        )
        if tracked.returncode != 0 or not dest.exists() or not dest.is_file():
            raise WriterSecurityError(
                f"대상 커밋에 없는 파일의 삭제 요청은 거부됩니다: {rel_path}"
            )
        dest.unlink()

    _run_git(target_dir, "add", "-A", "--")

    staged = _git_z_paths(
        target_dir,
        "diff",
        "--cached",
        "--name-only",
        "--no-renames",
        "--diff-filter=ACMRD",
        "-z",
        "--",
    )
    unexpected_staged = [
        path
        for path in staged
        if path not in declared_paths or not is_allowed_generated_output(path)
    ]
    if unexpected_staged:
        raise WriterSecurityError(
            f"허용되지 않은 staged 경로가 감지되었습니다: {unexpected_staged}"
        )

    unstaged = _git_z_paths(
        target_dir, "diff", "--name-only", "--no-renames", "-z", "--"
    )
    untracked = _git_z_paths(
        target_dir, "ls-files", "--others", "--exclude-standard", "-z", "--"
    )
    if unstaged or untracked:
        raise WriterSecurityError(
            "Stage 후 잔여 변경이 남아 있습니다: "
            f"unstaged={unstaged}, untracked={untracked}"
        )

    return sorted(staged)


def commit_and_push(
    target_dir: Path,
    *,
    branch: str,
    expected_head_sha: str,
    repo_full_name: str,
    app_token: str,
    app_slug: str,
    requester: Callable[[str], tuple[int, dict[str, Any]]],
    github_token: str = "",
) -> Decision:
    """허용된 staged 변경을 App bot 신원으로 커밋하고 fast-forward push한다."""
    if not app_token:
        raise WriterSecurityError("GitHub App installation token이 비어 있습니다.")
    if github_token and app_token == github_token:
        raise WriterSecurityError("App token은 기본 GITHUB_TOKEN과 같을 수 없습니다.")

    staged = _git_z_paths(
        target_dir, "diff", "--cached", "--name-only", "--no-renames", "-z", "--"
    )
    if not staged:
        return Decision(False, "no_op")
    invalid = [path for path in staged if not is_allowed_generated_output(path)]
    if invalid:
        raise WriterSecurityError(
            f"커밋 직전 허용되지 않은 경로가 발견되었습니다: {invalid}"
        )

    bot_name, bot_email = get_bot_identity(requester, app_slug)

    live_head = get_branch_head_sha(requester, repo_full_name, branch)
    if live_head != expected_head_sha:
        return Decision(False, "stale_head")

    _run_git(
        target_dir,
        "commit",
        "-m",
        COMMIT_MESSAGE,
        env_overrides={
            "GIT_AUTHOR_NAME": bot_name,
            "GIT_AUTHOR_EMAIL": bot_email,
            "GIT_COMMITTER_NAME": bot_name,
            "GIT_COMMITTER_EMAIL": bot_email,
        },
    )

    live_head_before_push = get_branch_head_sha(requester, repo_full_name, branch)
    if live_head_before_push != expected_head_sha:
        return Decision(False, "stale_head")

    with tempfile.TemporaryDirectory() as tmp:
        env_overrides = _git_askpass_env(app_token, Path(tmp))
        result = _run_git(
            target_dir,
            "push",
            "origin",
            f"HEAD:refs/heads/{branch}",
            env_overrides=env_overrides,
            check=False,
        )
        if result.returncode != 0:
            err = result.stderr.decode("utf-8", errors="replace").strip()
            raise WriterSecurityError(f"Fast-forward push 실패: {err}")

    return Decision(True, "pushed")


def _write_github_outputs(output_path: str | None, values: dict[str, str]) -> None:
    if not output_path:
        return
    with Path(output_path).open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def _load_event(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _verify_from_env(
    requester_factory: Callable[[str, str], Any] | None = None,
) -> tuple[Decision, Provenance | None, Any]:
    event_path = os.environ["GITHUB_EVENT_PATH"]
    event = _load_event(event_path)
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    repo_id = os.environ.get("GITHUB_REPOSITORY_ID", "")
    ref = os.environ.get("GITHUB_REF", "")
    enabled = os.environ.get("GENERATED_SYNC_WRITER_ENABLED", "")
    allowed_branches = os.environ.get("GENERATED_SYNC_WRITER_ALLOWED_BRANCHES", "")
    github_token = os.environ.get("GITHUB_TOKEN", "")
    api_url = os.environ.get("GITHUB_API_URL", DEFAULT_API_URL)

    decision, provenance = verify_workflow_run_event(
        event,
        github_repository=repo,
        github_repository_id=repo_id,
        github_ref=ref,
        enabled=enabled,
        allowed_branches=allowed_branches,
    )
    if not decision.proceed or provenance is None:
        return decision, provenance, None

    factory = (
        make_github_api_requester if requester_factory is None else requester_factory
    )
    requester = factory(github_token, api_url)
    verify_single_artifact(
        requester, provenance.repository_full_name, provenance.run_id
    )
    live_head = get_branch_head_sha(
        requester, provenance.repository_full_name, provenance.branch
    )
    if live_head != provenance.head_sha:
        return Decision(False, "stale_head"), provenance, requester
    return Decision(True, "ok"), provenance, requester


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "verify-run", help="Verify workflow_run provenance and live HEAD"
    )

    prepare = subparsers.add_parser(
        "prepare-write", help="Verify artifact and stage onto isolated checkout"
    )
    prepare.add_argument("--artifact-dir", type=Path, required=True)
    prepare.add_argument("--target-dir", type=Path, required=True)
    prepare.add_argument("--state-file", type=Path)

    push = subparsers.add_parser(
        "commit-and-push", help="Commit staged changes and fast-forward push"
    )
    push.add_argument("--target-dir", type=Path, required=True)
    push.add_argument("--state-file", type=Path, required=True)

    args = parser.parse_args(argv)
    output_path = os.environ.get("GITHUB_OUTPUT")

    try:
        if args.command == "verify-run":
            decision, _, _ = _verify_from_env()
            _write_github_outputs(
                output_path,
                {
                    "should_continue": "true" if decision.proceed else "false",
                    "skip_reason": decision.reason,
                },
            )
            print(f"verify-run: proceed={decision.proceed} reason={decision.reason}")
            return 0

        if args.command == "prepare-write":
            decision, provenance, _ = _verify_from_env()
            if not decision.proceed or provenance is None:
                _write_github_outputs(
                    output_path,
                    {"should_write": "false", "skip_reason": decision.reason},
                )
                print(f"prepare-write: skip reason={decision.reason}")
                return 0

            payload = validate_artifact_payload(args.artifact_dir, provenance)
            if not payload.changed:
                _write_github_outputs(
                    output_path, {"should_write": "false", "skip_reason": "no_op"}
                )
                print("prepare-write: skip reason=no_op")
                return 0

            server_url = os.environ.get("GITHUB_SERVER_URL", DEFAULT_SERVER_URL).rstrip(
                "/"
            )
            remote_url = f"{server_url}/{provenance.repository_full_name}.git"
            checkout_source_commit(
                remote_url,
                args.target_dir,
                provenance.head_sha,
                read_token=os.environ.get("GITHUB_TOKEN", ""),
            )
            staged = apply_payload(args.target_dir, payload)
            if not staged:
                _write_github_outputs(
                    output_path, {"should_write": "false", "skip_reason": "no_op"}
                )
                print("prepare-write: skip reason=no_op")
                return 0

            if args.state_file:
                args.state_file.parent.mkdir(parents=True, exist_ok=True)
                args.state_file.write_text(
                    json.dumps(
                        {
                            "repository_full_name": provenance.repository_full_name,
                            "branch": provenance.branch,
                            "head_sha": provenance.head_sha,
                            "staged_paths": staged,
                        },
                        indent=2,
                    ),
                    encoding="utf-8",
                )
            _write_github_outputs(
                output_path, {"should_write": "true", "skip_reason": "ok"}
            )
            print(f"prepare-write: staged {len(staged)} generated files")
            return 0

        decision, provenance, requester = _verify_from_env()
        if not decision.proceed or provenance is None or requester is None:
            print(f"commit-and-push: skip reason={decision.reason}")
            return 0

        state = json.loads(args.state_file.read_text(encoding="utf-8"))
        if (
            state.get("repository_full_name") != provenance.repository_full_name
            or state.get("branch") != provenance.branch
            or state.get("head_sha") != provenance.head_sha
        ):
            raise WriterSecurityError(
                "prepared state와 workflow_run provenance가 일치하지 않습니다."
            )

        app_token = os.environ.get("APP_TOKEN", "")
        app_slug = os.environ.get("APP_SLUG", "")
        github_token = os.environ.get("GITHUB_TOKEN", "")
        push_decision = commit_and_push(
            args.target_dir,
            branch=provenance.branch,
            expected_head_sha=provenance.head_sha,
            repo_full_name=provenance.repository_full_name,
            app_token=app_token,
            app_slug=app_slug,
            requester=requester,
            github_token=github_token,
        )
        print(
            f"commit-and-push: proceed={push_decision.proceed} "
            f"reason={push_decision.reason}"
        )
        return 0
    except WriterSecurityError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
