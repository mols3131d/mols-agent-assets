---
description: PR 256의 간결한 Promptfoo Eval 보완 순서, 검증 조건과 변경 허용 범위를 확인합니다.
---

# Eval 개선 계획

상태: **v3 실행·검토·로컬 검증 완료**. 준비·근거는 [Prepare](bootstrap-eval-improvement-prepare-2026-10-25.md), [Research](bootstrap-eval-improvement-research-2026-10-25.md), 검토는 [Review](bootstrap-eval-improvement-review-2026-10-25.md)를 따른다. 최종 source와 실행 결과는 [결과](bootstrap-eval-improvement-results-2026-10-25.md), 반영 commit·CI는 [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)에서 확인한다.

| 단계 | 작업 | 확인할 결과 |
| --- | --- | --- |
| 1 | 기존 사례를 참조하는 공개 가능한 정상/오답 3쌍을 `evals/skills/mols-dev-env-bootstrap-design/grader-cases.json`에 고정한다. 공통 generator와 native Echo config를 연결한다. | 기존 grader baseline. 정상도 모두 거부하는 채점기를 개선으로 오인하지 않음 |
| 2 | 공통 rubric에 원래 요청을 제공하고 한 criterion씩 native `llm-rubric`으로 판정한다. 누락된 필수 행동과 금지 행동의 부재를 구분한다. | 같은 6개 응답의 18개 기준 판정·사유. 예상과 불일치는 숨기지 않음 |
| 3 | Ollama 원응답을 제한적으로 진단하고 content parse 오류와 transport/envelope 오류를 구분한다. | 잘못된 content와 종료 metadata 보존, 자동 재시도·강제 PASS 없음 |
| 4 | 실제 누락을 대상으로 Skill의 설계 계약을 간결하게 보강한다. 의미 검토 후 다른 도구의 잠금·정책 사례 1건만 추가한다. | 기존 책임·설치 권한·범용성을 보존. 특정 도구 명령이나 새 wrapper 요구 없음 |
| 5 | 먼저 targeted test, 보정 사례, 두 로컬 모델의 trigger/behavior를 실행한다. | baseline과 current를 구분하고 자동 판정의 대표 PASS/FAIL을 원문 대조 |
| 6 | 리뷰·필요한 수정 후 문서·generated·전체 test와 PR CI를 검증한다. | 결과와 남은 한계·정확한 실행 명령을 inbox에 인계, Draft 유지 |

## 변경·검증 원칙

- 기존 `skills_promptfoo.py`를 확장한다. 원래 fixture의 기대 답안은 유지하고 source와 grader fixture의 관계를 명시한다. 보정 표본·기대 판정은 target이나 grader 입력에 누출하지 않는다.
- Echo 보정의 native CLI FAIL은 의도된 오답 거부일 수 있다. **실제 grader 판정과 기대 판정의 일치**를 확인하며 provider 오류를 보정 성공으로 계산하지 않는다. Grader 변경 전후는 서로 다른 측정으로 기록한다.
- 기준별 assertion은 각각 필수이며 하나라도 미충족이면 사례를 PASS로 보고하지 않는다. Native 점수 집계와 별개로 개별 결과를 보고한다.
- 테스트는 요청 맥락 보존, criterion 분리, source fixture 참조·검증, 오류 content 보존 등 실제 동작을 검증한다. 단순 문구·현재 설정 snapshot은 늘리지 않는다.
- 추가 모델·의존성·전역 설정은 도입하지 않는다. 기존 Python·캐시 CLI를 사용하며 모델과 fixture 조건을 기록한다.
- 불일치 또는 JSON 오류 사례만 제한 재시도한다. 두 모델의 전 사례 성공을 보장하지 않으며, 수정으로 개선되지 않는 한계도 근거로 남긴다.

진행 중 결과를 바꾸는 발견이 있으면 이 계획의 변경 기록과 Review를 먼저 갱신한다. 기준별 호출 비용은 현재 5행동×3기준, 확장 후 6행동×3기준으로 제한한다.

## 변경 기록

- v1: 계획 검토의 F1–F4를 반영했다. 구현·모델 실행은 아직 시작하지 않았다.
- v2: 요청 맥락·기준별 Qwen 채점은 오답 3건을 모두 거부하지만 정상 2건도 오거부한다. 같은 고정 6응답을 기존 Nemotron grader로 한 번 비교해 채점 모델의 영향을 분리한다. 새 모델은 설치하지 않으며, 다른 측정 조건의 결과를 합산하지 않는다.
- v3: Native Ollama grader는 기존에 temperature를 지정하지 않았다. 기존 target의 temperature=0과 별개다. 보정 조건을 고정하기 위해 Ollama grader에만 native temperature=0을 명시한다. Nemotron의 구조화 응답에서 thinking만 있고 content가 빈 것을 확인했으므로, 공식 `think=false`를 해당 실행에 명시해 이전 Skill로 1회 진단한다. 이 실제 공백에 한해 command-scoped `PROMPTFOO_RUNTIME_THINK`를 추가하고 기본값은 유지한다. 이후 결과는 설정 변경을 명시한다.
- v3 실행 판단: 고정 temperature에서 Nemotron 13/18, Qwen 10/18 기준 일치. 두 grader 모두 자동 승인 근거로는 불충분하다. 최종 runtime 실행은 표본에서 더 일치한 Nemotron을 진단용 grader로 사용하고 원문을 별도 대조한다. 모델·prompt 변경을 더 시도하며 표본 점수를 맞추지 않고 남은 오판을 명시한다. 같은 요청·응답·criterion이 실제 grader 입력에 들어갔음을 export에서 대조했다.
