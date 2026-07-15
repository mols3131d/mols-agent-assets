# Progressive Disclosure 원칙

- 기준 문서: [Agent Skills Specification](https://agentskills.io/specification)
- 구현 참고: [How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
- 확인일: 2026-07-15

## 1. 정의

Progressive disclosure는 **Agent가 필요한 정보를 필요한 시점에만 단계적으로 context에 로드하는 설계 원칙**이다.

모든 Skill의 전체 instructions와 resource를 처음부터 로드하지 않는다. 먼저 최소한의 metadata만 제공하고, 사용자 요청과 관련된 Skill이 선택되면 instructions를 로드하며, 실제 수행에 필요한 세부 reference와 script는 그 이후에 개별적으로 사용한다.

핵심 목적은 다음과 같다.

- 초기 context 크기와 token 사용량을 줄인다.
- 관련 없는 instructions 사이의 충돌과 간섭을 줄인다.
- 많은 Skill을 설치해도 session 시작 비용을 제한한다.
- 상세 지식과 실행 로직을 modular하게 관리한다.
- 현재 task에 필요한 정보에 Agent의 attention을 집중한다.

## 2. 3단계 Loading Model

| 단계 | 로드하는 내용 | 로드 시점 | 권장 크기 |
| --- | --- | --- | --- |
| 1. Discovery | `name`, `description` | Session 시작 | Skill당 약 50~100 tokens |
| 2. Activation | 선택된 Skill의 `SKILL.md` instructions | 사용자 요청이 Skill과 일치할 때 | 5,000 tokens 미만 권장 |
| 3. Execution | `references/`, `scripts/`, `assets/` | 해당 resource가 실제로 필요할 때 | Resource별 상이 |

### 2.1 Discovery

Agent는 session 시작 시 모든 Skill의 `name`과 `description`만 확인한다.

```yaml
---
name: data-engineering
description: Use this skill for data ingestion, transformation, data quality validation, and pipeline orchestration tasks.
---
```

이 단계에서 `description`은 Skill activation 여부를 결정하는 핵심 routing signal이다. 따라서 다음 내용을 포함해야 한다.

- Skill이 제공하는 capability
- Skill을 사용해야 하는 사용자 intent
- 관련 file type, domain 또는 workflow
- 인접한 Skill과 구분되는 적용 범위

Activation 조건을 `SKILL.md` body에만 작성하면 discovery 단계에서는 보이지 않으므로 trigger에 도움이 되지 않는다.

### 2.2 Activation

사용자 요청이 `description`과 일치하면 Agent가 해당 Skill의 `SKILL.md`를 context에 로드한다.

`SKILL.md`에는 다음과 같이 모든 실행에 필요한 내용만 둔다.

- 공통 workflow
- routing rule
- 반드시 지켜야 하는 constraint
- 중요한 gotcha
- validation requirement
- resource를 읽거나 script를 실행해야 하는 조건

Activation 시 `SKILL.md` 전체가 로드되므로 대형 reference manual처럼 작성하면 context 효율이 낮아진다. 공식 specification은 `SKILL.md`를 500 lines 미만으로 유지할 것을 권장한다.

### 2.3 Execution

Agent는 `SKILL.md`의 routing 결과에 따라 필요한 resource만 읽거나 실행한다.

```text
data-engineering/
├── SKILL.md
├── references/
│   ├── ingestion.md
│   ├── transformation.md
│   ├── data-quality.md
│   └── orchestration.md
├── scripts/
│   ├── validate-schema.py
│   └── check-quality.py
└── assets/
    └── pipeline-template.yaml
```

사용자가 ingestion pipeline을 요청했다면 `references/ingestion.md`만 우선 로드한다. Transformation이나 data quality instruction이 실제 task에 필요하지 않다면 해당 파일은 읽지 않는다.

## 3. 동작 흐름

```text
사용자 요청
    ↓
Skill catalog의 description과 비교
    ↓
관련 Skill의 SKILL.md 활성화
    ↓
SKILL.md의 routing rule 적용
    ↓
필요한 reference 또는 script만 사용
    ↓
검증 후 결과 반환
```

예를 들어 사용자가 다음과 같이 요청한다고 가정한다.

> CSV 파일을 warehouse에 적재하는 pipeline을 만들어줘.

Agent는 다음 순서로 처리한다.

1. `data-engineering` Skill의 description에서 ingestion capability를 확인한다.
2. `data-engineering/SKILL.md`를 로드한다.
3. Routing table에서 요청을 ingestion workflow로 분류한다.
4. `references/ingestion.md`를 읽는다.
5. Schema 검증이 필요하면 `scripts/validate-schema.py`를 실행한다.
6. 관련 없는 `references/transformation.md`와 `references/orchestration.md`는 로드하지 않는다.

## 4. Router 중심 Skill 설계

Progressive disclosure를 적용할 때 root `SKILL.md`를 얇은 entry point와 router로 사용할 수 있다.

```markdown
# Data Engineering

## Routing

Identify the user's primary intent and read only the corresponding file.

| User intent | Required instructions |
| --- | --- |
| Source extraction, API ingestion, file loading | `references/ingestion.md` |
| SQL modeling, dbt, data transformation | `references/transformation.md` |
| Validation, reconciliation, anomaly checks | `references/data-quality.md` |
| Scheduling, retry, dependency management | `references/orchestration.md` |

If the task spans multiple workflows, read the required files in execution order.
Do not read unrelated reference files.
```

이 방식은 “Skill 안의 Skill”처럼 보이지만, 실제로는 하나의 Skill 안에서 여러 instruction module을 조건부로 로드하는 구조다. 하위 module에는 `SKILL.md` 대신 일반 Markdown 파일을 사용하는 것이 portable하다.

## 5. 좋은 Routing Instruction

Routing instruction은 **resource와 load condition을 함께 지정**해야 한다.

좋은 예:

```markdown
API가 non-200 response를 반환하면 `references/api-errors.md`를 읽는다.

사용자가 destructive migration을 요청하면 먼저 `references/migration-safety.md`를 읽고 dry-run plan을 생성한다.
```

피해야 할 예:

```markdown
필요하면 references를 확인한다.

자세한 내용은 관련 문서를 참고한다.
```

모호한 지시는 Agent가 어떤 파일을 언제 읽어야 하는지 판단하기 어렵게 만든다.

## 6. 파일별 역할

| 위치 | 포함할 내용 | 포함하지 않을 내용 |
| --- | --- | --- |
| `description` | Capability와 activation trigger | 실행 절차와 긴 예시 |
| `SKILL.md` | 공통 workflow, router, constraint, gotcha | 모든 variant의 상세 설명 |
| `references/` | Domain별 상세 절차, API 문서, schema | 반복 실행 코드 |
| `scripts/` | Deterministic하고 반복되는 실행 로직 | 장문의 설명 문서 |
| `assets/` | Template, sample, image, output resource | Agent가 읽어야 하는 핵심 instructions |

## 7. 하나의 Skill과 여러 Skill의 선택 기준

| 조건 | 권장 구조 |
| --- | --- |
| 상위 trigger와 공통 workflow를 공유 | 하나의 Skill + reference routing |
| 같은 task에서 여러 module을 함께 사용 | 하나의 Skill + reference routing |
| 사용자 intent와 activation trigger가 완전히 다름 | 별도 Skill |
| Permission 또는 tool 요구사항이 다름 | 별도 Skill |
| 독립적으로 설치·배포·versioning해야 함 | 별도 Skill |
| 단순한 workflow variant | 하나의 Skill 안의 reference module |

Core specification은 nested `SKILL.md`의 discovery와 activation semantics를 별도로 정의하지 않는다. Skill 내부에 여러 하위 `SKILL.md`를 넣으면 client별 scan 방식에 따라 중복 discovery, name collision 또는 예상하지 못한 activation이 발생할 수 있다.

따라서 다음 구조를 권장한다.

```text
# 권장
parent-skill/
├── SKILL.md
└── references/
    ├── workflow-a.md
    └── workflow-b.md
```

다음 구조는 client portability가 필요한 경우 피한다.

```text
# 비권장
parent-skill/
├── SKILL.md
└── sub-skills/
    ├── workflow-a/SKILL.md
    └── workflow-b/SKILL.md
```

## 8. Anti-pattern

### 모든 Reference를 처음부터 읽기

```markdown
작업을 시작하기 전에 `references/`의 모든 파일을 읽는다.
```

Resource를 분리해도 모두 eager load하면 progressive disclosure의 효과가 사라진다.

### 대형 `SKILL.md`

모든 domain, framework, edge case, API 설명을 root file에 넣으면 activation마다 불필요한 context가 로드된다.

### 깊은 Reference Chain

```text
SKILL.md → reference-a.md → reference-b.md → reference-c.md
```

Agent가 필요한 resource를 발견하지 못하거나 관련 없는 파일까지 연속으로 읽을 수 있다. `SKILL.md`에서 필요한 reference를 직접 연결하는 one-level 구조가 권장된다.

### 모호한 Description

```yaml
description: Helps with data.
```

Capability와 trigger가 불명확하면 필요한 상황에서 Skill이 활성화되지 않거나 관련 없는 요청에서 활성화될 수 있다.

## 9. 설계 체크리스트

- [ ] `description`만 읽어도 Skill의 capability와 trigger를 판단할 수 있다.
- [ ] `SKILL.md`에는 모든 실행에 필요한 core instructions만 있다.
- [ ] 상세 workflow는 focused reference file로 분리했다.
- [ ] 각 reference의 load condition이 `SKILL.md`에 명시되어 있다.
- [ ] 관련 없는 reference를 eager load하지 않는다.
- [ ] Reference는 가능한 한 `SKILL.md`에서 직접 연결한다.
- [ ] 반복적이고 deterministic한 logic은 script로 분리했다.
- [ ] 독립적인 trigger나 permission이 필요한 기능은 별도 Skill로 분리했다.
- [ ] Nested `SKILL.md`에 client-independent 동작을 기대하지 않는다.
- [ ] 활성화된 instructions가 context compaction 과정에서 유실되지 않도록 client가 보호한다.

## 10. 결론

Progressive disclosure의 핵심은 단순히 파일을 여러 개로 나누는 것이 아니다. **Agent가 현재 task에 필요한 정보만 정확한 시점에 선택적으로 로드하도록 metadata, router, reference, script의 경계를 설계하는 것**이다.

효과적인 구조는 다음 원칙을 따른다.

1. `description`으로 Skill을 발견한다.
2. `SKILL.md`로 공통 workflow와 routing을 제공한다.
3. 세부 instructions와 executable resource는 필요할 때만 사용한다.
4. 독립적인 activation boundary가 필요한 기능은 별도 Skill로 분리한다.
