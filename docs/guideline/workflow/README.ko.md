---
title: 워크플로우 관리 가이드라인 (Workflow Management)
description: 효율적 실행을 위한 워크플로우 설계, 최적화 및 평가 체계
categories:
  - guideline
draft: false
date: 2026-02-27
lastmod: 2026-02-26T21:36:42.177Z
tags:
  - workflow-management
  - lifecycle
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 🔄 워크플로우 관리 (Workflow Management)

이 폴더는 에이전트의 실질적인 '작동 방식'을 결정하는 워크플로우를 엔지니어링하고 관리하는 공간입니다. 단순한 단계 나열이 아닌, 실행 효율과 성공률을 극대화하기 위한 **절차적 자산 관리**를 수행합니다.

## 📌 핵심 패러다임: "Workflow as Code"

- **절차의 자산화**: 워크플로우는 소스 코드와 마찬가지로 버전 관리, 테스트, 그리고 리팩토링의 대상입니다.
- **최적화 중심**: 한번 작성된 워크플로우는 고정된 것이 아니며, 실행 데이터를 바탕으로 더 빠르고 정확하게 개선되어야 합니다.
- **표준화된 흐름**: SCAN(탐색)-PLAN(계획)-EXEC(실행)-VERIFY(검증)의 표준 흐름을 통해 작업의 예측 가능성을 확보합니다.

## 📜 가이드라인 구성 정보

- **[워크플로우 라이프사이클 관리 (workflow.md)](./workflow.md)**:
    - 고가치 워크플로우의 기준 (무엇이 효율적인 절차인가?)
    - 엔지니어링 및 디자인 (어떻게 설계하는가?)
    - 최적화 루프 (실행 데이터를 바탕으로 어떻게 개선하는가?)
    - 평가 지표 (절차의 효율성을 어떻게 측정하는가?)

_워크플로우는 우리 프로젝트의 '근육'입니다. 지속적인 관리를 통해 더 빠르고 강력한 실행력을 갖추어 나갑니다._
