# 심층 조사 루프 Review — 부모/자식 근거 조정 및 설계 인계

- PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255), 2026-10-23
- 근거: [1차 실태 연구](research-agentic-testing.md) → 1차 Review → [중첩 oracle/비용 연구](research-oracle-validation.md) → Child Review → 부모 재검토
- 범위: **조사·기술적 판정·다음 설계 인계**. 실제 Skill 작성, 실행 기반 성능 평가, merge는 이 Run의 대상이 아니다.

## Run 경계

**Goal:** `mols-test-design`의 핵심 책임·우선 검증 원칙을 최신 에이전틱 개발 근거로 검토하고, 근거 한계·반례를 포함한 재사용 가능한 설계 결정까지 정리.

**In scope:** 일반 소프트웨어 테스트 설계, 오라클, 테스트 수준·반례, 결과 판정, 검증 비용, 다른 Agent Asset과의 ownership. Out of scope: PR의 최종 `SKILL.md` 구현, 테스트/모델 실측, CI workflow 수정.

**Acceptance:** (a) 최신 근거 직접 비교, (b) 적어도 하나의 결과를 바꾸는 반론/대안 검토, (c) 중첩 자식의 strict-subset scope와 부모 인계 기록, (d) 향후 설계에 적용 가능한 결론과 미확인 사항을 분리, (e) PR #255 인박스 문서로 지속.

## 관찰된 실행 구조 (mols-loops)

| 범위 | 단계 | 새로 확인하고 바뀐 결정 | 종료 검토 |
| --- | --- | --- | --- |
| Parent Main Loop 1 | Research → Plan → Work(실태 조사 문서) → Review | '더 많은 테스트' 대신 requirement, oracle, 독립 수용 조건을 기준으로 검증 | 추가 확인: reference 없는 oracle, mutation 비용, multi-agent 의무화의 타당성 |
| Nested child (strict subset) | Research → Plan → Work(oracle/비용 연구 문서) → Review | reference-validity 와 fault-sensitivity 분리, independent oracle, escalation cost 분석 | 결과 확보·부모에 인계. 권한/Goal 확대 없음 |
| Parent Main Loop 2 | Research(자식 인계 반영) → Plan → Work(종합 판정) → Review | 기술 선택을 위험·조건 기준으로 재조정, 테스트 설계 Skill의 책임과 next evaluation 정의 | 조사 Goal 충족 후보. 구현·runtime uplift는 후속 단계로 유지 |

계산: **substantive Review 3회 = loops_used 3**, nested child가 동일 Run budget을 공유하며 별도 카운터를 만든 것은 아니다. 위 단계의 독립성은 질문 범위의 분리이지 별도 Subagent 병렬·격리 실행을 뜻하지 않는다.

## 1. 충돌했던 주장과 근거 중심 판정

| 경쟁 관점 | 검토한 증거 | Disposition | 결정 |
| --- | --- | --- | --- |
| 'TDD가 최신 에이전틱 개발의 사실상 필수 프로세스' | [survey](https://arxiv.org/abs/2609.12012)에서는 test-driven 역할을 분리하고 [VS Code guide](https://code.visualstudio.com/docs/agents/guides/test-driven-development-guide)는 TDD를 선택 가능한 구체 워크플로로 제시 | **reject** | Skill의 필수 단계로 Red/Green/Refactor를 강제하지 않는다 |
| 'Code-first이면 실제 테스트 oracle은 충분히 독립적이다' | [error propagation preprint](https://arxiv.org/abs/2607.05139)에서 faulty implementation에 따라 만든 tests의 결함 검출 약화(14% vs 25%) | **absorb** | 구현을 기대값의 유일한 출처로 삼지 않는다. specification/consumer property 우선 |
| '실행되는 테스트는 이미 올바른 테스트다' | [ReqTestAgent](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1960601/full)의 generation-only invalid 51%~68%, [OpenAI benchmark audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)의 명세/테스트 불일치 | **reject** | 실행 가능성, 정상 reference 통과, 결함 판별력, acceptance completeness를 독립 판정 |
| 'Mutation score가 높으면 test oracle이 올바르다' | [SWE-Mutation](https://aclanthology.org/2026.findings-acl.1976/), [Hamidi et al.](https://arxiv.org/abs/2609.09315)에서 실행 oracle과 실제 결함 검출 간 간극 확인 | **reject** | Mutation은 필요 시 targeted escalation, 잘못된 oracle을 정당화하는 지표가 아님 |
| 'Multi-agent test writer/verifier 팀은 항상 효율적이다' | [TDFlow](https://aclanthology.org/2026.eacl-long.70/) 긍정 사례, [BDAI comparison](https://doi.org/10.1109/BDAI70753.2026.11655121) 반례, [ReqTestAgent](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1960601/full) 시간 비용 | **reject** | 전문 역할은 선택적; 독립 증거와 가장 값싼 검증이 우선 |
| '실행할 수 없으면 테스트 설계 지원은 무의미하다' | [Agentic Rubrics](https://aclanthology.org/2026.acl-long.697/)의 non-execution 평가 signal | **reject** | 정적 설계/검토는 허용하되 실행 근거·PASS와 엄격히 구분 |
| '기존 coding-context면 충분해 신설 Skill 가치가 확정되지 않음' | 현재 두 범용 coding Skill은 일반 judgment를 소유, 새 전문 Skill은 test-specific oracle quality 판단을 명확히 좁힐 수 있음 | **unresolved for performance** | 신설 설계 근거는 충분하나 **실제 uplift는 비교 Eval이 필요** |

## 2. 구현에 넘길 설계 계약 후보

> 아래는 조사에서 도출한 **후보**이지 이미 구현된 Skill 실행 계약이 아니다.

### 책임

'테스트가 **무엇을 증명해야 하는지**와 **어떤 증거가 충분한지**를 설계하고 기존 테스트의 검증 가치를 리뷰한다.'

1. **Select protected claims:** 요구사항·공개 계약·불변식·과거 결함 중 중요한 것을 식별한다. 사용자 목적과 시스템 경계가 중요하다.
2. **Ground oracles:** 기대값/관찰 포인트의 출처를 spec, reference example, consumer contract, domain property에서 정당화한다. 현재 구현을 무비판적인 정답으로 사용하지 않는다.
3. **Choose discriminating scenarios:** 정상/경계/실패/회귀 중 실제 결함에서 다른 결과를 내는 대표 케이스. **'이 테스트가 어떤 잘못된 구현을 실패시키는가?'**를 확인한다.
4. **Choose minimal execution surface:** Unit/integration/contract/e2e 구분은 관찰 범위/실패 위험과 비용으로 판단한다. Coverage 목표나 단위 테스트의 양을 보편적으로 강제하지 않는다.
5. **Review test quality:** over-mocking, oracle tautology, fixture contamination, flaky environment, overly strict implementation coupling, missing product acceptance, duplicated tests를 실제 위험에 따라 식별한다.
6. **Calibrate evidence:** 실행한 것, 설계만 한 것, 예상하는 것, 실행 불가를 구분한다. Runtime이 없으면 수동/정적 oracle rubric과 실행 가이드를 제공하되 동등한 PASS라고 하지 않는다.

### Activation과 거절 경계

| 요청 | 선택 방향 |
| --- | --- |
| '이 변경에 무엇을 테스트해야 충분해?' / '경계값과 회귀 테스트 설계해' | **선택** |
| '테스트가 너무 많이 mocking하는지 검토' / '이 fixture가 잘못된 결과를 통과시키나?' | **선택** |
| '원인 모를 flaky suite의 검증 신뢰성 개선' | **선택**(테스트 설계·격리 질문일 때) |
| '이 pytest 런타임 오류를 디버깅해서 코드를 고쳐줘' | 범용 debugging/coding owner 우선, 필요하면 보조 |
| 'PR Gate를 빠르게/안전하게 설계해' | `mols-ci-design` 우선 |
| 'LLM Tool 호출 횟수·Skill trigger를 평가해' | `mols-agent-asset`과 behavioral eval owner 우선 |
| '테스트 코드 하나 작성해' | 구현 주체가 우선, 설계 판단에 실질적 필요가 있을 때만 적용 |

### 보존할 이식성 경계

- Python/JS/Go/Rust, pytest/Jest/Vitest, 클라우드 runner에 대한 hard dependency를 두지 않는다.
- 특정 프로젝트의 `tests/`, `mise`, GitHub Actions 또는 Promptfoo 경로를 Skill 본문에 보편 명령으로 넣지 않는다.
- 기존 Skill이 자동 설치/활성화된다는 전제나 `mols-loops` 호출 의무를 본문에 심지 않는다.
- 복잡한 질문에 적합한 테스트 계획을 제공하되 단순한 요청에는 하나의 구체적인 테스트/의미 있는 반례만 제시할 수 있어야 한다.
- Test generation 도구보다 **테스트 설계 판단**을 Skill owner로 유지한다.

## 3. 효과 검증 제안 — 추후 별도 Work

실제로 새로운 Skill이 도움이 되는지는 **`mols-coding-context` 단독 대비** 공정한 비교로 판단한다.

- **System under evaluation:** 같은 base request, 코드/명세 상태, 사용 모델·runtime, token budget, tool access와 grader.
- **Trigger cases:** no-new-test, 단순 unit, 기존 suite 품질 리뷰, API/DB 통합, flaky, mutation, CI-only, code-only, Agent Eval-only.
- **Behavior cases:** wrong accepted value, hidden missing requirement, redundant assertions, test that mirrors current bug, high coverage but weak oracle, unit-only mock that hides integration bug, no actual runner, delivered-demo-but-not-library.
- **Outcomes:** (a) 잘못된 oracle를 거부하거나 uncertainty 표시, (b) 테스트로 실제 defect 구별, (c) 테스트 과잉 감소, (d) test-level relevance, (e) 실행 근거 진실성, (f) cost/time/context burden.
- **Grading:** 평가 시나리오의 독립적인 요구·known-good/bad implementation·expected failure path가 있을 때 직접 deterministic check를 우선한다. 의미 판단을 model grader에 맡기면 별도 calibration과 ambiguity 관리가 필요하다.
- **Leakage:** 평가용 hidden expected answer, mutants, grader criteria를 test-design agent에 무심코 주입하지 않는다.
- **미실행:** 현재 PR에는 Skill 구현이나 A/B 결과가 없다. '성능 향상됨'은 **아직 주장 불가**.

## 4. 남아 있는 제한과 stopping boundary

- 산업 규모에서 모든 테스트 전략 중 무엇이 범용으로 최적인지 보여 주는 결과는 없다.
- ReqTestAgent는 accepted implementation이 있는 Python 사례; CANDOR 비교는 단일 Java 프로젝트; Microsoft library 사례는 18회 통제 실행이다. 결과를 하나의 수치로 평균 내거나 강제 절차의 증거로 사용하지 않는다.
- '코드를 테스트로 만들고, 테스트로 코드를 확인'의 인과성을 검증하려면 실제 controlled setup이 필요하다. 이 조사에서는 하지 않았다.
- 학술 연구가 사용한 benchmark mutation pool의 대표성·equivalent mutants·data leakage가 모든 도메인에 동일하다고 가정하지 않는다.

**Parent Review / Finalize 후보:** 목표였던 deep research + nested bounded child + 결정 인계에 필요한 근거는 확보했다. 새 자료 추가가 이 Run의 테스트 설계 계약을 materially 바꿀 가능성이 낮고, 남은 실증 gap은 새 Skill 구현과 runtime Eval이 선행되어야 한다. 따라서 추가 검색 대신 **연구를 완료한 상태로 설계 단계에 인계**한다. 이는 PR #255 전체 완료나 merge 승인과 다르다.
