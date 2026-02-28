---
title: "ADR 001: ACE 워크플로우 통합 라이프사이클 채택"
description: 에이전트 지능 자산 개발을 위한 RFC-ADR 기반의 경험 중심 워크플로우를 공식 채택함
author: mols--Rin
categories:
  - ADR
draft: false
id: adr-001
adr-status: accepted
adr-keyword: ACE-Workflow
date: 2026-02-28
lastmod: 2026-02-27T17:14:18.711Z
tags:
  - adr
  - workflow
  - ACE
  - ko
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# ADR 001: ACE 워크플로우 통합 라이프사이클 채택

## 상태 (Status)

**Accepted** (2026-02-28)

## 맥락 (Context)

에이전트 컨텍스트 엔지니어링(ACE) 프로젝트는 에이전트의 지능(규칙, 워크플로우 등)을 자산으로 관리합니다. 이러한 지능 자산은 기존 소프트웨어 코드와 달리 객관적이고 자동화된 테스트가 불가능하거나 오판의 위험이 큽니다. 따라서 의사결정의 근거를 명확히 남기고, 실전에서의 재사용성을 통해 품질을 검증할 수 있는 새로운 워크플로우가 필요했습니다.

## 결정 (Decision)

[`/docs/rfc/2026/001--ACE-WF`](/docs/rfc/2026/001--ACE-WF)에서의 토론을 바탕으로, 다음과 같은 **'통합 RFC-ADR 라이프사이클'**을 프로젝트 공식 워크플로우로 채택합니다.

1.  **RFC 기반 토론**: 모든 새로운 로직이나 아키텍처 변경은 RFC 단계에서 페르소나들(Leni, Kana, Rin)의 비판적 검토를 거칩니다.
2.  **ADR 기록**: 합의된 결론은 ADR로 기록하여 '왜(Why)'에 대한 맥락을 영구히 보존합니다.
3.  **역동적 요구사항**: ADR 기반으로 요구사항(REQ)을 작성하되, 제작(Forge) 단계 진입 후에도 구현 과정의 통찰을 반영하여 보완할 수 있도록 합니다.
4.  **경험적 검증**: 자동화 테스트 대신 "다른 세션/프로젝트에서 재사용 시 의도대로 작동하는가"를 기준으로 주관적 승인 절차를 거칩니다.

## 결과 (Consequences)

- **장점**:
  - 의사결정 추적성(Traceability) 확보.
  - 형식적인 테스트가 아닌 실질적 효용성 중심의 품질 관리.
  - 드래프트 기반의 선제적 제작을 통한 개발 속도 유지.
- **트레이드오프**:
  - 객관적 수치 기반의 검증 부재(사용자의 주관적 판단에 의존).
  - 프로세스 준수를 위한 초기 문서화 오버헤드.
