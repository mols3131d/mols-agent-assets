---
title: ADR 효율적 관리 체계 제안
description: ADR의 검색성, 생명주기 관리 및 에이전트 구속력 강화를 위한 구조 제안
author: User--Leni
categories:
  - RFC
draft: false
id: rfc-002
date: 2026-02-28
lastmod: 2026-02-27T17:06:30.305Z
tags:
  - ADR
  - management
  - standard
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# Leni's Thesis: ADR 검색성 및 생명주기 고도화

## 1. 제안 배경 (Context)

ADR(Architecture Decision Record)은 시간이 흐름에 따라 누적되는 특성을 가집니다. 파일이 수십 개 이상 쌓이다 보면, 에이전트가 어떤 결정이 현재 유효한지(Effective) 혹은 과거의 것(Archived)인지 구분하는 데 비용이 발생합니다. 또한, 개별 파일로 흩어진 지식은 실시간 작업에서 구속력을 갖기 어렵습니다.

## 2. 핵심 제안 (Proposal)

ADR 관리를 단순한 '기록'에서 **'살아있는 규칙(Living Rules)'**으로 전환하기 위해 다음의 세 가지 메커니즘을 제안합니다.

### 2.1. 인덱스 기반 검색성 (Index-Driven Searchability)

- **ADR Master Index**: `/docs/adr/README.ko.md`를 단순한 가이드가 아닌, 모든 ADR의 '현재 상태'를 보여주는 **동적 대시보드**로 운영합니다.
- **상태 관리**: 표(Table) 형식을 사용하여 `ID | 제목 | 상태(Accepted/Superseded) | 관련 파일`을 한눈에 보게 함으로써, 에이전트가 단 하나의 파일만 읽고도 유효한 결정을 즉시 파악하게 합니다.

### 2.2. 불변성과 교체 메커니즘 (Immutability & Superseded)

- **결정의 불변성**: 한 번 확정된 ADR 파일 자체는 절대 수정하지 않습니다.
- **교체(Supersede)**: 결정이 변경될 경우 새로운 ADR을 작성하고, 기존 ADR의 프론트매터에 `superseded: [New-ADR-ID]` 필드를 추가하여 에이전트가 과거의 정보를 무시하도록 유도합니다.

### 2.3. 에이전트 구속력 강화 (AOS Bonding)

- **AOS와의 연결**: 시스템 수준의 핵심 결정은 **에이전트 운영 표준(AOS)**에 즉시 반영하거나, 링크를 통해 에이전트의 '상시 주의 사항'으로 격상시킵니다.
- **Reference Protocol**: 에이전트는 모든 실행(`[EXEC]`) 전, 워크워크플로우와 관련된 최신 ADR 인덱스를 먼저 훑어보는 것을 습관화합니다.

## 3. 기대 효과 (Expected Effects)

- **검색 비용 감소**: 수많은 파일 대신 인덱스 표 하나로 최신 상태 확인 가능.
- **논리적 일관성**: 과거 결정과 현재 결정이 충돌할 경우, Supersede 체계를 통해 명확한 우선순위 제공.
- **실전 활용도 향상**: 죽은 문서가 아닌, 에이전트 행동을 직접 제어하는 활성 자산화.

---

_이 제안은 ADR이 단순한 '일기'가 아닌, 프로젝트의 '헌법'으로서 강력하고 효율적으로 작동하게 하는 것을 목표로 합니다. 카나(Kana)의 비판적인 검토를 기다립니다._
