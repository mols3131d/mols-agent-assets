# Runtime Evaluation

## Principle

Runtime Eval은 실제 executor가 asset을 적용한 run과 observable output을 검사한다. Runtime이 없으면 static validation이나 simulation을 runtime pass로 표현하지 않는다.

## Supported Evidence Sources

- ChatGPT or Workspace Agent preview output
- OpenAI Responses API or Agents SDK run
- OpenAI trace and grader result
- Codex or sandbox execution log
- Waza run, task, grader and trial result
- Project-specific agent runner or CI result

## Minimum Run Record

- Asset version or digest
- Model and relevant runtime configuration when available
- Input case and fixture version
- Enabled tools, agents, permissions and guardrails
- Final output
- Tool calls, handoffs, file mutations or trace references
- Grader type and threshold
- Trial index and timestamps when available

## Grader Classes

| Class | Use |
| --- | --- |
| Deterministic | exact routing label, schema, file state, command result, prohibited mutation |
| Model | semantic correctness, evidence quality, completeness, harmful overreach |
| Human | ambiguous policy, product intent, irreversible approval and disputed severity |
| Composite | deterministic gate plus model or human quality score |

Deterministic grader가 가능한 항목을 Model grader에만 맡기지 않는다. Model grader의 rubric은 observable criteria와 failure examples를 포함해야 한다.

## Trials

여러 Trial은 stochastic variability를 측정한다. Trial 수를 Reviewer Loop 수와 혼동하지 않는다.

- Loop: 같은 snapshot에 대한 검토 과정 반복
- Trial: 같은 case를 실제 runtime에서 독립 실행
- Re-validation: asset 또는 baseline이 바뀐 뒤 fresh evaluation

## OpenAI Runtime

OpenAI runtime을 사용할 수 있으면 Agent run, tool call, handoff, guardrail과 trace를 수집하고 String, Python, Label, Score 또는 Multi grader를 적용할 수 있다. API나 trace에 접근하지 못하면 OpenAI Eval을 실행했다고 보고하지 않는다.

## Waza Runtime

Waza를 사용할 수 있으면 task, fixture, executor, grader와 trial configuration을 확인한다. Waza fixture가 존재한다는 사실만으로 run success를 주장하지 않는다.

## Sensitive Data

Trace와 tool output에는 secret, personal data와 proprietary content가 포함될 수 있다. 결과에는 필요한 최소 evidence만 남기고 credential이나 raw sensitive payload를 복사하지 않는다.
