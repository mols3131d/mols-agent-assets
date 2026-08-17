---
title: Personal Skill Standard
description: Agent Skills 외부 규격 위에 적용하는 repository-local Skill 확장 표준
---

# Personal Skill Standard

이 문서는 이 저장소에서만 사용하는 **Skill-specific repository-local extension**을
정의한다.

외부 규격의 authority chain과 공식 링크 registry는
[Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이
소유한다. 이 문서에서는 Tier 1 또는 vendor/harness 규칙을 다시 정의하지 않는다.

## Apply After External Contracts

Personal Standard는 적용 가능한 외부 contract를 만족한 뒤 적용한다.

- Portable Agent Skill 규격 → Tier 1 Specification
- Target-specific 추가·제약 → 해당 Tier 2 공식 원문
- Repository-local 추가 convention → 이 Personal Standard

Target runtime의 mandatory contract가 repository-local convention보다 우선한다.

## Front Matter

표준 front matter field와 constraint는
[Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이
소유한다.

현재 Personal Standard는 **추가 required top-level front matter field를 정의하지
않는다**.

Repository-local 추가 metadata가 필요하면 portable한 경우 표준 `metadata`
mapping을 우선한다. 특정 host가 별도 top-level field를 요구하면 Tier 2
host-specific contract로 다루며 portable field처럼 일반화하지 않는다.

## Personal Extensions

Repository-local target profile과 package surface 상세는
[Skill Target Profiles](agent-assets-skills-target-profiles.md)가 소유한다.

현재 Personal Skill Standard의 extension registry는 다음과 같다.

- `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` target profile
- flat chatbot payload budget
- directory package의 runtime/non-runtime surface
- `.docs/baseline/` preservation convention
- `load-context-*` context-only naming and activation convention

상세 constraint는 이 문서에 복제하지 않는다.

## Ownership Test

새 Skill 규칙은 가장 좁은 authoritative owner에 둔다.

- Portable 공통 규격 → Tier 1 Specification
- 특정 vendor/harness 규격 → Tier 2 공식 원문 링크
- Repository 전체의 Skill 확장 → Personal Standard
- 특정 target profile 상세 → 해당 focused reference
- 특정 Skill 하나의 contract → 해당 Skill

Personal convention이 더 이상 필요하지 않으면 삭제한다. 외부 표준이나 target
contract로 편입된 규칙을 중복 소유하지 않는다.
