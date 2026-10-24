# 중첩 조사 루프 — Oracle의 유효성·결함 판별력·검증 비용

- Parent: [research-agentic-testing.md](research-agentic-testing.md)의 1차 Review에서 결정한 좁은 증거 공백.
- Child scope (strict subset): **AI가 생성한 테스트의 기대 결과가 틀리지 않는지**, **실제 결함을 구분하는지**, **추가 검증이 비용만큼 가치가 있는지**만 판단한다.
- Parent로부터 계승: portable skill, 기존 asset-owner 경계, research-only 목적, PR #255의 Draft status, 같은 Loops Run budget. 새 Run이나 별도 권한이 아니다.
- 검증 방법: 동일 주제의 상반되는 empirical 결과를 비교하고 reference가 존재/부재하는 경우, 실행 가능/불가능한 경우를 분리했다.

## Child Research: 주장-근거-반례

### C1. 기준 구현을 통과하는 테스트는 필요하지만 그 자체로 충분하지 않다

[ReqTestAgent (2026-10-19, peer-reviewed)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1960601/full)은 25개 기본 과제에서 파생한 100개 모호한 요구사항 인스턴스에서 테스트 생성 과정을 비교했다.

| Configuration | Canonical pass | Effective mutation (macro average) | 평균 model-request time |
| --- | ---: | ---: | ---: |
| Direct generation | 0.490 | 0.361 | 9.07 s |
| Direct + execution verifier | 1.000 | 0.655 | 14.05 s |
| Full ReqTestAgent | 1.000 | 0.678 | 64.46 s |

- Verifier의 이득은 **틀린 기대값/불일치 테스트를 실제 accepted reference와 대조**한 것이다.
- Full pipeline은 direct+verifier 대비 effective mutation score +0.023, model-request 시간 약 4.59배. 차이를 무시할 수 있다는 뜻이 아니라 **비용 대비 보편적 의무화를 뒷받침하지 않는다**는 뜻이다. 더 강한 기록·추적이나 높은 위험이면 복합 워크플로가 유리할 수도 있다.
- Effective macro mutation 0.678과 pooled mutation 492/756=0.651은 분모·가중치가 달라 직접 혼합하면 안 된다.
- **핵심 경계:** *accepted reference가 있을 때*의 결과다. 존재하지 않는 신기능/초기 명세에 임의의 현재 구현을 정상 기준으로 채택하면 오히려 잘못된 동작을 고착할 위험이 있다. 해당 경우 spec/example/기존 consumer contract, domain acceptance 또는 사람의 결정이 먼저 필요하다.

**Child judgment:** 새 Skill은 '가능하면 reference/기존 계약에서 oracle을 정당화하라'고 하되 **모든 프로젝트에 golden implementation이 있다고 가정하지 않는다.**

### C2. Code-first tests는 동일한 오류를 재사용할 수 있다

[Konstantinou et al. (2026-07), preprint](https://arxiv.org/abs/2607.05139)은 잘못된 코드에 조건부로 만든 테스트가 동일 오류를 재생산하는 **error propagation**을 분석했다. 연구 설정에서 faulty code를 본 뒤 생성한 테스트의 결함 검출 비율이 14%, 독립적으로 생성한 경우 25%로 보고됐다.

- 차이는 연구 설정·모델·과제의 결과이지 '테스트를 코드보다 먼저 작성하면 항상 더 좋다'는 보편 인과 증거가 아니다.
- 독립성의 실질적 의미는 **코드 구현체를 정답의 유일한 원천으로 사용하지 않는 것**이다. 같은 agent라도 요구사항, 기존 계약, independent property, user-visible behavior를 출발점으로 테스트를 정당화할 수 있다.
- 추가 agent/새 모델을 호출하더라도 동일한 잘못된 spec에 의존하면 독립 oracle이 아니다.
- [Microsoft Research Building to the Test (2026-06)](https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/)는 oracle pass만으로 *package/deliverable completeness*가 확보되지 않는 반례다.

**Child judgment:** test-first는 독립성을 얻기 위한 **선택 가능한 설계 전략**으로 우선 고려한다. strict TDD, code/test writer 분리, 별도 멀티에이전트 팀은 기본값이 아니다.

### C3. Mutation은 강한 반례를 찾지만 모든 상황에서 ROI가 높은 것은 아니다

- [SWE-Mutation (2026, ACL Findings)](https://aclanthology.org/2026.findings-acl.1976/): 쉬운 mutate와 agentic mutate에서 검출률 차이(평균 71.04% vs 39.81%)를 보고했다. 모델이 만든 tests의 실제 failure discrimination을 독립 반례로 시험할 가치가 있다.
- [Hamidi et al. (2026-09, preprint)](https://arxiv.org/abs/2609.09315): coverage/mutation을 늘려도 *oracle 자체가 잘못되어* 실제 모델 생성 결함을 놓칠 수 있으며 mutation은 추가 비용 대비 약간의 우위만 보였다고 보고. 다른 모집단/변형 전략이므로 SWE-Mutation과 직접 점수 비교하지 않는다.
- [ReqTestAgent (2026-10)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1960601/full): mutation을 이용해 additional checks를 강화하지만, reference-validity gate 없이 mutant kill은 정당화할 수 없다고 설명한다.

**Child judgment:** 고위험·모호·반복 실패에서 가장 구별력 있는 작은 변형을 선정하고 검사한다. 일반 작업에는 property, boundary counterexample, regression reproduction 같은 값싼 oracle 검증이 우선일 수 있다. 모든 테스트 작성 요청마다 Mutation Testing을 켜지 않는다.

### C4. 멀티에이전트 조직과 인접 Tool이 자동으로 더 낫지는 않다

- [TDFlow (2026, EACL)](https://aclanthology.org/2026.eacl-long.70/): human tests가 주어진 code-repair workflow에서 역할 분리된 구성으로 높은 벤치마크 결과를 기록했다. 이는 **코드 패치 해결 성능**이지 독립 test-design Skill의 범용 성능이 아니다.
- [Agentic Iteration vs One-Shot (IEEE BDAI 2026)](https://doi.org/10.1109/BDAI70753.2026.11655121): 한 25-class Java 실험에서는 one-shot 방식이 CANDOR multi-agent 방식보다 높은 mutation score와 압도적으로 짧은 실행 시간. 원인은 multi-agent 방식이 class별 인접 의존성을 놓친 초기화 구조로 분석됨. 단일 실험이므로 모든 multi-agent 방식의 무용함을 뜻하지 않는다.
- [ReqTestAgent (2026-10)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1960601/full): full agent chain의 추가 품질 개선보다 비용 상승이 더 컸다.

**Child judgment:** 독립적인 반론을 검토할 이유가 있을 때만 분리된 verifier/reviewer를 쓰고, 그렇지 않으면 one-shot design + focused check가 단순하다. 별도 역할 사용 자체는 검증 근거가 아니다.

### C5. 실행할 수 없는 환경은 '통과'가 아니라 '검증 설계'만 제공한다

- [Agentic Rubrics (ACL 2026)](https://aclanthology.org/2026.acl-long.697/): 저장소를 탐색해 context-grounded rubric을 만든 뒤 테스트 실행 없이 candidate patch를 평가한 모델 실험에서 비교 기준을 상회했다. 이는 **정적/의미론적 판단도 유용한 signal**이 될 수 있음을 보이지만 **실행 동작을 증명하지는 않는다**.
- [Anthropic verification loops (2026)](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills): 가능한 환경에서는 실제 native test, linter, runtime feedback을 실행한다. Skill chaining은 비용·복잡성을 증가시킬 수 있음도 설명한다.
- [Scale SWE Atlas Test Writing](https://labs.scale.com/leaderboard/sweatlas-tw): repository exploration과 실제 실행·유지보수성 판단을 테스트 작성 과제로 평가한다. 텍스트 출력만으로 동일한 강도의 성공을 주장하면 안 된다.

**Child judgment:** 챗봇 등 제한된 환경에서 source/요구/기존 tests를 읽고 **가설, test outline, oracle, 예상 failure mode, 실행할 명령/검증 방법**을 제시할 수 있다. 실제 테스트 결과는 **not run / unknown**으로 남기며, code reasoning이나 LLM rubric을 PASS로 대체하지 않는다.

## 의사결정표: 언제 검증 강도를 높이는가

| Observed state | 가장 작은 신뢰 가능한 다음 확인 | stronger tier로 가는 조건 | 하지 않을 일 |
| --- | --- | --- | --- |
| 명확한 새 기능 명세, 실행 환경 없음 | requirements → observable behavior/oracle 설계, acceptance gap 표시 | 실행 환경 확보, high-risk 변경 | 미실행 테스트 PASS 선언 |
| 기존 버그에 재현 사례 존재 | 수정 전 올바른 이유의 실패 확인, 수정 후 PASS + 관련 P2P | 원인/여파 불명, 외부 경계 위험 | 현재 코드를 oracle의 유일 기준으로 삼기 |
| 기존 테스트가 충분한 단순 변경 | 테스트 재사용 또는 'new tests unnecessary' 결론 | consumer-visible path 변경 | 파일 수 달성을 위해 테스트 추가 |
| 실제 API/DB 상태·권한 변경 | 사용자/consumer contract를 보호할 얇은 integration/contract test | cross-service race, transaction, recovery | mock 내부 호출만 검증 후 end-to-end 보장 주장 |
| AI 생성 test의 기대값이 미심쩍음 | spec/reference example/known-good 및 counterexample로 oracle 확인 | normal/defect 변형이 관찰될 때 small mutation | mutation score만 높이면 유효 oracle이라고 간주 |
| 높은 coverage에도 실제 결함 누락 | assertions에서 구별해야 할 fault의 관찰 가능성 점검 | 고위험·다양한 결함 모델일 때 property/differential/mutation | coverage %만 더 올리기 |
| Flaky / nondeterministic tests | 시간, 순서, global state, 환경, concurrency의 특정 증거 확보 | 반복 실패의 실제 원인 미확정 | 무조건 retry/pass 처리 |
| 큰 장기 프로젝트 | 중요한 scenario별 evidence와 test maintenance cost 분리 | execution feedback 및 team coordination ROI 입증 | 모든 변경마다 고비용 종합 평가 고정 |

## Child Review — 판정과 Parent 인계

- **Verified in source:** ReqTestAgent의 validity-gate 비교·시간/품질 trade-off, Microsoft 연구의 deliverable 미충족, Hamidi 연구의 oracle failure 병목, CANDOR 비교 연구의 멀티에이전트 반례, ACL Agentic Rubrics의 무실행 signal.
- **Inferred / 추천:** `mols-test-design`은 **test oracle의 근거와 결함 구별력**에 최우선순위를 둔다. 필요 시 stronger technique으로 escalate하고 결과 해석을 evidence에 맞게 제한한다.
- **Rejected:** 무조건 테스트 먼저, 무조건 mutation, 무조건 multi-agent, 무조건 full suite, 무조건 code 실행 불가 환경은 무가치라는 극단.
- **Unresolved:** 참조 구현이 없는 신규 요구의 독립적 oracle 확보는 도메인별 권한과 사용자의 결정이 필요할 수 있다. 한 모델/한 프로젝트를 넘는 uplift는 아직 평가하지 않았다.
- **Parent implication:** research의 핵심 계약을 **'Claim → Oracle validity → Fault discrimination → Scope/cost → Evidence limit'**로 좁히되, 고정 문서 양식을 Skill에 강제하지 않는다.
- **루프 전환:** Child Review 종료, 부모의 Research/Plan으로 복귀. 신규 권한·scope 확대·독립 subagent 실행은 없었다.
