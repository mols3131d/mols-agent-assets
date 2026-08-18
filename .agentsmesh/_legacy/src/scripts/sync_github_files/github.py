import urllib.parse
import urllib.request
from pathlib import Path


def github_blob_to_raw(url: str) -> str:
    parsed = urllib.parse.urlparse(url)

    if parsed.netloc != "github.com":
        return url

    parts = parsed.path.strip("/").split("/")

    if len(parts) >= 5 and parts[2] == "blob":
        owner = parts[0]
        repo = parts[1]
        ref = parts[3]
        file_path = "/".join(parts[4:])
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{file_path}"

    return url


def filename_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    if path.endswith("/"):
        raise ValueError(f"cannot infer filename from sourceUrl: {url}")
    name = Path(path).name

    if not name:
        raise ValueError(f"cannot infer filename from sourceUrl: {url}")

    return name


def resolve_dest_path(source_url: str, dest_path: str) -> Path:
    if dest_path.endswith("/"):
        return Path(dest_path) / filename_from_url(source_url)
    return Path(dest_path)


def download(source_url: str) -> bytes:
    raw_url = github_blob_to_raw(source_url)

    req = urllib.request.Request(
        raw_url,
        headers={
            "User-Agent": "sync-assets.py",
            "Accept": "*/*",
        },
    )

    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()
