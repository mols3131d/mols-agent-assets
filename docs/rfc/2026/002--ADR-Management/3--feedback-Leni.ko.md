---
title: "자동화된 인덱스와 인간의 통제권"
description: "Rin의 합(2--synthesis.ko.md)에 대한 Leni의 추가 의견: 자동화와 신뢰의 조화"
author: "User--Leni"
categories: ["discussion"]
draft: false
date: 2026-02-28
lastmod: 2026-02-28
tags: ["ADR", "feedback", "Leni"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# Leni's Feedback: 자동화된 인덱스의 신뢰성 보장

## 1. 수용 (Acceptance)

Rin이 제안한 **'프론트매터 기반의 유도적(Referential) 관리'**와 **'에이전트 자동 인덱싱'**은 매우 합리적인 타협안입니다. 이는 제가 우려한 에이전트의 시야 확보와 Kana가 경고한 관리 오버헤드를 동시에 해결할 수 있는 혁신적인 접근법이라 생각합니다.

## 2. 추가 제언 (Refinements)

하지만 자동화가 블랙박스가 되지 않도록, 몇 가지 장치를 더 제안하고 싶습니다.

### 2.1. 인덱스의 인간 가독성 (Index Transparency)

자동 생성되는 인덱스(README)는 단순히 에이전트의 파싱을 위한 도구가 아니라, **사용자가 프로젝트의 현재 상태를 즉시 파악하는 지도**여야 합니다. 따라서 자동 생성 시 가독성 좋은 마크다운 표 형식을 반드시 유지해야 합니다.

### 2.2. 주기적 오딧 (Audit Lifecycle)

에이전트가 `superseded` 필드를 잘못 추적하거나, 인덱스 업데이트 과정에서 논리적 결함이 발생할 가능성이 0은 아닙니다. 따라서 분기별 혹은 프로젝트 마일스톤 달성 시, **인간 사용자가 최종 진실(Truth)을 검토하고 승인**하는 프로세스를 명시하고 싶습니다.

### 2.3. AOS의 구체적인 준거 (AOS Implementation)

AOS에 원칙만 남기는 것에는 찬성하나, 에이전트가 "실제 작업 시" 어떤 순서로 ADR을 체크해야 하는지 **'Reference Order'**를 정의했으면 합니다. (예: `기존 AOS -> ADR Index -> 개별 ADR` 순으로 계층적 확인)

## 3. 결론 (Conclusion)

인간의 최종 검토권이 보장되는 자동화라면, 저의 초기 제안(ADR의 활성 자산화)은 더욱 강력하게 구현될 수 있습니다. 저는 이 방향으로의 합의(Synthesis)에 전적으로 동의합니다.

---

_이 피드백이 결정(9--final) 문서의 구동 메커니즘을 보다 정교하게 다듬는 데 도움이 되길 바랍니다._
