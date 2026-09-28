---
description: Artifact Inbox에서 날짜 대신 branch, issue, Pull Request 같은 work unit identity를 기준으로 working artifact를 묶을 때 참고하는 확장 패턴입니다.
---

# Artifact Inbox: Work Unit Containers

[`Artifact Inbox`](artifact-inbox.md)는 working / non-canonical artifact를 canonical surface와 분리해 둘 수 있는 surface를 제공합니다. 단순한 작업에서는 날짜 기반 directory만으로 충분하지만, 하나의 branch, issue, Pull Request처럼 명확한 work unit을 중심으로 여러 artifact가 만들어지면 시간보다 작업 identity를 기준으로 묶는 편이 더 자연스러울 수 있습니다.

이 패턴은 Artifact Inbox 안에서 **work unit identity를 container로 사용하는 확장 방식**을 다룹니다.

## Core

Artifact를 실제로 소유하는 work unit이 명확하다면 날짜 대신 그 identity를 나타내는 directory를 container로 사용할 수 있습니다.

```text
inbox/
├── YYYY-MM-DD/
├── <branch-work-unit>/
└── <external-work-unit>/
```

핵심은 특정 naming scheme이 아니라 **관련 artifact를 그것을 실제로 소유하는 작업 단위로 묶는 것**입니다.

Branch, issue 또는 Pull Request와 단순히 관련 있다는 이유만으로 work unit container를 사용할 필요는 없습니다. Research, plan, review, handoff 같은 artifact를 함께 이해하고 이어가는 자연스러운 기준이 그 work unit일 때 유용합니다.

## Typical Forms

### Date

별도의 지속적인 work unit이 없거나 시간이 가장 자연스러운 구분 기준이라면 날짜 기반 container를 사용할 수 있습니다.

```text
inbox/
└── 2026-09-29/
    ├── research.md
    └── review.md
```

### Git Branch

하나의 change branch가 작업의 주된 단위라면 branch identity를 container에 사용할 수 있습니다.

```text
inbox/
└── feature-inbox-policy/
    ├── research.md
    ├── plan.md
    └── review.md
```

날짜가 identity나 충돌 회피에 실제로 도움이 된다면 함께 사용할 수도 있습니다.

```text
inbox/
└── 2026-09-29-feature-inbox-policy/
    └── ...
```

### Issue or Pull Request

Issue나 Pull Request가 작업을 식별하는 안정적인 단위라면 provider와 identifier를 container에 표현할 수 있습니다.

```text
inbox/
└── github-241-inbox-policy/
    ├── research.md
    ├── plan.md
    └── review.md
```

Project에서 issue와 Pull Request를 구분하는 편이 유용하다면 type을 이름에 포함할 수도 있습니다.

```text
inbox/
├── github-issue-241-inbox-policy/
└── github-pr-242-inbox-policy/
```

`github`는 대표적인 예시일 뿐입니다. 다른 issue tracker나 project system에서도 같은 원리를 적용할 수 있습니다.

## Choosing a Container

Container는 artifact와 단순히 연관된 식별자가 아니라 **현재 artifact 묶음을 가장 자연스럽게 소유하는 work unit**을 기준으로 선택합니다.

대표적인 판단은 다음과 같습니다.

- 독립적인 조사나 일회성 작업 → Date
- 하나의 code change를 따라가는 작업 → Branch
- Issue 자체의 조사·계획·해결 작업 → Issue
- Pull Request의 구현·검증·리뷰를 지원하는 작업 → Pull Request

Project가 반복적으로 사용하는 work unit이 분명하다면 selection order를 local convention으로 정할 수도 있습니다.

```text
Issue / Pull Request
        ↓
      Branch
        ↓
       Date
```

이 순서는 이 패턴의 invariant가 아닙니다. Repository의 workflow와 ownership model에 맞게 선택할 수 있습니다.

## Work Unit Transitions

작업이 진행되면서 work unit identity가 바뀔 수 있습니다. 대표적으로 branch에서 시작한 작업이 이후 Pull Request를 얻을 수 있습니다.

```text
inbox/
└── feature-inbox-policy/

        ↓ Pull Request 생성

inbox/
└── github-241-inbox-policy/
```

기존 artifact가 같은 작업을 계속 지원한다면 새 container로 옮겨 lineage를 유지할 수 있습니다. 반대로 기존 이름이 여전히 충분히 식별 가능하고 rename 비용이 더 크다면 그대로 유지할 수도 있습니다.

중요한 것은 naming history를 완벽히 반영하는 것이 아니라 **현재와 다음 작업자가 artifact의 소속과 관계를 쉽게 이해할 수 있는가**입니다.

## Container Contents

Work unit container 안에는 해당 작업을 지원하는 여러 종류의 artifact를 함께 둘 수 있습니다.

```text
inbox/
└── github-241-inbox-policy/
    ├── research.md
    ├── plan.md
    ├── review.md
    └── handoff.md
```

Artifact가 하나뿐이고 별도 grouping이 탐색이나 연속성에 도움을 주지 않는다면 work unit directory를 만들 필요는 없습니다. Sequence, index, 추가 metadata도 실제 탐색 문제가 생길 때 확장하는 편이 단순합니다.

## Options

Project 필요에 따라 다음을 선택적으로 사용할 수 있습니다.

- work unit type을 이름에 포함
- issue / Pull Request number 같은 stable identifier 포함
- 사람이 알아보기 위한 짧은 slug 추가
- 날짜와 branch identity 결합
- branch → Pull Request 전환 시 container rename
- container root에 overview 또는 navigation용 `README.md` 추가
- Date / Branch / external work unit container를 한 Inbox에서 함께 사용

어떤 옵션도 모든 Artifact Inbox에 필요한 것은 아닙니다.

## Relationship to Artifact Inbox

이 패턴은 [`Artifact Inbox`](artifact-inbox.md)의 대안이 아니라 확장입니다. Artifact Inbox가 working artifact와 canonical surface의 분리, scope와 lifecycle을 다룬다면 이 패턴은 그 안에서 **여러 artifact를 어떤 작업 identity로 묶을지**만 다룹니다.

Artifact의 승격, 유지, 삭제와 canonical ownership은 Artifact Inbox와 해당 project의 documentation lifecycle이 계속 소유합니다.

## Boundary

이 패턴은 **Inbox 내부에서 working artifact를 grouping하는 container identity**를 다룹니다.

다음을 정의하지 않습니다.

- Git branch lifecycle이나 branch naming convention
- Issue 또는 Pull Request workflow
- artifact type taxonomy
- canonical documentation ownership
- archive policy
- 특정 Git hosting 또는 issue tracker의 사용

Work unit container는 기존 workflow를 반영하는 organization surface이며, 그 workflow 자체를 새로 정의하지 않습니다.
