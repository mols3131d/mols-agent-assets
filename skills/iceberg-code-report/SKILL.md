---
name: iceberg-code-report
description: >
  USE WHEN: 사용자가 레포지토리, 핵심 컴포넌트, 실행 흐름, 코드 구조를 이해하기
  위한 일회성 code report, codebase tour, technical orientation, 또는 코드 읽기
  가이드를 원하거나 iceberg-code-report 사용법 또는 설정 관리를 원할 때.
  EXCLUDES: 결함·위험 중심 검토, 코드 수정, 리팩토링 제안, 영구 운영 문서 작성.
---

# Iceberg Code Report

## Goal

Code report 생성과 관련 config 관리를 최소 workflow만 로드해 수행한다.

## Global Boundaries

- Report 작업에서 코드 변경 금지.
- 파일·함수 나열보다 책임과 호출 관계를 우선한다.
- 코드로 확인한 사실과 추론을 구분한다.
- 핵심 실행 경로부터 조사하며 기존 문서를 그대로 요약하지 않는다.
- 평가와 개선 권고는 사용자가 요청한 경우만 별도 구분한다.

## Routing

1. `workflows/INDEX.csv`를 한 번 읽는다.
2. 요청의 outcome, operation, object, constraints를 식별한다.
3. `excludes`에 해당하는 route를 제거한다.
4. `use_when`을 충족하는 최소 route set을 선택한다.
5. 남은 route가 서로 다른 작업을 뜻하면 질문 하나로 확인한다.
6. ID를 index directory 기준으로 해석하고 선택한 workflow만 읽는다.
7. 선택한 workflow가 요구하는 resource만 읽고 validation을 수행한다.

Keyword가 아니라 의미로 routing한다. `workflows/`를 scan해 route를 찾지 않는다.

## Delegation

- 기본은 단일 agent가 조사와 작성을 수행한다.
- 범위가 넓고 독립 실행 경로가 2개 이상일 때만 경로별 코드 탐색을 sub-agent에 위임한다.
- sub-agent는 파일을 수정하지 않고 `symbol`, `file:line`, 사실, 추론을 구분해 반환한다.
- main agent가 공통 진입점, 교차 경계, 최종 문서와 link를 검증한다.
