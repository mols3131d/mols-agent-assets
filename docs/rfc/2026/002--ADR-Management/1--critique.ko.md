---
title: ADR 관리 체계의 경직성과 오버헤드
description: "Leni의 제안(0--proposal.md)에 대한 비판: 동기화 리스크 및 관리 비용 분석"
author: User--Kana
categories:
  - RFC
draft: false
date: 2026-02-28
lastmod: 2026-02-27T17:06:42.649Z
tags:
  - ADR
  - critique
  - overhead
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# Kana's Antithesis: 중앙 집중화된 인덱스의 위험성

## 1. 개요 (Overview)

Leni의 제안은 ADR의 검색성과 구속력을 높이는 데 기여하지만, 실제 운영 환경에서의 **'동기화 실패'**와 **'관리 오버헤드'**라는 치명적인 리스크를 간과하고 있습니다.

## 2. 주요 비판 (Key Critiques)

### 2.1. 인덱스 동기화의 단일 장애점 (Single Point of Failure)

- **리스크**: ADR 파일은 생성되었으나 인덱스(README) 업데이트를 깜빡할 경우, 에이전트와 사용자는 해당 결정이 존재하지 않는 것으로 오판하게 됩니다.
- **결과**: 파일 시스템의 실제 상태와 인덱스 표의 불일치는 에이전트에게 환각(Hallucination)을 유발하거나 잘못된 규칙을 적용하게 만드는 원인이 됩니다.

### 2.2. 복잡한 의존성 관리의 병목 (Dependency Bottleneck)

- **비판**: `superseded` 필드를 통한 교체 메커니즘은 결정이 소수일 때는 유효하나, 수십 개의 결정이 사슬처럼 얽힐 경우(A가 B를 교체하고, C가 A의 일부를 수정하는 등) 관리가 기하급수적으로 복잡해집니다.
- **우려**: 에이전트가 "현재 유효한 규칙"을 찾기 위해 여러 ADR의 꼬리를 물고 읽어야 한다면, 작업 속도가 급격히 저하될 것입니다.

### 2.3. AOS와 ADR의 역할 중복

- **비판**: ADR의 결정을 AOS에 즉시 반영하자는 제안은 동일한 정보를 두 군데 이상 관리하게 만듭니다.
- **문제**: 지식의 원천(Source of Truth)이 파편화되면, 나중에 AOS를 수정할 때 ADR을 놓치거나 그 반대의 상황이 발생할 확률이 매우 높습니다.

## 3. 대안적 관점 (Alternative Perspective)

- **자동화된 검색**: 수동으로 표를 업데이트하기보다, 에이전트가 `grep`이나 파일 탐색을 통해 최신 ADR을 스스로 식별하는 능력을 키워야 합니다.
- **최소주의**: 인덱스는 '목록' 역할만 수행해야 하며, 상세한 상태값이나 의존성 관계는 프론트매터 내부에서 분산 관리되어야 합니다.

---

_중앙 관리는 언제나 '관리 실패'라는 비용을 동반합니다. 린(Rin)은 이러한 구조적 경직성과 에이전트의 자율성 사이의 균형을 어떻게 맞출 수 있을지 고민해 주길 바랍니다._
