---
description: PR 256 Eval 개선 계획의 근거인 현재 채점 구조, 실행 자원과 native Promptfoo 대안을 확인합니다.
---

# Eval 개선 조사

- 기준 revision은 [준비 기록](bootstrap-eval-improvement-prepare-2026-10-25.md)과 같다. 최신 PR head도 `b381dbd`이며 Draft다.
- 공통 evaluator는 행동 사례의 3개 기준을 하나의 `llm-rubric`에 묶으며 원래 요청을 rubric에 제공하지 않는다. 이전 자동 PASS 3건씩은 원문 검토에서 모두 필수 기준을 누락했다.
- Ollama adapter는 HTTP/envelope 오류와 모델 content의 JSON parse 오류를 하나로 처리하고 잘못된 content를 버린다. 현재 기록만으로 Nemotron 오류의 원인을 확정할 수 없다.
- Trigger는 결정적으로 비교한다. 기대 선택·행동 기준은 target에 제공하지 않는다. 이 경계는 유지한다.
- 기존 Python 3.13 환경, Promptfoo 0.122.0 캐시, rumdl 0.2.54, 로컬 Qwen Coder 7B·Nemotron 4B를 재확인했다. 새 설치는 필요하지 않다. Node는 24.14.0으로 공통 runner의 최소 버전을 만족한다.
- [Promptfoo Echo](https://www.promptfoo.dev/docs/providers/echo/)는 고정 응답을 그대로 반환하고 native model-graded assertion과 함께 사용할 수 있다. target 호출 없이 동일 응답의 grader 보정이 가능하다.
- [LLM rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/)을 기존 공통 generator에서 재사용한다. 별도 채점 모델 호출 API나 독자 grading framework는 만들지 않는다.
- [Ollama chat](https://docs.ollama.com/api/chat)은 content와 종료 사유를 구분한다. 기본 설정을 바꾸기 전에 원응답의 content와 종료 metadata를 제한적으로 관찰한다. Thinking 전문은 보고서에 싣지 않는다.

**선택:** 원래 사례를 참조하는 정상/오답 3쌍과 Echo를 사용한다. 먼저 기존 채점 기준의 baseline을 얻고, 요청 맥락·기준별 판정을 보완한 뒤 같은 고정 응답을 다시 채점한다. 합산 점수 대신 native assertion 결과와 기대 판정을 비교한다.
