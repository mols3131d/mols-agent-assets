---
description: report·research·review·handoff·draft 같은 working/non-canonical artifact를 canonical source와 분리해 보관할 때 참고하는 pattern으로, inbox의 scope와 승격·유지·삭제 lifecycle 경계를 다룹니다.
---

# Artifact Inbox

작업 중 생성되는 report, research, review, handoff, draft 같은 **working / non-canonical artifact**를 완성 여부와 관계없이 canonical surface와 분리해 보관하는 패턴입니다.

## Core

- Inbox는 working artifact를 위한 별도 surface입니다.
- Inbox에 있다는 이유만으로 artifact가 canonical documentation, source, plan 또는 project state가 되지 않습니다.
- Root inbox와 nested inbox는 같은 패턴을 서로 다른 scope에서 적용한 형태입니다.

## Typical Forms

```text
inbox/
└─ ...

<scope>/
└─ inbox/
   └─ ...
```

대표적인 사용 방식은 다음과 같습니다.

- root `inbox/` — repository 또는 project 전체와 관련된 artifact
- `<scope>/inbox/` — 특정 directory, domain, component, asset 등 local scope와 가까운 artifact

어느 쪽을 사용할지는 artifact의 관계와 project 구조에 따라 정할 수 있으며, 이 패턴 자체는 root와 nested 사이의 고정된 우선순위를 요구하지 않습니다.

## Typical Contents

- research
- review
- briefing / report
- handoff
- draft
- temporary analysis or generated artifact

목록은 예시이며 inbox가 특정 artifact type만 허용한다는 뜻은 아닙니다.

## Options

Project 필요에 따라 다음을 선택적으로 추가할 수 있습니다.

- 날짜 기반 directory
- naming convention
- frontmatter나 metadata
- retention / cleanup policy
- index나 routing asset
- generator나 cleanup automation

단순한 repository에서는 평평한 `inbox/` 하나만으로도 충분할 수 있습니다.

## Lifecycle

Artifact는 inbox에서 생성·검토·수정할 수 있습니다. 장기적으로 유효한 지식이 생기면 적절한 canonical owner에 반영할 수 있으며, 원본 artifact는 별도로 유지하거나 삭제할 수 있습니다.

Inbox가 얼마나 오래 artifact를 보존할지와 어떤 승격 절차를 사용할지는 repository가 정합니다.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Work Unit Containers](artifact-inbox-work-unit-containers.md) | 날짜 외에 브랜치·Issue·PR 등 작업 단위로 아티팩트를 묶는 선택적 확장입니다. |
| [Durable Progress Handoff](durable-progress-handoff.md) | 작업을 이어가기 위해 어떤 상태를 남기고 다시 확인할지 다룹니다. Inbox는 그 기록을 둘 수 있는 하나의 surface입니다. |
| [Nonstandard Directory Guide](../documentation/nonstandard-directory-guide.md) | `inbox/` 같은 repository-local nonstandard surface에 local guide가 필요할 때 참고합니다. |
| [Directory Context Capsule](../context-engineering/directory-context-capsule.md) | Inbox 자체에 local agent rule, lifecycle guidance, routing 또는 task-specific context가 필요할 때 entrypoint와 nearby context surface를 붙이는 방식으로 함께 사용할 수 있습니다. |

## Boundary

이 패턴은 **working artifact와 canonical surface를 분리하는 저장 위치와 scope**를 다룹니다.

Inbox 자체가 archive, task tracker, workflow state, runtime dependency 등의 의미를 자동으로 갖지는 않습니다. Project가 그런 기능을 함께 사용하려면 별도 관행으로 정의할 수 있습니다.
