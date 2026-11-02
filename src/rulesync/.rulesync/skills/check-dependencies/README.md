---
description: check-dependencies 스킬 초안의 사용 경로, 오프라인 기본 동작과 이식 시 유지할 실행 범위를 확인할 때 참고합니다.
---

# Check Dependencies

Dependency inventory and optional public package/vulnerability verification Skill. The reusable package contains [SKILL.md](SKILL.md), a script, tests and a report template.

## Use

```text
/check-dependencies Inventory dependencies offline, identify unresolved versions, and create a Markdown report.
```

Resolve paths from the **installed Skill package** and the repository to inspect. Replace the placeholders before running. **Offline / no network**:

```sh
python "<installed-skill-dir>/scripts/check_dependencies.py" --root "<target-repo-dir>"
```

After explicit authorization to submit package names/versions to public endpoints:

```sh
python "<installed-skill-dir>/scripts/check_dependencies.py" --root "<target-repo-dir>" --online --max-packages 50
```

The script path is independent of the target repository; no checkout of the authoring repository is required.

Review the offline JSON inventory **before** authorizing online lookups. The script skips lock entries pointing at non-public npm registries and Python requirements with custom package indexes or `--no-index`. Unknown origins or registry configuration outside these files may still be private.

The script prints JSON to stdout and does not modify project files. A package not listed by a queried public registry may still exist elsewhere. Empty OSV advisory results never establish safety.

The bundled parser supports only root `package-lock.json` (npm), fallback `package.json` and simple pinned `requirements.txt`. It does not scan other lockfile formats.

Python 3.9+ and the standard library are sufficient; no third-party Python modules are needed.

Maintenance scope and acceptance criteria: [docs/spec.md](docs/spec.md).
