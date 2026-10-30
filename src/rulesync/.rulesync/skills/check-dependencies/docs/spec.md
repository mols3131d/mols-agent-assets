---
description: check-dependencies 스킬의 입력 범위, 상태 의미, 개인정보 경계 및 초안 수용 기준을 유지보수할 때 참조합니다.
---

# Check Dependencies — Maintenance Specification

> Status: Draft v0.2. The `check-dependencies` Skill owns dependency inventory and optional evidence-based public lookups.

## Responsibility and trust boundary

Input: repository root and optionally explicit public lookup permission. Default output: read-only JSON inventory; optional Markdown report. The Skill does not install packages, patch manifests or diagnose application behavior unrelated to dependencies.

**Privacy default:** no network. Online mode shares selected package names and exact versions with public providers; requires explicit user authorization. npm `@scope/name` entries are excluded by default even in online mode. Lock entries with explicit non-public npm `resolved` origins and Python requirements declaring custom indexes are skipped, even with `--online`. Entries with unknown origins may still be private; review the offline inventory and external `.npmrc`/pip configuration before opting in. The script does not automatically discover private registry overrides outside the manifests.

## Source ownership

- [`SKILL.md`](../SKILL.md): behavior and permission contract (canonical).
- [`scripts/check_dependencies.py`](../scripts/check_dependencies.py): deterministic local parser and opt-in public API caller.
- [`templates/dependencies.md`](../templates/dependencies.md): Markdown + script-free HTML report structure.
- [`tests/test_check_dependencies.py`](../tests/test_check_dependencies.py): deterministic regression fixtures/mocks.
- This file: maintenance acceptance and known scope limits.

## Supported inputs (v0.2)

- npm: `package-lock.json` lockfile versions 2/3 (`packages`) or 1 (`dependencies`) at repository root; fallback to `package.json` declarations if lockfile is absent.
- Python: simple `requirements.txt` entries using `name==concrete-version` at repository root.
- **Not covered by this built-in parser:** `pnpm-lock.yaml`, Yarn lockfiles, Poetry/PDM/uv lockfiles, nested workspace manifests, `pyproject.toml`, requirements includes/constraints, custom package sources or registries. Must disclose, never silently count as checked.
- Do not treat npm semver ranges, direct VCS/file dependencies, unresolved aliases, wildcard requirements or unsupported syntaxes as pinned exact versions.

## Result semantics

- `registry`: `NOT_CHECKED` | `EXISTS_PUBLIC` | `NOT_FOUND_PUBLIC` | `SKIPPED` | `ERROR`.
- `osv`: `NOT_CHECKED` | `FOUND` | `NONE_REPORTED` | `INCOMPLETE` | `ERROR`.
- Package identity includes ecosystem, package name and **resolved exact version** when possible. `public_origin` is a privacy decision signal (`PUBLIC`/`UNKNOWN`/`NONPUBLIC_ORIGIN`), not proof a package is or is not public.
- Python environment markers, optional extras and installed environment state are not resolved; inventory presence does not prove a package is installed in a particular environment.
- A 404 is evidence about *the queried public endpoint*, not all registries or package existence globally.
- OSV batch results provide advisory IDs; severity, CVSS or fixed versions need separate authoritative records, not inference.
- If the API fails, paginates beyond the limit or returns an incompatible payload, preserve `ERROR`/`INCOMPLETE` and a human-readable reason.

## Acceptance criteria

| ID | Scenario | Expected result |
|---|---|---|
| DC-01 | Offline invocation | No network requests and `NOT_CHECKED` online statuses |
| DC-02 | Lockfile and manifest present | Exact lockfile versions preferred over declared ranges |
| DC-03 | Unpinned requirement | Explicit `UNRESOLVED`, no OSV version query |
| DC-04 | Scoped npm package | Public query skipped without explicit flag |
| DC-05 | Public registry 404 | `NOT_FOUND_PUBLIC`, not global absence |
| DC-06 | OSV batch returns IDs | `FOUND` with real IDs, no invented CVSS |
| DC-07 | Empty OSV response | `NONE_REPORTED`, never 'safe' |
| DC-08 | API error/malformed response | Preserved as `ERROR`/`INCOMPLETE` |
| DC-09 | Unsupported dependency file | Named coverage omission |
| DC-10 | Markdown report | Source scope and unknowns visible without running HTML scripts |
| DC-11 | npm lock entry resolved at non-public host | No network lookup; entry explicitly `SKIPPED` |
| DC-12 | requirements.txt has custom `--index-url` | No PyPI/OSV lookup for any pinned Python package |

## Verification

Run built-in unit tests without network:

```sh
python -m unittest discover -s src/rulesync/.rulesync/skills/check-dependencies/tests -v
```

Then, in a disposable test project, run offline inventory and review paths, package identities and unknowns. Online integration tests are optional and must use intentionally public fixture packages, with permission for outbound requests. Do not equate mocked API coverage with actual network verification.

When installed into another project, use the test path relative to that installed Skill package.

## Compatibility and future changes

Preserve status meanings and opt-in network semantics. Support for additional lockfiles or vulnerability sources requires explicit parser accuracy tests and disclosure boundaries. Avoid introducing an installer or auto-fix behavior. The parsed dependency subset is not a complete SBOM.
