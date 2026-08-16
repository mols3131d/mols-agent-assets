# Reconciliation

## Purpose

여러 Reviewer, Loop, script, runtime과 grader 결과를 하나의 evidence-led result로 통합한다.

## Rules

1. Root cause가 같은 Finding을 병합한다.
2. Verified evidence를 simulated 또는 inferred claim보다 우선한다.
3. Reviewer 다수결로 사실이나 Severity를 결정하지 않는다.
4. Model grader 점수만으로 deterministic failure를 무시하지 않는다.
5. Runtime 결과가 inconsistent하면 pass rate와 variance를 평균으로 숨기지 않는다.
6. 적용되지 않는 축에는 `not_applicable`을 사용한다.
7. 미실행 검사는 `unknown` 또는 `not_run`으로 남긴다.
8. Final Disposition은 Lead가 소유한다.
9. Instruction·Context 비용은 규칙 수나 파일 크기만으로 판정하지 않고 실제 행동·변경 영향과 연결한다.
10. Human Comprehension Finding은 문체 취향이 아니라 운영·검토·변경 위험으로 정당화한다.

## Contradiction Handling

| Conflict | Action |
| --- | --- |
| Static pass vs runtime fail | Runtime failure를 우선하고 static coverage gap을 기록 |
| Reviewer disagreement | 각 Evidence를 재검증하고 unresolved ambiguity를 보존 |
| Two runtime trials disagree | Configuration, fixture, randomness와 trace delta 조사 |
| Project rule conflict | 임의 precedence를 만들지 않고 argument conflict 또는 owner decision 요구 |
| Baseline pass vs current fail | Current Evidence로 새 Disposition 결정 |
| Shorter asset vs safer asset | 제거된 규칙의 risk를 검토하고 길이를 품질 대리값으로 사용하지 않음 |
| Agent efficiency vs human readability | 중복을 제거하되 책임·근거·변경 경계를 잃지 않는 구조 선택 |

## Loop Ledger

각 Loop는 다음을 기록한다.

- Loop number
- Review lens and axes
- New Evidence or materially different challenge
- Findings and unknowns
- Changes applied in `improve` mode
- Post-change verification
- Loop outcome and continuation reason

재독, 요약, 동일 검사의 무의미한 재실행 또는 이전 Finding의 재서술은 별도 Loop로 계산하지 않는다. Finding이 없는 Loop도 검토 범위, 확인한 Evidence와 변경하지 않은 이유를 기록한다.

기본 Loop는 Completion을 만족하면 조기 종료할 수 있다. 사용자가 지정한 Loop는 capability blocker가 없는 한 정확히 수행한다. 수행하지 못한 Loop는 완료 수에 포함하지 않는다.
