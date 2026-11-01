---
description: PR #265의 다중 코딩 에이전트 소프트웨어 아키텍처 패턴에 대한 최종 셀프 리뷰 발견 사항과 후속 조사·개편 방향을 검토할 때 참고합니다.
---

# PR #265 — Multi-Agent Architecture Follow-up Research

상태: 최종 셀프 리뷰 기록 완료 / 추가 근거 조사 중. 대상: [Software Architecture for Multi-Agent Development](../../catalog/patterns/software-engineering/multi-agent-development-architecture.md) (검토 기준 `8dfd8f94bc2370f1fe85844a05db58eb10f43cd0`).

## Review findings (2026-11-02)

**판정: 보완 후 머지 권장.** 문서명은 다중 에이전트 개발용 소프트웨어 아키텍처를 약속하지만, 현재 다섯 패턴 중 네 항목의 초점은 주로 단일 에이전트의 탐색·검증·맥락 복원·리팩터링 후보 선택이다. 다중 에이전트 협업은 세 번째 패턴에 집중되어 있다.

| Priority | 위치 | Finding | 보완 목표 |
| --- | --- | --- | --- |
| High | 원문 53–67행 | 독립/생산자–소비자/공유 불변식을 분류하나, **한 기능을 여러 에이전트가 함께 개발하도록 하는 소프트웨어 책임·모듈·통합 경계**를 구체적으로 선택하게 만들지 못한다 | 다중 에이전트 변경 단위와 공유 의미의 소유 구조를 설계 후보로 제시 |
| High | 원문 98–143행 | 데이터 파이프라인 예시는 주로 agent 하나의 입력원 추가를 설명한다. 여러 agent가 **동시에 하나의 기능을 구현하는 before/after 반례**가 없다 | 동일 요구에 대한 구조 대안과 병렬 의존성, 통합 검증의 차이를 보여주는 시나리오 |
| Medium | 원문 27–51행, 69–79행 | search/tooling, test/runtime feedback, handoff 같은 비아키텍처 문제와 구조적 문제의 경계가 느슨하다 | 아키텍처가 직접 소유하는 책임 경계·검증 seam만 핵심에 두고 외부 메커니즘을 명시적으로 구분 |
| Medium | Grounding 및 전체 | agent/multi-agent 생산성 향상은 구조적 휴리스틱이지 인과적으로 검증되지 않았다 | 증거 수준 구분과 대표 시나리오 기반 비교·향후 모델 평가 설계 |

**보존할 점:** GPPC의 GPP 구조, 작고 선택적인 패턴, '현 구조 유지' 선택, 불변식과 안전성 우선, microservice·interface·linter·문서 추가 강제 없음.

**검토 범위:** 아키텍처 패턴의 설계 유도력과 설명 정합성. 이 기록은 독립 에이전트의 실제 병렬 실행·비교 실험, 실제 저장소 리팩터링, CI 결과가 아니다.

## Research questions

1. 파일 충돌 감소와 **의미적 충돌·변경 의존성 감소**는 어떤 구조 선택에서 달라지는가?
2. 다중 agent의 작업 독립성이 실제로 생기는 코드·데이터·계약·검증의 '완결 단위'는 무엇인가?
3. API/schema 변경, DB transaction, end-to-end workflow 등 협업이 필요한 경우 어떤 설계 대안이 있으며 무엇을 병렬화하지 말아야 하는가?
4. 구조 변경이 아닌 orchestration, workspace isolation, search, tool/harness improvements를 어떻게 구분하는가?
5. 설계 전후를 실제로 비교할 때 단순 agent 수나 파일 수가 아닌 어떤 결과를 측정할 것인가?

## Additional research

조사 결과, 반례, 설계 가설과 근거·한계를 이 절에 추가합니다.
