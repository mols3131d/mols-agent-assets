---
title: WF (Workflow)
description: 에이전트 작업 흐름 및 절차 정의
categories:
  - glossary
draft: false
date: 2026-02-28
lastmod: 2026-02-27T15:25:34.281Z
tags:
  - glossary
  - wf
  - ko
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# WF (Workflow)

**워크플로우(WF)**는 특정 목표를 달성하기 위해 에이전트가 수행해야 할 일련의 논리적 단계와 작업 순서를 정의한 것입니다.

## 개념 정의

- **본질**: 복잡한 태스크를 실행 가능한 작은 단위 작업(Task)으로 분해하고, 각 작업 간의 상관관계(순서, 조건, 분기)를 설계한 동적 명세.
- **역할**: 에이전트에게 '무엇을(What)' 해야 하는지가 아닌, '어떻게(How) 단계별로 나아갈지'를 안내하는 나침반 역할을 함.

## 구성 요소

1. **Trigger**: 워크플로우가 시작되는 조건.
2. **Steps**: 실제 수행되는 개별 작업 단위.
3. **Decision Points**: 조건에 따른 작업의 흐름 제어 및 분기.
4. **Output**: 워크플로우 종료 시 생성되는 결과물.

## 표준화 규칙

- 모든 워크플로우는 `{.agents}/workflows/` 디렉토리에 정의됨.
- 에이전트가 즉시 실행 가능하도록 명확한 명령어(Command)와 조건부가 포함되어야 함.
