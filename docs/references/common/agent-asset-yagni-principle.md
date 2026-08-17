---
title: Agent Asset YAGNI Principle
description: 현재 요구되지 않은 capability와 abstraction을 에이전트 자산에 미리 넣지 않기 위한 원칙
---

# Agent Asset YAGNI Principle

에이전트 자산에서 YAGNI는 **현재 쓰이지 않는 미래 capability를 예상해 미리 설계하지 않는 것**이다.

> 현재의 확인된 요구를 해결하고, 미래의 가상 요구는 미래의 정보로 결정한다.

## Core Rules

1. **현재 evidence가 있는 요구만 구현한다.** 명시적 사용자 요구, 지원하기로 한 환경이나 계약, 실제 실패 사례가 근거가 된다.
2. **presumptive capability를 만들지 않는다.** 아직 쓰이지 않는 provider, workflow, output type, mode를 위한 branch와 option을 미리 추가하지 않는다.
3. **첫 사례에서 generic abstraction을 만들지 않는다.** 실제 변형이 나타난 뒤 공통점을 추출한다.
4. **미래 기능보다 변경 용이성을 확보한다.** 필요해졌을 때 쉽게 바꿀 수 있는 단순한 구조를 우선한다.
5. **추측한 edge case로 정상 경로를 복잡하게 만들지 않는다.** 발생 가능성과 영향이 근거로 확인된 예외만 선제적으로 다룬다.
6. **비가역적 위험은 별도로 판단한다.** 안전, 데이터 손실, 보안, 호환성처럼 나중에 고치기 매우 비싼 위험은 YAGNI를 이유로 미루지 않는다.

## Evidence Test

새 규칙, 옵션, 자산, abstraction을 추가하기 전에 묻는다.

> **지금 이 요소를 소비하거나 요구하는 구체적인 evidence가 있는가?**

강한 evidence:

- 사용자가 현재 요구했다.
- 현재 지원 범위나 compatibility contract에 포함된다.
- 실제 task나 eval에서 반복 실패가 확인됐다.
- 안전이나 비가역적 비용 때문에 지금 결정해야 한다.

약한 evidence:

- 언젠가 필요할 것 같다.
- 다른 프로젝트에서 흔히 쓴다.
- 확장 가능해 보이면 좋을 것 같다.
- 아직 한 사례뿐이지만 일반화할 수 있을 것 같다.

약한 evidence만 있다면 보류한다.

## Cost of Premature Capability

에이전트 자산에서 미래 기능은 코드만 늘리지 않는다.

- 항상 또는 조건부로 읽히는 context가 증가한다.
- routing과 activation 선택지가 늘어난다.
- 충돌 가능한 규칙과 예외가 늘어난다.
- test와 eval surface가 커진다.
- 사용하지 않는 기능도 유지보수 대상이 된다.

따라서 **사용되지 않는 capability도 현재 비용을 만든다.**

## What YAGNI Is Not

- 계획을 세우지 말라는 뜻이 아니다.
- 이미 확정된 요구를 무시하라는 뜻이 아니다.
- 안전성과 compatibility를 뒤로 미루라는 뜻이 아니다.
- 변경하기 어려운 결정을 아무 생각 없이 내리라는 뜻이 아니다.
- 나중에 바꾸기 어렵게 만들어도 된다는 뜻이 아니다.

YAGNI는 미래를 무시하는 것이 아니라 **미래에 대한 추측을 현재의 구현으로 확정하지 않는 것**이다.

## Anti-patterns

- 지원하지 않는 tool이나 provider를 위한 placeholder routing을 만든다.
- 한 종류뿐인 output에 strategy나 plugin abstraction을 추가한다.
- 실제 소비자가 없는 metadata field를 미리 정의한다.
- 미래 확장을 위해 configuration option을 계속 노출한다.
- 한 사례를 보고 base Skill이나 generic framework를 만든다.
- 관찰되지 않은 예외를 모두 root instruction에 추가한다.

## Review Question

> **이 요소는 현재 확인된 문제를 해결하는가, 아니면 미래의 가상 문제를 대비하는가?**

후자라면 보류한다. 지금 하지 않으면 회복하기 어려운 구체적인 비용이 있을 때만 예외를 정당화한다.

## Research Basis

- [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) — 미래에 필요할 것이라 추정한 feature와 abstraction을 미리 구현하는 비용을 설명한다.
- [Agile Alliance: Simple Design](https://agilealliance.org/glossary/simple-design/) — 모든 설계 요소에는 비용이 있으며 미래 이익만으로 복잡성을 정당화하지 말 것을 강조한다.
- [GitHub: Optimizing AI usage](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) — persistent instruction은 generic best practice가 아니라 실제 관찰된 agent behavior와 시스템 요구에 근거해야 한다고 권고한다.
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — 실제 실행 결과와 correction에서 reusable guidance를 추출하고 반복적으로 다듬도록 권고한다.
