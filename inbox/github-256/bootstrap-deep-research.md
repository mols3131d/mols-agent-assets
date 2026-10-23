# Developer bootstrap — 심층 조사와 설계 결정 근거

> PR #256 · 2026-10-24 · **연구 아티팩트(제안), 현재 구현 계약이 아님**. 조사 기준: `mols/feat/dev-environment-bootstrap` @ `a965fbc6427b612e540c78b1feb5b3befe4a4c80`. 후속 설계: [UX 설계 인계](bootstrap-ux-design.md). 기존 [Skill 연구](bootstrap-skill-research.md)와 [부트스트랩 명세](development-environment-bootstrap-spec.md)는 별도 책임이다.

## Executive findings

가장 효과적인 방향은 **`mise`를 도구/태스크 오케스트레이터로 유지하고, `uv`를 Python 환경 owner로 유지하면서, `setup` / `update` / read-only diagnosis를 명확히 분리**하는 것이다. 최적화의 중심은 더 큰 설치 프레임워크가 아니라 **평상시 no-op, 필요한 작업만 실행, 불필요한 네트워크·lock 변경 방지, 실패 후 한 번의 재실행으로 복구 가능, 해석하기 쉬운 출력**에 있다.

확인된 중요 함정:

1. `mise run --continue-on-error`는 실패한 task에 의존하는 task까지 시작할 수 있으므로 dependency-aware graceful degradation의 안전한 구현 수단이 아니다. 일반 `depends`는 실패 시 즉시 중단한다. 독립 작업을 끝까지 수행하려면 필요한 범위에서 실행 orchestration과 결과 집계를 별도로 설계하거나 안전한 분리 실행을 선택해야 한다. [R3][R4]
2. `mise.lock`은 tools version뿐 아니라 현재 npm/PyPI backend에서는 **transitive dependency sidecar**를 포함할 수 있다. `mise.lock`만 커밋하면 재현성이 깨질 수 있다. npm 도구는 embedded aube 방식이고 Node는 주로 CLI 실행에 필요하다. [R1][R5]
3. `mise lock --bump`는 명시한 request의 허용 범위 내 version resolution만 바꾸지만 `mise upgrade --bump`는 request를 변경한다. `lockfile = true`는 자동 write도 허용한다. **setup이 tracked lock을 불변으로 유지한다는 조건과 settings가 충돌하지 않는지 검증**해야 한다. [R1]
4. `uv sync`와 `uv run`은 기본 동작에서 lock 갱신이 가능하다. `--locked`는 metadata drift에서 실패하며 `--frozen`은 drift 확인을 생략한다. `uv sync`는 `.venv`의 불필요 패키지를 제거한다(프로젝트 격리 범위 안의 의도된 변경이지만 no-op은 아니다). [R6]
5. Python interpreter도 uv가 자동 다운로드할 수 있다. 설치/네트워크 경계는 Python package뿐 아니라 managed Python에도 적용된다. [R7]
6. `mise bootstrap`은 **머신 전체** packages/files/services/repositories/dotfiles/tool 설정을 관리하는 native command로, 계획·상태 조회·follow-up 기능이 있지만 **파괴적인 변경도 가능**하다. 현재 repository-local 도구 준비 요구와는 목적/권한이 다르다. [R8]
7. CLI UX는 실행 전 가시성, 진행 표시, 명확한 stdout/stderr와 exit status, 미사용 TTY/CI 대응, 복구 안내를 중요하게 본다. 긴 로그보다 최종 액션 요약이 효과적이다. [R9]

## Research Run 1 — repository baseline / failure decomposition

**Goal.** 최초 설치와 개발 중 반복 실행에서 현재 발생 가능한 작업·실패·부작용을 항목별로 분해한다.

**Research evidence.** [mise.toml](../../mise.toml)은 다음 exact pin을 선언한다: uv 0.12.1, node 24.19.0, rumdl 0.2.54, Lefthook 2.1.10, Biome 2.5.6, Rulesync 16.24.1, skills CLI 1.5.23. `setup`은 아래 단계들을 순서대로 실행한다.

```text
mise auto-install (task runner의 선행 동작을 확인해야 함)
  -> uv sync --all-groups
  -> rulesync install --frozen
  -> rulesync generate
  -> uv run python scripts/agent_assets/skills_sync.py
  -> lefthook install
```

`skills_sync.py`는 `skills-lock.json`에 고정된 외부 Skill source를 사용자 cache에 fetch/checkout한 다음 upstream `install.sh`를 실행한다. Git/Bash 사전 검사는 전체 pipeline 앞이 아니라 이 단계의 실행 전후에 이루어진다. `--dry-run`은 원본/adapter 계획을 인쇄할 뿐, 실제 설치 상태나 설치 대상의 불변성까지 확인하지 않는다. 잠금 파일의 `computedHash`는 현재 wrapper의 무결성 검증에 사용되지 않는다. 유효성이 보장되지 않은 upstream tag/ref를 fetch해 실행한다. 이것은 **현재 구현에 대한 정적 관찰**이지 사고가 발생했다는 주장과 다르다.

현재 `lefthook install`은 Git hooks를 변경하며 `rulesync generate`는 프로젝트 파일을 생성한다. `uv sync --all-groups`는 dev와 test 그룹 설치를 모두 포함한다. `mise run setup`이 미설치 도구를 선행 설치하는 방식도 `run_auto_install` 설정에 영향받는다. `mise` 자체가 없으면 이 진입점을 사용할 수 없다.

**Failure map.**

| 사건 | 현재 동작 또는 확실한 위험 | UX 영향 | 개선 후보 |
| --- | --- | --- | --- |
| mise 미설치 | 진입점 호출 불가 | 첫 시작 차단 | 짧은 prerequisite 안내, 설치 책임 표시 |
| Git 또는 Bash 미설치 | Skill sync 후반부에서 발견 가능 | 선행 작업 이후 실패 | 시작 단계에서 모든 선택적/필수 prerequisite 탐지 |
| uv Python 다운로드 | 관리 환경에 network/system effect | 오프라인 원인 불명 | 관리 interpreter의 설치 권한·다운로드 안내 |
| lock drift | `uv sync`가 lock 변경 가능 | 의도치 않은 git diff | locked reconcile, 의도적 update만 resolve |
| Rulesync source/install 실패 | 후속 단계 중지 | 부분 셋업 가시성 낮음 | 독립 단계 계속·요약, 실패 의존 단계 skip |
| 외부 Skill `install.sh` | user-level vendor 경로 변경 | 사용자 환경 예상 밖 변경 | opt-in 분리, manifest/source integrity 확인 |
| Lefthook/custom hooks 충돌 | 사용자 Git 설정의 일부가 변경될 수 있음 | 세션/프로젝트별 부작용 | hooks 상태 preflight, 안전성·복구 안내 |
| 중간 실행 중단 | 여러 managed tree가 부분 설치 상태일 수 있음 | '어디까지 됐지?' | 반복 실행 후 reconcile, 단계별 상태 보고 |

**Review 1.** '전역 도구는 다 건너뛴다'는 분류가 너무 거칠다. mise tool cache, uv-managed interpreter, project-local `.venv`, native Skill installer, OS packages는 설치 **범위와 복구 소유권**이 다르다. 구체적인 사용자 동의 범위를 먼저 선언하되, 해당 범위 안의 tool-cache installer까지 무조건 수동화하는 것은 onboarding UX를 해친다.

## Research Run 2 — tool behavior, update/lock/caching

**Goal.** 재현성과 최신 허용 업데이트, 부분실패·속도 최적화를 동시에 만족시키는 native mechanism 조사.

| Surface | 확인한 upstream 기능 | 적용 시 함정 |
| --- | --- | --- |
| mise tools | `mise lock`, `mise lock --bump --dry-run`, `mise install --locked`, `mise outdated` | `lockfile=true` 자동 갱신, npm/PyPI sidecar, 플랫폼별 URL, 설치 캐시 무결성 비보장 [R1][R2] |
| mise task graph | `depends`, `wait_for`, `depends_post`, ordered `run` steps, `mise tasks deps` | 전부 병렬화하면 실제 순서 의존을 깨고, `--continue-on-error`는 실패 dependency도 진행 [R3][R4] |
| mise task UX | `usage`, `confirm`, `--dry-run`, `--skip-tools`, output style, task timings | `confirm` 전에 `depends`가 실행될 수 있음. confirm을 side-effect 없는 최초 경계에 둬야 함 [R4][R10] |
| mise caching | `sources` + `outputs` freshness와 experimental artifact cache | 성공 marker/freshness가 실제 user-level 설치 상태 drift를 검증하지 못함. mutable installer 결과에 무분별한 cache/skip_if 금지 [R11] |
| uv | `uv lock --upgrade --dry-run`, `uv sync --locked --all-groups`, `--offline`, managed Python setting | `--offline`은 cache 미보유 파일을 설치하지 못함. `--no-sync`는 환경 정확성 보장 안 됨 [R6][R7] |
| uv cache | registry/direct URL/Git cache, concurrent locking, same-FS link 효율 | `uv cache clean`은 일반적인 UX 최적화가 아니라 cache 제거. 임의 cleanup 하지 않음 [R12] |
| 외부 source | Rulesync frozen install, Skill native installer | Git moving refs/tag와 vendor installer는 semver package resolver와 같지 않음. 잠금 정보와 설치 산출물 무결성 별도 확인 |

**재현성의 층위.** (a) 버전 request가 통제됨, (b) commit된 lock에 concrete version/graph 기록, (c) 설치 시 lock을 사용, (d) 설치된 바이트/동작 검증. (b)를 달성했다고 (d)까지 확보됐다고 주장하지 않는다. mise lockfile 문서는 설치되어 있는 파일을 lockfile로 검증할 수 없고 npm lifecycle script 등 환경 영향이 남는다고 명시한다. [R1]

**범위 정책.** `node = "24"` 같은 bounded prefix는 허용 범위이며 `node = "24.19.0"`은 exact pin이다. 동일한 정책 파일을 `mise upgrade --bump`, 임의 `@latest` 호출, Python dependency constraint 재작성으로 우회하지 않는다. npm tool의 transitive graph를 함께 관리하지 않으면 top-level pin만으로 '완전 고정'이라고 말할 수 없다.

**Review 2 — 반증.** "lockfile이 있으면 설치가 반드시 오프라인/완전히 동일"이라는 주장은 틀리다. 다운로드 cache가 없거나 플랫폼별 artifact가 없으면 network가 필요할 수 있다. npm/PyPI sidecars가 없으면 locked install에서 오류가 날 수 있다. 또한 `mise bootstrap`은 프로젝트 셋업의 대체재가 아니라 host-level 별도 권한/수명주기의 기능이다.

## Research Run 3 — 사람 중심 UX와 대안 평가

**Goal.** Warm no-op, 실패 복구, 업데이트 신뢰도를 높일 수 있는 경험 설계 선택지를 비교한다.

### 사용자 여정

| 상황 | 사용자가 알고 싶은 질문 | 권장 상호작용 |
| --- | --- | --- |
| 첫 clone | 무엇이 준비되어야 하는가? 내가 뭘 허용하는가? | 한 화면 prerequisite + `mise run setup`, 미리 예상되는 side effect 설명 |
| 이미 셋업됨 | 업데이트 없이 빠르게 끝나나? | cached/unchanged summary + 추적 가능한 no-op |
| 하루 뒤/다른 branch | 잠겨 있는 버전이 달라졌나? | locked reconcile, 변경된 대상만 설치, git diff 비변경 |
| 업데이트 원함 | 실제 어떤 버전이 어디까지 올라가나? | read-only preview → `mise run update` → lock diff → verify |
| 인터넷 끊김 | 설치할 수 없는 것이 뭔가? | 캐시 재사용 가능한 부분 처리, 네트워크 요구 건별 기록 |
| 필수 도구 누락 | 다른 작업도 멈추나? | dependency graph에서 안전한 독립 작업 지속, blocked task는 skip |
| 권한 필요한 변경 | 내가 동의하지 않은 파일/전역 설치가 일어나나? | 영향 scope 고지, interactive opt-in 또는 clear manual path |
| 중간 실패/재실행 | 어디부터 다시 시작하나? | safe retry, 상태 요약과 단일 재실행 명령 |
| CI/자동화 | 프롬프트 없이 의미 있는 종료 코드가 나오는가? | no prompt, nonzero for mandatory gap, diagnostics on stderr |

### 3가지 설계안 비교

| 설계 | 초기 UX | 장기 UX/유지비 | 결론 |
| --- | --- | --- | --- |
| 현행 `mise run setup` 단일 순차 배열 | 가장 간단 | update 부재, 전체 중단, global 부작용 숨김 | 유지 불가(동작은 확장) |
| mise task graph + native lock tooling + 얇은 preflight/report | 진입점 그대로 | 부분실패/diagnosis를 좁은 계약으로 해결 | **기본 권고** |
| 대형 Python/shell bootstrap orchestrator 또는 full-machine `mise bootstrap` 전환 | 초기 설치를 하나로 포장 | 권한/구현/이식성·중복 owner 증가 | **기본 도입 기각**; 증거가 있으면 재검토 |

Dev Containers, Devbox/Nix는 호스트 동등성/OS 종속 패키지가 필요할 때 고려할 수 있는 더 강한 격리 대안이지만 도구 자체를 설치하고 팀 워크플로를 바꿔야 한다. 현재 요구사항이 tool/project bootstrap임을 고려하면 바로 마이그레이션하는 것은 YAGNI다. [R13][R14][R15]

### 성능 최적화 순서

1. **먼저 실제 측정.** 냉간 설치, 캐시가 있는 재실행, 새 branch 진입, lock 변경 이후, 네트워크 불가에서 elapsed time·install count·network fetch·tracked file write·경고 수를 측정. 현재 baseline 시간은 측정하지 않았다.
2. **불필요한 작업 제거.** `setup`에서는 version lookup/update 금지, 이미 충족된 범위/버전/verified integration은 no-op. `uv --locked`와 캐시 재사용을 우선.
3. **올바른 병렬성만 도입.** 진짜 독립적인 task만 병렬 진행. 동일 공유 cache/managed installation 또는 project generated path를 쓰는 task는 race를 확인한 뒤 허용.
4. **안정적인 증분 실행.** output 존재만으로 Git hooks, vendor installer 상태가 유효하다고 취급하지 말고 실제 state probe를 사용. Timestamp 기반 task freshness는 built artifact 같은 안정 출력에만 적용.
5. **최후에 다른 플랫폼/도구 교체 검토.** 추측한 speed improvement를 위해 다른 backend나 Docker/Nix로 즉시 이전하지 않는다.

### CLI 출력 원칙

- 첫 메시지는 **무엇을 확인/변경할지**를 한 문장으로 알린다. 진행 중 오래 걸리는 작업은 단계명과 현재 상태를 노출한다. 타이밍 수치는 측정한 경우에만.
- 상태는 `ready | unchanged | updated | skipped_optional | blocked_required | failed`처럼 구분하며, 실패 항목마다 **이유 / 영향 / 사용자가 바로 실행할 명령**을 붙인다.
- stdout은 간단한 사람이 읽는 기본 결과, 상세 로그는 문제 해결 시에만. stderr에 진단/오류. CI/non-TTY에서는 색·spinner·prompt 없음; 비밀값 redaction.
- 업데이트는 **lock diff 요약**을 먼저 보여주고, 사전에 승인한 범위 밖으로 움직일 가능성이 있으면 자동 진행하지 않는다.
- 언제나 "다음 작업"을 하나 또는 몇 개만 제시한다. 로그 경로·JSON output·색상 customization은 소비자가 실제로 필요한 경우만 추가한다.

**Review 3 — UX 반증.** "모든 단계마다 물어보면 안전하다"는 과잉 UX다. 선언된 project-local 설치는 batch하고 user-global/host write만 고지·승인한다. "매번 dry run 후 apply"가 강제되면 잦은 업데이트의 마찰이 커지므로 별도 preview command와 explicit update를 분리한다. "모든 오류가 nonzero"도 optional 사용자 기능의 누락 때문에 필수 개발 환경이 unusable인 것과 같게 취급하면 복잡하다. 종료코드는 **필수 준비 여부**, 상세 상태는 summary에서 표현한다.

## 최종 결정 / 확인해야 할 미해결 사항

1. 기존 `mise run setup`를 일상 진입점으로 유지하고 `mise run update`를 명시적 별도 command로 구현한다. 첫 사용에만 다른 bootstrap product를 요구하지 않는다.
2. `mise run doctor` 또는 `setup:check` 같은 **read-only 진단**은 필요하되 최종 이름·출력은 기존 `check` task와 충돌하지 않도록 결정한다. `mise doctor` native 결과도 재사용한다.
3. 실제 lock 설계는 `mise.lock`, 필요한 `.mise/locks` sidecar, `uv.lock` 범위까지 포함해 PoC를 먼저 수행한다. Project setup의 **lockfile mutation 금지** 계약과 `lockfile=true` 자동 갱신을 어떻게 양립시킬지 검증해 결정한다.
4. `setup`에서 외부 native Skill installer를 무인 실행하지 않는다. 기존 `mise run skills-sync` 경로는 보존하되 기본 실행에서 생략/opt-in 여부를 사용자가 선택할 수 있게 한다. Git Hook도 설치 위치/기존 사용자 설정을 확인한다.
5. 의존성 오류 처리와 마지막 summary는 **fail-dependency + continue-independent**에 충실해야 한다. 단순 `--continue-on-error` 사용 금지.
6. Node/npm tool 자체는 `mise` 소유, Python package는 `uv` 소유, Git/Bash 등 host prerequisite는 설치 안내 owner로 남긴다.
7. Scope별 권한, 상태 감지, cache/lock freshness, 권한 승인, error message/exit code를 독립 수용 테스트로 만든다.

### 아직 조사만으로 확정할 수 없는 점

- 실제 개발 머신의 OS 구성, 네트워크/방화벽, disk/shared-cache 환경, Git Hook customization, 설치 상태. 실제 로컬 실행은 하지 않았다.
- 사용하는 mise version, npm backend와 uv 0.12.1에서 모든 lockfile/sidecar 동작이 문서화된 **최신 버전**과 일치하는지. CI의 mise action 설정 버전은 2026.9.2이므로 필요한 기능 도입 전 버전 매트릭스 PoC가 필요하다.
- 현재 개발자 온보딩/반복 실행 시간의 수치. 성능 우선순위는 **측정 전 가설**이다.
- `computedHash`의 공식 생성 방식과 upstream native installer의 설치 결과 무결성. 검증식을 상상해서 구현하지 않는다.

## Source ledger

| ID | Source | 이 문서가 근거로 삼는 구체적 계약 |
| --- | --- | --- |
| R1 | [mise lockfile](https://mise.jdx.dev/dev-tools/mise-lock.html) | lock pin/update, --locked, 플랫폼 URL, npm/PyPI sidecars, installed cache 검증 한계 |
| R2 | [mise dev tools](https://mise.jdx.dev/dev-tools/) | outdated, upgrade, auto-update 범위와 권한 |
| R3 | [mise task architecture](https://mise.jdx.dev/tasks/architecture.html) | depends/wait_for/depends_post, 순차·병렬 execution |
| R4 | [mise running tasks](https://mise.jdx.dev/tasks/running-tasks.html) | --continue-on-error, --skip-tools, --dry-run, output |
| R5 | [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html) | embedded aube, node dependency, native dependency graph |
| R6 | [uv locking/sync](https://docs.astral.sh/uv/concepts/projects/sync/) | --locked/frozen, --upgrade, exact sync |
| R7 | [uv Python versions](https://docs.astral.sh/uv/concepts/python-versions/) | managed Python preference, automatic downloads |
| R8 | [mise bootstrap](https://mise.jdx.dev/bootstrap.html), [command reference](https://mise.jdx.dev/cli/bootstrap.html) | host-level authority, plan/status/follow-up, side effects |
| R9 | [CLI Guidelines](https://clig.dev/) | progress, errors, non-interactive, status, exit codes |
| R10 | [mise task configuration](https://mise.jdx.dev/tasks/task-configuration.html) | usage, confirm, skip_if, tool scope/output |
| R11 | [mise task caching](https://mise.jdx.dev/tasks/caching.html) | freshness vs artifact cache, cache mismatch/skip rules |
| R12 | [uv caching](https://docs.astral.sh/uv/concepts/cache/) | repeated dependency operations, cache locking/linking |
| R13 | [Development Container Specification](https://containers.dev/) | reproducible container-based dev environment 대안 |
| R14 | [Devbox](https://www.jetify.com/devbox) | Nix 기반 scoped environment 대안 |
| R15 | [Nix docs](https://nix.dev/) | declarative reproducibility 대안 |

## Handoff

UX 계약/실행 토폴로지/테스트 시나리오는 [bootstrap-ux-design.md](bootstrap-ux-design.md)에서 구체화한다. 이 연구는 **설계 근거가 확충된 상태**이며, 실제 `mise`/uv/Rulesync 세부 실행, 플랫폼별 호환성 및 성능 측정이 통과했다는 뜻은 아니다.
