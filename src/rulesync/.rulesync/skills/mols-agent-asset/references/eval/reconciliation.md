# Eval Reconciliation

여러 reviewer, trial, grader 또는 evidence source를 하나의 evidence-led result로 통합할 때 사용한다.

## Rules

- root cause가 같은 finding은 병합한다.
- 직접 관찰한 evidence를 simulated 또는 inferred claim보다 우선하되, 서로 다른 claim을 단순 evidence rank로 덮지 않는다.
- reviewer 다수결로 사실이나 severity를 결정하지 않는다.
- model grader 점수로 deterministic failure를 무시하지 않는다.
- runtime 결과가 inconsistent하면 pass rate와 variance를 평균 하나로 숨기지 않는다.
- 적용되지 않는 축은 `not_applicable`, 미실행 검사는 `unknown` 또는 `not_run`으로 남긴다.
- final disposition과 수정 여부는 lead가 소유한다.

## Conflicts

| Conflict | Action |
| --- | --- |
| Static pass vs runtime fail | claim 범위를 확인하고 runtime failure와 static coverage gap을 함께 기록 |
| Reviewer disagreement | 각 evidence를 다시 확인하고 unresolved ambiguity를 보존 |
| Runtime trials disagree | configuration, fixture, randomness와 observable delta를 조사 |
| Baseline pass vs current fail | current evidence로 fresh disposition 결정 |
| Shorter asset vs safer asset | 길이가 아니라 제거된 contract와 실제 risk를 비교 |

Finding 수나 aggregate score 자체를 전체 pass의 대리값으로 사용하지 않는다.
