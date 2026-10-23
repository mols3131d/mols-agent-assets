# Independent Testability — 심층 설계·리뷰 기록

PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255)  
날짜: 2026-10-23  
적용 자산: `mols-test-design` — 범용 소프트웨어 테스트 설계·품질 판단

## Prepare: 목표, 경계, 수용 조건

**Goal:** 병렬 개발자가 서로의 *내부 구현*을 몰라도 자기 책임 범위의 테스트를 설계·실행·유지할 수 있도록 하는 **Independent Testability** 판단을 Skill에 내재화한다. 물리적인 폴더 수, 테스트 수, 에이전트 수를 늘리는 것이 목표가 아니다.

**In scope:** Skill의 activation, 테스트와 모듈의 소유/관찰 경계, 상태/fixture 격리, consumer/provider contract의 독립 검증과 좁은 통합 evidence, 평가 사례 및 maintainer 기준. **Out of scope:** 실제 프로젝트의 module architecture redesign, 모듈/테스트 디렉터리 전면 재배치, CI provider/merge policy 변경, 별도 subagent 필수화.

**Acceptance:** (1) 내부 변경에 brittle하지 않되 사용자·consumer 계약은 보호, (2) 병렬 작업자가 필요한 테스트를 좁게 실행/유지, (3) 경계를 가로지르는 결함의 증거는 보존, (4) 요구사항/현재 구현/테스트 oracle의 권한 분리, (5) positive/near-miss/adversarial eval fixture, (6) 관련 생성물과 CI 검증.

## Parent Loop 1 — 현행 Skill의 gap 확인

**Research:** 기존 `SKILL.md`는 `Ground the oracle`, `Choose the observation boundary`, `Check reliability and cost`를 갖는다. 하지만 *다른 컴포넌트의 비공개 함수를 import한 assertion*, *호출 순서를 정확히 spy하는 테스트*, *외부 컴포넌트의 상태·fixture에 의존한 테스트*, *한 모듈 변경이 무관한 테스트 스냅샷을 깨는 현상*에 대한 명시적 판단은 약하다.

**Plan:** source ownership을 침범하지 않으면서 관찰 대상과 테스트의 변경/실행 범위를 정렬한다. 메타데이터는 'cross-component test coupling'이 주제일 때만 activation할 수 있도록 좁게 보강한다. 본문에는 새 절차/매개변수/Reference 대신 기존 judgment 두 부분에 integrated guideline을 더한다.

**Review 1 — challenge:** '격리'를 최우선으로 고정하면 실제 상호작용이 깨져도 mock이 통과하도록 설계될 수 있다. 또한 모든 구현 내부를 몰라야 한다는 말은 **자기 소유 모듈**의 내부 불변식 검증까지 금지하는 것이 아니다. 따라서 경계 밖의 *소유하지 않은 구현*과 자기 모듈의 내부 동작을 구별해야 한다.

Disposition: **absorb** — 좁은 자식 범위로 contract 대 통합 검증 간 균형 검토. 단순한 폴더 분리·mocking 강제는 **reject**.

## Nested child — 경계 독립성 vs 실제 상호작용 검증

**Strict subset:** 서로 다른 작업자/모듈이 소유한 consumer/provider 경계에서 어떤 테스트로 *내부 구현을 모르는 독립성*을 확보하되 실제 통합 결함은 잡을 수 있는가. Parent의 scope/권한/검증 조건을 상속하고 별도 Run budget이나 독립 실행 에이전트를 만들지 않는다.

**Research evidence:**
- [Pact 공식 Introduction](https://docs.pact.io/): Consumer/provider가 합의한 요청·응답 계약을 각각 검증해 상대편 구현 없이 호환성 evidence를 마련한다. provider의 내부 구조를 테스트할 필요는 없다.
- [Pact Provider Verification](https://docs.pact.io/provider): 아직 배포되지 않은 로컬 provider에 계약 검증을 실행해 병렬 피드백을 얻는다. 배포된 서비스만 대상으로 삼으면 실행 병목이 생긴다.
- [Pact FAQ](https://docs.pact.io/faq): consumer-driven contract test가 provider 비즈니스 로직과 모든 E2E 테스트를 대체하지 않으며 모든 API 또는 조직에 도구 적용이 적절한 것은 아니다.
- [Martin Fowler, Test Double](https://www.martinfowler.com/bliki/TestDouble.html): Mock/Stub/Fake/Spy는 서로 다른 기술적 역할을 가진다. 특정 상호작용을 검증할 목적이 있는 spy까지 관성적으로 금지하면 안 된다.

**검토한 반례:**

| Scenario | 올바른 설계 판단 | 피해야 할 잘못된 최적화 |
| --- | --- | --- |
| B의 내부 리팩터링 후 A의 mock-call sequence assertion만 실패 | A의 소비자 관찰 결과/안정 계약을 기준으로 재설계. 구현 상세 호출 순서는 필요할 때만 확인 | 내부 API까지 모든 테스트에 노출, A/B를 물리적으로 분리하면 충분하다고 주장 |
| Producer가 JSON field를 변경하면서 consumer와 호환성 깨짐 | 해당 요청/응답 계약을 소비자와 제공자 측에서 좁게 검증 | 단위 테스트 독립성을 이유로 실제 경계 검증 제거 |
| 결제/원장 변경이 DB 트랜잭션 원자성에 의존 | 트랜잭션을 실환경에 가깝게 관찰하는 가장 작은 integration test | 모든 의존성을 mock으로 대체해서 실패·롤백을 숨김 |
| 두 테스트가 공유 서버/전역 clock을 동시에 사용 | 필요한 fixture/state/time isolation 확보. 불가능하면 명시적으로 직렬/격리된 검증 공간을 사용 | 아무 근거 없이 병렬 실행 가능 또는 단순 retry로 성공 주장 |
| 한 모듈에 이미 적절한 unit contract tests 존재 | 기존 검사 재사용; 새 layer나 test package를 강제하지 않음 | 모듈마다 unit/contract/E2E 파일을 획일적으로 증설 |
| Test가 성능 또는 순서를 공개 계약으로 보호 | 그 계약이 실제로 존재하면 허용 가능한 순서/시간 assertions | 'implementation detail이므로 금지'를 기계적으로 적용 |

**Child Review:** `absorb` — '독립적인 변경/검증'은 **소유하지 않은 구현에 대한 불필요한 결합을 줄이는 것**이며, 필요한 cross-boundary compatibility는 **실제 계약 테스트나 초점 있는 통합 검증으로 남기는 것**. `reject` — 모든 mock 금지, 모든 shared fixture 금지, 모든 E2E 삭제. `unresolved` — 도메인별 안정된 계약이 없거나 소유자가 모호하면 아키텍처/요구사항 결정을 요청할 수 있으며 Skill이 이를 스스로 정의하지 않는다.

**Parent impact:** test level 판단에 '다른 소유자의 내부를 알아야 하는가?'와 '검증을 내 작업 경계에서 재현할 수 있는가?'를 포함한다. 실패의 원인이 실제 계약 위반인지 우연한 내부 변경인지 분리한다.

## Implementation plan

1. 단일 `SKILL.md`의 description과 기존 judgment 두 곳에 **독립적 테스트 가능성** 판단을 통합한다. 새 개발 아키텍처 Skill, Reference, tool/runner 설치는 만들지 않는다.
2. eval fixture에 positive/near-miss/behavior를 추가하여 coupling과 필요한 integration의 균형, 병렬 fixture isolation, 호출 순서가 실제 계약인 예외를 다룬다.
3. `docs/skills/mols-test-design/goal.md`에는 지속할 유지보수 목표만, `evaluation.md`에는 결과를 구분할 평가 질문만 남긴다.
4. canonical description 변경에 따른 `route/skills.jsonl`은 **공식 generator의 entry encoding, sorting과 같은 algorithm**으로 source-derived entry만 갱신하고 현재 head에서 검증한다.
5. 다관점 순차 Review: (a) correctness/contract loss, (b) parallel change/test isolation, (c) portable/context cost, (d) routing/over-activation. 독립 서브에이전트가 실행한 것처럼 주장하지 않는다.
6. GitHub PR Gate의 실제 테스트·projection·Rulesync 결과를 확인하고 실행하지 않은 model behavior eval을 PASS로 표시하지 않는다.

## Evidence limits

이 문서는 기술적 설계 검토와 루프 전환 결과다. 외부 문서는 원리와 반례의 근거이지 `mols-test-design`의 실제 모델 성능 향상을 측정한 실험이 아니다. 구현 뒤 루프별 Review와 validation evidence를 이어서 기록한다.
