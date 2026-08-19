# Platform Capabilities

## Principle

검증 수준은 실제 사용 가능한 capability에 맞춘다. 특정 ChatGPT plan, UI, connector, subagent, API, runtime 또는 trace 기능이 있다고 가정하지 않는다.

## Capability Classes

| Capability | Evidence enabled |
| --- | --- |
| File | Uploaded, connected or local asset content와 metadata 검사 |
| Code | Parser, compiler, script, test와 deterministic grader 실행 |
| Web | 현재 platform specification, dependency와 external claim 확인 |
| Connector | GitHub, Drive 또는 다른 connected source의 authoritative asset 읽기 |
| Agent | Independent Reviewer 또는 specialist delegation |
| Runtime | Asset을 실제 executor에 적용해 behavior case 실행 |
| Trace | Model turn, tool call, handoff, guardrail, mutation과 latency 분석 |

## Resolution

`auto`는 현재 환경과 프로젝트의 규칙, 컨벤션과 관행을 따른다. 이를 위한 고정된 탐색 순서는 정의하지 않는다.

Capability가 없으면 다음처럼 강등한다.

- File 없음: 제공된 snippet만 검사하고 coverage limitation 기록
- Code 없음: deterministic checks를 `not_run`으로 기록
- Web 없음: 외부 최신 claim을 확인하지 못했다고 기록
- Agent 없음: role-separated sequential simulation과 shared-context limitation
- Runtime 없음: behavior result를 `simulated`로 기록
- Trace 없음: final output과 observable state만 검증하고 internal route는 `unknown`

명시적으로 요구된 capability가 없으면 조용히 대체하지 않고 `blocked` 또는 제한된 scope를 기록한다.
