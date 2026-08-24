---
description: repository·subtree·path·task intent에 따라 instruction과 context를 서로 다른 scope mechanism에 배치할 때 참고하는 pattern으로, 자동 주입과 context 절약을 위한 structural scope와 semantic routing의 책임을 구분합니다.
---

# Layered Context Instructions

지침과 context를 적용 범위에 따라 다른 mechanism으로 배치해 **자동 주입을 유지하면서 불필요한 context load를 줄이는** 패턴입니다.

## Purpose

모든 지침을 하나의 파일이나 하나의 mechanism에 집중시키지 않고, 적용 대상을 가장 자연스럽게 판별할 수 있는 scope에 배치합니다.

## Core

구조적으로 적용 대상을 결정할 수 있으면 path/scope 기반 mechanism을 우선하고, **현재 task와의 semantic relevance를 모델이 판단해야 할 때 Skill을 사용**합니다.

대표적인 권장 mapping은 다음과 같습니다.

| Scope | Mechanism |
| --- | --- |
| repository 전체 기본 지침 | root `AGENTS.md` |
| 특정 directory subtree | nested `AGENTS.md` |
| 확장자, glob, 반복되는 path pattern | glob-scoped Rule |
| task 의미를 판단해야 선택 가능한 context, rule, knowledge | load-context Skill |

## Typical Use

- Repository 전체에 항상 필요한 기본 지침은 root `AGENTS.md`에 둘 수 있습니다.
- 특정 subtree에만 필요한 지침은 nested `AGENTS.md`로 scope를 좁힐 수 있습니다.
- directory hierarchy만으로 표현하기 어려운 확장자별·반복 path별 지침은 glob Rule로 적용할 수 있습니다.
- 현재 task의 intent를 모델이 판단해야 선택할 수 있는 context, rule, knowledge는 load-context Skill로 구성할 수 있습니다.

```text
structural scope
├─ repository      → AGENTS.md
├─ directory tree  → nested AGENTS.md
└─ path / glob     → Rule

semantic scope
└─ task intent     → Skill
```

## Options

- 작은 repository에서는 root `AGENTS.md` 하나만으로 충분할 수 있습니다.
- subtree가 독립적인 책임을 가질 때만 nested `AGENTS.md`를 추가할 수 있습니다.
- glob Rule은 file extension뿐 아니라 반복되는 하위 directory pattern에도 사용할 수 있습니다.
- load-context Skill은 필요한 문서, 규칙, 지식 또는 다른 context source를 선택적으로 로드하는 용도로 확장할 수 있습니다.
- 사용하는 harness가 동일한 mechanism을 지원하지 않으면 그 환경의 동등한 scope mechanism으로 조정할 수 있습니다.

## Considerations

- 같은 지침을 여러 layer가 동시에 소유하면 변경과 해석이 어려워질 수 있으므로 가능한 한 가장 자연스럽고 좁은 scope를 선택합니다.
- 항상 필요한 context와 task에 따라 선택해야 하는 context를 구분하면 기본 context 크기를 줄이는 데 도움이 됩니다.
- mechanism을 세분화하는 비용이 이득보다 크면 더 단순한 구성을 유지할 수 있습니다.

## Boundary

이 패턴은 **지침과 context를 어떤 scope mechanism에 배치하고 주입할지**를 다룹니다. 개별 지침의 내용, routing/index format, Skill 내부 구현 방식 자체를 정의하지 않습니다.

`AGENTS.md`, glob Rule, load-context Skill의 조합은 대표적인 구성이지 모든 repository에 동일하게 강제되는 규격은 아닙니다.
