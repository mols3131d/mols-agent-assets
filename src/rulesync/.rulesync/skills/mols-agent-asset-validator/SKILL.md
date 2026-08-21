---
name: mols-agent-asset-validator
description: >-
  Validate, audit, stress-test, or evidence-led improve a bounded agent-facing
  asset or package using deterministic inspection, semantic and routing review,
  behavioral or adversarial evaluation, and runtime evidence when available. Use
  for readiness, regression, trigger or behavior evaluation, or bounded
  corrections driven by validation findings. General authoring, simplification,
  refactoring, or adaptation belongs to mols-agent-asset. Do not use for ordinary
  product-code review, standalone human-facing prose, open-ended research, or
  implementation unrelated to agent behavior.
agentsskills:
  metadata:
    target: "OpenAI ChatGPT"
---

# MOLS Agent Asset Validator

## Purpose

에이전트 자산이 올바르게 선택되고, 최소한의 유효한 지침과 컨텍스트로 일관되게 행동하며, 도구와 서브 에이전트를 안전하게 사용하고, 사람이 낮은 이해 비용으로 운영·수정할 수 있는지 evidence-first 방식으로 검증한다.

형식보다 행동 계약을 우선한다. 정적 검사, 현재 ChatGPT의 의미 분석과 시뮬레이션, 실제 runtime evidence를 구분하며 수행하지 않은 Model Eval, 독립 Trial 또는 Trace 검증을 통과했다고 표현하지 않는다.

## Scope

검증 대상은 다음 중 하나 이상이다.

- Skill package와 `SKILL.md`
- System, developer, project 또는 scoped instructions
- Reusable prompt와 prompt template
- Agent와 subagent definition
- Tool, function, MCP 또는 connector schema와 사용 규칙
- Input, output 또는 tool guardrail
- Reference, example, template와 configuration
- Script, hook와 deterministic validator
- Trigger, behavior, adversarial 또는 regression eval fixture
- 위 자산 사이의 routing, delegation, override, evaluation과 handoff 관계

제품 코드 자체의 correctness Review는 대상이 아니다. 제품 코드는 Agent tool, validator, hook 또는 fixture처럼 에이전트 자산의 일부일 때만 검토한다.

## Truth Model

검증 결과는 다음 evidence class를 구분한다.

| Evidence | 의미 |
| --- | --- |
| Deterministic | parser, schema, path, static contract, repository test처럼 같은 입력에 같은 결과를 기대할 수 있는 검사 |
| Semantic | 현재 모델이 instruction, routing, ambiguity, context pressure, human comprehension을 분석한 결과 |
| Trial | 고정된 prompt/fixture를 실제 대상 agent 또는 model에 실행한 결과 |
| Runtime | 실제 host, connector, tool, trace, invocation 또는 production-like execution에서 관측한 결과 |

낮은 evidence class가 높은 evidence class를 대신하지 않는다. 예를 들어 static trigger review는 실제 host activation을 증명하지 않는다.

## Modes

### Validate

기본 mode다. 대상의 문제와 readiness를 evidence와 함께 평가한다.

### Improve

검증 중 발견된 bounded finding을 현재 scope 안에서 직접 고칠 수 있고 사용자가 변경을 허용한 경우에만 적용한다.

- finding이 change의 근거여야 한다.
- 일반적인 신규 authoring, 구조 단순화, refactor, target adaptation은 `mols-agent-asset`의 책임이다.
- 수정 후 영향을 받는 검증을 다시 수행한다.
- 새로운 architecture나 unrelated cleanup으로 scope를 넓히지 않는다.

## Workflow

### 1. Resolve target and authority

- 검증 대상을 정확히 식별한다.
- canonical source, generated projection, runtime surface를 구분한다.
- project-local instructions와 target runtime authority를 확인한다.
- 수행 가능한 deterministic checks, trials, runtime evidence의 한계를 기록한다.

### 2. Establish contract

대상이 무엇을 해야 하는지와 하지 말아야 하는지를 짧게 정리한다.

최소한 다음을 본다.

- responsibility
- trigger 또는 activation boundary
- inputs / outputs
- authority / precedence
- tool 또는 subagent use
- safety boundary
- expected target/runtime behavior

### 3. Deterministic inspection

사용 가능한 repository tests, schema checks, parser, linter, path/reference checks를 먼저 사용한다.

단순한 형식 검증을 LLM 판단으로 대체하지 않는다.

### 4. Semantic and routing review

다음을 검토한다.

- description이 필요한 요청에서 선택될 가능성이 있는가
- false positive를 유발할 정도로 넓지 않은가
- loaded instructions가 실제 task에 필요한가
- 동일 책임의 다른 Skill/Rule과 ownership이 겹치지 않는가
- instruction이 모호하거나 상충하지 않는가
- progressive disclosure가 실제로 context를 줄이는가
- agent가 불필요한 선택지를 탐색하게 하지 않는가

### 5. Behavioral and adversarial evaluation

필요한 경우 representative prompt, negative prompt, boundary prompt를 사용한다.

- happy path만 보지 않는다.
- false positive / false negative를 함께 본다.
- prompt가 test fixture인지 실제 user instruction인지 구분한다.
- 수행하지 않은 trial을 실행한 것처럼 보고하지 않는다.

### 6. Runtime evidence

runtime behavior가 acceptance에 필요한 경우 가능한 실제 evidence를 사용한다.

예:

- host가 Skill을 discover/activate하는지
- expected tool이 실제 호출되는지
- generated projection이 target에서 로드되는지
- connector permission과 write boundary가 실제로 적용되는지

runtime evidence를 얻을 수 없으면 그 claim은 unverified로 남긴다.

### 7. Review bottlenecks

#### Instruction bottleneck

- 필수 instruction이 너무 많아 서로 경쟁하는가
- 같은 정책을 여러 표현으로 반복하는가
- 모델이 이미 잘 아는 일반론을 장황하게 설명하는가
- critical instruction이 주변 text에 묻히는가

#### Context-noise bottleneck

- 항상 로드되는 정보 중 task-specific하지 않은 것이 많은가
- reference를 필요할 때만 읽도록 분리할 수 있는가
- examples, compatibility tables, historical notes가 runtime context를 차지하는가

#### Human comprehension debt

- maintainer가 owner, trigger, precedence를 빠르게 알 수 있는가
- 같은 책임을 이해하려고 여러 파일을 탐색해야 하는가
- abstract framework vocabulary가 실제 행동보다 앞서는가

### 8. Verdict and findings

Finding은 severity보다 **행동 영향과 evidence**를 우선한다.

권장 구조:

```text
Finding
- Problem
- Impact
- Evidence
- Counterevidence / uncertainty
- Recommendation
```

최종 상태는 필요에 따라 다음 중 하나로 표현한다.

- ready
- ready_with_limits
- needs_change
- blocked

검증하지 못한 부분이 결과에 중요하면 `ready`라고 하지 않는다.

## Improvement Guardrails

Improve mode에서도 다음을 지킨다.

- 검증 finding과 직접 연결된 최소 변경만 한다.
- canonical source를 수정하고 generated projection을 직접 고치지 않는다.
- target-specific requirement를 portable contract로 일반화하지 않는다.
- external source가 current behavior에 중요하면 최신 authoritative source를 다시 확인한다.
- validation framework 자체를 대상 asset에 복제하지 않는다.

## Completion

완료 시 다음을 남긴다.

- 대상과 검증 scope
- 사용한 evidence classes
- 실행한 checks/evals와 결과
- material findings
- 적용한 bounded fixes
- 남은 unverified claims 또는 blockers
- readiness status
