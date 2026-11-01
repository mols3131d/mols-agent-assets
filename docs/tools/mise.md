---
title: mise
description: mise의 프로젝트 설정 예외, CLI 잠금과 setup/update 실행, 최초 준비·복구·선택적 연동을 확인할 때 사용합니다.
---

# mise

mise는 개발 CLI의 설치·버전과 공통 task를 관리합니다. 설정·task는 [`mise.toml`](../../mise.toml), 선택된 CLI 버전과 플랫폼 아티팩트는 [`mise.lock`](../../mise.lock)이 소유합니다. Python 인터프리터와 패키지는 [uv](uv.md)가 맡으며 mise에 중복 선언하지 않습니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 native 설정·명령을 우선하고 mise 자체는 최신 안정 버전을 선호합니다. mise는 bootstrap의 호스트 선행 도구이며 이 프로젝트가 mise 자체를 설치·업데이트하지 않습니다.

- `task.run_auto_install = false`: task 시작 전에 암묵적으로 설치하지 않도록 합니다. 실제 설치는 승인된 bootstrap 경로에서 명시적으로 수행합니다.
- `lockfile = true`: 검토한 CLI 선택을 잠금으로 재현합니다. bootstrap은 별도로 `mise install --locked <tool@version>`을 사용하며, 설정만으로 strict locked install을 대신하지 않습니다.
- CLI 7종은 현재 exact pin입니다. 최신 안정 버전은 명시적 버전 갱신 때 검토하고, `setup`에서 `latest`로 바꾸지 않습니다. 현재 `update`도 CLI pin과 `mise.lock`을 갱신하지 않습니다.
- 공통 환경에는 `PYTHONUTF8`을 선언합니다. PC별 PATH는 Git에서 제외된 `mise.local.toml`에 두고, 기존 프록시·인증·캐시·Git 전역 설정은 불필요하게 바꾸지 않습니다.

바이너리 4종(uv·Node·rumdl·Lefthook)의 lock에는 7개 플랫폼 URL·sha256이 있습니다. Aqua 도구 3종에는 `github-attestations` 메타데이터도 있으나 Node에는 해당 필드가 없습니다. npm CLI 3종(Biome·Rulesync·skills)은 최상위 패키지 버전만 잠그며 전이 의존성 그래프까지 고정하지 않습니다.

## 권장 버전 정책의 적용 경계

mise 자체는 **Latest**를 우선 검토하는 호스트 선행 도구로, 이 저장소가 설치·업데이트하지 않습니다. mise 관리 CLI 7종의 Exact·Patch·Minor·Latest·LTS 배정은 [도구별 권장 정책](README.md#도구별-권장-정책)을 따릅니다.

현재 bootstrap은 Exact 요청만 허용하고 실행 버전도 `mise.toml`의 Exact 값과 비교하므로, 숫자 prefix나 `lts`로 설정만 바꾸면 실패합니다. 범위 정책 적용 시 **mise가 결정한 lock 버전**을 native API로 확인하도록 최소한의 수정·검증이 필요합니다. 별도 SemVer/LTS 선택기를 구현하지 않습니다.

## CLI Version Updates

CLI 7종은 현재 `mise.toml`에서 exact version을 선택하고 `mise.lock`으로 재현합니다. 보안 수정이나 지원 수명 변경도 채택 근거지만, 실행 시마다 자동 갱신하지 않습니다. 현행 Exact pin은 **선택한 새 버전을 `mise.toml`에 먼저 반영**해야 합니다. [SemVer 선택지](README.md#semver-버전-선택지)의 prefix·alias를 추후 지원할 경우에만 `mise lock --bump`로 허용 범위 내 최신 버전을 선택할 수 있습니다.

1. [공통 갱신 기준](README.md#버전-갱신-방법)으로 후보·영향 범위를 검토하고 새 exact pin을 반영합니다.
1. `mise lock`으로 기존 플랫폼의 URL·checksum을 갱신하고 `mise.lock` diff를 검토합니다. 새 지원 플랫폼이 필요하면 `mise lock --platform ...`을 사용합니다. npm backend가 dependency sidecar를 생성한 경우 해당 산출물도 함께 검토·관리합니다.
1. 승인된 환경에서 `mise install --locked`와 프로젝트 검증 명령을 실행합니다. Node·npm CLI 경로, formatter 출력, Rulesync schema·projection을 확인하고 기존 버전 제거·전역 변경은 자동으로 수행하지 않습니다.

Bootstrap은 [현재 코드](../../scripts/development_bootstrap.py)상 exact pin을 요구합니다. `latest`, `lts`, `^X.Y` 같은 range로 `mise.toml`을 단독 변경하는 것은 이 실행기와 호환되지 않으므로, range 추적을 채택하려면 별도 설계·검증이 필요합니다.

## First Use

실제 설치 전에 [개발환경의 설치 승인 경계](../development/development-environment.md#부트스트랩-운영-절차)를 확인합니다. 사용자가 [공식 설치 안내](https://mise.jdx.dev/getting-started.html)에 따라 mise를 준비하고 repository config의 신뢰 여부를 판단합니다. `setup` 진입에도 uv와 [`.python-version`](../../.python-version)의 Python이 먼저 필요합니다.

```bash
mise install --locked uv
mise exec uv -- uv python install
mise run setup --dry-run
mise run setup
```

`mise exec uv`는 전체 toolchain 대신 선언된 uv만 선택합니다. 이미 설치된 Python 3.13 이상이 있다면 `python scripts/development_bootstrap.py setup --dry-run`으로 mise/uv 진입 전 계획을 확인할 수도 있습니다. 호스트 도구를 OS package manager나 remote shell installer로 자동 설치하지 않습니다.

## Setup, Update and Diagnosis

[`development_bootstrap.py`](../../scripts/development_bootstrap.py)는 인자 검증·경로 보호·실패 집계를 맡습니다. task의 `raw_args`로 `--help`·`--dry-run`을 전달하며 `--yes`, `--force`, `--global` 등은 거부합니다.

| 명령 | 현재 동작 |
| --- | --- |
| `mise run setup` | exact CLI pin을 strict locked install·실행 버전으로 확인하고 `uv sync --locked --all-groups`와 `uv sync --check` 수행 |
| `mise run update` | Git의 입력 상태 확인 후 `uv lock --upgrade`로 Python 의존성만 갱신하고 sync·검증 |
| `mise run setup --dry-run` / `mise run update --dry-run` | 안전 조건·계획만 표시. resolver·설치·lock 갱신 없음 |
| `mise run check` / `mise run test` | 기존 toolchain·lock 검사와 deterministic tests. 버전 갱신 경로가 아님 |
| `mise run format-changed` | 변경된 파일만 기존 formatter로 정규화 |

`setup`은 policy·lock을 보존합니다. `update`의 dirty 검사는 `mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`, `mise.lock`에 한정합니다. `assume-unchanged`·`skip-worktree`로 변경이 숨겨지거나 index 조회가 실패하면 중단하며 사용자 플래그를 자동 변경하지 않습니다. `update` 중 허용된 변경은 `uv.lock`뿐입니다. 별도 Rulesync·Skill 파일의 기존 변경은 보존하되 실행 중 예상치 못한 policy·lock 변경은 중단합니다. 이 검사는 모든 동시 쓰기를 막는 sandbox가 아닙니다.

`--dry-run`은 runner의 읽기 전용 계획이며 host readiness나 전체 호스트 무변경을 보장하지 않습니다. mise config 평가·trust와 uv interpreter/cache probing은 script 이전 경계입니다. `mise run --dry-run setup`은 mise task 자체의 preview로 bootstrap 진단과 다릅니다.

### Installation Scope and Recovery

승인된 기본 쓰기 대상은 mise 관리 설치·cache와 프로젝트 `.venv`입니다. Python 자동 다운로드는 끄고, interpreter 누락 시 최초 준비를 명시적으로 수행합니다. 외부 환경을 가리키는 `UV_PROJECT_ENVIRONMENT`, `.venv` symlink/junction과 외부 package 경로는 차단합니다.

Native 도구는 exact request의 경로와 실행 버전을 확인합니다. npm CLI는 package identity·managed prefix를 확인하고 잠근 Node로 실행해 Windows `.cmd` shim을 직접 호출하지 않습니다. package 내부 동작까지 sandbox로 제한하는 것은 아닙니다. 단순한 `mise exec --locked` 위임을 채택하지 않은 근거는 [Windows fallback 실증](../../inbox/github-258/bootstrap-simplification-review-2026-11-01.md)에 있습니다.

Node 실패 시 npm 단계는 차단하되 독립적인 uv/Python 단계는 계속합니다. 필수 실패는 `FAILED`/`BLOCKED`와 nonzero로 보고하고, core 검증이 모두 통과했을 때만 `READY`를 반환합니다. 선택적 연동은 성공 범위에서 제외합니다.

같은 checkout의 중복 실행은 `.tmp/bootstrap.lock`으로 차단합니다. 정상 종료·Ctrl-C는 자기 lock을 해제하며, 강제 종료로 남은 lock은 process 종료를 확인한 뒤 수동 정리합니다. 다른 worktree와 공유하는 mise cache의 동시성은 native manager 책임입니다.

실패하면 표시한 native 명령과 policy·lock diff를 점검한 뒤 `setup`을 재실행합니다. 자동 rollback, 사용자 파일 삭제, `git clean`/reset, hook 덮어쓰기나 전역 설정 변경은 하지 않습니다.

### Optional Integrations

기본 `setup`/`update`는 Rulesync dependency·projection, HOME Skills와 Git hooks를 설치하지 않습니다. 각 설치 범위와 기존 파일을 검토하고 별도 승인 후 실행합니다.

```bash
rulesync install --frozen
rulesync generate --dry-run
mise run skills-sync
```

실제 projection은 preview의 출력 대상·기존 파일을 확인한 뒤 `rulesync generate`로 생성합니다. hook은 공유 `core.hooksPath`와 기존 hook을 확인한 뒤 `lefthook install`로 설치합니다. [Rulesync](rulesync.md), [skills CLI](skills-cli.md), [Lefthook](lefthook.md)의 별도 연동 경계를 따릅니다.

### Shared and Local Environment

Windows에서 Git Bash 경로가 필요한 경우 등 PC별 차이는 로컬 설정에 둡니다.

```toml
[env]
_.path = ["C:/Program Files/Git/bin"]
```

Git에서 제외된 `mise.local.toml`과 `rulesync.local.jsonc`를 PR로 자동 변경하지 않습니다. 이전 transport·LF 보정만을 위한 설정과 중복 환경값은 각 PC에서 필요성을 검토한 뒤 정리하고 유효한 PATH·인증·상위 프로세스 환경은 보존합니다.

## Official Sources

- [Configuration](https://mise.jdx.dev/configuration.html)
- [Lockfile](https://mise.jdx.dev/dev-tools/mise-lock.html)
- [Backends](https://mise.jdx.dev/dev-tools/backends/) · [npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
- [Tasks](https://mise.jdx.dev/tasks/) · [CI](https://mise.jdx.dev/continuous-integration.html)
