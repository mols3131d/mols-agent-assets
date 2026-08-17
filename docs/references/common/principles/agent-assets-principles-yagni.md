---
title: YAGNI
description: 현재 evidence가 없는 capability와 abstraction을 에이전트 자산에 미리 넣지 않는 원칙
---

# YAGNI

에이전트 자산에서 YAGNI는 **현재 evidence가 없는 미래 capability를 예상해 설계하지 않는 것**이다.

> 현재 확인된 요구를 해결하고, 미래의 가상 요구는 미래의 정보로 결정한다.

## Evidence

강한 근거:

- 사용자가 현재 요구했다.
- 현재 지원 범위나 compatibility contract에 포함된다.
- 실제 task/eval에서 반복 실패가 관찰됐다.
- safety, data loss, security처럼 지금 대응하지 않으면 회복 비용이 크다.

약한 근거:

- 언젠가 필요할 것 같다.
- 다른 프로젝트에서 흔하다.
- 확장 가능해 보이면 좋을 것 같다.
- 첫 사례에서 일반화할 수 있을 것 같다.

약한 근거뿐이면 보류한다.

## Rules

- 소비자가 없는 option, metadata, provider branch를 만들지 않는다.
- 첫 사례에서 generic abstraction을 만들지 않는다.
- 미래 기능을 넣는 대신 나중에 바꾸기 쉬운 단순한 구조를 택한다.
- 추측한 edge case로 정상 경로를 복잡하게 만들지 않는다.
- 비가역적 위험은 미래 기능과 구분해 현재 guardrail로 다룬다.

## Decision Test

> 지금 이 요소를 소비하거나 요구하는 구체적인 evidence가 있는가?

없다면 추가하지 않는다. 단, 지금 미루면 안전이나 호환성 측면에서 회복하기 어려운 구체적 비용이 있을 때만 예외를 정당화한다.

## Boundary

현재 필요성이 확인된 뒤의 구조 단순화는 [KISS](agent-assets-principles-kiss.md), 책임 분리는 [SRP](agent-assets-principles-srp.md)가 맡는다.

## Sources

- [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html)
- [Agile Alliance: Simple Design](https://agilealliance.org/glossary/simple-design/)
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
