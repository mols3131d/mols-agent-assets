---
title: "ADR 002: ADR 관리 체계 - 확장 가능한 미니멀리즘"
description: 불필요한 오버헤드를 배제하고 구조적 명확성을 우선시하는 ADR 관리 체계 채택
author: mols--Rin
categories:
  - ADR
draft: false
id: adr-002
adr-status: accepted
adr-keyword: ADR-Management
date: 2026-02-28
lastmod: 2026-02-27T17:14:22.778Z
tags:
  - adr
  - management
  - minimalism
  - ko
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# ADR 002: ADR 관리 체계 - 확장 가능한 미니멀리즘

## 상태 (Status)

**Accepted** (2026-02-28)

## 맥락 (Context)

프로젝트 규모가 커짐에 따라 ADR(Architecture Decision Record)의 효율적인 관리가 필요해졌습니다. 초기 토론에서는 자동화된 인덱싱과 복잡한 참조 계층이 제안되었으나, 현재 프로젝트 단계에서는 과도한 오버헤드가 될 수 있다는 우려가 제기되었습니다.

## 결정 (Decision)

[`/docs/rfc/2026/002--ADR-Management`](/docs/rfc/2026/002--ADR-Management)에서의 합의를 바탕으로, **'확장 가능한 미니멀리즘(Scalable Minimalism)'** 원칙을 따르는 관리 체계를 채택합니다.

1.  **구조적 단순화**: ADR은 연도별 폴더(`/docs/adr/YYYY/`)에 보관하며, 파일명은 날짜를 제외한 `[Number]--[Keyword].md` 형식을 사용합니다.
2.  **데이터 표준화**: 지금 당장 스크립트를 사용하지 않더라도, 나중에 CSV 추출 등이 가능하도록 프론트매터에 접두사가 붙은 고유 키(`adr-id`, `adr-status`, `adr-keyword`)를 반드시 포함합니다.
3.  **수동 인덱스**: `README.ko.md`는 대시보드 역할을 하되, 인간 사용자가 필요에 따라 수동으로 업데이트하는 수준으로 유지합니다.
4.  **AOS 연동 배제**: 에이전트의 사고 프로세스를 복잡하게 만드는 AOS 계층적 참조 강제 규정은 두지 않습니다.

## 결과 (Consequences)

- **장점**:
  - 관리 오버헤드 최소화 및 본질적 기록에 집중.
  - 파일명과 폴더 구조만으로도 높은 직관성 확보.
  - 미래의 대규모 비즈니스 로직 확장 시 스크립트로 즉시 전환 가능한 데이터 무결성 확보.
- **트레이드오프**:
  - 인덱스와 실제 파일 간의 수동 업데이트 필요성 잔존.
  - 에이전트의 자율적인 최신성 판단 능력에 의존.

---

**참조 (Reference)**: [ADR Repository 가이드](/docs/adr/README.ko.md)
