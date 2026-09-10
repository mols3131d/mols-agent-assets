# Dialectic Orchestration

이 reference는 `mols-dialectic`을 선택한 **현재 caller**가 토론을 운영할 때 사용한다. 별도 moderator agent의 역할 정의가 아니다.

## 1. Frame

세 specialist가 같은 문제를 다루도록 최소 brief를 만든다.

- question, Goal 또는 결정해야 할 proposition
- in-scope / out-of-scope
- 판단에 실제로 필요한 acceptance, constraint와 trade-off
- 적용되는 authority와 task-relevant evidence 또는 state basis
- 중요한 known unknown과 evidence limitation
- caller가 요구하는 최종 결과의 용도

전체 conversation이나 불필요한 upstream reasoning을 기본으로 전달하지 않는다. Domain 조사, 검증과 operational authority는 해당 task capability와 outer caller에 남긴다.

## 2. Establish Independent Openings

가능하면 Thesis와 Antithesis를 같은 base brief에서 독립적으로 시작한다.

- `mols-dialectic-thesis`에는 strongest constructive position을 요청한다.
- `mols-dialectic-antithesis`에는 materially different strongest counter-position을 요청한다.
- runtime이 independent concurrent execution을 지원하면 어느 한쪽 결과를 sibling에게 보여주기 전에 둘을 dispatch할 수 있다.
- concurrency나 isolation을 지원하지 않으면 순차 호출해도 되지만 먼저 받은 opening을 다음 opening의 context에 넣지 않고, 독립 실행했다고 주장하지 않는다.

Opening부터 인위적으로 정반대 결론을 강제하지 않는다. credible antithesis가 없거나 한쪽이 약하다고 판단되면 그 자체가 유효한 결과다.

## 3. Cross-Examine

Material conflict가 있으면 각 specialist에게 sibling의 **opening만** 전달해 한 번의 bounded cross-review를 수행한다.

### Thesis response

Thesis에게 다음을 요구한다.

1. Antithesis를 가장 강한 합리적 형태로 steelman한다.
2. 실제 disagreement를 premise, evidence, inference, value, constraint, scope 또는 trade-off 수준에서 특정한다.
3. 자기 thesis를 defend, narrow, revise 또는 concede한다.
4. 무엇이 자기 결론을 바꿀지 밝힌다.

### Antithesis response

Antithesis에게 다음을 요구한다.

1. Thesis를 가장 강한 합리적 형태로 steelman한다.
2. 가장 material한 premise나 inference를 공격하거나 realistic counterexample을 제시한다.
3. 단순 비판 대신 가능한 경우 더 강한 counter-position 또는 correction을 제시한다.
4. Thesis가 살아남는 지점은 concede하고, 무엇이 자기 반론을 무효화할지 밝힌다.

두 response를 서로에게 다시 넘겨 반복 논쟁을 만들지 않는다. 새로운 decision-relevant 정보 없이 표현만 반복되면 이 단계를 종료한다.

## 4. Synthesize

`mols-dialectic-synthesis`에 다음 최소 context를 넘긴다.

- base brief
- Thesis opening과 response
- Antithesis opening과 response
- caller가 확인한 material evidence/authority limitation

Synthesis에게 winner 선택이나 consensus를 요청하지 않는다. 다음을 요구한다.

1. common ground와 실제 conflict를 분리한다.
2. conflict가 empirical, normative, design, constraint, scope 또는 unresolved-knowledge 문제 중 무엇인지 구분한다.
3. 양쪽에서 살아남는 evidence, reasoning, constraint와 trade-off를 식별한다.
4. unsupported, contradicted, irrelevant 또는 dominated된 부분을 버린다.
5. 남은 내용을 단순 병합하지 말고 더 강한 proposition, framing 또는 solution으로 변환한다.
6. irreducible conflict나 missing evidence 때문에 정당한 승화가 불가능하면 `unresolved`로 남긴다.

## 5. Adversarially Refine When Material

Synthesis가 consequential하고 아직 깨지기 쉬운 핵심 assumption이 있을 때만 한 번의 refinement를 허용한다.

1. 현재 Synthesis만 Antithesis에 주고 strongest material challenge를 요청한다.
2. challenge가 Synthesis의 conclusion, boundary 또는 trade-off를 실제로 바꿀 수 있을 때만 Synthesis를 한 번 더 호출해 revise한다.
3. challenge가 이미 처리된 주장, wording preference 또는 비결정적 variation이면 재호출하지 않는다.

기본 pass는 Opening 2회 + Cross-review 최대 2회 + Synthesis 1회다. Optional refinement는 Antithesis 1회 + Synthesis 1회를 넘지 않는다. 실패, disagreement 또는 uncertainty만을 이유로 자동 retry하거나 새 cycle을 만들지 않는다.

## 6. Stop and Return

다음 중 하나면 종료한다.

- Synthesis가 Goal에 충분한 더 강한 결론을 만들었고 material unanswered challenge가 없다.
- 남은 conflict가 missing evidence, authority 또는 irreducible value/constraint 차이로 귀결된다.
- 다음 turn이 새로운 decision-relevant delta 없이 기존 논거를 반복한다.
- runtime capability 또는 invocation limit 때문에 신뢰할 수 있는 continuation이 불가능하다.

caller는 specialist transcript를 그대로 합치지 않는다. 최종 Synthesis, 결정에 중요한 근거, 실제 unresolved conflict와 limitation만 사용해 outer task의 user-facing response를 만든다. Specialist 결과가 outer authority, evidence 또는 safety contract와 충돌하면 그 contract를 우선하고 충돌을 숨기지 않는다.
