---
title: "Studio 루트"
description: "에이전트 중심 콘텐츠 생성을 위한 주요 환경"
categories: ["studio"]
draft: false
date: 2026-02-27
lastmod: 2026-03-01
tags: ["studio", "workspace"]
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
---

# 🎨 Studio

> 에이전트의 창의적 작업 공간.

이 디렉토리는 에이전트 기반의 콘텐츠 생성, 개선 및 평가를 위한 주요 환경입니다. 에이전트의 'OS'(규칙 및 프로토콜)가 담긴 `.agents` 디렉토리와 달리, `studio`는 실제 '작업'이 이루어지는 곳입니다.

## 📂 구조

- `**drafts/**`: 창작 단계. 새로운 파일이 이곳에서 초안으로 작성되고 반복적인 사이클을 통해 개선됩니다.
- `**evaluation/**`: 비평 단계. 파일들이 미리 정의된 지표와 에이전트 규칙에 따라 객관적으로 평가됩니다.
- `**outputs/**`: 전달 단계. 평가를 통과한 **최종 자산들이 카테고리별로 분류**됩니다 (예: `rules`, `workflows`).

## 🛠 워크플로우

1. **초안 작성(Drafting)**: `drafts/`에 초기 저충실도 콘텐츠를 생성합니다.
2. **반복 개선(Iterating)**: `/test` 또는 개선 프로토콜을 사용하여 콘텐츠를 다듬습니다.
3. **평가(Evaluating)**: 평가 스크립트를 실행하여 고밀도 로직을 보장하고 `rules` 준수 여부를 확인합니다.
4. **내보내기(Exporting)**: 확인된 고품질 자산을 `outputs/`의 적절한 카테고리로 이동합니다 (예: `outputs/rules/`).
