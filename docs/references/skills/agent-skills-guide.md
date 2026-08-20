# 좋은 Agent Skill 설계 가이드

좋은 Skill은 많은 정보를 담는 것이 아니라 **맞는 요청에서 활성화되고, 필요한 지침만 제공하며, 결과를 검증할 수 있게 만드는 것**에 가깝습니다.

이 문서는 설계 흐름만 소유합니다.

- canonical source boundary → [Rulesync Repository Conventions](../common/rulesync.md)
- repository-local authoring → [Skill Authoring Conventions](skill-authoring-conventions.md)
- Agent Skills portable contract와 vendor links → [Agent Skills Specification](specification.md)

## Model

```text
Discovery           Activation       Execution
name + description → SKILL.md load → 필요한 resource만 사용
```

단순 일회성 요청이나 모델이 이미 안정적으로 처리하는 일반 작업에는 Skill을 만들지 않습니다.

## Authoring Flow

### 1. Gather

실제 성공 작업, 사용자 교정, runbook, schema, patch와 실패 trace에서 반복되는 판단만 수집합니다. 일반 지식을 다시 설명하기 위해 Skill을 만들지 않습니다.

### 2. Bound

다음 세 질문으로 책임을 좁힙니다.

- 어떤 사용자 결과를 만드는가?
- 언제 사용하고 언제 사용하지 않는가?
- 독립 trigger, permission 또는 lifecycle이 필요한 책임이 섞였는가?

공통 intent와 workflow를 공유하면 한 Skill 안에서 route하고, 목적이나 권한이 달라지면 분리를 검토합니다.

### 3. Describe

`description`에는 내부 구현이 아니라 **사용자 intent와 activation boundary**를 씁니다. Capability와 겹치기 쉬운 near-miss를 구분할 수 있어야 합니다.

### 4. Author Core, Split Detail

`SKILL.md`에는 모든 실행에 공통인 것만 둡니다.

- 기본 workflow와 필요한 입력
- 중요한 분기·중단 조건
- critical constraint와 non-obvious gotcha
- 실패 복구와 완료 validation
- 추가 resource를 읽거나 실행할 조건

긴 API/schema/variant 지식은 `references/`, 반복적인 deterministic 로직은 `scripts/`, template·sample·출력 재료는 `assets/`로 분리할 수 있습니다. 빈 directory는 만들지 않습니다.

Resource를 분리했다면 `필요하면 읽는다`가 아니라 condition을 직접 연결합니다.

```text
API가 non-200 response를 반환하면 references/api-errors.md를 읽는다.
```

### 5. Validate

검증 대상을 섞지 않습니다.

- canonical contract → Rulesync
- portable/target contract → 해당 공식 specification
- repository invariant → deterministic test
- trigger/execution behavior → 실제 eval/runtime evidence

생성이나 projection 성공만으로 runtime behavior를 성공으로 간주하지 않습니다.

## Avoid

- 일반 LLM 지식을 장황하게 반복합니다.
- 서로 다른 사용자 목적이나 권한을 한 Skill에 몰아넣습니다.
- 모든 상세를 거대한 `SKILL.md`에 넣습니다.
- `references/` 전체를 무조건 로드합니다.
- Rulesync schema나 target contract를 repository-local 규격으로 복제합니다.
- 실제 evidence 없이 trigger 또는 runtime parity를 주장합니다.

## Completion Check

- 하나의 일관된 사용자 목적과 activation boundary가 있는가?
- `description`만으로 주요 near-miss를 구분할 수 있는가?
- 공통 workflow와 critical guardrail만 core에 남겼는가?
- 각 resource에 실제 책임과 load condition이 있는가?
- 필요한 canonical, target, repository, runtime validation을 구분했는가?

## Official References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
