# mols-test-design — 조사 기준선

PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255)  
조사 단계: repository-owned 자산 비교 및 2025~2026년 외부 연구·실무 사례 비교 완료(2026-10-23). Skill 구현과 실제 routing/behavior 성능 검증은 미진행.

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

---

## 2026-10-23 최신 에이전틱 개발 테스트 설계 조사

**Scope:** 2025~2026년 공개된 원문·공식 문서·동료심사 논문·프리프린트를 비교한다. 코딩 에이전트가 *제품 코드를 개발할 때 사용하는 software tests*가 주요 대상이다. *에이전트 자체의 행동 평가(evals)*는 독립적인 인접 영역으로 구분한다.

### 판단 요약

1. **Test-first ≠ 항상 TDD.** 테스트는 사전 명세, 후보 코드 선택, 실행 기반 수정, 회귀 보호, 사후 평가 등 서로 다른 결정에 관여한다. 특정 red/green/refactor 단계를 범용 Skill의 의무로 고정하지 않는다. [2026-09-10 survey](https://arxiv.org/abs/2609.12012)
2. **Pass ≠ feature completeness.** 테스트가 통과해도 테스트 대상에만 구현을 맞추고 실제 요구한 deliverable을 누락할 수 있다. 구현 결과물/공개 인터페이스에 대한 별도 acceptance 확인이 필요하다. [Microsoft Research 2026-06](https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/)
3. **Test oracle의 질이 테스트 양보다 중요.** 과하게 엄격한 hidden assertions, 명세 누락, under-testing, 평가 요구와 실제 테스트 불일치는 올바른 구현을 실패시키거나 잘못된 구현을 통과시킨다. [OpenAI 2026-07](https://openai.com/index/separating-signal-from-noise-coding-evaluations/), [SWE-Bench Pro V2 2026-09](https://labs.scale.com/leaderboard/swe_bench_pro_public_v2)
4. **구현과 테스트의 상호 자기확인은 취약하다.** 동일한 잘못된 가정에서 코드와 테스트를 함께 생성할 수 있다. 요구사항·기존 계약·reference behavior·반례에 근거한 oracle 확인과, 고위험일 때 별도 검증 경로를 우선한다. 독립 *agent*를 항상 요구하지 않는다. [2026-09 survey](https://arxiv.org/abs/2609.12012)
5. **실제 feedback이 있는 loop가 유효하다.** failure를 재현할 수 있는 조건, 올바른 실패 이유, 수정 후 성공, 변경 이전부터 통과하던 테스트 유지가 핵심이다. 실행 불가능하면 설계 결과만 보고 실행 근거는 미확인으로 남긴다. [Microsoft VS Code TDD guide](https://code.visualstudio.com/docs/agents/guides/test-driven-development-guide), [Red Hat 2026-10-21](https://next.redhat.com/2026/10/21/red-hat-enterprise-specific-benchmarks-for-coding-agents-swe-bench/)
6. **Context와 운영 비용도 품질 요소.** 에이전트에 모든 검사 절차·프레임워크를 일괄 주입하기보다 활성화 범위를 좁혀야 한다. 검증할 때는 실행 가능한 환경·logs·traces·UI feedback을 노출하고 같은 repository-native tool을 활용한다. [OpenAI harness engineering 2026-02](https://openai.com/index/harness-engineering/), [OpenAI skill guidance 2026-09](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

### 검토한 자료와 적용 가능성

| 날짜 | 원문 | 관찰된 사항 | 근거 범위/주의 |
| --- | --- | --- | --- |
| 2026-10-21 | [Red Hat RH SWE-bench](https://next.redhat.com/2026/10/21/red-hat-enterprise-specific-benchmarks-for-coding-agents-swe-bench/) | 재현 가능한 환경, fail-to-pass(F2P), pass-to-pass(P2P), 무효/불안정 테스트 필터링 | 특정 기업·저장소 기반 벤치마크의 설계 사례. 모든 코드 변경에 동일한 환경을 강제하지 않음 |
| 2026-10-14 | [OpenAI software maintenance](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family) | flaky test 해결 및 CI 최적화를 독립적인 evidence-driven 유지보수 과제로 다룸 | 단일 팀의 실무 사례. 제시된 효율 개선은 타 프로젝트로 직접 일반화 불가 |
| 2026-09-22 | [Scale SWE-Bench Pro V2](https://labs.scale.com/leaderboard/swe_bench_pro_public_v2) | 89개 과제 제거, 테스트와 명세가 충돌한 69개 설명 수정, clean verifier에서 재평가, gold-pass/empty-fail 양면 검사 | benchmark integrity 설계. production testing의 보편 프로세스가 아님 |
| 2026-09-11 | [OpenAI skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | 스킬의 좁은 적용 범위, 짧은 description, 불필요한 지침/스킬 중복 제거 권고 | 최근 모델에 관한 vendor guidance. 독립적인 성능 비교 연구는 아님 |
| 2026-09-10 | [Test-driven approaches survey](https://arxiv.org/abs/2609.12012) | 87개 연구·지원 자료 기반 메커니즘 구분, test availability/validity/feedback/independence 분리 | scoping survey 프리프린트. 개별 방법의 보편 우수성을 증명하지 않음 |
| 2026-07 | [SWE-Mutation](https://aclanthology.org/2026.findings-acl.1976/) | 다양한 변형 구현을 통과시키는 테스트의 판별력 평가; LLM 생성 suite의 검증 공백 | ACL Findings 연구의 특정 benchmark 결과를 모든 모델의 통상 품질로 환산 불가 |
| 2026-07-08 | [OpenAI benchmark audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) | SWE-Bench Pro public split의 상당수에서 명세/테스트 설계 문제 확인 | 모델 평가 데이터셋 품질 감사. 일반 프로젝트의 결함 발생률이 아님 |
| 2026-06 | [Microsoft Research: Building to the Test](https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/) | 18회 제한 실험에서 높은 oracle score와 요구한 라이브러리의 완성이 분리됨 | 프리프린트·특정 Angular 라이브러리 실험. 보편적 발생률 미확정 |
| 2026-04 | [TDFlow EACL](https://aclanthology.org/2026.eacl-long.70/) | 사람 작성 테스트를 바탕으로 역할 분리와 실행 피드백 기반 수정 | benchmark-specific workflow. 모든 테스트 설계에 4개 서브에이전트 강제 금지 |
| 2026-03 | [Testing with AI Agents empirical study](https://arxiv.org/abs/2603.13724) | test-related commits 2,232개 관찰; AI-generated tests의 coverage gain이 사람 작성 테스트와 비교 가능한 사례 | coverage와 assertion 수는 oracle의 진실성·결함 탐지력의 직접 증거가 아님 |
| 2026-01~02 | [Over-Mocked Tests study](https://arxiv.org/abs/2602.00409) | 코드 에이전트의 mocking 추가가 비교 집단보다 많음을 관찰(에이전트 커밋 36%, 비에이전트 커밋 26%) | observational study. mock 자체가 오류라는 인과적 증거는 아님 |
| 2026-01-14 | [Anthropic property-based testing](https://www.anthropic.com/research/property-based-testing) | 모델이 일반 property/invariant를 제안하고 실행 도구가 반례를 찾도록 결합 | Python 주요 패키지 버그 찾기 연구; 모든 도메인에 property-based test가 필요한 것은 아님 |
| 2026 Microsoft | [VS Code AI-assisted TDD workflow](https://code.visualstudio.com/docs/agents/guides/test-driven-development-guide) | red 단계의 유효한 실패 확인, green 후 테스트 재실행, refactor 후 회귀 검사, 역할 기반 handoff | 제공되는 하나의 *선택 가능한* 워크플로 예시. 범용 테스트 설계의 강제 순서가 아님 |
| 2026-02-24 | [METR developer productivity update](https://metr.org/blog/2026-02-24-uplift-update/) | 후속 생산성 실험에서 참가자 선택 편향 때문에 최신 AI 생산성 효과를 안정적으로 측정하기 어렵다고 보고 | productivity trend의 불확실성 참고. test quality의 직접 실험 아님 |

### 에이전틱 개발에서 반복되는 유효 패턴

#### A. Requirement-to-test trace: 검증 대상을 먼저 명시

- 기능 요구, API/데이터 계약, 과거 버그, 운영상 중요한 invariant를 확인한다.
- 각 중요한 claim에 observable outcome 및 올바름을 판정할 oracle을 연결한다.
- 누락되거나 충돌하는 요구는 테스트 코드로 임의 확정하지 않고 명시적 gap으로 표시한다.
- 테스트 자체를 통과하게 만든 것과 deliverable 전체가 존재·연결·동작하는지는 별도로 확인한다.

**설계 의미:** 테스트 파일 수, assertions, raw coverage를 1차 성공 목표로 삼지 않는다. coverage는 누락 탐색 신호이며 적합한 oracle과 구별한다.

#### B. F2P + P2P: 재현과 회귀를 함께 본다

- 이미 존재한 버그라면 변경 전 해당 사례가 **의도한 이유로 실패하는지** 확인한다.
- 수정 후에는 새 사례가 성공하고 기존 관련 동작도 유지되는지 본다.
- 구조적으로 중요한 통합 경계(API, DB transaction, dependency, UI)에서는 단위 mock만으로 전체 계약을 주장하지 않는다.
- 기존 suite에서 충분히 검증하면 새 테스트를 추가하지 않아도 된다.

**설계 의미:** 모든 변경에 테스트를 먼저 만드는 절차를 강제하지 않으면서, 실제 테스트를 추가하는 경우 검증의 판별력을 확보한다.

#### C. Stronger oracles on demand: 중요한 실패에만 추가 기법 적용

- 특성 기반(property-based)/metamorphic: 일반 불변식이 분명하고 사례 폭이 넓을 때
- Mutation/fault injection: 테스트가 실제 결함을 잡는지 의문이고 실행·유지 비용을 감당할 가치가 있을 때
- Differential/reference testing: 기존 구현·이전 버전·독립 구현 등 신뢰 가능한 reference가 있을 때
- Contract/integration/e2e: 격리한 단위만으로 consumer-observable behavior를 증명할 수 없을 때
- Human/domain oracle: 기대 결과가 규칙·정책·제품 의도에 달려 자동으로 정의할 수 없을 때

**주의:** property나 mutation에 대한 정의가 잘못되면 강한 실행 결과도 잘못된 결론을 줄 수 있다. 독립 검증이 필수인 맥락과 단순한 코드 변경의 비용을 구분한다.

#### D. Review the test: 테스트도 결함 있는 코드다

- 실패하지 않는 빈 assertions, 기존 구현만 그대로 복제하는 기대값, 변화와 관계없는 snapshots를 경계한다.
- mock이 보호할 실제 경계를 가리고 있지는 않은지 검토한다. mock 사용 자체는 금지하지 않는다.
- flaky test는 재시도로 감추지 않고 time/order/shared-state/network/concurrency 원인과 검증 환경을 분리한다.
- test failure가 target defect인지 fixture/runner/environment defect인지 판단한다.

#### E. Independent evidence ≠ multi-agent ceremony

코드 생성자와 동일한 이해에 갇히지 않도록 **독립 요구 근거**와 반례가 중요하다. 고위험이면 별도 reviewer, 새 context, 다른 oracle 또는 isolated runner를 고려할 수 있으나, 모델 수나 agent 수가 직접적인 근거 품질은 아니다. 새 역할을 하나 더 호출하기보다 단일 authoritative specification이나 실제 실행 결과가 더 효과적일 수 있다.

### 설계 원칙으로 채택 / 채택하지 않을 것

| 결정 | 판단 | 이유 |
| --- | --- | --- |
| Observable behavior → oracle → minimal sufficient test | **채택** | 테스트 품질과 유지비용에 직접 연결 |
| 중요한 누락/경계/실패/회귀를 위험 기반으로 선택 | **채택** | 넓지만 빈약한 suite보다 적합 |
| 설계 근거와 실행 결과의 분리 | **채택** | 실제 검증 근거 없는 성공 주장 방지 |
| 테스트 생성 후 oracle 자체를 검토 | **채택** | 자기확인, 과검증, 미검증 위험 감소 |
| 실사용자 인터페이스/통합 경계를 필요 시 테스트 | **채택** | 단위 테스트만으로 불충분한 계약 보완 |
| 구현과 테스트의 별도 실행자/서브에이전트 항상 사용 | **비채택** | 격리 비용 대비 이득이 조건부; 독립 oracle이 더 본질적 |
| 모든 변경에 strict TDD red/green/refactor | **비채택** | 개발 단계의 여러 방식 중 하나일 뿐 |
| 항상 e2e/property-based/mutation testing 수행 | **비채택** | 도메인 특성·위험·비용·툴 유무에 의존 |
| 일정 coverage 수치, test count, assertion count 강제 | **비채택** | 무엇이 보호되는지 또는 올바른 oracle인지 증명하지 못함 |
| 특정 Python/JS tooling, Docker, Promptfoo, CLI 의무화 | **비채택** | 이식성 및 타 프로젝트 적합성 악화 |
| Skill이 CI admission/merge 정책을 직접 소유 | **비채택** | 테스트 설계와 CI orchestration은 다른 결정 |

### 최소 Skill behavior contract 제안

**Activation:** 테스트 전략 수립, 추가할 검증 사례 선택, 기존 테스트의 충분성/오라클/신뢰성 검토처럼 *테스트 설계 판단*을 요청할 때. 단순 코드 설명, test runner 에러의 즉각적인 디버깅, CI YAML 작성이나 Agent Asset의 런타임 eval 설계만 요청하면 해당 owner를 우선한다.

**내부 판단 순서(필요한 부분만):**

1. **Claim & consequence** — 검증하려는 behavior/contract와 실패 비용
2. **Available evidence** — 기존 suite, 명세, reference behavior, 실행 환경
3. **Oracle & counterexample** — 무엇을 보면 참/거짓인지, 어떤 defect에서 테스트가 실패해야 하는지
4. **Smallest sufficient scope** — 필요한 test level, 대표 정상·경계·실패/회귀 시나리오; 테스트 미추가도 허용
5. **Quality & evidence boundary** — 독립성·flakiness·mocking·관찰 한계, 무엇을 실제 실행/확인했는지

이 순서는 사고를 돕는 설계 기준이며 모든 요청에 고정된 표·단계를 출력하라는 의미가 아니다. 고위험 의존성·컨텍스트가 모호하면 질문하거나 가정을 명시하고, 제한된 챗봇 환경에서도 실행한 것처럼 말하지 않는다.

**검토할 출력:** 대상 계약, 꼭 필요한 테스트 시나리오·oracle·test scope, 기존 증거, 남은 gap과 우선순위. 특정 testing framework API나 코드 템플릿은 타겟이 정해진 경우만 사용한다.

### 신설 타당성에 대한 반론

- **반론:** `mols-coding-context`에 이미 최소 유효 검증의 기본 판단이 있으므로 새 Skill은 중복일 수 있다.
- **재평가:** 독립 capability는 *test-specific 선택·충분성·oracle 평가*에 집중하고 범용 코딩 workflow/권한/실행을 소유하지 않으면 별도 activation 가치가 있다. 하지만 실제 routing/behavior 결과의 개선은 아직 실험하지 않았다. Skill을 만들고 평가할 때 단순 coding-context-only baseline과 비교해야 한다.
- **반론:** TDD를 강제하면 작업 품질이 좋아지지 않는가?
- **재평가:** Microsoft VS Code의 단계형 workflow와 TDFlow는 유용한 **사례**이나, 세분화된 TDD 절차는 workspace/변경 유형에 따라 비용과 의존성이 높다. 새 Skill에 고정 phase workflow를 주입하면 좁고 이식 가능한 design capability를 흐린다.

### 후속 조사·평가 과제

1. `mols-coding-context`만 사용했을 때와 새 Skill을 적용했을 때 **동일 시나리오에 대한 oracle 질/누락/과잉 테스트**를 비교한다. 이 단계에서는 성능 향상을 주장하지 않는다.
2. Positive/negative/near-miss activation 평가에 단순 함수, DB/API 통합, 회귀, flaky suite, no-new-test, CI-only, Agent Asset eval-only를 포함한다.
3. 프롬프트와 기대 결과가 충돌하는 case, 구현을 복제하는 잘못된 oracle, 실제 기능이 빠졌지만 superficial tests가 PASS하는 case를 별도로 검증한다.
4. 사용한 runtime/model, test access, execution 가능 여부, task budget, grader와 결과를 명시한다.
5. 별도 reference를 둘지 결정할 때 progressive loading으로 실제 context 절감이 있는지만 판단한다. 지금은 test taxonomy/reference를 필수 파일로 신설할 근거가 없다.

**Research 결론:** 신규 `mols-test-design`은 좁은 책임의 선택 가능한 Skill로 타당하지만, 효과성은 구현 후 비교 평가를 통해 확인해야 한다. 2026년의 강한 신호는 '더 많은 tests'가 아니라 **검증하려는 계약에 대한 신뢰할 수 있는 oracle, 실행 가능한 반례, 제한된 feedback loop, 독립된 acceptance evidence**다.
