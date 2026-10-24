# PR #256 — 부트스트랩 과설계·복잡성 검토

> **상태:** 다관점 조사·검토 인계 / 비정본. 실제 코드·스킬·테스트 수정 없이 작성한 분석이다.
>
> **Revision:** [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256), base `b29aa490d0c251d5ca478fa5c787b90258f09d79` → head `5a33b7b5b30e2100e026d89a5f2e957727e35acf` (2026-10-25). 이후 변경에는 재검토가 필요하다.
>
> **판단 기준:** [Development Principles](../../docs/development/principles.md)의 효과성 → 운영 편의성 → 단순성, 안전과 호환성은 선행 제약. [구축 정책 정본](../../docs/development/development-environment.md) · [설계 Skill](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md) · [이전 안전 리뷰](bootstrap-isolation-review-2026-10-25.md)를 함께 적용.

## 결론

**부분적으로 과설계 위험이 있다.** 현 `development_bootstrap.py` 약 466줄, 전용 테스트 약 540줄이라는 **크기 자체**가 결함인 것은 아니다. 그러나 seven-tool exact-pin + uv 프로젝트 환경을 준비하려는 핵심 목적과 비교하면, **mise 내부 설치 결과를 스크립트가 다시 해석하고, 설정 파일의 소유권을 중복 선언하며, 설치하지 않는 자산까지 core 실행의 차단 조건으로 묶는** 부분은 명확한 유지보수 비용을 만든다.

반면, **기존 사용자의 상태를 보호하는 최소 안전 검사**는 과설계가 아니다. 특히 이전 보고서의 F1(Git 상태 우회), F2(uv group override로 거짓 READY), F3(system-site-packages venv)는 실제 보호 계약의 결함이다. 단순화를 이유로 해당 방어를 빼지 말고 **각 결함의 근본 원인을 적은 변경으로 고칠 것**을 권장한다.

| 판정 | 구체 대상 | 권고 |
| --- | --- | --- |
| **단순화 후보** | 7개 도구 목록의 이중 소유, 모든 asset lock을 core dirty gate에 포함 | 정책 소유권과 실제 변경 대상에 맞춰 축소 |
| **조건부 단순화 후보** | npm CLI `package.json`·설치 경로 직접 탐색 | mise의 native 실행으로 대체 가능한지 Windows + pinned mise에서 PoC 후 판단 |
| **유지할 가치가 높음** | uv 프로젝트 격리, setup/update 분리, dirty lock 보호, `--locked`, 필수 실패의 nonzero, HOME/hook 기본 제외 | 안전 계약을 보존하고 필요한 회귀만 추가 |
| **확장 금지** | 보편적 전역 도구 탐지/권한 엔진, 모든 OS용 자체 패키지 관리자, 자동 복구·롤백, 별도 테스트 프레임워크 | 실제 필요가 입증될 때까지 도입하지 않음 |
| **정리 대상** | 작업 중 생성된 다수의 inbox 연구 문서와 변경된 정본 간 탐색 혼동 | 원본 연구는 근거로 보존하고, 실행 정책은 정본 한 곳으로만 연결. 중복 규칙 추가 금지 |

## 검토 루프와 증거

### Loop 1 — 범위·비용 구조 파악

- [`mise.toml`](../../mise.toml)은 7개 exact-pin CLI의 버전을 선언한다. PR 전에는 setup이 uv, Rulesync, Skill, hook을 순차 실행했고 PR에서는 후자들을 선택적 경로로 분리했다. **HOME에 쓰는 자동 단계 제거는 실제 안전·UX 이득**이며 철회하지 않는다.
- [runner](../../scripts/development_bootstrap.py)는 `POLICY_FILES`, `TOOL_COMMANDS`, `read_tools()`, 설치 순회·실행 바이너리 확인, 경로 검증, 실패·복구 및 report를 자체 관리한다. [테스트](../../tests/scripts/test_development_bootstrap.py)는 성공/실패/경로/OS별 npm 진입 및 실제 uv bounded update를 다룬다.
- 재사용 [Skill](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md)은 단일 `SKILL.md` 약 63줄로 별도 reference tree·runtime 구현이 없다. **Skill 자체는 구조적으로 과하게 쪼개지지 않았다.** 설치 실행·권한 시스템을 Skill에 넣지 않는 현 방침을 유지한다.
- Inbox에는 최초 UX, CLI/OS, 안전, 조사 보고서 등 여러 durable artifact가 있다. **이 파일들은 runtime에 자동 로드되지 않는 조사 근거**여서 개수만으로 context 오버헤드라고 단정할 수 없다. 다만 오래된 구현 제안이 정본처럼 읽히는 위험은 있다.

### Loop 2 — Native owner와 중복 설계 반증

공식 [mise 설치·선택 동작](https://mise.jdx.dev/dev-tools/), [mise exec](https://mise.jdx.dev/cli/exec), [npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html), [uv group·sync](https://docs.astral.sh/uv/concepts/projects/sync/)를 현재 source와 대조했다. **공식 문서의 최신 기능이 이 프로젝트에 설치된 정확한 mise 버전/Windows 결과를 증명하지는 않는다.**

- `mise install`은 설치된 일치 버전을 재사용한다. 현재 스크립트가 매번 `mise install <exact>`를 호출한다고 **실제 중복 다운로드**가 발생한다는 주장은 부정확하다. 설치 전 `mise where` 호출을 추가해 자체 캐시 판단 로직을 만드는 것은 오히려 불필요하다.
- `mise exec -- <command>`는 선택한 도구 환경에서 자식 실행을 제공한다. 그런데 현재 npm CLI의 `tool_command()`는 `mise where` 후 `node_modules`와 `lib/node_modules`, `package.json`의 `bin`·이름·버전을 직접 파싱하고 Node 경로를 조합한다. 이는 특정 Windows `.cmd` 우회 이유가 있으므로 **실제 Windows 검증 없이 삭제하라는 결론은 내리지 않는다**.
- `uv sync --locked --all-groups`는 잠금을 따르는 프로젝트 환경을 native하게 관리하지만, sync 옵션을 바꿀 수 있는 외부 환경변수와 기존 venv의 격리 특성에 대해 모든 안전 보장을 제공하는 것은 아니다. **F2/F3의 짧고 정확한 방어는 필요**하다. 모든 `UV_*` 환경변수를 무차별 삭제하는 새 일반 정화 엔진은 인증·사내 인덱스 설정을 망가뜨릴 수 있으므로 지양한다.

### Loop 3 — 다관점 재검토와 범위 축소

**효율/소유권 관점**

- [runner](../../scripts/development_bootstrap.py)의 `read_tools()`는 `mise.toml`의 키가 `TOOL_COMMANDS`의 7개 키와 **완전히 동일**해야 한다. 버전 정본 자체는 하나지만, *도구 목록*은 두 곳에서 관리한다. 정당한 새로운 CLI 선언도 별도 Python 코드 갱신 전까지 `setup`을 차단한다. 명시적인 지원 목록이라는 장점과 유지보수 마찰 사이를 비교하되, 범용 dynamic CLI detector를 새로 만들지는 않는다.
- `POLICY_FILES`에 `rulesync.jsonc`, `rulesync.lock`, `skills-lock.json`이 포함되고 `check_update_state()`가 모두 clean이어야 한다. 실제 `update`는 현재 **Python `uv.lock`만 갱신**하므로, 관련 없는 Rulesync/Skill 자산 미커밋 변경 때문에 Python 업데이트가 차단된다. 파일 변경 감지 의도는 이해되지만, **사전 dirty gate와 작업 중 의도치 않은 수정 감시는 다른 책임**이다. 우선 실행할 작업이 쓰는 파일만 사전 clean 요건에 포함하는지 검토할 가치가 크다.
- `unchanged_policy()`는 각 단계 전후 7개 파일의 바이트를 다시 비교한다. 아주 작은 텍스트 I/O라 성능 최적화의 우선 대상이 아니다. 일괄 삭제보다 **검사 대상이 core 목적에 맞는지**가 핵심이다.
- `.venv` 내부 `Lib/lib64/Scripts` symlink/junction 검사와 `.tmp` 독점 실행 lock은 실제 범위 밖 쓰기/동시 실행을 줄이려는 목적이 있어 쉽게 제거하지 않는다. 다만 포괄적 filesystem sanitizer나 범용 자산 소유권 데이터베이스로 확장하지 않는다.

**UX 관점**

- `report()`는 매 `setup` 완료 시 별도 실행하지 않는 Rulesync projection, HOME Skills, Git hooks의 `[skipped]` 안내를 **매번 출력**한다. 초기 온보딩 때는 유용하지만 반복 실행에서는 status 노이즈로 볼 수 있다. 명확한 `core READY`·부분 실패 요약은 유지하면서, 상세 안내는 첫 실행 가이드/명시적 선택 경로로 보내는 편이 낫다. 정량 사용성 근거는 없어 **Low·개선 후보**로 분류한다.
- `--dry-run`은 이미 존재하는 미커밋 policy 파일을 이유로 `update` 계획 단계에서도 `BLOCKED`가 된다. 실제 update 전에 dirty state를 거부하는 것은 맞지만, 사용자가 **변경을 하지 않고 계획만 보려는 UX**와는 다를 수 있다. 기능 계약을 먼저 결정해야 하며 자동으로 버그로 판정하지 않는다.
- 설치 전 사용자 허가는 [정본](../../docs/development/development-environment.md)에 따라 **호출자 agent가 작업 묶음 단위로** 얻도록 정해졌다. 전체 도구에 매번 승인 창, CLI `--yes`, 시스템 전역 permission registry를 새로 구현하는 것은 이번 스코프 밖이며 권장하지 않는다.

**테스트·문서 관점**

- 약 540줄 전용 테스트에는 native 명령의 정확한 호출 인자·npm 설치 내부 구조와 관련된 여러 케이스가 있다. 파괴적 경로 보호 검사는 가치가 있으나, native 실행에 전부 위임할 수 있다는 검증이 확보되면 **그 내부 구조를 모방한 테스트도 함께 제거**할 수 있다.
- 반대로 F1/F2/F3을 보완할 때는 각각 **하나의 대표 회귀 실패→통과 케이스 및 필요한 경계 케이스**면 우선 충분하다. 모든 UV 옵션×모든 OS×모든 설치 주체의 조합 테스트나 새로운 Eval harness를 만들 필요는 없다.
- Inbox의 대규모 연구·명세는 사용자가 명시적으로 요청한 반복 연구의 **작업 근거**이므로 길이만으로 삭제하지 않는다. 관리 비용을 줄이려면 [개발환경 구축 정본](../../docs/development/development-environment.md)에서 현재 규칙만 유지하고, 기존 연구는 비정본 상태·정본 링크로 구분한다. 정본과 [mise 운영 안내](../../docs/references/tooling/mise.md), [Skill maintainer](../../docs/skills/mols-dev-env-bootstrap-design/README.md) 간 규칙 복제를 늘리지 않는다.

## 판정 및 우선순위

| ID | 판정 | 관찰된 비용·제약 | 최소 행동 |
| --- | --- | --- | --- |
| O1 | 🟡 Medium · 개선 권장 | `TOOL_COMMANDS`의 고정 지원 목록과 `mise.toml` tool list가 결합되어 도구 추가 시 2곳 변경 요구 | 지원 목록 검증이 실제 필요한가 먼저 판단. 검증 명령의 명시적 매핑은 필요 시 남기고 **키 동등성 차단만** 완화할 수 있는지 테스트 |
| O2 | 🟡 Medium · 조건부 | npm CLI 내부 package layout 탐색은 vendor backend 변화에 취약하며 전용 테스트 유지비 발생 | pinned mise + Windows에서 native `mise exec`/권한 경계를 PoC. **동등하면** 내부 resolver와 관련 테스트 축소, 아니면 현 구현 유지 |
| O3 | 🟡 Medium · 개선 권장 | Python-only update가 unrelated Rulesync/Skill lock dirty 상태에도 막힘 | 설치 범위와 충돌 검사 대상 분리. side-effect 보호 필요분은 변경 감지로 유지 |
| O4 | 🔵 Low · UX 후보 | 반복 `setup`에서 실행하지 않는 선택적 기능 안내 3건 매번 출력 | 실패/READY 한 줄 중심, 상세 선택적 안내는 문서로 이동 검토 |
| O5 | 🔵 Low · 결정 필요 | 변경 없는 update plan도 dirty policy에서 중단 | preview와 apply의 역할 계약 확정 후 선택. 현재를 임의 결함으로 단정하지 않음 |
| O6 | **과설계 아님** | Skill 단일 파일, setup/update 구분, project `.venv`·lock 보호, 부분 실패 보고, source-native Eval 재사용 | 유지. 다른 abstraction·layer·configuration 불필요 |

### 이미 확인된 안전 결함과의 구분

[이전 안전 보고서](bootstrap-isolation-review-2026-10-25.md)의 **F1 (Git 환경 상속), F2 (UV_NO_GROUP), F3 (기존 venv system-site-packages), F4 (generated docs index)**는 여전히 별도 개선 대상이다. 본 리뷰는 이 결함을 고치지 않았으며, **과설계 최소화 = 안전 검사를 생략한다는 뜻이 아니다.**

적절한 최소 수선은 개별 관찰 실패를 고치는 좁은 Git 환경 고정, uv group override 차단, venv 설정 점검, native 문서 index 재생성이다. 복잡한 프레임워크·범용 보안 스캐너·일괄 파일 해시 레지스트리·시스템 설치 추상화는 요구하지 않는다.

## 제안된 진행 순서와 중단 기준

1. **안전 결함 F1–F3을 가장 작은 패치로 해결**, F4 파생 index 재생성. 실행 가능한 회귀 테스트로 확인.
2. **O3**의 실제 변경 파일 범위와 dirty gate를 분리하는 최소 수정 검토. 단, 원치 않는 외부 자산 파일 변경을 놓치지 않는다는 이유가 있다면 현 감시를 유지하고 사전 차단만 줄인다.
3. **O2**는 Windows native `mise exec` 실증 없이는 리팩터링하지 않는다. 비교 결과가 동등하지 않으면 작업을 종료하고 현재 npm metadata guard를 유지한다.
4. **O1/O4/O5**는 반복 사용·유지보수에 비용이 드는지 보고 필요할 때만 반영한다. 추가 구조나 문서 체계를 만드는 것으로 해결하지 않는다.
5. 모든 수정 뒤 **관찰 가능한 필수 계약**만 재검증한다: setup lock 보존, update bounds, .venv 격리, user HOME/Hooks 미변경, 실제 필수 실패→nonzero, 승인된 동작과 역할 경계.
6. **Stop rule:** 기존 관리자/테스트/문서가 이미 책임을 수행하고 추가 코드가 새로운 관찰 가능 계약을 보호하지 않으면 새 코드·옵션·추상화를 추가하지 않는다.

## 검증 수준

- **직접 확인:** PR head의 source/설계/정본/테스트 구조와 본문, mise 공식 문서가 설명하는 manager behavior. O1·O3의 코드상 결합과 선택적 안내의 반복 출력은 source에서 확인.
- **합리적 추론:** O2의 유지보수 비용, O4/O5의 실제 사용자 불편 정도 및 native 대체의 장기 이점. 다른 OS·mise 버전·사용자 workflow에서는 달라질 수 있다.
- **이번 작업에서 미실행:** PR 브랜치의 테스트, npm CLI 대체 PoC, 실제 Windows/macOS/Linux cold bootstrap, Skill runtime Eval, 변경 후 CI. 이전 리뷰의 uv 재현 결과는 별도의 근거로 남는다.

**이 보고서는 과설계 검토만 수행했다.** runner·Skill·CI·테스트·설치 명령과 기존 연구 문서는 수정·실행하지 않았으며, PR Draft를 유지한다.
