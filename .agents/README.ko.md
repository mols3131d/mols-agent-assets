---
title: Agentic Control Plane
description: 에이전트 컨텍스트 엔지니어링(ACE)을 위한 핵심 인프라
categories: ["core", "infrastructure"]
draft: false
date: 2026-02-27
lastmod: 2026-02-27T12:08:00.000Z
tags: ["ACE", "안티그래비티", "컨트롤플레인"]
author: "mols"
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# OVERVIEW

- `.agents/`는 **ACE (Agent Context Engineering)** 수행을 위한 규칙(Rules)과 워크플로우(Workflows)를 관리하는 프로젝트의 핵심 '컨트롤 플레인'입니다.
- 이 디렉토리는 **안티그래비티(Antigravity)** 시스템의 아키텍처를 따르며, 에이전트의 자율적 추론과 실행의 근거가 됩니다.

# DIRECTORY STRUCTURE

- `rules/`: 에이전트의 사고 방식, 페르소나, 제약 사항을 정의하는 정적 로직.
- `workflows/`: 특정 태스크를 수행하기 위한 단계별 실행 절차 및 동적 로직.
- `brain/`: 태스크 로그, 맥락 메모리, 세션 상태 등을 추적하는 동적 데이터.

# 제약 사항

- **결과물 저장 금지 (NOT_FOR_RESULT)**: 이곳은 에이전트의 제어 로직과 맥락만을 위한 공간입니다. 프로젝트의 실제 결과물이나 배포 자산은 절대 이곳에 저장하지 마십시오. 결과물은 `/outputs/`에 저장해야 합니다.
- **우선순위 (PRIORITY)**: 루트 `README.md`와 `/docs/`의 지침이 `.agents/` 내의 로직보다 우선합니다.

---

_EOF: 에이전트 컨트롤 플레인 안내_
