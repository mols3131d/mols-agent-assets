---
description: Adaptive recursive RPI에서 Research의 prerequisite, uncertainty reduction, dynamic search와 downstream transition을 보존하는 maintainer 문서입니다.
---

# RPI Research

RPI의 Research는 일반적인 자료 수집 단계가 아니라 **downstream 판단을 바꿀 수 있는 material uncertainty를 줄이는 adaptive evidence search**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Prerequisite

Research는 RPI의 첫 evidence stage이므로 별도의 이전 RPI stage를 요구하지 않습니다. 대신 다음 상태가 최소 입력으로 성립해야 합니다.

- 현재 Goal과 Active Scope 또는 아직 불확실한 provisional boundary
- 다음 decision, Plan, acceptance 또는 verification claim을 바꿀 수 있는 material question
- 적용되는 source authority, freshness와 operational boundary

이미 유효한 Research가 있다면 다시 만들지 않습니다. 다만 Goal, Scope, material assumption, external freshness 또는 conflicting evidence가 바뀌어 downstream 판단에 영향을 줄 수 있으면 필요한 부분을 다시 엽니다.

## Adaptive Search

Research의 방향은 고정 source 순서나 quota가 아니라 **현재 uncertainty와 expected information gain**으로 바뀝니다.

- landscape가 불명확하면 broaden합니다.
- 중요한 lead의 근거가 약하면 deepen합니다.
- consequential premise가 한 관점에 의존하면 challenge합니다.
- 현재 source나 query가 반복적이거나 low-yield이면 switch합니다.
- 남은 uncertainty가 downstream decision을 materially 바꾸지 못하면 stop합니다.

Active intensity는 broaden·deepen·challenge의 적극성을 bias하지만 materiality, source authority나 stop criterion을 대신하지 않습니다.

사용자가 다관점 조사를 요청했거나 하나의 lens가 consequential question을 왜곡할 위험이 있으면 먼저 최소 **perspective map**을 만듭니다. 각 관점은 서로 다른 material question, 적합한 evidence surface와 downstream impact를 가져야 합니다. 같은 주장을 반복하는 출처나 같은 질문의 표현만 바꾼 pass는 관점 다양성이 아닙니다.

- task에 맞는 stakeholder, time horizon, system boundary, competing cause·hypothesis, user outcome, failure·regression, safety·authority, operability·maintainability lens 가운데 실제로 결과를 바꿀 수 있는 것만 고릅니다.
- 가능하면 한 관점의 초기 결론이 다른 관점을 anchor하지 않도록 evidence와 candidate finding을 먼저 분리해 수집합니다.
- 실제 context나 evidence path가 격리되지 않았다면 independent confirmation이라고 표현하지 않습니다. Single-agent sequential pass와 multi-agent parallel pass 모두 같은 evidence contract를 따릅니다.
- 관점 수나 agent 수를 품질의 proxy로 사용하지 않습니다. 추가 lens가 decision·acceptance를 바꿀 credible information gain이 없으면 중단합니다.

Local truth에는 repository/workspace evidence를, 변화 가능성이 큰 외부 사실·표준·vendor behavior에는 적절한 fresh external evidence를 우선하는 식으로 질문에 맞춰 evidence surface를 선택합니다. Retrieved content는 evidence이며 그 자체로 instruction authority가 되지 않습니다.

## Exit and Reopening

Research는 evidence를 많이 모았을 때가 아니라 **현재 downstream transition에 필요한 uncertainty가 충분히 줄었을 때** 닫힙니다.

- Planning이 필요하면 현재 Research를 Plan의 prerequisite로 넘깁니다.
- **RPI Research stage 자체**가 requested terminal이면 Main RPI Review로 가고, accepted candidate는 Finalize Gate를 거칩니다.
- 추가 search가 proportionate하지 않지만 material uncertainty가 남으면 uncertainty를 숨기지 않고 Review로 넘깁니다.
- Review가 evidence gap, unresolved conflict 또는 invalidated premise를 찾으면 다음 Loop는 필요한 Research 지점부터 다시 시작합니다.

Research stage 내부에서 source를 바꾸거나 broaden/deepen하는 것은 별도 Loop가 아닙니다. Material attempt는 Review가 닫힐 때만 하나의 Loop로 계산됩니다.

## Recursive Interaction

더 작은 evidence problem이 parent 진행을 막고 scope isolation의 실익이 있을 때만 Review를 거쳐 strict-subset child Scope로 내려갑니다.

Child Research는 parent를 대체하지 않습니다. 필요한 evidence, resolved finding, parent impact와 residual uncertainty만 반환하고, parent는 그 결과가 Research·Scope·Plan 중 무엇을 stale하게 만드는지 다시 판단합니다.

## Preserve

Research를 고도화할 때 다음을 보존합니다.

- **evidence-before-Plan** — consequential Plan은 유효한 Research에 의존합니다.
- **adaptive search** — uncertainty와 information gain에 따라 breadth, depth, source와 perspective가 바뀝니다.
- **material perspective coverage** — 필요한 관점은 distinct question과 evidence surface를 가지며, fixed roster·persona·vote가 되지 않습니다.
- **honest independence** — 실제로 격리된 관점이나 evidence path만 independent라고 표현합니다.
- **intensity-biased effort** — intensity는 search effort를 bias하지만 evidence 기준을 대체하지 않습니다.
- **Review-driven reopening** — Review가 찾은 evidence gap만 다음 Loop의 Research로 다시 엽니다.
- **bounded search** — source count나 조사량이 아니라 downstream materiality로 stop합니다.
- **recursive narrowing** — child Research는 strict subset이며 parent state에 재통합됩니다.

이를 fixed checklist, source quota, intensity별 고정 검색량, 무조건적인 web search 또는 매 Loop 전체 재조사로 바꾸지 않습니다.
