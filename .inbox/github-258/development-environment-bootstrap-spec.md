# 개발환경 부트스트랩 구현 범위와 초기 설계

> 대상: [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258). 기존 [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)에서 프로젝트 구현 부분을 분리했습니다. 이 문서는 원래의 설계 계약과 후속 구현 범위를 구분하는 **비정본 작업 자료**다. **개발환경 구축·실제 설치 허가의 운영 정책 정본은 [Development Environment](../../docs/development/development-environment.md)**이며, 도구별 실행은 [mise 안내](../../docs/development/tooling/mise.md), 정확한 정책 값과 실행 동작은 `mise.toml`·native config/lock·스크립트가 소유한다.
>
> **최신 결정(2026-10-25):** 재사용 Skill은 설계·리뷰·구현 인계만 소유하며 구현은 일반 코딩 에이전트의 작업이다. 에이전트가 실제 설치·업데이트를 실행하려면 설치 대상·위치·영향을 안내하고 사용자의 명시적 허가를 받아야 한다. 한 번에 승인한 작업 범위 안에서만 재확인 없이 실행한다. [토론·인계](bootstrap-authorization-update-discussion.md).

## 구현 상태 — 2026-11-01

- `setup`/`update`를 [`development_bootstrap.py`](../../scripts/development_bootstrap.py)의 좁은 orchestration으로 연결했다. Setup은 exact CLI pin 설치·버전 검증과 locked uv sync, update는 기존 Python dependency constraints의 native resolution을 수행한다.
- `mise.lock`을 도입하고 `mise install --locked`를 사용한다. 네이티브 도구 4종의 7개 플랫폼별 아티팩트 URL·체크섬과 npm 도구 3종의 버전을 잠근다. npm 전이 의존성 그래프 전체를 잠근다는 뜻은 아니다. Tool prefix/range 확대는 도입하지 않았으며 모든 CLI exact pin과 외부 Asset revision을 유지한다.
- User HOME Skill·Git hook뿐 아니라 기존 projection의 소유권을 확정하기 어려운 Rulesync 설치·생성도 기본 실행에서 분리했다. 이번 PR의 기본 완료 범위는 **core toolchain/Python**으로 확정한다. Core 검증 통과는 `READY`이며 별도 연동은 `excluded and not verified`로 표시한다.
- 최초 mise/uv/Python은 사용자가 명시적으로 준비한다. Task pre-install을 끄고 인자를 단일 parser로 전달하며, runner는 외부 venv/junction·dirty update 입력·Git의 assume-unchanged/skip-worktree 입력·같은 checkout의 동시 실행을 차단한다. Python-only update의 변경 예외는 `uv.lock` 한 파일이며 예기치 않은 `mise.lock` 변경도 보존하면서 중단한다.
- 현재 구현 근거는 [`f70a8bd`](https://github.com/mols3131d/mols-agent-assets/commit/f70a8bd258895dbdd5616157131abb32b48d5836)다. Windows·WSL cold-cache 설치와 반복 복구·update의 실행 source 및 한계는 [후속 검증 기록](bootstrap-simplification-review-2026-11-01.md)에 구분해 남겼다.
- 아래의 범위·OS·성능·전체 연동 수용 조건은 **원래 목표**다. Deterministic test와 Windows·WSL CLI 검증을 전체 host bootstrap·다른 OS·native HOME installer·Skill runtime eval 성공으로 확대하지 않는다.

## Goal

하나의 개발환경 진입점에서 **처음 사용하는 머신의 설정**과 **개발 중 반복하는 유지·업데이트**를 지원한다. 업데이트 범위는 미리 선언하고, 실행기는 그 범위를 재정의하지 않고 최신 허용 버전을 선택한다. 자동 설치가 부적절하거나 불가능한 도구 때문에 독립적인 나머지 작업이 중단되지 않으면서도, 불완전한 환경을 성공으로 오인하지 않게 한다.

이 PR은 위 동작을 **실제 repository 부트스트랩으로 구현·검증**한다. 재사용 가능한 독립 Agent Skill `mols-dev-env-bootstrap-design`의 작성·검증은 **PR #256**이 소유한다. 이 PR은 Skill의 원본, 배포 route, Eval을 변경하지 않는다.

## 이번 PR의 수용 범위

리뷰 F1을 수용해 설계 문서만으로 완료 처리하지 않고 실행 코드·회귀 검증을 함께 반영한다. 현재 수용 범위는 다음과 같으며, 아래 초기 설계의 더 넓은 조건을 모두 달성했다는 뜻은 아니다.

- **필수 구현:** exact CLI pin reconcile·버전 검증, locked Python setup, 선언된 dependency constraint 안의 명시적 update, 경로·dirty lock 보호, 의존 단계 skip/독립 단계 지속, 실제 실패 exit와 안전한 재시도.
- **선택적 별도 연동:** Rulesync dependency/projection, native HOME Skill, Git hooks. 기본 core readiness와 분리하고 기존 명시적 실행 경로·사전 검토 안내를 유지한다. 기본 setup의 필수 기능을 조용히 생략하는 대신 설치 권한과 완료 계약을 이 범위로 명시한다.
- **허용 버전:** 현재 exact CLI pin과 `mise.lock`을 유지하며 tool update의 no-op도 정상이다. Python bounded update는 native uv resolver가 소유한다. CLI range 확대·자동 갱신과 npm 전이 의존성 잠금 도입은 별도 후속 과제다.
- **검증:** deterministic 회귀, 격리된 실제 Windows·WSL Ubuntu x86_64 cold-cache/반복 setup·Python-only update와 로컬 wheel bounded update를 각각 구분한다. WSL은 사용자 승인 후 실제 CLI 7종 설치·task 진입점·native lock 누락/플랫폼 불일치 실패와 전체 테스트 335개를 확인했다. 설치 실증은 기존 mise·Python을 재사용했으며 완전한 host 초기 설치가 아니다. 설계 Skill의 positive/near-miss·behavior capability eval은 별도 PR #256의 근거이며 이 실행기의 성공을 대신하지 않는다.
- **남은 실환경 검증:** macOS 실행 환경은 확보하지 못해 native setup/replay/update가 미검증이다. WSL x86_64 성공을 Linux arm64·musl 등 다른 플랫폼의 성공으로 확대하지 않는다. Python 최초 다운로드·OS-level containment와 HOME native installer는 이번 core 설치 묶음 밖이다.
- **PR 상태:** 2026-11-01 확인 시 Draft가 아닌 Ready for review 상태이며 Branch Check와 PR Gate가 통과했다. 이 상태를 미검증 플랫폼의 지원 완료나 merge 승인으로 해석하지 않는다.

## 재사용 설계 스킬

- **Canonical source:** [`mols-dev-env-bootstrap-design/SKILL.md`](https://github.com/mols3131d/mols-agent-assets/blob/1f1efa63efaad63f4bda19fe4781920bb2c6c541/src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md)
- **책임:** 초기 setup, 개발 중 유지/업데이트, 버전 허용 범위와 lock, 누락된 도구의 권한·부작용, 부분 실패·복구·검증을 평가하고 실행 가능한 설계 인계를 만든다.
- **이식성:** mise/uv/Rulesync에 종속하지 않는다. 도구별 실제 version manager, lock, installer semantics와 프로젝트 정책을 조회하고, 적합한 native 방법을 선택한다.
- **범위 밖:** 실제 설치·업데이트 실행 및 구현 코드 자체의 작성, 일반 패키지 업데이트, CI만의 admission design. 부트스트랩 구현은 이 PR의 **별도 결과물**이며 일반 엔지니어링 작업이 소유한다. 스킬이 실행 결과나 설치 권한을 대신 증명하지 않는다.
- **완료 조건:** positive/near-miss activation을 분리하고, 허용 범위 외 버전 차단·미설치 host tool 회피·user/global side-effect 보호·독립 단계 지속·거짓 성공 방지 사례를 설계 근거로 검증한다. Rulesync structural validation과 route drift check를 수행하고, 실제 runtime/eval 미수행은 구분한다.

## UX 심층 조사와 설계 인계

- [부트스트랩 심층 조사](bootstrap-deep-research.md) — 현재 실행 구조, mise/uv 최신 공식 동작, 잠금·설치 권한·성능·UX 대안과 미해결 근거.
- [UX 구현 인계](bootstrap-ux-design.md) — setup/update 사용자 여정, 단계별 상태·실패·복구 모델, 안전한 병렬화와 테스트/성능 측정 계획.
- [CLI·인자·OS 심층 조사](bootstrap-cli-os-research.md) — mise task args 전달, 안전한 flags, Windows native/WSL/macOS/Linux 및 shell·arch·파일시스템 차이.
- [CLI·OS 설계 인계](bootstrap-cli-os-design.md) — 최소 공개 CLI, 옵션 도입 기준, 운영체제별 capability/지원 테스트와 실패 UX.
- [안정성·전역 영향 심층 조사](bootstrap-safety-global-effects-research.md) — pre-task auto-install, system Python sync 위험, 외부 Skill installer의 HOME·Agent 변경, Git hooks, 캐시·공급망 신뢰 경계.
- [안전 설계 인계](bootstrap-safety-design.md) — 실제 쓰기 대상 preflight, 사용자/OS 전역 변경 승인, 실패·복구·격리와 회귀 테스트.

아래 초기 설계는 당시의 확장 목표를 보존한 자료이며 현재 운영 정책이나 구현 계약이 아니다. 이후 범위를 넓힐 때 mise lockfile sidecar, uv managed Python 다운로드, task runner의 의존성 오류 전파와 minimum release age처럼 정확한 동작에 영향을 주는 조건은 별도 PoC로 판단한다. 벤더 문서의 최신 기능이 CI에 설정된 mise 버전에서 지원되는지도 검증한다.

## 초기 설계의 사용자 진입점과 의미

아래 절부터 작업 계획까지는 초기 설계의 확장 목표를 보존한다. 현재 실행·수용 여부는 위 **이번 PR의 수용 범위**와 [운영 안내](../../docs/development/tooling/mise.md)가 우선한다. `mise.lock` 자체는 도입했지만 tool range 갱신, 자동 Rulesync/hook/HOME 연동, `DEGRADED` 상태는 현재 runner의 제공 기능이 아니다.

| 진입점(목표) | 기대 동작 | 버전 변경 |
| --- | --- | --- |
| `mise run setup` | 최초 또는 반복 실행 시 승인된 프로젝트 환경을 재현하고 누락된 관리 대상만 채운다 | committed lock을 따른다. 버전 탐색·승격 없음 |
| `mise run update` | **명시적으로 실행한 경우에만** 선언된 허용 범위 안의 최신 릴리스로 해석·검증·반영한다 | 변경된 lockfile을 검토 가능한 변경으로 남긴다 |
| `mise run check` / `mise run test` | 설치 여부와 기능 상태를 진단·검증한다 | lockfile이나 버전 정책을 갱신하지 않는다 |

두 경로는 동일한 적용·검증 동작을 재사용하되, `setup`은 **현재 잠긴 상태를 복구**하고 `update`는 **허용 범위 안에서 잠긴 상태 자체를 갱신**한다. `setup`을 실행했다고 최신 버전으로 변경되면 안 되며, `update`를 자동 또는 매 세션 시작 시 실행하지 않는다.

`mise`가 미설치 상태라면 `mise run` 자체를 호출할 수 없으므로 설치를 지시하는 짧은 **최소 사전 요구사항**을 문서화한다. 이를 이유로 `curl | sh`, OS package manager, `sudo`, 전역 환경 재구성용 별도 bootstrap chain을 자동 실행하지 않는다.

## 버전 정책과 상태 소유권

| 대상 | 사전 선언하는 정책 | 실제 선택 결과 | setup / update |
| --- | --- | --- | --- |
| mise-managed 개발 CLI (`uv`, Node, rumdl, Lefthook, Biome, Rulesync, skills CLI) | `mise.toml`의 도구별 version request (지원하는 major/minor prefix 등) | `mise.lock` 도입 후 정확한 해석 결과 기록 | `setup`: locked install, `update`: 허용된 request에 대해 lock 재해석 후 설치 |
| Python 실행환경 | `.python-version` 및 `pyproject.toml`의 요구조건 | uv가 관리하는 interpreter와 `.venv` | `setup`: 선언된 Python 사용 및 lock대로 동기화. Python 버전 범위가 불명확하면 자동 범위 승격 금지 |
| Python 패키지 | `pyproject.toml`의 dependency specifier | `uv.lock` | `setup`: `uv sync --locked --all-groups`, `update`: `uv lock --upgrade` 후 locked sync |
| Rulesync 외부 source | `rulesync.jsonc`의 source/ref와 허용 정책 | `rulesync.lock` | `setup`: `rulesync install --frozen`. 허용 범위 없는 Git ref/commit은 임의 업데이트 금지 |
| 외부 native Skill | `skills-lock.json`의 source/ref, native installer | 잠긴 revision과 설치 결과 | `setup`: 선택된 설치 경로를 실행. 허용 범위 없는 ref는 `update`에서도 유지 |

**허용 범위는 선언부가 소유한다.** 스크립트에 `latest`, 특정 major, upper bound, 예외 버전을 별도로 하드코딩하지 않는다. Exact pin은 길이 0인 허용 범위로 보고 업데이트하지 않는다. 범위를 넓히는 작업은 일반 `update`가 아니라 별도 정책 변경과 검토다.

현재 `mise.toml`은 CLI를 모두 exact version으로 고정한다. 이는 의도적으로 허용 범위를 정하기 전에는 `update`로 갱신할 수 있는 CLI가 없다는 뜻이다. 구현 단계에서 **도구별 호환성 판단 후**, 필요한 항목만 제한된 prefix/range request로 옮긴다. 현재의 모든 정확한 버전을 무작정 `latest`로 바꾸지 않는다.

`mise.lock`을 도입한다면 `[settings] lockfile = true`와 `mise lock`으로 명시적으로 생성·commit한다. `setup`은 잠긴 해석 결과를 사용하고, `update`는 `mise lock --bump`로 사전 정의된 요청 범위 안의 최신을 해석한다. 설치는 `mise install --locked`로 분리한다. `mise upgrade --bump`처럼 request 자체를 넘어서는 명령을 업데이트 자동화에서 사용하지 않는다.

`uv lock --upgrade`는 `pyproject.toml`의 기존 dependency bounds 안에서만 패키지를 올리므로 업데이트에 적합하다. `uv sync --all-groups`만 단독으로 실행하는 것은 초기 셋업과 업데이트의 경계를 모호하게 만들 수 있으므로 locked sync로 바꾼다.

Git branch `main` 같은 이동 ref는 명시적인 SemVer 허용 범위가 아니다. 따라서 현재 `rulesync.lock`의 `resolvedRef`와 `skills-lock.json`의 pinned ref를 일반 CLI 업데이트와 같이 무조건 최신으로 갱신하지 않는다. 외부 source 업데이트 규칙을 별도로 승인하기 전까지 **skip + 사유 보고**한다.

## 누락된 도구와 자동 설치 권한

**설치 위치와 영향 반경**으로 정책을 나눈다. `명령이 존재하지 않는다`는 이유만으로 OS 전역 패키지를 설치하지 않는다.

| 분류 | 예시 | 기본 정책 | 누락 시 |
| --- | --- | --- | --- |
| 진입점 prerequisite | `mise`, 필요 시 Git·셸 | 사용자 관리 | 실행 전 확인 또는 가능한 단계에서 진단 후 공식 설치 안내. 자동 OS 전역 설치 금지 |
| mise-managed versioned tool | Node, uv, Rulesync, Biome 등 | **mise 관리 영역에만** 선언된 잠긴 버전 자동 설치 허용 | 설치 실패 시 그 도구를 요구하는 단계만 BLOCKED, 나머지 독립 단계 계속 |
| 프로젝트 격리 의존성 | Python `.venv` 패키지 | locked 자동 설치·복구 허용 | 해당 기능만 실패 처리 |
| 저장소 로컬 연동 | Rulesync-generated project files, `.git/hooks` | 사전 점검 후 기존 사용자 변경 보존하며 설정 | 충돌 또는 부재 시 단계 skip/blocked와 복구 안내 |
| 사용자/OS 공유 영역 | OS package manager, 전역 npm/pip, `sudo`, 사용자 홈 vendor Skill installer | **무인 설치 금지**; 명시적으로 요청된 허용 경로만 실행 | 다른 단계 계속, 정확한 수동 명령 또는 opt-in 작업 안내 |

`mise`는 기본 설정에서 task가 시작되기 전에 누락된 도구를 자동 설치할 수 있다. 그러므로 `setup`의 개별 단계에서 '누락되면 skip'을 구현하려면 **mise의 task/tool auto-install 단계에서 선행 실패하지 않는지**도 함께 확인해야 한다. 구현 때 task별 tool scope 또는 `task.run_auto_install` 설정을 검증하고, 프로젝트에서 허용한 mise-managed 설치만 일어나도록 해야 한다. 모든 task에서 `continue-on-error`를 켜 의존 단계까지 실행하는 방식은 피한다.

현재 `skills_sync.py`는 upstream `install.sh`를 호출하여 사용자 홈의 벤더별 설치 디렉터리를 바꿀 수 있다. 이를 Python의 프로젝트-local 설치와 동일하게 취급하지 않는다. 초기 설정 시 해당 동작을 명시적으로 opt-in하거나 기존 사용자 설정을 훼손하지 않는다는 근거가 확인된 경로만 기본 실행에 포함한다. 반대로 이미 설치한 외부 Skill의 lock drift를 진단하는 read-only 단계는 자동으로 수행할 수 있다.

## 실행 모델과 실패 처리

`setup`과 `update`는 preflight → eligible tasks 실행 → 결과 요약 순서로 구성한다.

1. **Preflight:** 현재 root/ref, 영향을 받는 tracked lockfile의 수정 여부, 필수 host tool, 네트워크 요구, 작업별 설치 영역·권한, 허용 범위를 확인한다. 사용자가 수정 중인 lockfile이나 hook을 조용히 덮어쓰지 않는다.
1. **Resolve:** `setup`은 변경 없는 lock 조회. `update`만 도구 및 패키지의 최신 허용 해석 결과를 lock에 반영하며, 해석 실패나 범위 위반이면 대상 업데이트를 중단한다.
1. **Apply:** 해당 도구가 충족된 독립 단계만 실행한다. 일단 실패한 의존성을 요구하는 후속 단계는 수행하지 않는다. 설치·생성·hook·user-level Skill 등 변경 경계를 로그에서 구분한다.
1. **Verify:** 실제 실행 가능한 도구·프로젝트 의존성을 최소 검증한다. 설치 자체가 끝났다는 사실을 정상 작동의 충분한 증거로 보지 않는다.
1. **Report:** 성공, 기존 상태 유지, 업데이트, skip, 실패와 수동 복구 명령을 단계별로 보여준다. 가능하면 machine-readable 상태도 지원하되 필수 로그 경로를 추가하지 않는다.

권장 최종 상태:

- `READY` (exit 0): 필요한 모든 작업 완료·검증.
- `DEGRADED` (exit 0, 눈에 띄는 warning): 선택적 작업이 skip되었으나 필수 개발 기능은 준비됨. 전체 완료로 표현하지 않음.
- `BLOCKED` 또는 `FAILED` (non-zero): 필수 준비가 누락됐거나 실제 실행·검증이 실패함. 다른 독립 작업의 성공은 보고하되 전체 성공으로 취급하지 않음.

미설치 여부를 정확히 알 수 없으면 '정상'으로 추정하지 않는다. 외부 설치기를 실행한 경우 어떤 scope를 건드렸는지 추적 가능하게 남기고, 실패 시 전체 repository나 사용자 홈을 자동 초기화·rollback하지 않는다. 완료하지 못한 단계만 다음 실행에서 안전하게 재시도한다.

## 구현 경계

- `mise.toml`은 command entrypoint·version requests를 소유하며, Python wrapper를 만든다면 **누락 분류, 부분 실패 집계, 상호 의존 순서, 사용자별 권한**처럼 mise 태스크만으로 표현하기 어려운 동작에 한정한다.
- Python/CLI/installer/Rulesync의 공식 업데이트·설치 semantics를 로컬 wrapper가 다시 구현하지 않는다.
- `setup`은 버전 정책 파일, `uv.lock`, `mise.lock`, `rulesync.lock`, `skills-lock.json`을 몰래 수정하지 않는다.
- `update`만 해당 lockfile을 의도적으로 변경하며, 자동 commit/push/merge, host-level installer, 기존 버전 무단 pruning은 하지 않는다.
- CI 검증에서는 환경 복구와 버전 업데이트를 분리하고, 기존 `--locked`/ `--frozen` 계약을 보존한다.
- `check`, `test`, `format`, `skills-sync`, 기존 Rulesync workflow 같은 별도 entrypoint를 삭제하거나 한 거대한 설정 스크립트로 흡수하지 않는다.

## 작업 계획과 완료 조건

| 단계 | 변경 대상 | 수용 기준 |
| --- | --- | --- |
| 1. 정책 및 명세 | 이 문서, mise reference | 설정 소유권, setup/update 및 미설치 분류가 모순 없음 |
| 2. 버전 정책 정비 | `mise.toml`, 필요시 `mise.lock`, `pyproject.toml` | 정확한 pin vs 허용 범위가 항목별로 명시되고 initial setup 재현 가능 |
| 3. 실행 경로 | mise task와 필요 최소 wrapper | setup은 기존 lock 재현, update는 범위 내 lock만 갱신, 필수/선택적 오류 격리 |
| 4. 외부 연동 | Rulesync, Skill installer, Lefthook | user-level 부작용은 opt-in 또는 명시된 승인 경로로 제한 |
| 5. 검증·운영 안내 | deterministic tests, mise reference, CI | 재실행 안전성, 실제 누락/복구, 업데이트 제한, 단계별 종료 상태 확인 |
| 6. 재사용 설계 스킬 | `src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md`, `route/skills.jsonl` | 단일 canonical Skill, 독립적인 activation/설계 책임, route 갱신·구조 검증, 대표·경계 사례 검토 |

최소 회귀 시나리오:

- 깨끗한 환경에서 locked `setup`이 의존성과 도구를 준비한다.
- 같은 `setup`을 다시 실행해 허용되지 않은 버전·파일·사용자 환경 변경이 없다.
- `update`가 범위 내 새 버전은 선택하고 범위 밖 새 버전은 선택하지 않는다.
- 정확한 pin만 남은 대상의 update는 변경 없이 종료된다.
- uv lock upgrade는 dependency upper bound를 넘지 않는다.
- Git, Bash, mise가 없는 경우를 분리해서 안내하고 독립적인 작업은 계속한다.
- user-level native installer는 opt-in 없이 실행되지 않는다.
- 중간 실패 시 재실행으로 안전하게 복구할 수 있고, 보고된 종료 코드가 실제 준비 상태와 일치한다.
- CI/기존 hook은 독립적으로 검증을 계속한다.

## 근거와 현재 상태

- 현재 구현: [mise.toml](../../mise.toml), [skills_sync.py](../../scripts/agent_assets/skills_sync.py), [mise reference](../../docs/development/tooling/mise.md), [skills CLI reference](../../docs/development/tooling/skills-cli.md)
- 외부 계약: [mise lockfile](https://mise.jdx.dev/dev-tools/mise-lock.html), [mise upgrade](https://mise.jdx.dev/cli/upgrade.html), [mise task auto-install](https://mise.jdx.dev/dev-tools/), [uv locking/sync](https://docs.astral.sh/uv/concepts/projects/sync/)
- 현재 구현은 exact CLI pin·`mise.lock` 기반 setup과 Python-only update다. Windows·WSL cold-cache 설치·반복 복구·update의 source와 검증 한계는 [후속 검증 기록](bootstrap-simplification-review-2026-11-01.md)을 따른다. macOS native E2E는 미검증으로 유지한다. 별도 설계 Skill runtime의 [실패·grader 한계](https://github.com/mols3131d/mols-agent-assets/blob/1f1efa63efaad63f4bda19fe4781920bb2c6c541/docs/skills/mols-dev-env-bootstrap-design/evaluation.md)는 이 core 실행기 검증과 구분한다.
