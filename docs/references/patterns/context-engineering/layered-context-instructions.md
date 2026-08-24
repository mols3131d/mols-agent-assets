---
description: repository·subtree·path·task intent에 따라 instruction과 context를 서로 다른 scope mechanism에 배치할 때 참고하는 pattern으로, 자동 주입과 context 절약을 위한 structural scope와 semantic routing의 책임을 구분합니다.
---

# Layered Context Instructions

지침과 context를 적용 범위에 따라 다른 mechanism에 배치해 **구조적으로 적용할 지침과 의미에 따라 선택할 지침을 구분하고 불필요한 context load를 줄이는** 패턴입니다.

## Purpose

모든 지침을 하나의 파일이나 mechanism에 모으지 않고, **적용 여부를 가장 자연스럽게 판단할 수 있는 scope에 둡니다.**

- **Structural scope** — repository, directory, path, glob처럼 작업 대상의 구조만으로 적용 여부를 결정할 수 있습니다.
- **Semantic scope** — 현재 task의 의미와 관련성을 모델이 판단해야 적용 여부를 결정할 수 있습니다.

## Core

구조만으로 적용 대상을 정할 수 있다면 구조적 scope가 보통 더 단순합니다. 구조만으로 충분하지 않은 지침 context에는 **모델이 Skill을 선택하는 특성을 활용해 task에 맞는 지침을 선택적으로 로드**할 수 있습니다.

| 적용 기준 | 대표 mechanism | 역할 |
| --- | --- | --- |
| repository 전체 | root `AGENTS.md` | 전역 기본 지침과 entry/routing 안내 |
| 특정 directory subtree | nested `AGENTS.md` | 해당 subtree에 적용되는 지침 |
| 확장자, glob, 반복 path pattern | scoped Rule | 여러 위치에 공통으로 적용되는 구조적 지침 |
| task intent와 의미적 관련성 | 모델이 선택한 Skill | 필요한 instruction context를 선택적으로 로드 |

```text
structural scope
├─ repository      → root AGENTS.md
├─ directory tree  → nested AGENTS.md
└─ path / glob     → scoped Rule

semantic scope
└─ task intent     → model-selected Skill → instruction context
```

## Skill for Instruction Context

Skill은 흔히 재사용 가능한 도구나 workflow 같은 capability를 제공하는 데 쓰입니다. 이 패턴에서는 그 용법에 더해, **모델이 Skill을 선택하는 메커니즘을 instruction context loading에도 적극 활용**합니다.

예를 들어 code review, 문서 윤문, 특정 domain 작업처럼 path만으로 필요한 지침을 확정하기 어려운 경우, 모델이 Skill의 discovery signal을 보고 관련 Skill을 선택할 수 있습니다. 선택된 Skill은 지침을 직접 제공하거나 필요한 reference와 context를 추가로 로드하도록 안내할 수 있습니다.

```text
task intent
   ↓
model selects relevant Skill
   ↓
load task-specific instruction context
   ↓
perform task
```

이는 Skill을 instruction file로 재정의하는 것이 아닙니다. **Skill의 기존 선택 메커니즘을 의미 기반 instruction routing에도 활용하는 것**이 핵심입니다.

Skill은 의미 기반 routing의 유일한 수단도 아닙니다. 별도 routing/index asset이나 runtime 고유의 선택 메커니즘이 더 적합할 수 있으며, 이 패턴은 그중 **모델이 Skill을 선택해 필요한 지침 context를 로드하는 구성**을 적극 활용하는 사례를 보여줍니다.

## Placement Guidance

- Repository 전체에 항상 필요한 기본 지침은 root `AGENTS.md`에 둘 수 있습니다. Root는 모든 세부 context를 품기보다 필요한 entrypoint와 routing을 안내할 수 있습니다.
- 하나의 directory subtree로 자연스럽게 표현되는 지침은 가까운 nested `AGENTS.md`에 둘 수 있습니다.
- 여러 subtree, extension 또는 glob/path pattern에 반복 적용되는 지침은 scoped Rule이 더 자연스러울 수 있습니다. Rulesync 같은 framework를 사용한다면 canonical Rule에서 target별 표현으로 projection할 수도 있습니다.
- task의 의미를 봐야 필요한 지침을 알 수 있다면 모델이 Skill을 선택해 context를 로드하는 방식을 고려할 수 있습니다.

구조적으로 확정할 수 있는 지침까지 모델 판단에 맡길 필요는 없습니다. 반대로 의미적 관련성이 중요한 지침을 항상 주입하면 기본 context가 불필요하게 커질 수 있습니다.

## Considerations

- 같은 지침을 여러 layer가 독립적으로 소유하지 않고 가능한 한 authoritative owner를 하나로 유지합니다.
- 작은 repository에서는 root `AGENTS.md` 하나만으로 충분할 수 있습니다.
- Skill의 discovery signal이 지나치게 넓으면 불필요한 context가 로드되고, 너무 좁으면 필요한 지침이 누락될 수 있습니다.
- harness가 같은 mechanism을 지원하지 않으면 해당 runtime의 동등한 scope 또는 routing mechanism으로 조정할 수 있습니다.
- 후보가 많아 별도 discovery/routing surface가 필요하면 [Routing & Index Assets](routing-index-assets.md) 패턴을 함께 참고할 수 있습니다.

## Boundary

이 패턴은 **지침과 context를 어떤 scope mechanism에 배치하고 선택적으로 주입할지**를 다룹니다. Skill의 일반적인 목적이나 전체 capability model을 재정의하지 않으며, 개별 지침의 내용, routing/index format, Skill 내부 구현 방식, vendor별 discovery와 precedence도 정의하지 않습니다.

`AGENTS.md`, scoped Rule, Skill의 조합은 대표적인 구성이지 모든 repository와 harness에 동일하게 강제되는 규격은 아닙니다.
