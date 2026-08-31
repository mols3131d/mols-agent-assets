---
description: mols-text-optimizer를 변경할 때 보존해야 할 핵심 목표와 책임 경계를 설명하는 maintainer 문서입니다.
---

# Text Optimizer Goal

이 문서는 `mols-text-optimizer`의 핵심 목표와 유지보수 불변조건만 기록한다. Runtime behavior의 canonical source는 `SKILL.md`다.

## Goal

`mols-text-optimizer`의 목표는 **주어진 텍스트의 material meaning과 기능을 유지하면서 불필요한 wording 비용을 줄이는 것**이다.

더 짧은 표현이 의미, 행동 효과 또는 정확한 기술 정보를 흔들 수 있다면 줄이지 않는다. 안전한 절감이 없을 때 원문을 유지하는 것도 올바른 결과다.

Semantic stability는 별도 기능이 아니라 optimization의 제약이다. 가장 짧은 표현보다 **같은 의미로 안정적으로 해석되는 더 가벼운 표현**을 우선한다.

## Generic Fallback

이 Skill은 범용 fallback이다. 대상이나 작업에 더 구체적으로 적용되는 Skill, 지침, 문서·도메인 guidance, framework contract 또는 procedure가 있으면 그 owner를 우선한다.

범용 편의성을 이유로 전문 owner의 책임이나 authority를 흡수하지 않는다. 이 경계가 흐려지면 Skill의 activation 범위가 넓어지고 전문 자산과 충돌한다.

## Preserve

이 Skill을 변경할 때 다음 성질을 함께 보존한다.

- **substance before reduction** — 정보, 요구사항, 조건, 예외, 불확실성과 관계를 wording 절감보다 우선한다.
- **behavioral identity** — instruction, policy, prompt 같은 agent-facing text에서는 activation, permission, prohibition, gate와 stop condition의 효과를 유지한다.
- **exact technical identity** — identifier, path, command, API, 수치, 단위와 literal token을 임의로 바꾸지 않는다.
- **protected structure** — section, 문단, 목록, 순서, delimiter와 exact format contract를 optimization 대상으로 삼지 않는다.
- **safe no-op** — 의미 보존이 불확실하거나 절감 가치가 작으면 원문을 유지할 수 있다.

## Boundaries

이 Skill은 요약, 번역, humanization, tone/persona, 문법 교정, Markdown 재구성, 문서 가독성 설계, latent context compression 또는 tokenizer algorithm을 일반적으로 소유하지 않는다.

향후 기능을 추가할 때도 **의미와 기능을 보존하는 범용 wording-cost reduction**이라는 한 문장으로 책임을 설명할 수 있어야 한다. 그렇지 않다면 이 Skill을 확장하기보다 더 구체적인 owner를 두는 방향을 우선 검토한다.
