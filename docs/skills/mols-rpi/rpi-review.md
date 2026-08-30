---
description: Adaptive recursive RPI에서 Review의 prerequisite validation, challenge reconciliation과 next-transition dispatch를 보존하는 maintainer 문서입니다.
---

# RPI Review

RPI의 Review는 결과를 끝에서 확인하는 checklist가 아니라 **현재 state를 검증하고 다음 Loop의 시작점을 결정하는 adaptive control gate**입니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Prerequisite

Review는 해당 Loop에서 도달한 현재 result와 그 result가 의존하는 prerequisite lineage를 함께 봅니다.

- 현재 Goal과 Active Scope
- 적용되는 Research와 Plan
- 수행된 Work 또는 requested terminal stage
- acceptance conditions와 실제 validation evidence
- material uncertainty, deviation, Scope issue 또는 unresolved child impact

Review는 prerequisite를 대신 만들지 않습니다. Research나 Plan이 원래 선행하지 않았다면 Review에서 뒤늦게 작성해 과거 Work를 compliant하게 만들 수 없습니다.

## Verify, Challenge, Reconcile

Review는 가장 작은 유용한 단위로 세 가지 판단을 수행합니다.

1. **Verify** — result가 Goal, Scope, prerequisite artifacts와 acceptance conditions를 실제로 충족하는지 확인하고 verified / inferred / unknown을 구분합니다.
2. **Challenge** — material risk나 uncertainty가 남아 있을 때 strongest plausible failure, counterexample, missed constraint, regression 또는 unsupported claim을 다른 관점에서 찾습니다.
3. **Reconcile** — challenge를 authority로 받아들이지 않고 evidence와 governing boundary에 대조해 `absorb`, `reject`, `unresolved`로 처리합니다.

Challenge는 비판을 많이 만드는 절차가 아닙니다. Direct evidence가 material question을 이미 닫았다면 가짜 반론을 만들지 않습니다. 반대로 plausible material finding은 reviewer의 remedy가 나쁘다는 이유만으로 버리지 않습니다.

Verify, Challenge와 Reconcile은 하나의 Review 안에서 이루어지는 local operations입니다. 이들이 별도 Loop를 만들지 않으며, substantive Review가 닫힐 때 현재 attempt가 하나의 Loop로 닫힙니다.

## Adaptive Dispatch

Review의 핵심 산출물은 **무엇을 고칠지**보다 **어느 prerequisite 또는 owning control로 돌아갈지**를 결정하는 것입니다.

- evidence gap 또는 unresolved premise → Research
- Research는 유효하지만 Plan decision/coverage gap → Plan
- Plan은 유효하고 bounded Work gap만 존재 → affected Work
- Scope boundary change → Scope Control; expansion은 Research → Plan prerequisite를 다시 거칩니다.
- narrower material blocker → 필요할 때 strict-subset recursive child Scope
- no credible gain / saturation → convergence 또는 blocker 판단
- terminal result가 충분히 검증됨 → acceptance candidate

Review는 이 transition을 **dispatch**할 뿐, Scope 변경·Run 종료·authority 변경 같은 다른 control concern의 실행 규칙을 대신 소유하지 않습니다.

새 material gap이 발견되면 같은 Review 안에서 무한히 재검토하지 않습니다. Review를 닫고 다음 counted Loop를 **earliest stale prerequisite**에서 시작합니다.

## Acceptance and Reopening

Review는 known material gap을 남긴 채 terminal result를 accept하지 않습니다.

- `absorb` finding이 아직 unverified change를 요구하면 해당 dependency를 다시 엽니다.
- `unresolved` finding이 acceptance를 바꿀 수 있으면 필요한 evidence를 Research로 돌리거나 trustworthy path가 없을 때 blocker로 남깁니다.
- 이미 유효한 Research, Plan과 Work는 그대로 재사용하고 finding 때문에 stale해진 dependency만 다시 엽니다.

이 판단이 RPI의 동적 적응을 만든다. 다음 Loop는 항상 Research부터 시작하는 것이 아니라 Review가 확인한 dependency validity에 따라 Research, Plan 또는 bounded Work에서 시작할 수 있습니다.

## Recursive Interaction

Recursive descent 역시 Review가 선택하는 transition입니다.

- parent 진행을 막는 narrower problem이 있고 isolation이 materially 유리할 때만 child Scope를 push합니다.
- child Scope는 parent의 strict subset이며 같은 Run과 Loop budget을 공유합니다. Authority와 safety boundary는 parent에서 상속하거나 더 좁힐 수 있을 뿐 넓힐 수 없습니다.
- child Review가 끝나면 evidence, decision, parent impact와 residual limitation만 parent에 반환합니다.
- parent Review는 child 결과가 parent Research, Scope 또는 Plan 중 무엇을 stale하게 만드는지 재검증합니다.

Recursion을 요청받았다는 이유만으로 child Scope를 만들지 않고, Review 관점 전환이 필요할 뿐이라면 perspective switching으로 해결합니다.

## Preserve

Review를 고도화할 때 다음을 보존합니다.

- **Review-before-acceptance** — consequential terminal result는 Review 없이 accept하지 않습니다.
- **evidence-based challenge reconciliation** — critique는 candidate finding이며 evidence와 authority를 거쳐야 합니다.
- **earliest-stale dispatch** — 다음 Loop는 가장 이른 invalidated prerequisite에서 시작합니다.
- **adaptive dispatch** — Research reopening, replanning, bounded Work, Scope handling, recursion과 termination을 구분해 해당 owner로 보냅니다.
- **bounded Review** — Review 내부의 verify/challenge/reconcile을 hidden recursion이나 fake Loop로 만들지 않습니다.

이를 static checklist, reviewer-majority decision, 매번 full restart 또는 무조건적인 recursion trigger로 바꾸지 않습니다.
