---
title: 언어 표준
description: MOLS Agent 워크스페이스의 필수 언어 사용 정책
categories:
  - standards
draft: false
date: 2026-02-27
lastmod: 2026-02-26T23:12:10.274Z
tags:
  - standards
  - language
agent-readable: true
agent-editable: false
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 언어 표준

이 문서는 프로젝트 내에서 인간과 에이전트가 사용하는 언어의 역할과 범위를 정의합니다.

## 표준 상세 내용

### 1. 인간 인터페이스

- **주 언어**: 한국어 (KR)
- **범위**: 에이전트와의 대화, 추론 과정 설명, 인간 친화적 문서 (`.ko.md`).
- **목적**: 사용자와의 의사소통 정확도 및 신뢰성 극대화.

### 2. 에이전트 인터페이스

- **주 언어**: 영어 (EN)
- **범위**: 모든 소스 코드, 커밋 메시지, 기술적 자산, 에이전트 전용 문서 (`.md`), 로그.
- **목적**: LLM 간의 논리적 이식성 확보 및 토큰 효율성 개선.

## 제약 사항

- **기술적 자산의 영어화**: 대화 언어와 관계없이 모든 기술적 결과물과 논리 명세는 영어를 유지해야 합니다.
- **동기화**: 한국어 설명과 영어 명세 사이의 논리적 연속성을 유지해야 합니다.