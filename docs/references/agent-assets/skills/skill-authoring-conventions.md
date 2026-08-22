---
title: Skill Authoring Conventions
description: source framework과 target contract가 소유하지 않는 mols의 reusable Skill authoring convention
---

# Skill Authoring Conventions

이 문서는 source framework와 target contract가 소유하지 않는 **mols의 Skill authoring 관행**만 정의합니다.

## Package

Required entrypoint, path, metadata와 discovery semantics는 실제 authored source framework와 target contract가 소유합니다. 이 convention은 그 representation을 다시 정의하지 않습니다.

실제 entrypoint가 정해진 뒤에는 기본적으로 single-file을 선호합니다. 하나의 entrypoint로 activation과 runtime behavior가 충분하면 파일 길이만으로 분리하지 않습니다.

- chatbot/agent, flat/runtime을 별도 Skill taxonomy로 만들지 않습니다.
- 실제 runtime resource가 필요할 때만 supporting reference, script, asset 또는 template을 추가합니다.
- Runtime-required resource는 deployable Skill package 안에, repository-only verification은 host의 `tests/`·`evals/` 같은 verification surface에 둡니다.
- Supporting material이 host에서 별도 Skill entrypoint로 발견될 수 있는 이름이나 위치를 사용하지 않습니다.

Rulesync를 canonical source로 사용하는 이 repository의 구체적인 workspace와 path는 [Rulesync](../../tooling/rulesync.md)와 [Source Authority](../../../development/source-authority.md)가 소유합니다.

## Markdown Responsibility

Single-file Skill에서는 여러 top-level `#` heading을 **독립적인 Markdown responsibility boundary**로 사용할 수 있습니다.

- 한 heading은 한 책임을 가집니다.
- `##` 이하는 부모 책임을 점진적으로 분해합니다.
- 같은 depth는 비슷한 abstraction level을 유지합니다.
- 공통 invariant는 가장 가까운 공통 owner에 한 번만 둡니다.
- 의미 없는 미세 분할은 하지 않습니다.

## Discovery and Body

Canonical `description`은 Skill 선택에 필요한 capability, 적용 상황과 중요한 negative boundary에 집중합니다.

Prerequisite, fallback, handoff, execution order와 validation workflow는 body가 소유합니다. Body는 Skill이 이미 선택되어 로드되었다고 가정합니다.

## Maintainer Documentation

Skill maintainer documentation의 placement, family ownership과 portability contract는 [Asset Capsules](../../../document/asset-capsules.md)가 소유합니다.

Maintainer-only knowledge를 runtime dependency로 숨기지 않습니다.

## Context-Only Naming

주책임이 workflow execution이 아니라 domain-specific context discovery/loading이면 `<domain>-context`를 사용합니다.

`domain`은 context가 적용되는 문제·지식·runtime surface를 사람이 구분할 수 있을 만큼만 표현합니다. 구현·mutation·검증·최종 output이 주책임인 Skill에는 `-context`를 사용하지 않습니다.

이 naming은 Skill family convention이지 별도 Agent Asset type이나 metadata schema가 아닙니다.

## Target Metadata

유효한 target-specific metadata는 현재 projection target이 아니라는 이유만으로 제거하지 않습니다.

Repository-wide shared metadata를 만들기 위해 target namespace를 재사용하거나 passthrough schema를 추가하지 않습니다.

## Boundary

- Agent Skills standard와 target source registry → [Agent Skills Specification](specification.md)
- Rulesync/repository workspace boundary → [Rulesync](../../tooling/rulesync.md)
- 검증 위치와 evidence 수준 → [Testing](../../../development/testing.md)
