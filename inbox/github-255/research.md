# mols-test-design — 조사 기준선

PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255)  
조사 단계: repository-owned 기존 자산 및 책임 경계 확인. 외부 방법론 비교와 실제 Skill 평가 결과는 아직 확보하지 않음.

## 문제

범용 coding context에는 변경한 동작과 중요한 실패 경로를 최소 유용 비용으로 검증하라는 원칙이 있지만, **무엇을 검증할지와 어떤 형태의 테스트가 충분한지** 판단하는 재사용 가능한 전문 Capability는 현재 라우트 목록에서 확인되지 않는다. 테스트 개수나 coverage 수치 대신 계약 중심의 테스트 설계와 유지보수 비용에 대한 판단을 분리할 가치가 있는지 검증한다.

## 관찰된 기존 책임

| Source | 현재 담당 | 신설 Skill이 재정의하지 않을 것 |
| --- | --- | --- |
| [coding-context](../../src/rulesync/.rulesync/skills/coding-context/SKILL.md) 및 [mols-coding-context](../../src/rulesync/.rulesync/skills/mols-coding-context/SKILL.md) | 구현·변경 전반의 engineering judgment, 가장 값싼 유효 검증 | 일반 코드 변경/구현 workflow |
| [mols-ci-design](../../src/rulesync/.rulesync/skills/mols-ci-design/SKILL.md) | PR admission, cost, trigger, impact routing, blocking/deferred evidence | 테스트의 실행 위치와 merge policy |
| [mols-agent-asset](../../src/rulesync/.rulesync/skills/mols-agent-asset/SKILL.md) | Agent Asset validation, routing/behavior evaluation | Agent Asset 특화 계약과 eval 절차 |
| [Testing policy](../../docs/development/testing.md) | 이 저장소가 소유한 executable behavior의 deterministic test 의미 | 특정 저장소의 테스트 정책 |
| [Evaluation policy](../../docs/development/evaluation.md) | runtime/model-dependent behavior evidence의 범위 | 테스트 성공과 agent 행동 성능을 동일시하는 해석 |
| [Executable Output Checks](../../catalog/patterns/software-engineering/executable-output-checks.md) | 관찰 가능한 산출물 검사 메커니즘의 참고 패턴 | 저장소 전체의 새 강제 규칙 |
| [Source-Mirrored Test Structure](../../catalog/patterns/software-engineering/source-mirrored-test-structure.md) | 테스트 파일 탐색성을 위한 배치 패턴 | 모든 대상의 디렉터리 구조 |

이 목록은 새 Skill과의 **책임 중복을 판단하기 위한 초기 관찰**이며 신설의 효과를 증명하는 평가 결과는 아니다.

## 초기 설계 가설

1. 새 Skill의 activation은 테스트 **전략·경계·충분성·품질을 판단할 때**에 초점을 맞춘다. 일반적인 코드 작성 요청마다 자동 활성화하지 않는다.
2. 계약/위험 → 관찰 가능한 outcome → 가장 작은 신뢰 가능한 테스트 수준·케이스·oracle → 현재 검증 한계 순으로 판단하되 고정 보고 양식을 모든 요청에 강제하지 않는다.
3. Testing pyramid, unit-first, coverage threshold, mocking 방법, TDD 같은 보편적 처방을 피한다. 도메인과 실행 환경의 계약을 우선한다.
4. 기존 테스트가 충분하거나 추가 테스트의 가치가 낮다면 '새 테스트를 만들지 않음'도 허용한다.
5. 고장 원인을 숨기는 flaky fixture, 과도한 mocking, 동일 구현을 재현하는 테스트와 false-positive/false-negative를 구별한다.

## 조사해야 할 질문

- 기존 자산의 일반 testing judgment와 분리했을 때 routing 및 결과 품질이 실제 개선되는가?
- Test level 선택에 universal taxonomy가 필요한가, 아니면 검증 경계/observability/비용 중심이 더 적합한가?
- 변화 범위, 위험, 현재 evidence에 따라 '새 테스트 필요 없음'과 '테스트 필요'를 어떻게 구분하는가?
- Unit/integration/contract/E2E 및 property-based, mutation, model-based 등은 언제 핵심 원칙이고 언제 선택적 참고 지식인가?
- 프로젝트에 기존 suite나 런타임이 없는 경우 구현 가능성과 검증 불가능성을 어떻게 구분하는가?
- Artifact 유형(Skill의 테스트 설계 vs Agent 자체의 behavior eval)의 near-miss에서 올바른 owner를 선택하는가?
- ChatGPT처럼 제한된 런타임에서도 실행 불가를 근거 없는 PASS로 바꾸지 않고 유효한 계획·검토 결과를 낼 수 있는가?

## 검증용 대표 상황 후보

| 상황 | 기대되는 판단 |
| --- | --- |
| 순수 함수의 경계·오류 조건 | observable contract와 비중복 representative cases |
| 외부 API 또는 데이터 저장을 수반한 변경 | unit mock만으로 부족한 통합/계약 근거 구분 |
| 회귀 버그 재발 방지 | 실패 재현과 안정적인 regression oracle |
| 기존 flaky 테스트 정리 | 불안정성 원인과 격리·시간·상태 의존성 판단 |
| 문구·형식만 바뀌는 저위험 변경 | 추가 behavioral tests를 자동 강제하지 않음 |
| 'CI를 빠르게 만들어줘' | `mols-ci-design`에 양보 |
| '에이전트 Skill의 trigger를 평가해줘' | Agent Asset eval 책임에 양보 |
| 'pytest 실패 로그 디버깅' | 일반 coding/debugging 작업을 불필요하게 가로채지 않음 |

## Research Exit

공식·실무 reference에서 결과를 바꿀 만한 test design principle만 조사하고, 위 가설 중 무엇이 유지·수정·폐기됐는지 근거와 함께 기록한다. 단순 링크 수집이나 방법론을 빠짐없이 열거하는 조사는 목표가 아니다.
