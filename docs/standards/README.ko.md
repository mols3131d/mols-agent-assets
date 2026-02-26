---
title: 표준 가이드라인 (Standards)
description: 프로젝트의 기술적 명세 및 필수 준수 규칙
categories:
  - standards
draft: false
date: 2026-02-27
lastmod: 2026-02-26T23:11:43.210Z
tags:
  - standards
  - protocol
  - spec
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 표준

이 폴더는 프로젝트에서 반드시 지켜야 하는 **기술적 명세와 필수 규칙(Hard Rules)**을 정의합니다. 

## 핵심 원칙

- **강제성**: 표준은 선택 사항이 아니며, 프로젝트의 모든 자산은 이곳에 정의된 명세를 100% 준수해야 합니다.
- **무결성**: 파일 구조, 명명 규칙, 데이터 스키마 등을 표준화하여 프로젝트의 기술적 무결성을 유지합니다.
- **명확성**: 모호함을 제거하기 위해 수치화되거나 구조화된 명세를 지향합니다.

## 주요 표준 영역

- **`/docs/standards/language.md`**: 프로젝트에서 사용하는 주 언어와 보조 언어 정책
- **`/docs/standards/markdown.md`**: Frontmatter 스키마 및 링크 프로토콜 명세
- **`/docs/standards/agent.md`**: 에이전트의 행동 및 응답 패턴 표준
- **`/docs/standards/document.md`**: 모든 문서에 대한 에이전트/인간 이중 타겟 페어링 표준(DPS)

## 제약 사항

- **구성**: 모든 새로운 문서와 표준은 반드시 **[`/templates/`](/templates/README.ko.md)**의 설계도를 기반으로 작성되어야 합니다.

_우리는 표준을 준수함으로써 협업의 마찰을 줄이고, 기계와 인간 모두가 신뢰할 수 있는 데이터를 생산합니다._