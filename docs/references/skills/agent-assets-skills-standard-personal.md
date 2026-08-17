---
title: Personal Skill Standard
description: Agent Skills Specification을 확장한 repository-local Skill authoring과 deployment 표준
---

# Personal Skill Standard

이 문서는 [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)을
기반으로 이 저장소에서 사용하는 **Skill-specific repository-local extension**을
정의한다.

Portable format과 front matter 규격은 Specification이 소유한다. 이 문서는 그
규격을 복사하거나 재정의하지 않고, 이 저장소에서 추가한 convention만 소유한다.

## Extension Model

Skill 규칙은 다음 두 층으로 구분한다.

1. **Specification** — portable `SKILL.md`, front matter, standard resource convention.
1. **Personal Standard** — 이 저장소의 source/deployment profile과 추가 convention.

Target runtime의 mandatory contract가 있으면 repository-local convention보다
우선한다. Personal Standard를 외부 Agent Skills specification의 일부처럼
표현하지 않는다.

## Front Matter

표준 front matter field와 constraint의 authoritative reference는
[Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이다.

현재 Personal Standard는 **추가 required top-level front matter field를
정의하지 않는다**.

Repository-local 추가 metadata가 필요하면 portable한 경우 표준 `metadata`
mapping을 우선한다. 특정 host가 별도 top-level field를 요구하면 해당 host/profile
규칙으로 다루고 Agent Skills 표준 field처럼 일반화하지 않는다.

## Personal Extensions

이 저장소의 Skill 확장은
[Skill Target Profiles](agent-assets-skills-target-profiles.md)가 상세 규격을
소유한다.

그 문서가 다음을 정의한다.

- `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` target profile
- flat chatbot payload budget
- directory package의 runtime/non-runtime surface
- `.docs/baseline/` preservation convention
- `load-context-*` context-only naming convention

이 목록은 extension registry이며 상세 constraint를 이 문서에 복제하지 않는다.

## Authority Boundary

새 Skill rule을 추가할 때 먼저 확인한다.

- 외부 Specification에 이미 정의된 규칙인가? → Specification reference가 소유한다.
- 이 저장소에서만 필요한 추가 규칙인가? → Personal Standard 또는 focused detail이 소유한다.
- 특정 target profile에만 필요한가? → 해당 profile reference가 소유한다.
- 특정 Skill 하나에만 필요한가? → 그 Skill 내부 contract로 둔다.

Personal convention이 더 이상 필요하지 않으면 삭제한다. 외부 Specification으로
편입된 규칙은 이 문서에서 중복 소유하지 않는다.
