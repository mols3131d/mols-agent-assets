#!/usr/bin/env python3
"""Read-only npm/PyPI inventory; public registry and OSV lookup only with --online.

Python 3.9+ standard library. Prints JSON to stdout. Never runs package manager commands.
"""
import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

EXACT_VERSION = re.compile(r"^\d+(?:\.\d+){1,3}(?:[-+][A-Za-z0-9._+\-]+)?$")
PYPI_PIN = re.compile(r"^([A-Za-z0-9][\w.\-]*)(?:\[[^\]]+\])?\s*==\s*([^;\s#]+)(?:\s*;.*)?$")
UNSUPPORTED_NAMES = ("pnpm-lock.yaml", "yarn.lock", "poetry.lock", "pdm.lock", "uv.lock", "pyproject.toml", "Pipfile.lock", "Cargo.lock", "go.sum")


def record(ecosystem, name, version, source, pinned, reason=None, scope=None):
    return {
        "ecosystem": ecosystem,
        "name": name,
        "version": version or None,
        "source": source,
        "scope": scope,
        "version_status": "PINNED" if pinned else "UNRESOLVED",
        "reason": reason,
        "registry": "NOT_CHECKED",
        "osv": "NOT_CHECKED",
        "advisory_ids": [],
        "errors": [],
        "public_origin": "UNKNOWN",
    }


def npm_name_from_path(lock_path):
    if "node_modules/" not in lock_path:
        return None
    return lock_path.rsplit("node_modules/", 1)[-1]


PUBLIC_NPM_HOSTS = frozenset({"registry.npmjs.org", "registry.yarnpkg.com"})


def npm_origin(metadata):
    """Do not disclose custom/private registry hosts in output; mark eligibility only."""
    resolved = metadata.get("resolved")
    if not isinstance(resolved, str) or not resolved:
        return "UNKNOWN"
    parts = urllib.parse.urlsplit(resolved)
    if parts.scheme in ("https", "http") and parts.hostname in PUBLIC_NPM_HOSTS:
        return "PUBLIC"
    return "NONPUBLIC_ORIGIN"


def npm_lock(root, warnings):
    source = root / "package-lock.json"
    if not source.is_file():
        return None
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        warnings.append(f"Cannot read package-lock.json: {exc}")
        return []
    result = []
    if not isinstance(data, dict):
        warnings.append("Unsupported package-lock.json root type")
        return result
    if isinstance(data.get("packages"), dict):
        for loc, metadata in sorted(data["packages"].items()):
            if not loc or not isinstance(metadata, dict):
                continue
            name = metadata.get("name") or npm_name_from_path(loc)
            if not name:
                warnings.append(f"Unrecognized lock path: {loc}")
                continue
            version = metadata.get("version")
            pinned = isinstance(version, str) and bool(EXACT_VERSION.fullmatch(version)) and not metadata.get("link")
            entry = record("npm", str(name), version, f"package-lock.json:{loc}", pinned,
                           None if pinned else "non-exact/non-registry lock entry", "direct" if loc.count("node_modules/") == 1 else "transitive")
            entry["public_origin"] = npm_origin(metadata)
            result.append(entry)
    elif isinstance(data.get("dependencies"), dict):
        def visit(deps, prefix=""):
            for name, meta in sorted(deps.items()):
                if not isinstance(meta, dict):
                    continue
                version = meta.get("version")
                pinned = isinstance(version, str) and bool(EXACT_VERSION.fullmatch(version))
                entry = record("npm", name, version, f"package-lock.json:{prefix}{name}", pinned,
                               None if pinned else "non-exact/non-registry lock entry")
                entry["public_origin"] = npm_origin(meta)
                result.append(entry)
                children = meta.get("dependencies")
                if isinstance(children, dict):
                    visit(children, f"{prefix}{name}/")
        visit(data["dependencies"])
    else:
        warnings.append("Unsupported/empty package-lock.json structure")
    return result


def npm_manifest(root, warnings):
    source = root / "package.json"
    if not source.is_file():
        return []
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        warnings.append(f"Cannot read package.json: {exc}")
        return []
    result = []
    if not isinstance(data, dict):
        warnings.append("Unsupported package.json root type")
        return result
    for group in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        declared = data.get(group)
        if declared is not None and not isinstance(declared, dict):
            warnings.append(f"Unsupported package.json {group} field")
            continue
        for name, spec in sorted((declared or {}).items()):
            # A declared range is not an observed locked package version, even if it looks exact.
            result.append(record("npm", name, str(spec), f"package.json:{group}", False,
                                 "manifest declaration without lockfile resolution", group))
    return result


def python_requirements(root, warnings):
    path = root / "requirements.txt"
    if not path.is_file():
        return []
    result = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        warnings.append(f"Cannot read requirements.txt: {exc}")
        return []
    # A custom index may host names that must not be disclosed to the public PyPI API.
    private_index = any(re.match(r"^\s*(?:-i(?:\s|=)|--(?:extra-)?index-url(?:\s|=)|-f(?:\s|=)|--find-links(?:\s|=))", line)
                        for line in lines)
    if private_index:
        warnings.append("Custom Python package index or find-links found; skip all PyPI online lookups by default")
    for line_no, raw in enumerate(lines, 1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        # Strip an inline comment only after a whitespace; do not alter URL fragments.
        value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
        if value.startswith("-") or value.startswith(("git+", "http:", "https:", "file:")):
            warnings.append(f"Unparsed requirements.txt:{line_no} directive/reference; not audited")
            continue
        match = PYPI_PIN.fullmatch(value)
        if match:
            name, version = match.groups()
            pinned = bool(EXACT_VERSION.fullmatch(version))
            entry = record("PyPI", re.sub(r"[-_.]+", "-", name.lower()), version,
                           f"requirements.txt:{line_no}", pinned,
                           None if pinned else "wildcard/non-exact requirement")
            entry["public_origin"] = "NONPUBLIC_ORIGIN" if private_index else "UNKNOWN"
            result.append(entry)
        else:
            name = re.match(r"^([A-Za-z0-9][\w.\-]*)", value)
            result.append(record("PyPI", re.sub(r"[-_.]+", "-", name.group(1).lower()) if name else value,
                                 None, f"requirements.txt:{line_no}", False,
                                 "unpinned/unsupported requirement syntax"))
    return result


def inventory(root):
    warnings = []
    found = [name for name in UNSUPPORTED_NAMES if (root / name).is_file()]
    if found:
        warnings.append("Unsupported root files (not audited): " + ", ".join(found))
    locked = npm_lock(root, warnings)
    packages = (locked if locked is not None else npm_manifest(root, warnings)) + python_requirements(root, warnings)
    if not (root / "package-lock.json").is_file() and not (root / "package.json").is_file() and not (root / "requirements.txt").is_file():
        warnings.append("No supported root manifest/lockfile found")
    # Repeated package/version instances at different source paths are reported separately to retain provenance.
    return packages, warnings


def request_json(url, payload=None, timeout=10):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Accept": "application/json", "User-Agent": "check-dependencies/0.2"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, OSError, UnicodeError, ValueError) as exc:
        return None, str(exc)


def lookup_public(package, timeout):
    name = urllib.parse.quote(package["name"], safe="")
    version = package["version"]
    if package["ecosystem"] == "npm":
        url = f"https://registry.npmjs.org/{name}/{urllib.parse.quote(version, safe='')}"
    else:
        url = f"https://pypi.org/pypi/{name}/{urllib.parse.quote(version, safe='')}/json"
    data, error = request_json(url, timeout=timeout)
    if error == "HTTP 404":
        package["registry"] = "NOT_FOUND_PUBLIC"
    elif error:
        package["registry"] = "ERROR"
        package["errors"].append(f"public registry: {error}")
    elif isinstance(data, dict):
        package["registry"] = "EXISTS_PUBLIC"
    else:
        package["registry"] = "ERROR"
        package["errors"].append("public registry: unexpected response")


def query_osv(packages, timeout):
    # Query unique exact package versions; preserve original result rows for multiple occurrences.
    keys = list(dict.fromkeys((p["ecosystem"], p["name"], p["version"]) for p in packages))
    answers = {}
    for start in range(0, len(keys), 50):
        chunk = keys[start:start + 50]
        pending = [(key, None) for key in chunk]
        state = {key: {"ids": set(), "status": "NONE_REPORTED", "errors": []} for key in chunk}
        for _page in range(10):
            if not pending:
                break
            query = [{"package": {"ecosystem": key[0], "name": key[1]}, "version": key[2],
                      **({"page_token": token} if token else {})} for key, token in pending]
            data, error = request_json("https://api.osv.dev/v1/querybatch", {"queries": query}, timeout)
            results = data.get("results") if isinstance(data, dict) else None
            if error or not isinstance(results, list) or len(results) != len(pending):
                for key, _ in pending:
                    state[key]["status"] = "ERROR"
                    state[key]["errors"].append(f"OSV: {error or 'invalid batch response'}")
                pending = []
                break
            next_pending = []
            for (key, _token), entry in zip(pending, results):
                if not isinstance(entry, dict) or not isinstance(entry.get("vulns", []), list):
                    state[key]["status"] = "ERROR"
                    state[key]["errors"].append("OSV: invalid result entry")
                    continue
                state[key]["ids"].update(str(v["id"]) for v in entry.get("vulns", []) if isinstance(v, dict) and v.get("id"))
                token = entry.get("next_page_token")
                if token:
                    next_pending.append((key, token))
            pending = next_pending
        for key, _token in pending:
            state[key]["status"] = "INCOMPLETE"
            state[key]["errors"].append("OSV: pagination limit reached")
        for key, val in state.items():
            ids = sorted(val["ids"])
            status = val["status"]
            if status == "NONE_REPORTED" and ids:
                status = "FOUND"
            answers[key] = (status, ids, val["errors"])
    for p in packages:
        result = answers[(p["ecosystem"], p["name"], p["version"])]
        p["osv"], p["advisory_ids"], errs = result
        p["errors"].extend(errs)


def verify_online(packages, warnings, max_packages, timeout, include_scoped):
    eligible = []
    for p in packages:
        if p["ecosystem"] == "npm" and p["name"].startswith("@") and not include_scoped:
            p["registry"] = "SKIPPED"
            p["reason"] = (p["reason"] + "; " if p["reason"] else "") + "scoped npm package excluded from public lookups"
            continue
        if p["public_origin"] == "NONPUBLIC_ORIGIN":
            p["registry"] = "SKIPPED"
            p["reason"] = (p["reason"] + "; " if p["reason"] else "") + "non-public or custom source excluded from public lookups"
            continue
        if p["version_status"] != "PINNED":
            continue
        eligible.append(p)
    # Deduplicate for network calls while retaining the source provenance.
    seen = set()
    selected = []
    for p in eligible:
        key = (p["ecosystem"], p["name"], p["version"])
        if key not in seen and len(selected) < max_packages:
            seen.add(key)
            selected.append(p)
    if len(seen) < len(set((p["ecosystem"], p["name"], p["version"]) for p in eligible)):
        warnings.append(f"Online lookup limited to first {max_packages} unique pinned packages; others NOT_CHECKED")
    for p in selected:
        lookup_public(p, timeout)
    if selected:
        query_osv(selected, timeout)
    lookup_results = {(p["ecosystem"], p["name"], p["version"]): p for p in selected}
    for p in packages:
        src = lookup_results.get((p["ecosystem"], p["name"], p["version"]))
        if src is not None and src is not p:
            # Do not propagate results onto intentionally excluded private scoped entries.
            if p["registry"] != "SKIPPED":
                p["registry"] = src["registry"]
                p["osv"] = src["osv"]
                p["advisory_ids"] = list(src["advisory_ids"])
                p["errors"] = list(src["errors"])
    return len(selected)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="project root (not recursive)")
    parser.add_argument("--online", action="store_true", help="send package names/versions to public registry and OSV endpoints")
    parser.add_argument("--include-scoped", action="store_true", help="also submit npm @scope names online")
    parser.add_argument("--max-packages", type=int, default=50, help="max unique package/version pairs queried online")
    parser.add_argument("--timeout", type=int, default=10, help="network timeout seconds")
    args = parser.parse_args(argv)
    if args.max_packages < 1 or args.timeout < 1:
        parser.error("--max-packages and --timeout must be >= 1")
    if args.include_scoped and not args.online:
        parser.error("--include-scoped requires --online")
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    packages, warnings = inventory(root)
    queried = verify_online(packages, warnings, args.max_packages, args.timeout, args.include_scoped) if args.online else 0
    output = {
        "tool": "check-dependencies/0.2",
        "root": str(root),
        "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "online_enabled": args.online,
        "online_unique_packages_queried": queried,
        "coverage": {"packages_listed": len(packages), "pinned": sum(p["version_status"] == "PINNED" for p in packages),
                     "unresolved": sum(p["version_status"] != "PINNED" for p in packages)},
        "warnings": warnings,
        "packages": packages,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
