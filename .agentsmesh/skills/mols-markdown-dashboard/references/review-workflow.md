# Review Workflow

Dashboard를 변경하지 않고 사실성, 집계와 구조를 평가할 때만 읽는다.

## Review Priorities

1. 현재 evidence가 dashboard의 주장과 일치하는가?
1. Requirement와 Verification Target의 분모가 근거를 갖는가?
1. status, progress와 gaps가 서로 모순되지 않는가?
1. 오래된 snapshot 또는 stale evidence가 현재 상태로 표현됐는가?
1. 핵심 세 표가 중복 없이 독자의 판단을 돕는가?

스타일 취향보다 잘못된 상태 판단을 유발하는 문제를 우선한다.

## Output

- **Verdict** — `Pass`, `Revise`, `Blocked`
- **Findings** — 중요도, 위치, 문제, 근거, 권장 수정
- **Preserved strengths** — 유지해야 할 구조가 있을 때만
- **Unknowns** — 확인하지 못한 source 또는 상태가 있을 때만

Review mode에서는 source dashboard를 수정하지 않는다.
