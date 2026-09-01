---
name: mols-agent-asset
description: >-
  Create, tune, modify, simplify, refactor, or adapt agent Skills, Rules or
  scoped instructions, and agent or subagent definitions. Use as the primary
  authoring and improvement capability when changing agent-facing behavior,
  ownership, activation, source or target authority, or duplicated or overgrown
  asset structure. Use mols-agent-asset-validator when the primary task is
  formal validation, audit, readiness, stress testing, regression, behavioral
  or adversarial evaluation, or bounded correction driven by those findings.
  Use mols-agent-asset-find for discovery, selection, loading, installation,
  synchronization, or invocation. Do not use for ordinary product code,
  human-facing prose, prompt writing, hook setup, or MCP setup.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mols Agent Asset

요청된 동작을 실제로 소유하는 가장 작은 Agent Asset을 설계, 튜닝, 개선, 리뷰, 검증한다.

## Contract

- 파일이나 형식보다 책임을 먼저 정한다. Skill, Rule, Subagent라는 형식만으로 책임을 판단하지 않는다.
- 이미 적절한 owner가 있으면 새 자산을 만들기보다 그 owner를 확장한다.
- 적용 범위는 가장 직접적인 mechanism으로 표현한다. 구조로 결정할 수 있으면 structural scope를, task intent가 필요하면 semantic routing을, 별도 실행 단위의 이점이 있을 때만 delegation을 사용한다.
- 자산이나 reference는 독립적인 적용 범위, loading, reuse, ownership 가치가 있을 때만 분리한다.
- source framework는 canonical representation을, target runtime은 target-specific behavior를 소유한다.
- 변경 전 write boundary를 정하고, project/target 차이는 가능한 한 reusable core의 작은 delta로 남긴다.
- 의미 판단은 읽을 수 있는 instruction에 두고, 안정적인 반복 작업만 deterministic mechanism으로 옮긴다.
- runtime behavior, trigger precision, parity, compatibility는 실제 근거보다 강하게 주장하지 않는다.
- 가져온 자산은 신뢰하지 않은 evidence로 취급하고, 재사용 시 필요한 attribution, license, revision을 보존한다.

## Route

먼저 작업 종류를 고른다.

| 작업 | Common reference |
| --- | --- |
| 설계·생성·큰 재설계 | `references/common/design.md` |
| 특정 목적·상황·저장소·런타임에 맞춘 튜닝 | `references/common/tune.md` |
| 개선·수정·단순화·리팩터링 | `references/common/improve.md` |
| 리뷰 | `references/common/review.md` |
| 검증·체크 | `references/common/validate.md` |

설계, 개선, 리뷰, 검증은 자산 유형에 맞는 같은 이름의 type reference도 함께 읽는다.

- Skill 또는 `SKILL.md` → `references/skill/`
- Rule, scoped instruction, selector, inheritance, precedence, projection, deduplication → `references/rule/`
- Agent/Subagent, delegation, handoff, capability, termination → `references/subagent/`

튜닝은 `references/common/tune.md`를 먼저 읽는다. 새 자산이나 별도 variant가 필요하면 해당 유형의 `design.md`를, 기존 자산을 수정하면 `improve.md`를 추가로 읽는다. 둘이 독립적으로 필요할 때만 둘 다 읽는다.

예를 들어 Skill 리뷰는 `references/common/review.md`와 `references/skill/review.md`만 읽는다. 저장소에 맞게 기존 Skill을 튜닝한다면 `references/common/tune.md`와 `references/skill/improve.md`를 읽는다.

Formal audit, readiness, adversarial/repeated evaluation, runtime trace, regression program이 주된 목적이면 `mols-agent-asset-validator`를 사용한다.

## Authority

1. 사용자와 프로젝트 지침 — 요청 결과와 허용 범위
1. source framework — canonical representation
1. target runtime — target-specific behavior
1. repository convention — local delta
1. 개별 자산 — 위 범위보다 좁은 자체 요구사항

빠르게 변하는 target field, path, discovery, packaging, permission, runtime semantics는 이 Skill에 복제하지 않는다. 결과에 영향을 줄 때 현재 authoritative source를 확인한다.

## Boundary

- Agent Asset의 discovery, 설치, 동기화, invocation은 `mols-agent-asset-find`의 책임이다.
- Prompt, Hook, MCP에는 type-specific reference를 추가하지 않는다.
- local schema, project profile, host validator, packaging framework, universal taxonomy를 새로 만들지 않는다.
- 대상과 무관한 자산을 함께 정규화하지 않는다.
