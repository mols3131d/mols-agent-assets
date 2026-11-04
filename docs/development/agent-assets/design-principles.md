---
title: Agent Asset Design Principles
description: Agent Asset 추가·분리·단순화 시 원본 권한, 실제 필요, 책임과 context 비용을 판단할 때 사용합니다.
---

# Agent Asset Design Principles

**적용되는 계약을 우선하고 현재 필요한 행동을 최소한의 책임 구조로 유지합니다.** 파일 수·길이보다 행동 신뢰성, 정본 일관성, 이해·검증·변경 비용을 기준으로 판단합니다.

## 판단 순서

1. **Standard First / Local Delta Only** — 적용되는 표준, source framework, target/runtime과 프로젝트 권한이 이미 결정한 행동은 복제하지 않습니다. Local content는 의도적 차이(deviation), 없는 기능의 확장(extension), 모호성 해소(ambiguity resolution)만 소유합니다.
1. **YAGNI** — 현재 요구, 관찰된 실패, 승인된 정책 또는 보존할 근거 있는 불변조건이 없는 구조·호환성·metadata·instruction은 만들지 않습니다. 가상의 미래 요구나 막연한 모델 불안정성은 근거가 아닙니다.
1. **SRP** — activation, authority, permission, lifecycle, validation 또는 변경 이유가 실질적으로 다를 때 책임을 나눕니다. 길이만으로 나누거나 항상 함께 적용·변경되는 책임을 쪼개지 않습니다.
1. **DRY** — 같은 의미의 정본은 하나만 둡니다. 다른 책임자는 link·reference·composition으로 연결하되 runtime 독립성을 해치는 숨은 의존성을 만들지 않습니다.
1. **KISS** — 이해·운영·검증에 기여하지 않는 복잡성만 제거합니다. 단순화를 위해 필요한 경계·검증·안전 장치를 없애거나 서로 다른 책임을 합치지 않습니다.
1. **Progressive Disclosure** — discovery → core → conditional detail로 필요한 맥락만 노출합니다. 세부 정보를 분리해도 언제 읽어야 하는지와 중요한 예외는 가까운 진입점에서 찾을 수 있어야 합니다.

앞 단계에서 해결할 수 있는 문제를 뒤 단계의 추상화나 instruction 추가로 보완하지 않습니다.

## 원본과 실행 수단

재사용 자산에 작성 저장소의 경로·명령·권한·평가 환경을 필수 조건으로 넣지 않습니다. 프로젝트 전용 동작은 그 프로젝트가 소유합니다. 변경이 위의 local delta 세 유형에 해당하지 않으면 별도 지침을 추가하지 않고 현재 정본이나 공식 자료로 연결합니다. 빠르게 바뀌는 외부 계약도 복제하지 않습니다.

규칙을 실제로 강제·검증하는 native 또는 deterministic 수단이 있고, 필요한 이식성과 정본 단일성을 해치지 않는다면 prose instruction보다 우선합니다. 반대로 모델의 의미 판단·예외 처리가 필요한 행동은 읽을 수 있는 instruction에 둡니다. 특정 target/version의 중요한 차이나 안전 경계를 일반화해서 없애지 않습니다.

## 맥락과 유지보수

자동 또는 자주 로드하는 맥락은 **없으면 반복 오류가 생기는 지식, 보존할 불변조건, 현재 결정을 바꾸는 근거·선택 조건**에 집중합니다. 그 역할이 없다면 제거하거나 정본으로 연결하거나 조건부 로딩으로 내립니다. 비가역적 위험과 중요한 금지·중단 조건은 간결함을 이유로 숨기지 않습니다.

사람이 정본·책임·변경 이유를 이해할 수 있도록 원본만으로 복구하기 어려운 durable rationale과 불변조건은 남깁니다. 재생성 가능한 상태와 일반 작업 기록은 Git history에 맡깁니다.

## Boundary

- 행동을 instruction으로 표현하는 방법 → [Instruction Design](instruction-design.md)
- Skill-specific 작성 관행 → [Skill Authoring Conventions](skills/skill-authoring-conventions.md)
- 반복적인 해결 방식 → [Patterns](../../../catalog/patterns/README.md)
- source framework·target의 형식, precedence, loading 계약 → 해당 공식 원본

## Sources

- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
