---
title: mise
description: 이 저장소의 mise·uv 소유권, setup/update의 exact pin·lock·설치 권한, 최초 준비와 실패 복구, 선택적 Skill·hook 연동 경계를 확인할 때 사용합니다.
---

# mise

이 문서는 **mise·uv의 실제 사용법과 통합 동작 안내**입니다. 개발환경 구축·복구·업데이트 및 **사용자 설치 허가의 운영 정책 정본은 [Development Environment](../../development/development-environment.md)**입니다. 에이전트가 설치 명령을 실행하기 전에 해당 정책의 명시적 허가 절차를 적용합니다.

Repository tool version authority는 root [`mise.toml`](../../../mise.toml)입니다. Python 자체의 version과 dependency environment는 uv가 소유합니다.

| Owner | Scope |
| --- | --- |
| mise | `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync, skills CLI의 binary/version과 cross-tool tasks |
| uv | `.python-version`, `pyproject.toml`, `uv.lock`, Python environment와 Python dependencies |

Python을 `mise.toml`에 중복 선언하지 않습니다. Non-Python tool을 Python dependency group에 넣지 않습니다. npm backend로 관리하는 CLI는 `mise.toml`에서 exact version을 pin하며 repository task는 `@latest`를 직접 호출하지 않습니다.

## First use

Repository root에서 시작합니다. `mise`는 [공식 설치 안내](https://mise.jdx.dev/getting-started.html)에 따라 사용자가 먼저 설치하고 repository config의 신뢰 여부를 판단합니다. Task가 시작하기 전의 자동 도구 설치는 `task.run_auto_install = false`로 끕니다. 누락된 host tool을 OS package manager나 remote shell installer로 자동 설치하지 않습니다.

`setup` 자체를 시작하려면 `uv`와 [`.python-version`](../../../.python-version)의 Python이 이미 필요합니다. 이 최초 준비는 관리형 도구·Python cache 쓰기를 승인한 뒤 명시적으로 수행합니다.

```bash
mise install uv
mise exec uv -- uv python install
mise run setup --dry-run
mise run setup
```

`mise exec uv`는 전체 toolchain 대신 선언된 uv만 선택합니다. 최초 준비를 생략하면 help도 시작하지 못할 수 있으며, 출력된 missing prerequisite를 먼저 해결합니다. 직접 실행할 수 있는 Python 3.13 이상이 있다면 `python scripts/development_bootstrap.py setup --dry-run`으로 mise/uv 진입 전 계획을 확인할 수도 있습니다.

## Setup, update and diagnosis

두 task는 단일 명령과 `raw_args`를 사용하며, [`development_bootstrap.py`](../../../scripts/development_bootstrap.py)가 인자 검증·경로 보호·실패 집계를 소유합니다. `--help`와 `--dry-run`만 공개하며 `--yes`, `--force`, `--global` 등은 실행 전 거부합니다.

**이번 bootstrap의 완료 범위는 core 개발환경(toolchain + project Python)**입니다. Rulesync dependency/projection, 사용자 HOME Skill과 Git hooks는 선택적 별도 연동으로 확정하며, core 성공의 전제 조건으로 설치하거나 검증하지 않습니다. `READY`도 이 core 범위만 뜻하고 선택적 기능의 설치·준비 완료를 뜻하지 않습니다.

| Command | 동작 |
| --- | --- |
| `mise run setup` | 기존 exact CLI pin 설치·실행 버전 검증 후 `uv sync --locked --all-groups`, `uv sync --check` |
| `mise run update` | clean policy/lock을 확인하고 `uv lock --upgrade`로 기존 Python dependency constraint 안에서 해석한 뒤 setup과 같은 sync·검증 |
| `mise run setup --dry-run` / `mise run update --dry-run` | 안전 조건과 실행 계획만 표시. 후보 버전 해석·설치·lock 갱신 없음 |
| `mise run check` / `mise run test` | 기존 toolchain/lock 검사와 deterministic tests. update의 대체 경로가 아님 |
| `mise run format-changed` | 변경된 파일만 기존 formatter로 정규화 |

현재 CLI 정책은 모두 exact pin이므로 `update`도 CLI 버전을 바꾸지 않습니다. `mise.lock`이 도입되어 도구별 릴리스 아티팩트 URL, 체크섬 및 provenance가 플랫폼별로 잠금 관리됩니다. Python package의 허용 범위는 [`pyproject.toml`](../../../pyproject.toml)이 소유하며 wrapper는 별도 범위를 만들지 않습니다. Rulesync/Skill source revision은 일반 update에서 유지합니다.

### CLI tool versioning policy and cases

저장소가 관리하는 7개 CLI 도구(`uv`, `node`, `rumdl`, `lefthook`, `biome`, `rulesync`, `skills`)는 호환성 우선(exact pin)과 bounded 최신 지향 정책에 따라 아래 4가지 케이스로 분류합니다.

| 케이스 | SemVer 규칙 및 범위 | LTS / 안정성 전략 | 호환성 및 운영 위험도 | 적용 대상 CLI |
| --- | --- | --- | --- | --- |
| **1. 패치 버전 준수하는 최신 버전** | `~X.Y.Z` (`X.Y.*`)<br>• Major·Minor 고정<br>• 최신 Patch만 수용 | 특정 안정 Minor 라인 유지, 보안 패치 및 결함 수정만 지속 반영 | **호환성 최우선 (Zero Risk)**<br>CLI 플래그·포맷 규칙 변경에 따른 churn 및 오작동 원천 차단 | • `uv` (0.x 코어 resolver)<br>• `rumdl` (0.x Markdown 린터)<br>• `npm:@biomejs/biome` (포맷팅 일관성) |
| **2. 마이너 버전 준수하는 최신 버전** | `^X.Y.Z` (`X.*`)<br>• Major 고정<br>• 최신 Minor·Patch 수용 | 장기 지원 메이저 라인 내에서 비파괴적 최신 기능과 성능 개선 지속 흡수 | **제한적 최신성 (Low Risk)**<br>하위 호환성 유지(SemVer 엄격 준수 성숙 도구 대상) | • `lefthook` (v2 Git hook 실행기)<br>• `node` (Active LTS 메이저 내 최신) |
| **3. 메이저 버전 준수하는 최신 버전** | 지원 수명 주기 준수<br>• 비LTS(Current 홀수 등) 배제<br>• 검증된 LTS 메이저 추적 | 릴리스 즉시 승격하지 않고 공식 LTS 전환 및 마이그레이션 검증 후 승격 | **계획된 현대화 (Medium Risk)**<br>Breaking change 가능성이 있어 명시적 검증 후 전환 | • `node` (Node.js 짝수 Active LTS 준수)<br>• `npm:rulesync` (호환 검증된 메이저 라인) |
| **4. 최신 버전** | `latest` / `*`<br>• 상한선 없는 최신 릴리스<br>• 프리릴리스 제외 | 최신 안정 공식 릴리스 선호, Alpha/Beta/RC 배제 | **생태계 동기화 (High Risk)**<br>빠르게 진화하는 외부 스펙 대응 우선, lock 재현 필수 | • `npm:skills` (Agent Skills 생태계 연동) |

#### 도구별 버전 정책 및 잠금 소유권

| 도구 | 현재 Pin (`mise.toml`) | 버전 정책 케이스 | 허용 범위 및 규칙 | 잠금 소유자 |
| --- | --- | --- | --- | --- |
| `uv` | `0.12.1` | Case 1 (패치 준수) | 0.x 단계에서 resolver·동작 변경 방지를 위해 패치만 허용 | `mise.lock` |
| `node` | `24.19.0` | Case 2 & 3 (LTS 메이저 준수) | Node 짝수 Active LTS 메이저 내 최신 마이너/패치 | `mise.lock` |
| `rumdl` | `0.2.54` | Case 1 (패치 준수) | 0.x 단계 Markdown 포맷팅 churn 방지를 위해 패치만 허용 | `mise.lock` |
| `lefthook` | `2.1.10` | Case 2 (마이너 준수) | v2 메이저 호환성 유지 하에 하위 호환 마이너 업데이트 | `mise.lock` |
| `npm:@biomejs/biome` | `2.5.6` | Case 1 (패치 준수) | 린트/포맷 규칙 변경으로 인한 대량 diff 방지 | `mise.lock` |
| `npm:rulesync` | `40.2.0` | Case 3 (메이저 준수) | 프로젝트 호환성이 검증된 안정 릴리스 라인 유지 | `mise.lock` |
| `npm:skills` | `1.5.23` | Case 4 (최신 안정) | 외부 스킬 저장소·프로토콜 연동을 위한 최신 안정 지향 | `mise.lock` |

- **Setup 원칙 (Zero Drift):** 어떤 정책 케이스이든 `mise run setup`은 항상 선언된 exact pin과 `mise.lock`의 사전 확인된 URL·체크섬을 100% 그대로 재현합니다. 네트워크 resolver를 통한 임의의 버전 승격은 발생하지 않습니다.
- **Update 원칙 (Bounded Update):** `mise run update`만 선언된 정책 범위 내에서 최신 버전을 탐색하고 lockfile/manifest를 갱신합니다.
- **현재 구현 상태:** `mise.lock`이 활성화되어 7개 CLI 도구의 7개 플랫폼(Linux, macOS, Windows) 바이너리가 잠금 관리되며, 현재는 모든 CLI 도구의 허용 범위를 길이 0(Exact Pin)으로 유지합니다.

Setup은 policy/lock을 갱신하지 않습니다. Update는 `mise.toml`, `pyproject.toml`, `.python-version`, `uv.lock`, `mise.lock`의 기존 미커밋 변경을 사전 차단하며, 갱신된 `uv.lock` 및 `mise.lock`을 자동 commit하거나 rollback하지 않습니다. 별도 Rulesync/Skill 파일의 기존 미커밋 변경은 차단하지 않지만 작업 도중 감지한 예기치 않은 policy/lock 변경은 중단합니다. 모든 동시 수정 경쟁을 차단하는 sandbox는 아닙니다.

### Installation scope and recovery

- 기본 setup이 수행할 수 있는 쓰기 대상은 **mise-managed tool/cache**와 repository **`.venv`**입니다. 실행 전 사용자 설치 허가는 [Development Environment](../../development/development-environment.md)가 소유합니다. 네트워크·공유 cache 접근은 필요할 수 있습니다. Python 자동 다운로드는 끄며 interpreter 누락 시 최초 준비를 명시적으로 수행합니다.
- `UV_PROJECT_ENVIRONMENT`가 다른 환경을 가리키거나 `.venv`/package·실행 디렉터리가 외부 symlink/junction이면 차단합니다. 활성 foreign venv와 project/config override는 child process에서 제거합니다.
- Native tool은 exact request로 경로와 실행 버전을 확인합니다. npm CLI는 설치된 package metadata에서 bin을 찾고 pinned Node로 실행하여 Windows `.cmd` shim을 직접 실행하지 않습니다. Package 내부의 동작까지 sandbox로 제한하지는 않습니다.
- Node 실패 시 npm 단계는 건너뛰되 uv/Python 등 독립 단계는 계속합니다. 필수 실패는 `FAILED`/`BLOCKED`, nonzero입니다. 필수 core 검증이 전부 통과하면 `READY`, exit 0이며 별도 선택적 연동은 `excluded and not verified`로 명시합니다. 선택적 설치를 시도하다 실패한 상태를 exit 0으로 숨기는 경로는 없습니다.
- 같은 checkout의 동시 실행은 `.tmp/bootstrap.lock`으로 차단합니다. 정상 종료·Ctrl-C는 자기 lock만 해제합니다. 강제 종료로 남은 lock은 해당 process가 끝났는지 확인한 뒤 수동 정리합니다. 다른 worktree의 공용 mise cache는 native manager 책임이며 HOME 설치를 병렬 실행하지 않습니다.
- 실패하면 표시한 native 명령을 직접 점검하고 policy/lock diff를 보존한 채 setup을 재실행합니다. 사용자 파일 삭제, `git clean`/reset, hook 덮어쓰기, 전역 설정 변경은 하지 않습니다.

`--dry-run`은 **runner의 read-only 계획**이지 resolver 후보 preview나 전체 host 무변경 보장이 아닙니다. Mise config 평가·trust와 uv의 interpreter/cache probing은 script 이전 경계입니다. 그 경계까지 제외하려면 이미 설치된 Python으로 script를 직접 실행합니다. `mise run --dry-run setup`은 mise task 자체의 preview이므로 bootstrap의 안전 진단과도 다릅니다.

### Optional integrations

기본 setup/update는 Rulesync 설치·projection, 외부 native Skill installer, Git hook 설치를 실행하지 않습니다. 기존 source/대상·symlink/custom 파일·Git shared config를 검토한 뒤 아래 경로를 **별도로** 실행합니다.

```bash
rulesync install --frozen
rulesync generate --dry-run
# 출력 대상과 기존 파일을 검토한 뒤 rulesync generate
mise run skills-sync
# core.hooksPath와 기존 hook을 검토한 뒤 lefthook install
```

외부 Skill dependency의 lock과 source-native 동기화 경계는 [skills CLI](skills-cli.md)를 따릅니다. `skills-sync`는 기존 명시적 실행 경로이며 HOME 쓰기·native installer의 권한을 sandbox로 제한하거나 설치 결과를 보증하는 새 기능이 아닙니다.

**검증 범위:** Windows에서 mise 인자 전달, runner의 격리 fixture·symlink/junction·부분 실패 테스트를 확인했습니다. 로컬 wheel만 제공하는 실제 uv fixture에서 범위 밖 `2.0.0` 대신 허용된 `1.1.0` 선택, sync/check와 setup 재실행의 lock 보존도 확인합니다. 실제 Windows 임시 snapshot에서 기존 exact tool cache를 사용해 새 `.venv` setup과 warm 재실행이 모두 `READY`/exit 0이며 policy/lock hash와 비어 있는 임시 HOME이 유지됨을 확인했습니다. 이는 clean-machine/cold tool-cache 설치나 OS sandbox 검증이 아닙니다.

Linux/macOS/WSL host smoke와 사용자 HOME installer 실행은 아직 미검증입니다.

Promptfoo처럼 Node runtime이 필요한 기존 command는 mise environment에서 실행합니다.

```bash
mise exec -- npm run eval:promptfoo:mols-loops
```

## Shared and local environment

공통 실행 환경은 [`mise.toml`](../../../mise.toml)의 `[env]`가 소유하며 Python에 UTF-8을 적용합니다. Git 설정은 mise나 설치 wrapper에서 덮어쓰지 않습니다. Rulesync dependency는 GitHub transport로 설치하므로 Git 임시 clone의 LF 보정이 필요하지 않습니다. 설치 명령과 API 인증은 [Rulesync](rulesync.md#repository-local-installation)를 따릅니다.

PC별 설치 경로만 Git에서 제외된 `mise.local.toml`에 둡니다. 예를 들어 Windows에서 Git Bash를 PATH에 추가해야 한다면 다음처럼 설정합니다.

```toml
[env]
_.path = ["C:/Program Files/Git/bin"]
```

Git에서 제외된 로컬 파일은 PR로 자동 변경하지 않습니다. 각 PC에서 기존 `PYTHONUTF8` 중복과 이전 LF 보정 전용 `GIT_CONFIG_*` 값을 검토한 뒤 불필요한 항목만 제거합니다. PC별 PATH, 인증용 Git 설정과 상위 프로세스 환경은 보존하고 Git 전역 설정은 변경하지 않습니다. Rulesync의 로컬 설정 정리는 [Rulesync](rulesync.md#repository-local-installation)를 따릅니다.

## Official sources

- [mise configuration](https://mise.jdx.dev/configuration.html)
- [mise tools and backends](https://mise.jdx.dev/dev-tools/backends/)
- [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
- [mise tasks](https://mise.jdx.dev/tasks/)
- [mise CI](https://mise.jdx.dev/continuous-integration.html)
- [uv Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [uv projects](https://docs.astral.sh/uv/concepts/projects/)
- [rumdl installation](https://github.com/rvben/rumdl#installation)
- [Lefthook with mise](https://lefthook.dev/installation/mise/)
- [Lefthook install](https://lefthook.dev/usage/commands/install/)
- [Biome configuration](https://biomejs.dev/reference/configuration/)
- [Biome CLI](https://biomejs.dev/reference/cli/)
- [Rulesync](rulesync.md)
- [skills CLI](skills-cli.md)

Version-dependent behavior는 `mise.toml`의 pin과 current official source를 함께 확인합니다.
