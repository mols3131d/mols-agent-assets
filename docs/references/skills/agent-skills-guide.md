# 좋은 Agent Skill 설계 가이드

Agent Skill은 특정 영역의 지식과 반복 가능한 절차를 필요할 때 불러 쓰는 경량
패키지다. 좋은 Skill은 많은 정보를 담는 것이 아니라 **맞는 요청에서 활성화되고,
필요한 지침만 제공하며, 결과를 검증할 수 있게 만드는 것**에 가깝다.

이 문서는 설계 흐름만 소유한다. Canonical representation과 전문 규격은 해당 authority가 소유한다.

- Repository canonical representation →
  [Rulesync Repository Conventions](../common/standards/rulesync-repository-conventions.md)
- Repository-local Skill authoring →
  [Skill Authoring Conventions](skill-authoring-conventions.md)
- Agent Skills output / portable contract →
  [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)
- 상세 authoring 원칙 →
  [Skill Creation Best Practices](agent-skills-io/agent-skills-io-best-practices.md)

## Core Model

```text
Discovery              Activation               Execution
name + description  →  SKILL.md 로드         →  필요한 resource만 사용
```

Progressive Disclosure는 초기 context와 관련 없는 instruction 간섭을 줄인다.

Skill은 반복 workflow, project/domain-specific knowledge, 비자명한 예외, 엄격한
output contract가 있을 때 유용하다. 단순한 일회성 요청이나 모델이 이미 안정적으로
처리하는 일반 작업에는 만들지 않는다.

## Authoring Flow

### 1. Gather

실제 성공 작업, 사용자 교정, runbook, schema, patch, 장애와 실패 trace에서 반복되는
판단과 지식을 수집한다. 일반 지식을 다시 설명하기 위해 Skill을 만들지 않는다.

### 2. Bound

다음 세 질문으로 책임을 좁힌다.

- 어떤 사용자 결과를 만드는가?
- 언제 사용하고 언제 사용하지 않는가?
- 독립 trigger, permission, 배포 주기가 필요한 책임이 섞였는가?

공통 intent와 workflow를 공유하면 한 Skill 안에서 route한다. 목적이나 권한이
달라지면 분리를 검토한다.

### 3. Describe

`description`에는 내부 구현이 아니라 사용자 intent와 activation boundary를 쓴다.

```text
Use this skill when [사용자 목적과 상황].
Do not use it when [겹치기 쉬운 제외 조건].
```

Canonical field shape는 Rulesync schema를 따른다. Agent Skills projection의 field
constraint가 필요한 경우
[Specification](agent-skills-io/agent-skills-io-specification.md)을 따른다. Trigger
품질을 측정하고 개선할 때는
[Optimizing Skill Descriptions](agent-skills-io/agent-skills-io-optimizing-descriptions.md)을
사용한다. 이 Guide에서 eval recipe를 다시 정의하지 않는다.

### 4. Author the Core Workflow

`SKILL.md`에는 모든 실행에 공통으로 필요한 것만 둔다.

- 기본 실행 순서와 필요한 입력
- 중요한 분기와 중단 조건
- 반드시 지킬 constraint와 비자명한 gotcha
- 실패 복구와 완료 validation
- 추가 resource를 읽거나 실행할 조건

세부 resource를 만들었다면 load condition도 같이 쓴다.

```markdown
If the API returns a non-200 response, read `references/api-errors.md`.
```

### 5. Split Resources Only When Needed

| 내용 | 기본 위치 |
| --- | --- |
| 공통 workflow와 제약 | `SKILL.md` |
| 긴 절차, API, schema, 예외 | `references/` |
| 반복적이고 결정적인 실행 로직 | `scripts/` |
| template, sample, 출력 재료 | `assets/` |

빈 directory를 형식상 만들지 않는다. 파일을 나눠도 시작 시 전부 읽는다면
Progressive Disclosure가 아니다.

Script 설계의 상세 규칙은
[Using Scripts in Skills](agent-skills-io/agent-skills-io-scripts.md)가 소유한다.

### 6. Calibrate Control

실패 비용에 맞춰 instruction 강도를 조절한다.

- 방법이 다양함 → goal과 완료 조건 중심
- 선호 경로가 있음 → default procedure 제공
- 파괴적·보안·순서 의존 작업 → 순서, 승인, validation을 명시

선택지를 늘리기보다 안전한 default 하나를 우선한다.

### 7. Validate and Improve

검증을 분리한다.

- **Canonical contract**: Rulesync schema, front matter, path, projection
- **Target contract**: generated target artifact의 format과 mandatory semantics
- **Trigger behavior**: 필요한 요청에서 활성화되고 near-miss를 피하는지
- **Execution behavior**: 실제 task trace에서 retry, 누락, 불필요한 context가 있는지

Agent Skills output의 static format은 Specification이 안내하는 validator를 사용할 수 있다.
Trigger evaluation은
[Optimizing Skill Descriptions](agent-skills-io/agent-skills-io-optimizing-descriptions.md),
실행 기반 개선 원칙은
[Skill Creation Best Practices](agent-skills-io/agent-skills-io-best-practices.md)를 따른다.

검증하지 않은 항목을 성공으로 간주하지 않는다.

## Avoid

- 모델이 이미 아는 일반 지식을 장황하게 반복한다.
- 서로 다른 사용자 목적이나 권한을 한 Skill에 몰아넣는다.
- 모든 상세와 예시를 거대한 `SKILL.md`에 넣는다.
- `references/` 전체를 무조건 로드한다.
- resource를 만들고 읽을 조건을 정의하지 않는다.
- Rulesync schema나 target contract를 repository-local 규격으로 복제한다.
- validation 없이 생성이나 실행만으로 완료 처리한다.

## Completion Check

- [ ] 하나의 일관된 사용자 목적과 activation boundary가 있다.
- [ ] Rulesync canonical contract와 실제 target contract를 확인했다.
- [ ] 필요한 경우에만 repository-local Skill convention을 적용했다.
- [ ] `description`만으로 사용 조건과 주요 near-miss를 구분할 수 있다.
- [ ] 실제 작업 또는 실패에서 필요한 지식을 추출했다.
- [ ] 공통 workflow, 분기, 중단, 복구, 완료 조건이 명확하다.
- [ ] 추가 resource마다 실제 책임과 load condition이 있다.
- [ ] 위험한 단계의 통제 수준이 실패 비용에 맞다.
- [ ] 적용 가능한 canonical, target, trigger, execution validation을 구분해 수행했다.

## Sources

- [Rulesync](https://github.com/dyoshikawa/rulesync)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
