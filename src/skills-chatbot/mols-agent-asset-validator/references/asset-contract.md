# Asset Contract

## Purpose

Agent asset는 파일 형식이 아니라 행동 계약으로 검증한다. 동일한 의미가 YAML, Markdown, JSON, Python 또는 UI configuration에 존재할 수 있다.

## Asset Types

| Type | Minimum contract |
| --- | --- |
| Skill | name, trigger boundary, purpose, workflow, inputs, outputs, failure behavior, supporting resource relationship |
| Instruction | authority, scope, applicability, precedence, prohibited behavior, exceptions |
| Prompt | variables, assumptions, expected output, ambiguity handling, injection boundary |
| Agent | role, instructions, tools, handoffs, guardrails, output contract, termination |
| Subagent | specialization, delegation trigger, context received, result returned, decision ownership |
| Tool | name, description, input schema, output, side effects, permissions, approval, error behavior |
| Guardrail | inspected surface, pass condition, tripwire behavior, failure propagation |
| Reference | owner, read condition, authority, compatibility, staleness boundary |
| Template | fields, optionality, renderer assumptions, ownership of format |
| Config | schema, defaults, override semantics, conflict handling, portability |
| Script | runtime, dependencies, deterministic behavior, exit code, input/output, destructive boundary |
| Eval | case purpose, input, fixture, expected behavior, grader, threshold, evidence classification |

## Cross-Asset Invariants

- 한 행동의 최종 decision owner는 명확해야 한다.
- Trigger와 negative boundary는 실제 목적을 구분해야 한다.
- Reference는 선언된 조건에서만 읽고 owner instruction을 몰래 override하지 않는다.
- Project override가 있으면 merge, replace 또는 precedence semantics가 명시되어야 한다.
- Tool description과 실제 schema·side effect가 일치해야 한다.
- Subagent가 반환하는 정보와 Lead가 필요로 하는 정보가 호환되어야 한다.
- Example은 contract를 설명해야 하며 숨은 새로운 규칙을 만들지 않는다.
- Eval은 implementation 문구를 그대로 재현하는 문제가 아니라 behavior를 검사해야 한다.
- 각 지침은 material failure를 방지하거나 안정적인 경계를 정의해야 하며 상식적 절차를 무의미하게 반복하지 않는다.
- 기본 로드 컨텍스트는 현재 판단에 직접 기여하고 조건부 자산은 필요한 경우에만 읽는다.
- 핵심 행동 계약은 이름, 경로, override와 실패 조건의 변화에도 추적·복구 가능해야 한다.
- 사람은 목적, Trigger, owner, Evidence와 변경 영향을 암묵적 팀 지식 없이 파악할 수 있어야 한다.

## Evidence Priority

일반적인 우선순위는 다음과 같다.

1. 실제 runtime trace와 resulting state
2. Deterministic parser, test, command와 script output
3. Current source asset and explicit contract
4. Independent semantic review와 behavior simulation
5. Example, summary와 prior verdict

더 높은 evidence가 낮은 evidence와 충돌하면 원인을 조사하고 낮은 evidence를 사실로 유지하지 않는다.
