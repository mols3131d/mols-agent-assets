---
description: mols-text-optimizer를 변경할 때 보존해야 할 핵심 목표와 책임 경계를 설명하는 maintainer 문서입니다.
---

# Text Optimizer Goal

이 문서는 `mols-text-optimizer`가 왜 존재하고 어떤 성질을 잃으면 안 되는지만 기록한다. Runtime behavior의 canonical source는 `SKILL.md`다.

## Goal

`mols-text-optimizer`는 **더 구체적인 owner가 없는 텍스트에서 의미와 기능을 보존하면서 불필요한 표현 비용을 줄이는 범용 fallback Skill**이다.

우선순위는 항상 **의미·행동·정확성 보존 → 구조 보존 → 표현 비용 절감**이다. 더 짧은 표현이 의미 범위, 요구 강도, 조건·예외, 기술 식별자 또는 행동 효과를 흔들 수 있으면 줄이지 않는다. 안전한 절감이 없을 때 원문을 유지하는 것도 성공이다.

의미 안정성은 별도 기능이 아니라 축약의 제약이다. 가장 짧은 표현보다 같은 의미로 안정적으로 해석되는 더 가벼운 표현을 우선한다. 정확한 token 절감은 실제 tokenizer로 측정할 수 있을 때만 주장한다.

## Generic Fallback

대상이나 작업에 더 구체적으로 적용되는 Skill, 지침, 문서·도메인 guidance, framework contract 또는 procedure가 있으면 그 owner를 우선한다. 범용 편의성을 이유로 전문 owner의 책임이나 authority를 흡수하지 않는다.

이 선택 경계는 Skill의 부가 기능이 아니라 정체성의 일부다. 전문 owner를 가로채기 시작하면 더 이상 이 Goal을 충족하지 않는다.

## Boundaries

이 Skill은 정보를 줄이는 요약, 번역, humanization, tone/persona, 문법 교정, Markdown·문서 구조나 가독성 개선, latent context compression, tokenizer algorithm을 일반적으로 소유하지 않는다.

기능을 추가할 때도 **“의미와 기능을 보존하는 범용 표현 비용 절감”**이라는 한 문장으로 책임을 설명할 수 있어야 한다. 그렇지 않다면 이 Skill을 확장하기보다 더 구체적인 owner를 두는 방향을 우선 검토한다.

## Maintenance Check

변경 후에도 다음 질문에 모두 `예`라고 답할 수 있어야 한다.

- 전문 owner가 있으면 이 Skill이 물러나는가?
- 의미, 행동 효과, 정확한 기술 정보와 기존 구조가 절감보다 우선하는가?
- 안전한 경우에는 실제 표현이 가벼워지고, 불확실한 경우에는 원문을 유지할 수 있는가?
- 새로운 책임이나 정확하지 않은 token 절감 보장을 추가하지 않았는가?
