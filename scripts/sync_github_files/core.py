import hashlib
from pathlib import Path
from typing import Any

from .github import download, resolve_dest_path
from .lockfile import iter_assets, load_lockfile, save_lockfile


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes_if_exists(path: Path) -> bytes | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"destination exists but is not a file: {path}")
    return path.read_bytes()


def write_file(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(content)
    tmp.replace(path)


def classify_state(
    dest_exists: bool,
    synced_hash: str,
    remote_hash: str,
    local_hash: str | None,
) -> str:
    if not dest_exists:
        return "missing"

    if not synced_hash:
        if local_hash == remote_hash:
            return "adopted"
        return "untracked-local"

    remote_changed = remote_hash != synced_hash
    local_changed = local_hash != synced_hash

    if not remote_changed and not local_changed:
        return "unchanged"

    if remote_changed and not local_changed:
        return "remote-changed"

    if not remote_changed and local_changed:
        return "local-modified"

    return "conflict"


def sync_asset(
    name: str,
    item: dict[str, Any],
    *,
    dry_run: bool,
    check: bool,
    force: bool,
) -> tuple[bool, bool]:
    source_url = item["sourceUrl"]
    dest_path = item["destPath"]
    synced_hash = item.get("computedHash", "")

    final_path = resolve_dest_path(source_url, dest_path)

    print(f"checking: {name}")
    print(f"  source: {source_url}")
    print(f"  dest:   {final_path}")

    remote_content = download(source_url)
    remote_hash = sha256_bytes(remote_content)

    local_content = read_bytes_if_exists(final_path)
    local_hash = sha256_bytes(local_content) if local_content is not None else None

    state = classify_state(
        dest_exists=local_content is not None,
        synced_hash=synced_hash,
        remote_hash=remote_hash,
        local_hash=local_hash,
    )

    lock_changed = False
    needs_action = False

    if state == "unchanged":
        print("  status: unchanged")
        return False, False

    if state == "adopted":
        print("  status: adopted")
        if not check and not dry_run:
            item["computedHash"] = remote_hash
            lock_changed = True
        return False, lock_changed

    if state == "missing":
        print("  status: missing")
        needs_action = True

        if check or dry_run:
            print(f"  action: would install {final_path}")
            return True, False

        write_file(final_path, remote_content)
        item["computedHash"] = remote_hash
        print(f"  action: installed {final_path}")
        return True, True

    if state == "remote-changed":
        print("  status: remote-changed")
        needs_action = True

        if check or dry_run:
            print(f"  action: would update {final_path}")
            return True, False

        write_file(final_path, remote_content)
        item["computedHash"] = remote_hash
        print(f"  action: updated {final_path}")
        return True, True

    if state == "local-modified":
        print("  status: local-modified")

        if force:
            needs_action = True

            if check or dry_run:
                print(f"  action: would overwrite local changes {final_path}")
                return True, False

            write_file(final_path, remote_content)
            item["computedHash"] = remote_hash
            print(f"  action: overwritten by --force {final_path}")
            return True, True

        print("  action: skipped")
        print("  hint:   use --force to overwrite local changes")
        return True, False

    if state == "untracked-local":
        print("  status: untracked-local")

        if force:
            needs_action = True

            if check or dry_run:
                print(f"  action: would overwrite untracked local file {final_path}")
                return True, False

            write_file(final_path, remote_content)
            item["computedHash"] = remote_hash
            print(f"  action: overwritten by --force {final_path}")
            return True, True

        print("  action: skipped")
        print("  hint:   computedHash is empty and local file differs; use --force to overwrite")
        return True, False

    if state == "conflict":
        print("  status: conflict")

        if force:
            needs_action = True

            if check or dry_run:
                print(f"  action: would resolve by overwriting {final_path}")
                return True, False

            write_file(final_path, remote_content)
            item["computedHash"] = remote_hash
            print(f"  action: conflict resolved by --force {final_path}")
            return True, True

        remote_path = Path(str(final_path) + ".remote")

        if check or dry_run:
            print(f"  action: would write remote copy to {remote_path}")
            print("  hint:   use --force to overwrite local file")
            return True, False

        write_file(remote_path, remote_content)
        print(f"  action: local file preserved; remote copy written to {remote_path}")
        print("  hint:   resolve manually or rerun with --force")
        return True, False

    raise RuntimeError(f"unknown state: {state}")


def sync(lockfile: Path, *, dry_run: bool, check: bool, force: bool) -> int:
    lock = load_lockfile(lockfile)

    any_action_needed = False
    lock_changed = False

    for name, item in iter_assets(lock):
        action_needed, item_lock_changed = sync_asset(
            name,
            item,
            dry_run=dry_run,
            check=check,
            force=force,
        )

        any_action_needed = any_action_needed or action_needed
        lock_changed = lock_changed or item_lock_changed

    if lock_changed and not dry_run and not check:
        save_lockfile(lockfile, lock)
        print(f"lockfile updated: {lockfile}")

    if check and any_action_needed:
        return 1

    return 0
