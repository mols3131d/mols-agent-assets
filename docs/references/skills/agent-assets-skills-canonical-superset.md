---
title: Skill Canonical Superset
description: 여러 agent와 chatbot target에 투영할 Skill의 repository-local canonical superset 기준
---

# Skill Canonical Superset

## Chosen Superset

여러 Skill runtime에 같은 capability를 배포할 때 이 저장소의 최적 Superset은 **Agent Skills open-standard directory package**다.

```text
skill-name/
├─ SKILL.md
├─ references/   # optional
├─ scripts/      # optional
└─ assets/       # optional
```

이 source shape는 activation metadata, instructions와 optional resources를 한 capability authority에 보존하면서, 더 제한적인 target에는 flat 또는 host-native projection을 만들 수 있다. 공개 규격이 존재하므로 vendor 하나의 private schema를 canonical layer로 삼는 것보다 portability가 높다.

## Superset Owns

- capability identity와 responsibility
- activation intent와 discovery semantics
- 행동 contract와 invariant
- portability에 필요한 environment/compatibility requirement
- capability에 실제 필요한 references, scripts와 assets
- target마다 달라져야 하는 semantics가 있을 때 그 차이의 authoritative intent

Repository-local `.docs/`와 `.docs/baseline/`은 maintainer surface이며 runtime Superset payload 자체는 아니다.

## Repository Projections

```text
Agent Skills package
├─ skills/                  # workspace-capable
├─ skills-chatbot/          # flat single Markdown
├─ skills-chatbot-runtime/  # hosted bundled/runtime
└─ vendor-native Skill
```

- `skills/`는 workspace/filesystem/shell authority가 필요한 runtime에 최적화한다.
- `skills-chatbot/`은 self-contained single Markdown payload로 평탄화한다.
- `skills-chatbot-runtime/`은 bundled resources와 progressive loading이 필요한 hosted runtime에 최적화한다.

같은 capability가 여러 profile에 존재하는 것은 target별 projection이다. 독립 payload에 필요한 semantic overlap 자체를 DRY 위반으로 보지 않는다.

## Projection Rule

Target projection은 canonical capability를 재설계하지 않고 해당 target이 실제로 소비할 수 있는 형태로 적응시킨다.

Flat projection은 required runtime semantics를 한 Markdown에 완결하되 capability의 본질을 token budget 때문에 임의로 삭제하지 않는다. Bundled resource가 capability에 필수라면 flat projection 대신 적절한 runtime profile을 선택한다.

Target이 canonical Agent Skills package를 직접 소비할 수 있으면 별도 sibling을 만들지 않고 direct reuse를 우선한다.

Portable format의 상세 규격은 [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md), repository-local profile과 package surface는 [Skill Target Profiles](agent-assets-skills-target-profiles.md)가 소유한다.

## Primary Reference

- [Agent Skills Specification](https://agentskills.io/specification) — portable `SKILL.md` package와 optional resource surface

## Boundary

- 이 문서는 Skill 유형의 **최적 canonical Superset**을 소유한다.
- 모든 target이 Agent Skills package를 그대로 소비한다고 가정하지 않는다.
- target-native metadata와 runtime feature를 Tier 1 portable field로 가장하지 않는다.
- 하나의 target만 필요한 Skill에 불필요한 sibling projection을 만들지 않는다.
- target projection은 canonical capability의 source authority를 암묵적으로 가져가지 않는다.
