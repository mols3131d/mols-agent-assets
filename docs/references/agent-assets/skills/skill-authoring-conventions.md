---
title: Skill Authoring Conventions
description: Agent Skill을 작성·리팩터링할 때 공통 표준·작성 프레임워크·target contract 이후에도 적용되는 mols의 package, description, context와 metadata 관행을 확인할 때 사용합니다.
---

# Skill Authoring Conventions

공통 Agent Asset 판단은 [Agent Asset Design Principles](../common/design-principles.md), 작성 원본과 결정별 권한은 [작성 원본과 권한](../../../development/source-authority.md)이 소유합니다. 정확한 Skill field, path, discovery 동작과 대상별 동작은 [Agent Skills Specification](specification.md)에서 현재 공식 source로 route합니다.

이 문서는 그 이후에도 반복해서 필요한 **Skill에만 해당하는 mols의 추가 관행**만 소유합니다.

## Package

필수 entrypoint, package path, 공통 metadata와 discovery 동작은 적용되는 작성 프레임워크, Agent Skills 표준과 대상 계약이 소유합니다.

실제 entrypoint가 정해진 뒤에는 기본적으로 **single-file Skill**을 선호합니다. 하나의 `SKILL.md`로 activation과 핵심 runtime behavior가 충분하면 파일 길이나 책임 수만으로 package를 분해하지 않습니다. 적용되는 표준이나 대상의 현재 limit와 guidance는 함께 따릅니다.

보조 파일은 다음 중 하나가 실제로 있을 때만 추가합니다.

- 특정 조건에서만 필요한 세부 내용을 분리해 context noise를 줄일 수 있음
- 재사용할 deterministic script, template, schema 또는 static asset이 필요함
- runtime에서 별도 resource로 접근해야 하는 자료가 있음

다음 원칙을 함께 적용합니다.

- chatbot/agent, flat/runtime을 별도 Skill taxonomy로 만들지 않습니다.
- runtime에 필요한 resource는 deployable Skill package 안에 둡니다.
- Repository-only test, eval과 maintainer artifact는 host의 verification 또는 documentation surface가 소유합니다.
- 보조 자료가 host에서 별도 Skill entrypoint로 오인될 이름이나 위치를 사용하지 않습니다.
- 보조 파일을 만들었다는 이유만으로 별도 directory taxonomy나 manifest를 추가하지 않습니다.

Rulesync를 작성 원본으로 사용하는 이 repository의 구체적인 workspace와 path는 [Rulesync](../../tooling/rulesync.md)와 [작성 원본과 권한](../../../development/source-authority.md)이 소유합니다.

## Markdown Responsibility

Single-file Skill에서는 여러 top-level `#` heading을 **독립적인 Markdown responsibility boundary**로 사용할 수 있습니다.

- 한 heading은 한 책임을 가집니다.
- `##` 이하는 부모 책임을 점진적으로 분해합니다.
- 같은 depth는 비슷한 abstraction level을 유지합니다.
- 공통 invariant는 가장 가까운 공통 owner에 한 번만 둡니다.
- 의미 없는 미세 분할이나 heading-only wrapper를 만들지 않습니다.

파일 분리는 책임 수가 아니라 **loading boundary, runtime resource 또는 ownership benefit**이 실제로 생기는지가 기준입니다.

## Description

공통 `description` contract와 대상별 listing 또는 truncation 동작은 official source가 소유합니다. mols convention에서는 `description`을 **routing contract**로 작성합니다.

- capability와 적용 범위를 먼저 드러냅니다.
- 가까운 sibling Skill과 혼동될 실질적인 제외 경계가 있으면 포함합니다.
- prerequisite, fallback, handoff, execution order와 validation workflow는 선택 자체에 필요하지 않으면 body가 소유합니다.
- 선택 경계를 sibling Skill 이름에만 의존하지 않습니다. 명시적인 composition, delegation 또는 handoff contract에서는 필요한 이름 참조를 허용합니다.

`description` 문구 최적화와 trigger eval 방법은 [Agent Skills Specification](specification.md)의 creator guidance로 route합니다. 대상이 별도 discovery surface를 제공하면 정확한 동작은 해당 대상 계약을 따릅니다.

## Progressive Context

Skill의 조건부 보조 resource에는 [Agent Asset Design Principles](../common/design-principles.md)의 Progressive Disclosure를 적용합니다. Resource를 분리했다면 핵심 본문의 가장 가까운 decision point에서 **무엇을 언제 읽는지** 발견할 수 있게 합니다.

더 일반적인 routing shape는 [Progressive Context Routing](../../../../catalog/patterns/context-engineering/progressive-context-routing.md)이 소유합니다.

## Context-Only Naming

일반적인 Agent Asset naming은 [Agent Asset Naming Convention](../common/naming.md)이 소유합니다.

주책임이 workflow execution이 아니라 domain-specific context discovery/loading이면 Skill family extension으로 `<domain>-context`를 사용할 수 있습니다.

`domain`은 context가 적용되는 문제, 지식 또는 runtime surface를 사람이 구분할 수 있을 만큼만 표현합니다. 구현, mutation, 검증 또는 최종 output이 주책임인 Skill에는 `-context`를 사용하지 않습니다.

이 suffix는 별도 Agent Asset type, metadata schema 또는 runtime capability를 의미하지 않습니다.

## Target Metadata

유효한 target-specific metadata는 현재 projection target이 아니라는 이유만으로 제거하지 않습니다. 반대로 한 대상의 field를 repository-wide portable contract처럼 끌어올리지 않습니다.

- Target metadata semantics는 실제 대상 계약이 소유합니다.
- Source framework가 target metadata를 보존하거나 projection하는 방식은 해당 source framework가 소유합니다.
- Canonical source가 필요한 target requirement를 표현하지 못하면 shadow source나 local superset을 만들기보다 [작성 원본과 권한](../../../development/source-authority.md)에 따라 source representation을 다시 판단합니다.

## Verification

이 repository에서 Rulesync로 관리하는 Skill의 structural validation은 [Validation](../../../development/validation.md)이 소유합니다. 공통 Skill specification, target compatibility와 behavioral quality는 각각 해당 official source와 [Evaluation](../../../development/evaluation.md)을 따릅니다.

한 validator의 통과를 전체 compatibility나 behavior quality로 확대 해석하지 않습니다.

## Boundary

- 공통 Agent Asset 설계 → [Agent Asset Design Principles](../common/design-principles.md)
- Behavioral instruction 설계 → [Instruction Design](../common/instruction-design.md)
- Standard와 target/source registry → [Agent Skills Specification](specification.md)
- General Agent Asset naming → [Agent Asset Naming Convention](../common/naming.md)
- Progressive context routing → [Progressive Context Routing](../../../../catalog/patterns/context-engineering/progressive-context-routing.md)
- Argument와 argument-gated disclosure → [Argument-Driven Assets](../../../../catalog/patterns/context-engineering/argument-driven-assets.md)
- Maintainer documentation → [Asset Maintainer Documentation](../../../documentation/asset-maintainer-documentation.md)
- 작성 원본과 권한 → [작성 원본과 권한](../../../development/source-authority.md)
- Repository-managed asset validation → [Validation](../../../development/validation.md)
- Deterministic test 설계와 PR Gate → [Testing](../../../development/testing.md)
- Behavioral evaluation → [Evaluation](../../../development/evaluation.md)