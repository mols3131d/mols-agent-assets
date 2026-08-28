---
description: OpenSpec workflow를 project에 맞게 조정할 때 profile, project configuration, custom schema의 책임을 분리하고 가장 가벼운 customization surface부터 선택하는 reusable pattern입니다.
---

# OpenSpec Customization

OpenSpec을 프로젝트에 맞게 바꿀 때 **필요한 효과를 가장 작은 customization surface에 배치하는 패턴**입니다.

OpenSpec의 실제 field, command, path와 runtime semantics는 공식 문서가 소유합니다. 이 pattern은 어떤 mechanism을 선택할지에 대한 reusable design judgment만 다룹니다.

## Core

- workflow 설치 범위와 delivery 선택, project-level instruction, artifact 구조 변경을 같은 설정 문제로 취급하지 않습니다.
- 기존 workflow에 지침을 더하는 것으로 충분하면 project configuration을 우선합니다.
- artifact 종류, dependency flow, template 또는 schema-level instruction 자체가 달라져야 할 때 custom schema를 사용합니다.
- repository policy는 OpenSpec이 실제로 소비해야 하는 최소 delta만 전달하고 canonical owner를 OpenSpec으로 옮기지 않습니다.
- project-specific 선택과 reusable pattern, OpenSpec 공식 contract를 서로 다른 권한으로 유지합니다.

## Config Before Schema

기본 workflow 구조를 유지하면서 planning context나 특정 artifact·operation에 지침을 더하는 정도라면 schema를 fork하지 않습니다.

Schema fork는 upstream built-in schema의 개선을 자동으로 따라가지 않는 별도 snapshot을 소유하는 선택이므로, additive configuration으로 표현할 수 없는 구조적 차이가 있을 때 사용합니다.

## Delta-only Context

`config.yaml`을 project handbook의 복사본으로 만들지 않습니다.

모든 workflow run에 영향을 줘야 하는 정보만 global context에 두고, artifact나 operation 하나에만 필요한 요구사항은 더 좁은 surface에 둡니다. 기존 repository 문서를 agent가 안정적으로 읽을 수 있다면 canonical 문서를 가리키고 OpenSpec에는 필요한 delta만 남기는 방식을 우선합니다.

## Narrowest Surface

대표적인 판단 순서는 다음과 같습니다.

| 필요한 효과 | 우선 검토할 surface |
| --- | --- |
| 어떤 workflow를 설치하고 어떤 형태로 제공할지 | Profile |
| project 전반의 planning context | Project configuration |
| 특정 artifact에만 필요한 추가 규칙 | Artifact-scoped project rule |
| apply/archive 수행 방식에 필요한 추가 guidance | Operation guidance |
| project에서 사용할 schema 선택 | Project configuration |
| artifact, dependency, template, schema instruction 변경 | Custom schema |

표는 OpenSpec schema를 재정의하지 않습니다. 정확한 지원 범위와 이름은 현재 공식 문서를 확인합니다.

## Preserve Authority

Testing, architecture, security, documentation, language policy 같은 repository 규칙이 이미 canonical owner를 갖고 있다면 OpenSpec customization은 그 정책을 대체하지 않습니다.

같은 규칙이 repository instruction, OpenSpec configuration, schema template에 반복되면 먼저 실제 owner를 정하고 불필요한 copy를 제거합니다. OpenSpec이 workflow 실행을 위해 직접 받아야 하는 내용만 예외적으로 복제합니다.

## Verify the Resolved Behavior

Configuration이나 schema file이 보기 좋게 작성되었다는 사실만으로 customization이 의도대로 작동한다고 간주하지 않습니다.

필요한 claim에 맞춰 현재 OpenSpec CLI가 제공하는 resolved instruction, schema validation, schema resolution 또는 template resolution을 확인합니다. 가장 작은 observable surface로 원하는 변화가 실제 agent input이나 workflow 구조에 반영됐는지 검증합니다.

## Three-layer Review

OpenSpec customization을 설명하거나 검토할 때 다음을 분리하면 변경 이유와 권한이 명확해집니다.

1. **Official** — OpenSpec이 공식적으로 제공하는 mechanism과 contract
1. **Pattern** — 여러 프로젝트에 재사용할 수 있는 mechanism 선택 원칙
1. **Project** — 현재 repository의 증거로 결정한 구체적인 값과 규칙

Vendor upgrade, pattern 개선, project policy 변경을 서로 독립적으로 검토할 수 있는 것이 이 분리의 핵심입니다.

## Boundary

이 pattern은 OpenSpec의 공식 schema나 CLI 사용법을 대신하지 않습니다. 특정 repository의 mandatory policy도 소유하지 않습니다.

OpenSpec과 무관한 repository workflow 설계, 일반 Agent Asset routing, spec 작성 방법 자체는 각각의 별도 owner가 다룹니다.
