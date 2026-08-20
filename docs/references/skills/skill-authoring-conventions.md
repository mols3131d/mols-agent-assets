---
title: Skill Authoring Conventions
description: Rulesync canonical Skill에 적용하는 repository-local authoring convention
---

# Skill Authoring Conventions

이 문서는 Rulesync와 target contract가 소유하지 않는 **mols의 Skill authoring 관행**만 정의합니다.

Canonical schema, field와 target namespace는 current Rulesync를 따릅니다. Portable/target contract가 필요하면 해당 official specification을 확인합니다.

## Package

Canonical entrypoint:

```text
src/rulesync/.rulesync/skills/<skill-name>/SKILL.md
```

기본은 single-file입니다. `SKILL.md` 하나로 activation과 runtime behavior가 충분하면 파일 길이만으로 분리하지 않습니다.

- chatbot/agent, flat/runtime을 별도 Skill taxonomy로 만들지 않습니다.
- 실제 runtime resource가 필요할 때만 `references/`, `scripts/`, `assets/`, `templates/`를 추가합니다.
- Runtime-required resource는 package 안에, repository verification은 `tests/`·`evals/`에 둡니다.
- Nested `SKILL.md`는 별도 entrypoint로 해석될 수 있으므로 supporting template 이름으로 사용하지 않습니다.

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

`docs/skills/<skill-name>/`은 source만으로 중요 intent/invariant를 복구하기 어렵거나 durable decision·recovery knowledge가 실제 maintenance cost를 낮출 때만 사용합니다. 단순하고 self-explanatory한 Skill에는 만들지 않습니다.

Maintainer-only knowledge를 runtime dependency로 숨기지 않습니다.

## Context-Only Naming

주책임이 workflow execution이 아니라 context discovery/loading이면 `load-context-<topic>`을 사용할 수 있습니다.

범용 loader와 개인 관행을 분리해야 하면 `load-context-<topic>-<owner>`를 personal overlay로 사용할 수 있습니다. 구현·mutation·검증·최종 output이 주책임인 Skill에는 `load-context-*`를 사용하지 않습니다.

## Target Metadata

Target-specific metadata는 의미가 있는 Rulesync target section에 둡니다. 현재 projection target이 아니라는 이유만으로 유효한 metadata를 제거하지 않습니다.

`agentsskills:`는 Agent Skills target section이지 repository-wide shared metadata namespace가 아닙니다. Shared passthrough schema를 추가하지 않습니다.

## Boundary

- Skill 설계 workflow → [Agent Skill Design Guide](agent-skills-guide.md)
- Rulesync/repository workspace boundary → [Rulesync](../tooling/rulesync.md)
- 검증 위치와 evidence 수준 → [Testing](../../testing.md)
