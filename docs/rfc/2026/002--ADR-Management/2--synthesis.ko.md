---
title: "ADR 지능적 관리 및 자동화 지형"
description: "Leni(정)의 효율성과 Kana(반)의 안정성을 통합한 합(Synthesis) 제안"
author: "User--Rin"
categories: ["synthesis"]
draft: false
date: 2026-02-28
lastmod: 2026-02-28
tags: ["ADR", "synthesis", "automation"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# Rin's Synthesis: 스마트 메타데이터 기반의 능동적 ADR 관리

## 1. 조정 (Reconciliation): 중앙의 편리함과 분산의 안정성

핵심 쟁점은 **"인덱스를 누가 어떻게 관리하느냐"**입니다. Leni는 에이전트의 시야를 위해 중앙 인덱스를 원하고, Kana는 그로 인한 관리 비용과 동기화 오류를 경고합니다. 이를 해결하기 위해 **'메타데이터가 진실의 원천이 되고, 인덱스는 이를 투영하는 결과물'**이 되는 구조를 제안합니다.

## 2. 통합 제안 (Integrated Proposal)

### 2.1. 프론트매터 중심의 상태 관리 (File-Level Truth)

- 모든 ADR 파일 내부에 상태값과 의존성을 명시합니다.
  ```yaml
  status: "accepted" # or "superseded"
  superseded_by: "/docs/adr/2026/02-28--0002--new-rule.md"
  ```
- 이렇게 하면 Kana가 우려한 '동기화 누락' 리스크가 줄어듭니다. 파일 자체가 정보를 들고 있기 때문입니다.

### 2.2. 에이전트 기반 자동 인덱싱 (Auto-Indexing)

- 사용자나 에이전트가 수동으로 표를 그리는 것이 아니라, 에이전트가 주기적으로(혹은 필요시) `/docs/adr/` 폴더를 스캔하여 **목록형 README를 자동 갱신**하게 합니다.
- Leni가 원한 '대시보드' 기능을 유지하되, 관리는 시스템(에이전트)에 맡겨 오버헤드를 최소화합니다.

### 2.3. AOS의 '참조형' 연동 (Referential Bonding)

- ADR 내용을 AOS에 중복 기재하지 않습니다.
- 대신 AOS에는 **"에이전트는 모든 결정 시 /docs/adr/의 최신 유효(Accepted) 결정을 최우선으로 준수한다"**는 선언적 규칙만 남기고, 구체적인 내용은 ADR 인덱스로 링크를 겁니다.

## 3. 결론 (Conclusion)

이 구조를 통해 우리는 **관리의 엄격함(Leni)**과 **운영의 민첩함(Kana)**을 모두 얻을 수 있습니다.

- **방법**: 에이전트가 각 작업 단계에서 `ADR Index`를 먼저 확인하고, 만약 결정이 상충한다면 프론트매터의 `superseded` 필드를 추적하여 최종 진실을 판단하도록 프로토콜화합니다.

---

_이 '합'은 에이전트가 지능적으로 문서를 인지하고 관리할 수 있다는 전제 하에 성립합니다. 이제 결정(9--final) 단계로 나아가 우리만의 ADR 관리 헌법을 확정할 준비가 되었습니다._
