---
description: Rulesync의 파일·필드·타입·의미 계약별 검증 책임과 최소 충분한 CI·테스트 수준을 정하는 최적화 제안서입니다.
---

# Rulesync 검증 수준 최적화 제안서

> **적용 버전 주의:** 이 제안서는 처음에 Rulesync **v16.24.1**을 기준으로 작성되었다. PR #257의 CLI pin은 현재 **v40.2.0**이며, CLI 명령은 유지되지만 `skillsPath` lock·frozen integrity 동작이 바뀌었다. 기존 원칙을 보존하되 구체적 migration과 검증 순서는 [v40 업그레이드 계획](rulesync-v40-upgrade-plan.md)과 [인계 보고서](rulesync-v40-handoff.md)가 소유한다. 16.x 확인 결과를 40.x 실제 실행으로 간주하지 않는다.

## 권고안

**Rulesync의 입력 스키마는 Rulesync가, 저장소 고유의 관계와 생성기는 저장소가, 실제 외부 의존성 설치는 frozen install이 검증한다.** 같은 계약을 Python·pytest·CI에서 각각 재정의하지 않는다.

권장 최소 구성은 기존 `Branch Check` 및 `PR Gate`를 유지하면서 다음을 분리하는 것이다.

1. **항상 또는 현재 PR Gate 안에서 저비용으로:** 루트와 재사용 라이브러리의 `doctor --strict`, 라이브러리의 `generate --dry-run`, repository-owned deterministic pytest·생성 route/index drift.
2. **루트 source/lock이 바뀔 때만:** 루트에서 `rulesync install --frozen` 실행, lock 불변 확인(네트워크·원격 소스의 실제 접근 가능성을 포함).
3. **특정 장애·고위험 변화에서만:** OS별 실제 설치, 새 target의 runtime smoke/Eval, 더 넓은 매트릭스.

**이번 PR #257에는** 이미 결정된 [GitHub transport 복귀](rulesync-github-transport.md)와 불필요한 래퍼·테스트 제거를 우선 적용한다. CI 설계 전체 변경은 독립적으로 검토·실행할 수 있게 한다. 현재 관찰과 배경은 [검토 보고서](rulesync-ci-test-review.md)를 참고한다.

## 무엇을 테스트하는가: 검증 책임의 5단계

| 단계 | 질문 | 최소 충분한 검증 | 이 체크가 증명하지 않는 것 |
| --- | --- | --- | --- |
| A. 형식·스키마 | 파일을 읽을 수 있는가? 필수 키·타입·허용 값이 맞는가? | 각 workspace의 Rulesync `doctor --strict`, 공식 parser·schema | 에이전트가 실제로 올바르게 작동하는지 |
| B. 저장소 고유 계약 | 원본 위치, `targets` 명시, source-to-route 이름·경로 대응이 맞는가? | upstream이 검사하지 않는 **명시적 repository invariant만** 자체 validator/기존 route generation | 전체 Rulesync schema의 적합성 |
| C. 생성 가능성·drift | 설정한 target의 projection을 만들 수 있고, 커밋한 파생물이 최신인가? | 라이브러리 `generate --dry-run`; repo-owned route/index 생성기 비교 | remote lock과 설치 가능성 |
| D. 외부 의존성 | 잠긴 ref·선택·경로·integrity로 실제 설치되는가? | 루트 `install --frozen`을 관련 변경에서 실행 | upstream 최신 버전 여부나 다른 PC의 인증 |
| E. 행동 검증 | 모델/벤더 런타임에서 자산이 의도대로 발동·동작하는가? | 별도 smoke/Eval, **동작 변경이 실제 요구할 때만** | 구조 검증만으로 자동 성립하지 않음 |

이렇게 두는 이유는 실패마다 신뢰할 수 있는 *가장 싼* 근거가 다르기 때문이다. `doctor`를 여러 번 자체 Python 파서로 감싸서 같은 타입을 검사하는 것은 신뢰도를 높이기보다 drift 가능성을 키운다.

## 파일·필드·값 타입에 대한 상세 판단

| 질문 | 권고 | 왜 그런가 / 어디서 검사하는가 |
| --- | --- | --- |
| `rulesync.jsonc` 파일 존재·JSONC 문법 | **검증 필요, 자체 테스트 불필요** | CLI가 실제로 입력을 로드한다. 실패·오타는 `doctor --strict`로 확인 |
| `targets`, `sources`, `transport`, `path`, `skills`의 필드명·값 타입·enum | **검증 필요, 규칙 복제 금지** | pinned Rulesync v16.24.1의 schema/doctor가 contract owner. 필드별 수동 화이트리스트는 유지보수 부담 |
| 오타·알 수 없는 config key | **`doctor --strict` 필수** | non-strict schema가 알 수 없는 필드를 무시할 수 있어 일반 parse만으로는 부족 |
| `SKILL.md`, Rule, Subagent 형식과 frontmatter `name`, `description`, `targets` 타입 | **검증 필요, upstream 우선** | Rulesync가 실제 사용하는 파일 형식과 target parser를 재사용 |
| 재사용 asset의 `targets` **명시 필수**, `["*"]` 사용 금지 | **좁은 자체 검사 고려** | [저장소 Rulesync 정책](../../docs/development/tooling/rulesync.md#target-and-schema)이 upstream보다 엄격하다. Upstream이 허용하는 누락 또는 wildcard를 차단할 필요가 있는지 확인한 뒤 작은 검사만 추가 |
| 원격 source에서 선택한 Skill 이름·실제 `SKILL.md` 위치 | **검증 필요, 수동 파일 열거 금지** | `install --frozen` 및 현 repository route generator의 name drift 검사. 모든 파일명을 별도 snapshot으로 유지하지 않음 |
| `rulesync.lock`의 `lockfileVersion`, `resolvedRef`, integrity 등 모든 필드와 타입 | **자체 전수 검증 비권장** | lock 구조는 upstream-owned. `install --frozen`으로 lock coverage·원격 integrity를 확인하고 route generator의 실제 필요값만 검증 |
| `.agents/route/*.jsonl`의 schema·source 관계 및 갱신 여부 | **저장소 검사 유지** | upstream Rulesync가 아닌 이 저장소의 생성기·route contract |
| 벤더별 projection 결과의 모든 필드·값 snapshot | **기본 비권장** | upstream adapter 계약을 복제하게 됨. 커밋된 output이 있다면 official `generate --check`를 쓰되, 현재 무시되는 vendor projection까지 commit/snapshot으로 강제하지 않음 |
| 특정 vendor semantic, LLM 실제 실행 결과 | **필요한 변경 때만 Eval** | parser와 파일 타입 검사로는 보장 불가 |

**핵심 원칙:** 어떤 필드에 대한 자체 검사를 추가하려면 반드시 “공식 도구가 유효하다고 통과시키지만 이 저장소에서는 머지를 거부해야 하는 구체적인 반례”를 먼저 보여야 한다. 반례가 없으면 새 검사·테스트를 만들지 않는다.

## 현재 두 workspace에 적용할 경계

### 1) 루트 설치 소비자: `rulesync.jsonc` + `rulesync.lock`

루트는 GitHub 소스의 Skill 11개를 잠가 설치하는 **dependency consumer**다. `src/rulesync`의 라이브러리와 같은 단계로 섞으면 안 된다.

- 일반 PR: CLI가 준비되어 있다면 루트 `rulesync doctor --strict`는 값싸게 실행할 수 있다.
- 루트 `rulesync.jsonc`나 `rulesync.lock` 변경 PR: **`rulesync install --frozen`**을 고정된 CLI 버전으로 수행하여 잠긴 selection과 설치 성공을 확인한다.
- `--frozen` 실행 전후에 committed lock이 갱신되지 않아야 한다. 임시 runner의 `.curated/` 다운로드는 source mutation과 구분한다.
- `install --update`나 `--outdated`를 머지 검사에 섞지 않는다. 최신 upstream을 따라가는 작업은 별도 dependency update의 책임이다.
- 외부 GitHub API·네트워크 또는 rate limit 실패는 테스트 실패 원인을 구분해 보고한다. 무조건 retry·토큰 노출·새 전용 workflow는 추가하지 않는다.

**현재 결함:** CI가 `src/rulesync`를 검증하는 것은 맞지만, `rulesync.jsonc`·`rulesync.lock`을 바꾸는 PR이 자동으로 frozen 설치 검증까지 받는 것은 아니다.

### 2) 재사용 자산 라이브러리: `src/rulesync/.rulesync/`

- 현 `doctor --strict`는 유지한다.
- 현 `generate --dry-run`은 **write 없이 생성 가능한지**를 살피는 용도로 유지한다. dry-run 성공을 “커밋된 출력이 최신”이라는 주장으로 바꾸지 않는다.
- `generate --check`는 **Rulesync가 생성한 vendor output을 실제로 커밋하고 동기화를 계약으로 정한 경우에만** 사용한다. 이 저장소는 reusable authored source와 generated vendor projection을 구분하므로, 현재 범위에서 기계적으로 추가하면 오검출 또는 불필요한 generated source 관리가 생길 수 있다.
- Rulesync의 YAML/frontmatter 타입을 다시 구현하지 않는다. 다만 `targets` 명시 같은 repository-only 차이는 작은 검사와 1~2개 대표 부정 사례로 보호할 수 있다.

### 3) 이 저장소가 직접 작성한 tooling

- `routes_repository_generate.py`, `generated_artifacts_validate.py` 등 **우리 코드**는 parsing·선택·충돌·에러 동작을 pytest로 검증한다.
- 단위 테스트는 모든 필드 조합이 아니라 **성공 대표 사례 + 실질적으로 머지를 막아야 할 오류 사례 + 경계 사례**를 우선한다.
- 현재 Rulesync CLI 호출 래퍼의 8개 테스트는 wrapper의 fail-closed 결과 처리라는 가치가 있다면 남기되, CLI 기본 exit code로 안전하게 대체 가능한 경로의 에러 포맷별 테스트는 축소한다. 제거 전에 동일한 실패가 여전히 차단되는지 비교한다.
- Git transport용 별도 installer를 제거한다면 그 구현만 검사하던 4개 테스트는 함께 제거한다.
- `tests/conftest.py`의 Git hook 환경 격리는 필요성 자체와 **session autouse 적용 범위**를 독립적으로 판단한다. 모든 테스트에 대한 무조건적인 삭제/유지는 권고하지 않는다.

## 구현 제안: 새로운 CI 프레임워크 없이

| 위치 / 트리거 | 수행 | Blocking | 변경 여부 |
| --- | --- | --- | --- |
| 기존 `Branch Check` (branch push) | 기존 source check, deterministic pytest, local projection drift | 조기 피드백 | **유지** |
| 기존 `PR Gate` (merge candidate) | 기존 source check, deterministic pytest, generated projection validation | 예 | **유지** |
| 기존 `PR Gate` Rulesync 단계 | 라이브러리 `doctor --strict`, `generate --dry-run` | 예 | **유지; wrapper 축소는 별도 검토** |
| 기존 `PR Gate` 내 루트 config 검사 | 루트 `doctor --strict` | 예 | **작은 단계로 추가 제안** |
| 기존 `PR Gate`에서 루트 `rulesync.jsonc` 또는 `rulesync.lock` 변경 | 루트 `install --frozen`과 lock 불변 확인 | 예 | **선택 실행 추가 제안** |
| 도구 업데이트·transport 변경·실제 OS 문제 | Windows/Linux/macOS 중 영향받는 환경의 실제 설치나 smoke | 필요에 따라 검토 | **상시 PR gate 제외** |

조건부 선택은 기존 PR diff 정보를 재사용하는 **작은 파일 경로 판정**으로 충분하다. selection 실패·base를 찾을 수 없는 경우에는 검사를 **실행하는 쪽으로 fallback**한다. 새 독립 job, 복잡한 path-routing 프레임워크, 대형 test matrix는 만들지 않는다.

CI의 한 단계가 한 계약만 검증해야 한다는 뜻은 아니다. 추가 도구 설치 시간보다 충분한 검증의 가치가 크면 지금의 단일 job을 유지한다. 최적화가 꼭 필요한지 여부는 반복 실행 시간과 실패 종류를 먼저 모아 결정한다.

## 권장 대표 실패 사례 — 무엇이 잡혀야 하는가

| 사례 | 담당 체크 | 새 테스트 코드가 필요한가? |
| --- | --- | --- |
| 루트 config의 `source` 타입을 객체로 바꿈, 지원하지 않는 `transport` 값 입력 | 루트 `doctor --strict` | 공식 CLI가 검출하면 **불필요** |
| `targets`를 `target`으로 오타냄 | `doctor --strict` | 공식 CLI가 검출하면 **불필요** |
| 루트 config에서 Skill을 추가하고 lock selection을 갱신하지 않음 | `install --frozen` | **불필요**, install 실패 근거 확보 |
| 잠긴 commit의 artifact가 누락되거나 integrity가 달라짐 | `install --frozen` | **불필요**, 필요 시 targeted smoke |
| `SKILL.md`가 parsing 불가한 YAML을 포함 | 라이브러리 Rulesync 검증 | **불필요**, upstream이 처리하는 범위 확인 |
| 루트와 분리된 authored Skill의 `targets`를 생략 | 좁은 repository-only contract 검사 | upstream이 허용한다면 **단일 부정 사례 유효** |
| route family가 존재하지 않는 Skill을 참조 | 기존 route generator / pytest | **유지** |
| 저장소가 관리하는 route/index가 stale | 기존 generated projection 검증 | **유지**, 필드별 snapshot 불필요 |
| Git hook 호출 시 임시 Git 저장소에 상위 `GIT_DIR`가 누출 | 대상 Git test/helper에서 재현 | **재현 시 유지** |

**금지할 과잉 검증:** upstream schema를 Python으로 복제한 validator, 모든 vendor target·버전·OS 조합에 대한 PR 필수 matrix, 외부 도구가 발생시키는 모든 warning JSON 변형별 unit test, lock의 각 hash를 직접 다시 계산하는 전수 검사, 현재 repository에서 commit하지 않는 vendor projection의 snapshot.

## 안전하게 도입하는 순서

1. **계약 분류:** 검증 스텝마다 owner·실패 모드·중복을 표시하고 현재 녹색 상태를 baseline으로 남긴다.
2. **PR #257 단순화:** GitHub transport로 복귀, Git 전용 래퍼·테스트 제거, 무관한 hook 격리와 공통 환경 설정은 분리 평가한다.
3. **결핍 보완:** root `doctor --strict`와 변경 시 `install --frozen`을 PR Gate에 추가할지 작은 diff 기반 설계로 구현한다. 도입 전 고정 v16.24.1에서 확인한다.
4. **실패 증거 확인:** 설정 오타·stale lock·stale route·잘못된 authored metadata 사례가 각각 **올바른 단계에서 실패하는지** 확인한다. 필요시 targeted 수동 실험이면 충분하다.
5. **중복 정리:** 실제 검출 경로가 겹치는 테스트부터 제거하거나 범위를 줄인다. 규칙을 코드로 복제하는 대신 upstream 명령으로 대체하고 진단 메시지 품질을 유지한다.

## 완료 판정과 남는 위험

- `main`에 허용할 수 없는 **루트 설정·lock 불일치**, authored input 문제, committed route drift, repository-owned generator regression이 merge 전에 검출된다.
- 줄인 테스트마다 **유지되는 실패 검출 경로**가 확인된다. 사라지는 검출 경로가 있다면 단순화를 보류한다.
- Rulesync 타입/enum/필드 복사본과 관련 snapshot의 추가가 없고, vendor projection·upstream 최신성·모델 행동 검증을 하나의 “Rulesync 테스트 통과”로 오해하지 않는다.
- 루트 frozen 설치는 GitHub API와 외부 원격에 의존한다. 네트워크 장애는 제품 결함과 구분해 진단하지만, 실제 lock/source 계약이 깨졌다는 증거를 조용히 무시하지 않는다.
- 실제 OS·벤더 runtime 호환성과 LLM behavior는 이 설계가 전부 증명하지 않는다. 변경의 영향으로 그 수준의 검증이 merge-critical해지면 별도로 승격한다.

## 근거

- Repository: [PR #257](https://github.com/mols3131d/mols-agent-assets/pull/257), [CI 정책](../../docs/development/ci.md), [Testing](../../docs/development/testing.md), [Validation](../../docs/development/validation.md), [Rulesync 통합 문서](../../docs/development/tooling/rulesync.md)
- 현재 고정 버전 v16.24.1: [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/reference/cli-commands.md), [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/guide/declarative-sources.md)
- Upstream current docs: [Doctor 관련 FAQ](https://rulesync.dyoshikawa.com/faq.html), [Dry Run vs Check](https://rulesync.dyoshikawa.com/guide/dry-run), [Configuration schema](https://rulesync.dyoshikawa.com/guide/configuration)

**상태: 설계 제안 완료. 구현·고장 주입 검증·새 HEAD CI는 별도 작업.**
