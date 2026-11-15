# CI · Lefthook 검증 체계 개선 인계

## 목표와 범위

로컬 코딩 에이전트의 Lefthook, GitHub API·ChatGPT 플러그인·웹 UI·원격 에이전트의 직접 커밋, Branch Check 및 PR Gate를 모두 고려하여 **검사 누락 없이 빠르고 유지보수 가능한 검증 체계**를 만든다. `main`의 병합 승인 기준을 지키면서 불필요한 도구 설치·네트워크 호출·검사 반복을 줄인다.

- **필수:** 검증 경로에 관계없이 merge-critical failure는 `PR Gate`에서 재현 가능한 근거로 차단한다. 로컬 Hook 결과를 서버 검증의 충분조건으로 간주하지 않는다.
- **선택 가능한 최적화:** Hook과 CI의 동일 검사 중복 제거는 허용되지만, 독립성·변경 SHA·실행 환경·실패 위험·실행 비용을 확인하고 **그 검사만** 생략할지를 판단한다. "Lefthook에서 검사했으니 CI에서 빼는 것이 최적"이라는 전제는 두지 않는다.
- **비목표:** Hook의 자동 설치, 작업 트리 자동 포맷·자동 stage 확대, CI의 commit/push, 새 CI provider, 새 eval framework, 상시 유료 LLM 호출, 무근거 OS matrix, Ruleset의 무단 변경·완화.

기준 ref: `main` @ `c39d094f72cfb331217bc70abb303c738493dd4c`. 작업 branch: `mols/chore/ci-lefthook-quality-gates`. 구현 전 변경된 upstream 상태와 현재 검증 결과를 다시 확인한다.

## 정본과 현행 사실

| 정본·실행면 | 확인한 상태 |
| --- | --- |
| [CI 정책](../../docs/development/ci.md) | 모든 쓰기 경로에서 검증 근거를 확보하고, `main`의 merge-critical 실패를 required `PR Gate`에서 차단. Impact 판단 불명확 시 확대 또는 실패 |
| [Formatting](../../docs/development/formatting.md) | 수정은 `mise run format[-changed]`; Hook에서는 일반 파일의 자동 포맷·stage를 하지 않음 |
| [Lefthook](../../lefthook.yml) | pre-commit staged projection sync, commit-msg 메시지 검사, pre-push 전체 pytest. 자동 설치는 선택 |
| [Mise](../../mise.toml), [Python](../../pyproject.toml) | Ruff·rumdl·Biome 지정; `mise run format-changed`는 **수정 명령**, `mise run check`의 Biome은 일부 설정만 검사 |
| [Branch Check](../../.github/workflows/branch-check.yml) | 비-main push: frontmatter, 전체 pytest, local 3종 projection |
| [PR Gate](../../.github/workflows/pr-gate.yml) | main 대상 PR merge 후보: frontmatter, pytest, 영향 projection, mise Doctor, root Rulesync lock, library Rulesync 구조 검증 |
| [Projection selector](../../scripts/generated_artifacts_sync.py) · [validator](../../scripts/generated_artifacts_validate.py) | 수정 경로로 검사 대상을 선택. 공통 orchestration/selector 변경 시 영향 누락 가능성을 테스트 필요 |
| [GitHub 정책](../../docs/development/github.md) | CI·agent 실행을 바꾸는 통제 표면은 자체 변경에 의존하지 않는 독립 검토와 명시적 인간 승인 필요 |

2026-11-15 확인 실행: [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43710194442), [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43710198355) 모두 성공. 이는 현행 단계의 성공일 뿐 누락 검사를 검증한 증거가 아니다. 기존 약 12초 / 29초의 실행 시간은 *단일 관측*이며 최적화 목표치가 아니다.

활성 `protect-main` [Ruleset](https://github.com/mols3131d/mols-agent-assets/rules/21094860): 필수 `PR Gate`, squash-only, review thread resolution, 0 required approvals, `strict_required_status_checks_policy=false`. 사람 승인 요구 및 최신 base 검사 필요성은 **별도 운영 결정**이며 이 PR로 설정을 자동 변경하지 않는다.

## 변경 경로와 검증 책임

| 작성 경로 | Lefthook 가능 여부 | 필수 서버 경계 |
| --- | --- | --- |
| 로컬 코딩 에이전트의 Git commit/push | **설치된 경우에만** pre-commit·commit-msg·pre-push 실행 | Branch Check(초기 피드백) + PR Gate(병합) |
| ChatGPT GitHub 플러그인·GitHub Contents API·MCP·웹 UI | 로컬 Hook **미실행** | 원격 branch push / PR 이벤트에서 동작하는 검증 |
| 클라우드 코딩 에이전트·자동화 | 실행 환경별로 불확실; 기본적으로 Hook 미보장 | 동일한 서버 검증. 에이전트 진술은 실행 증거가 아님 |

서버 CI는 `contents: read` 유지, `uv --locked` 및 검증 스크립트 재사용. 생성물은 CI에서 **검사만** 하고 영구 기록하지 않는다. 로컬 `pre-commit`의 projection sync/stage 예외는 기존 소유권과 부분 스테이징 안전성을 보존한다.

## 실패 → 검증 근거와 판단

| 실패/변경 | 검증 후보 | 권장 경계 / 판단 |
| --- | --- | --- |
| Python 실행 결함, 도구·검증기 회귀 | deterministic pytest | PR blocking; Branch Check에는 비용과 조기 피드백 가치를 보고 유지/선택 |
| malformed 문서 metadata, config | frontmatter·정적 validator | PR blocking; 가능하면 Branch Check에서 조기 발견 |
| 생성된 INDEX·라우트 stale/누락 | official generator 기반 drift 검증 | PR blocking; branch는 local projection. selector 공통 코드·판별 불가 변경 시 전체/상위 검증으로 확대 |
| Rulesync 관리 자산 구조 불일치 | strict doctor + generate dry-run | 영향 구조에 대한 PR blocking; 원격 설치는 필요한 조건만 |
| Ruff·rumdl·Biome 규칙 위반 | check-only lint/format | 먼저 **명시적 repository contract vs 순수 style** 구분. 파싱/호환성/채택된 강제 규칙은 PR blocking, 선택적 미관은 로컬 안내 |
| Hook YAML 문법·실행 계약 위반 | `lefthook validate` 및 필요 시 별도 시나리오 테스트 | Hook 자체 변경 시 CI 정적 검사. 설치나 실제 local hook 발화는 검증했다고 주장하지 않음 |
| LLM routing / runtime behavior | fixture 계약 + 필요한 좁은 eval | 기존 deterministic fixture는 유지. model 호출은 위험 근거가 있을 때만 별도 검토; 기본 PR 상시 실행 금지 |
| Ruleset drift / human approval | live Ruleset 확인 + 독립 검토 | 문서 차이 기록. 사용자 승인 없이 설정 mutation/필수 reviewers 변경 금지 |

## 구현 계획

1. **기준선 확보:** 정확한 `main` ref와 branch status 확인, 현재 `mise`/uv/포매터 버전과 baseline lint/format 결과를 읽기 전용으로 조사. 정본 규칙과 충돌하거나 레거시 전체 정리를 유발하는 검사인지 분류. 필요한 변경 파일 대상만 선택.
2. **Projection 영향 경계 보완:** `scripts/generated_artifacts_sync.py`, `scripts/generated_artifacts_validate.py`, `scripts/generated_artifacts.py`와 공통 helper·소유 source의 변경이 해당 projection/전체 projection에 올바르게 퍼지는지 증명. 애매한 경우 넓은 검사 또는 실패. `tests/scripts/`에 selector 변경·입력 삭제·외부 경로·영향 누락 회귀 테스트.
3. **단일 읽기 전용 검사 진입점:** 가능하면 `mise.toml`과 native CLI만으로 Ruff `check`/`format --check`, rumdl `check`/formatter check, Biome `check`(필요시 formatter 전용)를 구성. 실제 pin 버전의 옵션을 검증하고 동일 규칙을 YAML/파이썬 wrapper에 복제하지 않음. `mise run format-changed`는 write 경로로만 유지. baseline에 맞춰 종류별 검사 범위와 빌드 산출물 제외를 설정.
4. **Lefthook 조정:** 로컬 agent용 staged 파일 검사 위주로 빠르게 피드백. 부분 스테이징 시 index 내용과 worktree의 불일치, 파일명 공백·한글, 삭제·rename, formatter 도구 미설치, 실패 코드, 기존 generated-artifacts sync의 stage 범위를 테스트. 일반 source 자동 포맷·stage 금지. pre-push pytest 유지 여부는 비용·유용성 측정으로 결정.
5. **Branch Check/PR Gate 보강:** CI에 merge-critical static checks, 필요시 `lefthook validate` 배치. Hook이 없던 plugin/API 직결 커밋에도 branch/PR 이벤트가 검사를 제공해야 함. Required PR Gate를 주 판단 경계로 유지. `HEAD^1` 비교가 merge ref의 base parent를 뜻한다는 전제와 이벤트/checkout 조건을 테스트. CI에서 수정·commit·push 금지.
6. **효율 비교:** 동일 SHA의 Branch/PR 이중 pytest, static checks, Rulesync 다운로드와 mise 도구 설치 비용을 로그로 기록. **무조건 제거하지 않고** 시점·실행 비용·실패 발견 시점·독립 신뢰성을 비교하여 실익 있는 중복만 제거. 작은 repo에서는 기존 중복 유지가 최적일 수도 있음. CI 캐시·path filter·검사 matrix는 근거 없이 확대하지 않음.
7. **정본·운영 정합성:** `docs/development/ci.md`, `formatting.md`, `testing.md`, `validation.md`, `docs/tools/lefthook.md`, `docs/tools/mise.md` 중 **실제 의미가 변한 owner만** 수정. GitHub Ruleset 최신-base 및 control-surface human approval 문제는 영향·비용·권한을 따로 판단하고, 정책 변경이 필요하면 명시 승인 요청.

## 완료 기준과 테스트 설계

- [ ] 로컬 agent 경로와 플러그인/API 원격 커밋 경로에서 같은 merge-critical 실패를 각각 검출할 수 있다. CI는 Hook의 존재/통과를 **가정하지 않는다**.
- [ ] 파일 타입별 위반 시나리오(`.py`, `.md`, `.json[c]`, frontmatter)의 **차단/비차단 기준**과 실제 오류 코드가 명시되어 있다. 순수 스타일은 강제 계약 없이 범용 병합 차단으로 승격하지 않는다.
- [ ] 영향 판별 불가·공통 스크립트 변경·source 삭제·결과 생성 누락 시 projection 검증이 침묵하며 통과하지 않는다.
- [ ] staged-only 선택은 미스테이징 변경을 임의 포함·포맷·stage하지 않으며 기존 projection 동기화 계약을 깨뜨리지 않는다.
- [ ] `PR Gate`의 read-only 권한·merge candidate 검증·required check 이름/연동이 보존된다. 실제 Actions 실행에서 새 static checks가 실행됨을 확인한다.
- [ ] Hook 설치 없는 GitHub Plugin/API 방식의 branch commit과 PR update를 대표 시나리오로 다루고, 동일 SHA와 변경 경로에 대한 CI 로그를 남긴다.
- [ ] 새 검증기/선택 규칙의 정상·실패 테스트가 통과하고 기존 generator/pytest 회귀가 없다.
- [ ] 중복 제거 여부는 실행 시간·비용·진단 품질을 측정하여 결정하고, 제거하지 않아도 정당한 결과로 남긴다.
- [ ] 정본 문서·mise task·Hook·Actions가 일관되며 기존 정책(선택적 Hook 설치, 무단 write-back 없음)을 보존한다.
- [ ] 통제 표면 변경분은 해당 변경에 의존하지 않는 검토 근거를 확보하고 사람의 명시적 승인 후에만 merge한다.

## 점검과 인계

이 문서는 **구현 작업의 비정본 계획**이다. PR 본문의 체크박스는 구현 완료 때만 체크하고, GitHub checks 성공을 실행 경계 전부의 성공으로 확대하지 않는다. 구현자는 코드·설정 변경 전에 관련 `AGENTS.md`, [GitHub 정책](../../docs/development/github.md), [CI](../../docs/development/ci.md), [Formatting](../../docs/development/formatting.md) 및 `mols-ci-design`의 원본을 다시 읽고, 변화가 큰 단계마다 자체 검토 후 다음 단계로 넘어간다.

인계 대상의 기본 완료 상태는 `PLAN READY / IMPLEMENTATION NOT STARTED`이다. 프로젝트 내부 명령·대화·로그·외부 계정 정보는 이 PR에 복제하지 않는다.
