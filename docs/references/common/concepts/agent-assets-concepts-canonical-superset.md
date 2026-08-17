---
title: Canonical Superset Agent Assets
description: Agent Asset 유형에 공통되는 canonical superset과 target projection 관계
---

# Canonical Superset Agent Assets

**Canonical Superset**은 여러 target에서 같은 Agent Asset을 관리하기 위한 repository-local authoring spec이다.

특정 변환 backend, CLI, vendor file format의 source schema가 아니다. Superset 문서는 **무엇을 보존해야 하는지와 canonical field를 정의**하고, 실제 target file 생성 방식은 별도 tooling/workflow가 소유한다.

## Common Model

```yaml
---
<common fields>
targets: [<target>]

<target>:
  <target-specific fields>
---

<canonical body>
```

- **Common fields** — 여러 target에서 같은 의미를 가지는 canonical semantics.
- **Target namespace** — 특정 harness에서만 의미가 있는 extension 또는 override.
- **Body** — 해당 자산 유형의 핵심 natural-language contract.

Target block의 존재는 특정 backend 사용을 의미하지 않는다. 예를 들어 `copilot:`이나 `antigravity:`는 단지 해당 target에서만 필요한 정보를 보존하는 namespace다.

## Rules

1. 공통으로 표현할 수 있는 의미를 target block에 복제하지 않는다.
1. Target-specific capability를 억지로 공통 field로 일반화하지 않는다.
1. 같은 target 의미의 authority는 한 곳에만 둔다.
1. Projection 과정의 omission, approximation, unsupported semantics를 숨기지 않는다.
1. Canonical spec과 generated/native target asset의 의미가 충돌하면 canonical spec을 먼저 검토한다.

필요한 semantic overlap은 DRY 위반이 아니다. DRY 문제는 같은 의미가 여러 **독립 authority**로 갈라지는 경우다.

## Type-Specific Supersets

- [Rule Canonical Superset](../../rules/agent-assets-rules-canonical-superset.md)
- [Skill Canonical Superset](../../skills/agent-assets-skills-canonical-superset.md)
- [Prompt Canonical Superset](../../prompts/agent-assets-prompts-canonical-superset.md)
- [Agent Canonical Superset](../../agents/agent-assets-agents-canonical-superset.md)

## Boundary

이 문서는 공통 ownership과 extension convention만 소유한다. 각 자산의 실제 field, requiredness, body contract는 유형별 Superset 문서가 소유한다.

변환 backend, generator, sync Skill, CLI command, target path는 Superset spec의 일부가 아니다.
