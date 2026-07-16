---
name: scriptify
description: 사용 시점: 사용자가 LLM 토큰과 불확실성을 줄이기 위해 결정론적인 자연어 절차를 스크립트로 변환하고자 할 때. 제외 대상: LLM의 추론, 맥락 이해, 또는 모호성 해결이 필요한 작업.
---

# 에이전트 자산 스크립트화 (Scriptify Agent Asset)

## Goal

완전 또는 부분적으로 결정론적인 자연어 워크플로우를 스크립트로 변환하여 LLM 의존도, 토큰 비용 및 실행 불확실성을 최소화합니다.

## When to Use

자연어 지침을 스크립트로 대체하여 반복적이고 결정론적이거나 순수 기계적인 절차를 최적화할 때 이 워크플로우를 사용합니다.

## When NOT to Use

- 해당 작업이 유연한 텍스트 생성이나 추론을 요구할 때.
- 자연어로 충분하고 효율적인 작업을 억지로 코드로 변환할 때.

## Instructions

- `references/`에 위치한 세부 레퍼런스 문서를 참고하여 스크립트화 단계를 단계별로 검토, 계획, 실행하십시오.
- 검토 기준은 [references/scriptify-evaluate.human.ko.md](../references/scriptify-evaluate.human.ko.md)를 참고하십시오.
- 계획 수립은 [references/scriptify-plan.human.ko.md](../references/scriptify-plan.human.ko.md)를 참고하십시오.
- 실제 실행은 [references/scriptify-apply.human.ko.md](../references/scriptify-apply.human.ko.md)를 참고하십시오.

## Workflows

### Arguments from Context

- 대상 워크플로우 또는 자산 경로
- 스크립트화할 구체적인 단계나 절차
- 스크립트 작성 언어: 복수 가능, 기본값: Python
- 스크립트 저장 경로: 명시되지 않은 경우 에이전트가 문맥에 따라 판단

### Procedure

1. **검토 (Evaluate)**: [references/scriptify-evaluate.human.ko.md](../references/scriptify-evaluate.human.ko.md)에 따라 적합성을 분석합니다. 부적합 판정 시 즉시 종료합니다.
2. **계획 (Plan)**: [references/scriptify-plan.human.ko.md](../references/scriptify-plan.human.ko.md)에 따라 언어, 경로, 편집 내용을 수립하고 사용자 승인을 받습니다.
3. **실행 (Apply)**: [references/scriptify-apply.human.ko.md](../references/scriptify-apply.human.ko.md)에 따라 스크립트를 작성하고 마크다운을 수정한 뒤 검증합니다.

### Validation

- 스크립트가 대상 경로에 존재하며 오류 없이 실행됩니다.
- 워크플로우가 스크립트를 올바르게 참조합니다.
- 스크립트 내부에 강제된 LLM 추론 로직이 없습니다.
