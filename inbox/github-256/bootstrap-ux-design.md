# Bootstrap UX — 실행 가능한 설계 인계

> PR #256 · 2026-10-24 · 제안된 UX/implementation handoff, **아직 미구현**. 근거와 미확인 사항: [심층 조사](bootstrap-deep-research.md). 기존 명세: [development-environment-bootstrap-spec.md](development-environment-bootstrap-spec.md). 정확한 옵션 지원은 사용 중인 mise/uv 버전에서 검증한다.

## 사용자 약속

- **Onboarding:** 처음 clone한 개발자는 무엇이 설치되고 무엇이 설치되지 않는지 알 수 있으며 mise 사전 설치 후 하나의 setup 명령으로 작업을 시작한다.
- **Daily:** 같은 setup을 여러 번 호출해도 정책/lock이 갱신되지 않고, 충족한 조건은 불필요하게 다시 설치하지 않으며, 종료 시 준비 상태를 알 수 있다.
- **Update:** 명시적인 update 요청에만 사전 선언한 허용 범위 안의 최신 버전을 선택하고 lock diff·검증 결과를 보여준다.
- **Recovery:** 실패한 의존 단계는 건너뛰어도 독립 단계는 끝까지 수행한다. 필수 조건의 실패를 exit 0으로 감추지 않는다.
- **Safety:** 설치 범위와 영향이 크면 사전에 드러낸다. OS/global/user-home installer를 비승인 상태에서 실행하지 않는다.

## 최소 공개 진입점

| Command | 의미 | 기대 상태 |
| --- | --- | --- |
| `mise run setup` | locked reconcile, 안전하게 필요한 설치·복구 | READY / DEGRADED / BLOCKED |
| `mise run update` | 선언된 허용 범위 안에서만 lock 재해석 및 명시적 설치·검증 | UPDATED / UNCHANGED / BLOCKED |
| `mise run setup:check` (가칭) | read-only 진단, 기존 `mise run check`와 비교 후 필요할 때만 신설 | READY / DEGRADED / BLOCKED |
| `mise lock --bump --dry-run`, `uv lock --upgrade --dry-run` | 각 native resolver의 update preview | 계획 정보, 파일 수정 없음 |

공식 진입점은 두 개로 유지한다. `setup:check` 또는 `update:preview`는 기존 command와 구분되는 가치가 검증될 때만 추가한다. 별도 설치 매니저, 자체 global version schema, 신규 `bootstrap.sh`를 기본 도입하지 않는다.

**README의 첫 화면에 필요한 내용:** (1) mise 설치 확인, 미설치 시 공식 안내 (2) repository root에서 `mise run setup` 실행 (3) 실패 시 출력 마지막의 next action. Git/Bash/Windows 요구사항은 실제 지원 범위를 확인해 표기하고, 다운로드된다고 단정하지 않는다.

## 1. Setup 흐름 (reconcile, not upgrade)

```text
mise entrypoint exists?
  No -> minimal official prerequisite instructions (cannot self-start)
  Yes
    -> preflight root/config/lock/permissions/network expectations
    -> native locked mise tools install, only authorized scope
    -> uv locked Python/environment sync
    -> Rulesync frozen install -> authorized projection
    -> optional user-home Skill install? explicit opt-in
    -> Git hooks? inspect existing hook state, protect customized state
    -> verify core readiness, summarize all skipped and failed work
```

Preflight는 모든 파일과 도구를 다시 설치하기 위한 작업이 아니다. 위험한 충돌을 선행 발견하고, 가능한 native read-only check를 사용해 현재 상태를 확인한다. 이미 설치되어도 검증하지 않은 결과를 ready라고 단정하지 않는다.

**오프라인:** 진단, 로컬 캐시·lock에 있는 기능은 가능한 만큼 진행하되 cache miss를 필수 준비 완료로 포장하지 않는다. locked installation은 offline을 의미하지 않는다.

## 2. Update 흐름 (explicit, bounded resolution)

```text
user invokes update
  -> inspect dirty lock/manifests and current policy
  -> preview available candidate changes (optional, read-only)
  -> reject constraint expansion or unapproved floating ref movement
  -> native resolve: write lock plus required sidecars
  -> inspect changed paths and versions
  -> install allowed locked result
  -> version/feature checks -> summarize updated/unchanged/skipped
```

Exact pin은 update해도 그대로다. Rulesync source Git ref, native Skill lock revision은 별도 승인된 정책 없이 최신으로 이동하지 않는다. 기존 미커밋 lock/sidecar 또는 충돌하는 사용자 파일은 덮어쓰지 않는다. 여러 lock owner 사이에는 자동 원자성/rollback이 없으므로 중간 실패 시 **이미 변경된 파일과 적용 범위**를 정확히 출력한다. `git reset`/`stash`/`clean`을 대신 실행하지 않는다.

## 설치 권한 모델

| 위치·소유권 | 기본 정책 | UI 대응 |
| --- | --- | --- |
| mise/Git/Bash 같은 host prerequisite | OS/global 자동 설치 금지 | 공식 설치 방법 안내 후 재실행 |
| mise-managed tool cache | repository가 명시적으로 승인한 범위만 자동 | 버전과 설치 cache 변경을 표시 |
| uv managed Python / 프로젝트 `.venv` | 사전에 선언된 설치 범위만 자동 | Python 다운로드 가능성, network/cache 표시 |
| Rulesync-generated project files | 상태를 확인하고 쓰기 | 미커밋 충돌 시 중단, 생성 파일 고지 |
| Git hooks, custom `core.hooksPath` | 변경 전 조회, 기존 설정 보존 | 충돌 시 opt-in 또는 수동 안내 |
| upstream Skill installer/user HOME | 기본 setup에서 자동 실행하지 않음 | `mise run skills-sync` 명시 실행 또는 별도 opt-in |
| OS package manager, sudo, 전체 머신 bootstrap | 권한 밖 | 안내만; `mise bootstrap`으로 암묵 확대 금지 |

**동의 UX:** 이미 승인된 project-local 설치까지 매번 묻지 않는다. 사용자 공유 영역에 대한 새 side effect만 opt-in. non-TTY/CI는 prompt 대신 명시적인 skip/block; global `MISE_YES`를 위험 설치 권한으로 해석하지 않는다. Mise task의 `confirm`은 일반 `depends` 이후에 발생할 수 있으므로 승인 이전 실행 가능성도 설계·테스트한다.

## 종료 상태 및 사용자에게 보이는 결과

| 상태 | Exit | 정의 |
| --- | --- | --- |
| READY | 0 | 필수 기능·검증 모두 준비 |
| DEGRADED | 0(제안) | **선택적** 구성만 빠졌고 필수 workflow는 작동 |
| BLOCKED | nonzero | 필수 의존성·승인·locked artifact·network가 부족 |
| FAILED | nonzero | 실행/검증 실패, 보존된 부분 상태와 다음 행동 출력 |
| UPDATE_NOOP | 0 | 범위 내 변경할 버전·lock이 없어 unchanged |

선택 사항이 필수로 승격되면 DEGRADED 대신 BLOCKED. `mise run` 자체가 시작 전에 실패하면 wrapper의 요약을 표시할 수 없으므로 README/prerequisite 안내와 native stderr도 UX의 일부다.

**제안 출력 예시이며 실제 실행 로그가 아님:**

```text
$ mise run setup
Checking environment ...
  [ready]     uv locked
  [ready]     Python dependencies (.venv)
  [unchanged] Rulesync projection
  [skipped]   External Skill (user-home install needs opt-in)
  [ready]     Git hooks

Result: DEGRADED — core development environment ready.
Next: mise run skills-sync to opt in to external Skill installation.
```

```text
$ mise run update
  [updated]   Node 24.x: old -> new (illustrative placeholders)
  [unchanged] uv exact pin; not eligible
  [skipped]   External Skill source; no approved update policy

Result: UPDATED, verification passed.
Changed: mise.lock, sidecars (if created), uv.lock (if changed)
Next: review lockfile diff before committing.
```

실제 값이 없으면 출력에 가짜 버전이나 duration을 넣지 않는다. 첫 피드백은 빨리 주고, 요약은 짧게. 장시간 task의 시작·종료를 식별할 수 있게 한다. 상세 native output은 오류나 verbose 요청에서 접근 가능하게 한다. CI/non-TTY에선 spinner/color/prompt 없음, 오류는 stderr, 종료 코드는 실제 readiness를 반영한다.

## 의존성·동시성 규칙

- `rulesync generate`는 성공한 `rulesync install --frozen` 이후에만 수행한다.
- `uv sync`와 다른 tasks의 `.venv` 동시 쓰기, upstream native Skill installer와 동일 HOME 경로의 동시 설치를 기본 허용하지 않는다.
- `mise run --continue-on-error`는 실패한 의존 task까지 실행할 수 있다. 기본 `depends`는 실패 시 전체 실행을 중지할 수 있다. 따라서 둘 중 어느 것도 그대로 **독립 단계만 계속** 계약을 충족하지 않는다.
- 작은 orchestration/result aggregator를 필요한 범위로만 구현하거나 독립 task를 안전하게 묶어 실행한다. 뒤늦게 종속 task가 실패하지 않도록 prerequisite edges를 명시한다.
- Native `skip_if`의 성공(0)은 작업 성공으로 간주되므로 실제 기능 상태를 확인할 수 없는 skip predicate를 쓰지 않는다. Timestamp/outputs cache는 mutable user-home/hook 상태의 readiness 검증으로 대체하지 않는다.
- 먼저 실제 elapsed/failure를 측정하고, 유효성이 확인된 독립 작업만 병렬화한다.

## 테스트 매트릭스

| ID | 상황 | 기대 기준 |
| --- | --- | --- |
| U01 | 빈 환경 첫 setup | 허용된 관리 범위에 설치, 핵심 dev 기능 검증 |
| U02 | warm setup 재실행 | lock/manifest 변경 0, 불필요한 설치 및 version lookup 최소 |
| U03 | mise 미설치 | self-bootstrap 실패를 안내, 전역 설치 무단 실행 금지 |
| U04 | Git/Bash 없고 uv는 사용 가능 | Python 독립 작업 완료, native Skill 단계 skip/block |
| U05 | manager cache miss / network unavailable | 영향을 받는 필수 step만 blocked, cache 가능한 독립 작업 진행 |
| U06 | 기존 사용자 hooks/Skill path 있음 | 무단 덮어쓰기 0, opt-in·복구 안내 |
| U07 | dirty lock/manifest | 파일 보존, 제한된 사전 진단 후 충돌 출력 |
| U08 | 허용 범위 내·밖 release 동시 존재 | 최신 허용 버전만 선택 |
| U09 | exact pin, mutable Git source | 무단 승격 0, 사유 표시 |
| U10 | npm transitive sidecar 누락 | locked install의 정확한 실패 원인·재생성 절차 |
| U11 | partial installer failure, interrupt | partial state를 보존하고 재실행으로 안전 복구 |
| U12 | non-TTY / CI | prompt/animation 없음, exit code 정확 |
| U13 | cold vs warm cache | baseline wall time/network calls/install count 비교 |
| U14 | Linux/macOS/Windows | 실제 지원 플랫폼만 pass, 미검증은 unknown |
| U15 | update 도중 일부 lock만 변경 | 자동 원복 가장 금지, 변경된 파일과 복구 경로 설명 |
| U16 | source-native malicious/mutable installer | 승인·integrity gate 미충족이면 실행 차단 |

검증 단계: **정적 정책 검사 → mocked tools 및 temp HOME → 격리된 실제 tool-manager 테스트 → clean-machine 실측**. 시스템 전역 변경 테스트는 임시 환경/컨테이너로 격리하며 실제 사용자 머신에서 미리 위험한 명령을 실행하지 않는다.

## 최적화 지표와 실험

현재 실행 시간 baseline은 측정하지 않았다. Cold setup / warm no-op / lock changed / offline / failure retry에서 **wall time, 실제 installer 호출 수, remote request, tracked diff, 준비 실패 수, 추가로 입력해야 한 명령 수, 출력의 recovery completeness**를 수집한다.

수치 목표를 임의로 설정하지 않는다. 최우선 불변 조건은 **무단 전역 변경 0, setup의 lock 정책 변경 0, 범위 밖 version 변경 0, 필수 실패의 거짓 성공 0**이다. 개선 전후 측정 후 P50/P95 목표를 설정한다. native cache/sources optimization이나 병렬화는 correctness를 먼저 증명해야 채택한다.

## 최신 버전 해석 시 주의사항

mise에서는 도구마다 설정한 허용 범위 외에도 릴리스 경과 시간(minimum_release_age), prerelease 허용 여부, backend 지원이 후보 선택에 영향을 준다. 공식 설정에 따르면 여러 backend의 minimum_release_age 기본값은 24시간이다. 따라서 최신은 단순히 현재 공개된 최고 버전이 아니라 **사전 승인된 모든 선택 정책을 만족하는 최신 후보**로 정의해야 한다. 출시 직후 버전까지 원하는지, 안전성 지연을 허용할지는 실제 버전 범위를 정할 때 함께 결정한다. [공식 설정](https://mise.jdx.dev/configuration/settings.html#minimum_release_age).

최신 mise 문서에 존재하는 머신 관리용 `mise bootstrap`과 이 PR의 프로젝트 `mise run setup`은 책임이 다르다. CI 설정에는 mise 2026.9.2가 지정되어 있으므로, 최신 mise 문서의 기능을 사용할 때는 version skew도 확인해야 한다.

## 구현 우선순위

- **P0:** locked reconcile, opt-in/global boundary, stage dependency/failure behavior, update version constraints + npm sidecars, state-change collision protection.
- **P1:** preflight, concise one-command onboarding, summary/next action, read-only diagnosis, non-TTY behavior.
- **P2:** warm no-op, safe parallelism, optional preview UX, task timings and performance baseline.
- **보류:** 전체 머신 `mise bootstrap`로 통합, 별도 범용 프레임워크, 자동 사용자 홈 cleanup, background update.

실제 기능 검증 전 남은 주요 의사결정: 현재 mise의 lockfile/sidecar 지원 범위와 `uv 0.12.1` 호환, `lockfile=true` 자동 rewrite 경계, Git hooks 충돌 탐지, 외부 Skill update policy, Windows shell support. 이 문서는 명세 근거가 아니라 실험과 구현을 위한 가설/acceptance handoff다.
