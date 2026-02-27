---
title: Discussion Governance
description: Protocols for collaborative reasoning and synthesis
categories: ["governance", "discussion"]
draft: false
date: 2026-02-27
lastmod: 2026-02-27T11:23:00.000Z
tags: ["discussion", "PDD", "TAS", "WWH", "governance"]
author: "mols"
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# Discussion

- `discussion/`은 제안과 토의를 통해 결정을 도출하는 디렉토리입니다.

## Discussion Protocol

- [PDD](/docs/methods/PDD.md): 제안-토의/토론-결정 프로세스
- [TAS](/docs/methods/TAS.md): 토의/토론 진행
- [WWH](/docs/methods/WWH.md): 문서 내용 구성

## Discussion Sequence

토의는 0번부터 9번까지의 시퀀스를 따르며, 단계별로 논리의 밀도를 높입니다.

- **0**: 제안 (정의 최초 제안)
- **1-6**: 자유 토의 및 토론
  - 1-3: 정반합 토의 (의견 공유)
  - 4-6: 정반합 토론 (의견 피력)
- **7**: 제안측 최종
- **8**: 비판측 최종
- **9**: 결정

## DIRECTORY STRUCTURE

- `<Discussion-ID>/`: 토의 공간
- `<Discussion-ID>/<No(0-9)>--<TITLE>.md`: 토의 문서
