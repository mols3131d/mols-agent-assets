import json
from pathlib import Path
from typing import Any


def load_lockfile(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"lockfile not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("lockfile must be a JSON object")

    if data.get("version") != 1:
        raise ValueError("unsupported lockfile version; expected version=1")

    if "assets" not in data or not isinstance(data["assets"], dict):
        raise ValueError("lockfile.assets must be an object")

    return data


def save_lockfile(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )


def iter_assets(lock: dict[str, Any]):
    for name, item in lock["assets"].items():
        if not isinstance(item, dict):
            raise ValueError(f"asset must be an object: {name}")

        source_url = item.get("sourceUrl")
        dest_path = item.get("destPath")

        if not isinstance(source_url, str) or not source_url:
            raise ValueError(f"asset.sourceUrl must be a non-empty string: {name}")

        if not isinstance(dest_path, str) or not dest_path:
            raise ValueError(f"asset.destPath must be a non-empty string: {name}")

        computed_hash = item.get("computedHash", "")
        if not isinstance(computed_hash, str):
            raise ValueError(f"asset.computedHash must be a string: {name}")

        yield name, item
