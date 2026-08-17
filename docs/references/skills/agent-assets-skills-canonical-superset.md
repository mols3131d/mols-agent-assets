---
title: Skill Canonical Superset
description: 여러 agent와 chatbot target에 투영할 Skill의 repository-local canonical superset 기준
---

# Skill Canonical Superset

여러 Skill runtime에 같은 capability를 배포할 때의 권장 Superset은 **Agent Skills open-standard directory package**다.

```text
skill-name/
├─ SKILL.md
├─ references/   # optional
├─ scripts/      # optional
└─ assets/       # optional
```

이 형태는 activation metadata, instructions와 optional resources를 한 capability source에 보존하고, target이 더 작은 payload를 요구하면 필요한 projection으로 축소할 수 있다.

## Superset Owns

- capability identity와 responsibility
- activation intent와 discovery semantics
- 행동 contract와 invariant
- portability에 필요한 environment/compatibility requirement
- capability에 실제 필요한 references, scripts와 assets
- target마다 달라져야 하는 semantics가 있을 때 그 차이의 authoritative intent

Repository-local `.docs/`와 `.docs/baseline/`은 maintainer surface이며 runtime Superset payload 자체는 아니다.

## Why This Superset

Agent Skills package는 이 저장소의 `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/`보다 상위의 **portable source shape**로 사용하기 적합하다.

- `skills/`는 workspace-capable runtime에 최적화한다.
- `skills-chatbot/`은 self-contained single Markdown payload로 평탄화한다.
- `skills-chatbot-runtime/`은 hosted runtime의 bundled/progressive-loading surface에 맞춘다.

같은 capability가 여러 profile에 존재하는 것은 target별 projection이며, 필요한 semantic overlap 자체를 DRY 위반으로 보지 않는다.

## Projection

Target projection은 canonical capability를 재설계하지 않고 해당 target이 실제로 소비할 수 있는 형태로 적응시킨다.

```text
Agent Skills package
├─ workspace Skill
├─ flat chatbot Skill
├─ hosted-runtime Skill
└─ vendor-native Skill
```

Flat projection은 required runtime semantics를 한 Markdown에 완결하되, target budget을 맞추기 위해 capability의 본질을 임의로 삭제하지 않는다. Bundled resource가 필수라면 flat projection이 아니라 적절한 runtime profile을 선택한다.

Portable format의 상세 규격은 [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md), repository-local profile과 package surface는 [Skill Target Profiles](agent-assets-skills-target-profiles.md)가 소유한다.

## Boundary

- 이 문서는 Skill 유형의 **최적 canonical Superset**을 소유한다.
- 모든 target이 Agent Skills package를 그대로 소비한다고 가정하지 않는다.
- target-native metadata와 runtime feature를 Tier 1 portable field로 가장하지 않는다.
- 하나의 target만 필요한 Skill에 불필요한 sibling projection을 만들지 않는다.
- target projection은 canonical capability의 source authority를 암묵적으로 가져가지 않는다.
