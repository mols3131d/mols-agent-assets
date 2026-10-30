---
description: check-dependencies 스킬 초안의 사용 경로, 오프라인 기본 동작과 이식 시 유지할 실행 범위를 확인할 때 참고합니다.
---

# Check Dependencies

Dependency inventory and optional public package/vulnerability verification Skill. This repository maintains the reusable source at [SKILL.md](SKILL.md), together with its script, tests and report template.

## Use

```text
/check-dependencies Inventory dependencies offline, identify unresolved versions, and create a Markdown report.
```

From this repository root, **offline / no network**:

```sh
python src/rulesync/.rulesync/skills/check-dependencies/scripts/check_dependencies.py --root .
```

After explicit authorization to submit package names/versions to public endpoints:

```sh
python src/rulesync/.rulesync/skills/check-dependencies/scripts/check_dependencies.py --root . --online --max-packages 50
```

In another repository, invoke the copy of `scripts/check_dependencies.py` bundled with the installed Skill instead of assuming this source-repository path exists.

Review the offline JSON inventory **before** authorizing online lookups. The script skips lock entries pointing at non-public npm registries and Python requirements with custom package indexes. Unknown origins or registry configuration outside these files may still be private.

The script prints JSON to stdout and does not modify project files. A package not listed by a queried public registry may still exist elsewhere. Empty OSV advisory results never establish safety.

The bundled parser supports only root `package-lock.json` (npm), fallback `package.json` and simple pinned `requirements.txt`. It does not scan other lockfile formats.

Python 3.9+ and the standard library are sufficient; no third-party Python modules are needed.

Maintenance scope and acceptance criteria: [docs/spec.md](docs/spec.md).
