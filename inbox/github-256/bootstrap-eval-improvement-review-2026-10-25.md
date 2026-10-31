---
description: PR 256 Eval 개선 계획과 실행 결과의 실질 검토, 조치와 다음 단계를 인계합니다.
---

# Eval 개선 검토

## 계획 검토 — Work 전

계획을 효과성·측정 신뢰성·범위/비용 관점에서 순차 검토했다. 독립적인 사람 검수가 아니다.

| Finding | 판단·계획 반영 |
| --- | --- |
| F1: 오답만 보정하면 모든 응답을 FAIL하는 grader도 좋아 보인다. | **absorb**: 정상/오답 3쌍을 고정하고 양쪽 일치율·개별 판정을 보고한다. |
| F2: 잘못된 응답을 거부한 CLI FAIL을 보정 실패로 오인할 수 있다. | **absorb**: native assertion 결과와 별도 기대 판정 metadata를 비교한다. Inverse assertion으로 provider 오류를 성공시키지 않는다. |
| F3: 공통 adapter 수정이 다른 Skill에 영향을 준다. | **absorb**: 기존 source 참조를 재사용하고 공통 generator·다른 Skill fixture 연결의 회귀 테스트를 수행한다. |
| F4: 전 모델·전 플랫폼 확대는 사용자의 간결한 Eval 범위를 넘는다. | **absorb**: 기존 두 로컬 모델, 보정 6응답, 범용성 신규 1사례로 한정한다. 실제 OS·IDE 검증은 제외한다. |
| F5: 매 실패마다 Skill을 길게 늘리면 소형 모델과 특정 fixture에 과적합할 수 있다. | **absorb**: 재현된 누락만 수정하며 기대 답안을 유지한다. 현재 Skill의 범용 원칙을 제거하거나 새 설치 체계를 만들지 않는다. |

**판정:** 계획은 실행 가능하다. 먼저 보정 표본과 기존 grader baseline을 확보한다. 미확정 JSON 원인은 이후 진단 단계에서 확인한다. `loops_used=1/6`, 다음 단계 Work.

## 보정 baseline 검토

- 공통 generator와 native Echo 연결의 targeted test 33개가 통과했다. 현재 Skill·행동 fixture와 기존 grader 판단은 그대로 둔 상태에서 실행했다.
- `pr256-grader-baseline.json`: 6응답 모두 자동 PASS. 정상 3건은 맞지만 오답 3건도 통과해 기대 사례 판정과 **3/6 일치**했다. 실행 27s, provider error 0.
- F1 재검증: 정상 표본이 모두 통과하므로 이후 모든 응답을 거부하는 변화와 구분할 수 있다. Labels는 metadata에만 있고 Echo/채점 rubric에 전달되지 않는다.
- **판정:** 위양성이 재현됐다. 계획대로 원래 요청과 단일 criterion을 제공하는 채점으로 바꾸고 같은 표본을 다시 실행한다. JSON 오류는 content와 종료 metadata를 보존해 진단한다. `loops_used=2/6`, 다음 단계 Work.

## Qwen 기준별 채점 검토

- 회귀 테스트 37개 통과. 같은 6응답의 기준별 판정은 11/18 일치했다. 오답 3건은 모두 사례 FAIL이지만 정상 3건 중 2건도 FAIL이므로 이를 신뢰성 해결로 표시하지 않는다.
- 정상 portable 응답의 명시적 setup/update·Node 24 보존, 정상 Python 응답의 host 재사용·global Ruff 거부가 없다고 오판했다. Context 제공만으로 Qwen의 모든 오판이 해결된다는 가설은 기각한다.
- **absorb:** 다른 기존 로컬 grader와 같은 표본을 비교해야 채점 모델과 rubric의 영향을 더 구분할 수 있다. 계획 v2에 Nemotron 1회 비교를 추가했다. 샘플·기대값은 유지한다.
- `loops_used=3/6`, 다음 단계 Work: Nemotron 원응답 진단 후 고정 표본 grader 비교.

## Grader 비교·JSON 진단 검토

- Nemotron grader는 같은 18기준에서 14/18 일치했다. 오답 3건은 모두 거부했지만 정상 portable 응답도 오거부했다. 단순 모델 교체를 완전한 해결로 보지 않는다.
- JSON 진단: Nemotron exact-pin의 `message.content`는 빈 문자열, thinking은 존재, `done_reason=stop`, `eval_count=90`이었다. Timeout이나 응답 잘림이라고 단정하지 않는다.
- **absorb:** target은 temperature=0이지만 native grader는 별도 temperature 설정이 없었다. 계획 v3에 Ollama grader 조건 고정과 동일 표본 확인을 추가했다. 다른 provider의 configuration은 유지한다.
- **absorb:** [Ollama chat](https://docs.ollama.com/api/chat)과 [Promptfoo Ollama](https://www.promptfoo.dev/docs/providers/ollama/)의 공식 계약에 따라 structured output과 thinking의 조합을 제한적으로 진단한다. 성공 시 해당 실행에서만 override하고 설정 차이를 보고한다. Thinking 전문을 JSON 답변으로 억지 변환하지 않는다.
- Skill은 관찰된 범위 오거부·버전 owner 혼동·부분 성공/OS 지원 과장·인계 누락만 보강했다. 도구별 명령·설치 정책은 넣지 않았다. Rust/Cargo 1사례는 기존 tool owner를 따르는 범용성 점검용으로 고정했다.
- `loops_used=4/6`, 다음 단계 Work: 조건 고정 보정, 제한적 target 재평가와 원문 검토.

## 구현·재평가 검토

- 공식 전체 test 279개와 targeted 43개가 통과했다. Context·criterion 분리, source 참조와 label 비노출, 오류 content 보존, 명시적 thinking override 및 다른 provider 설정 보존을 확인했다.
- 최신 12건의 자동·원문 결과와 오류를 [결과](bootstrap-eval-improvement-results-2026-10-25.md)에 대조했다. 두 모델 모두 원문 18기준 중 7개 충족·11개 미충족이며 전 기준 PASS 사례는 없다. Nemotron의 trigger envelope 오류는 동일 조건 1회 재시도에서도 재현됐다.
- **absorb:** grader 보정만으로 모델 오판을 해결했다고 주장할 수 없다. 고정 조건 보정은 13/18·10/18이며 자동 PASS에도 누락이 있다. 문서·인계에서 진단용 결과와 원문 판정을 구분했다.
- **reject:** 오답을 통과시키기 위한 기대값 완화, runtime 오류 강제 보정, 새 모델 설치나 OS/IDE 검증 확대. 현재 범위의 근거를 개선하지 않거나 사용자 범위를 넘는다.
- **확인:** Source와 CLI·조건이 달라진 결과를 순수 Skill 개선 효과로 비교하지 않는다. 보정 표본은 agent 작성·검토이며 실제 grader 입력 대조로 adapter 오염은 배제했지만 독립적인 사람의 정답 인증은 아니다.
- **판정:** 계획의 코드 보완·진단·제한된 Skill 개선·재평가·근거 기록을 수행했다. 작은 모델의 행동 및 의미 채점 한계는 명시적 잔여 결과다. 현재 표본에서 prompt를 더 조정하며 점수를 맞추지 않는다.
- `loops_used=5/6`, 다음 단계 **Finalize**: 포맷·metadata·generated·Rulesync validation·hook·PR CI의 bounded 검증과 반영. 새 연구·설계 확대는 하지 않는다.

## Finalize 검증

포맷·frontmatter·index/route drift·Rulesync 구조·diff 검증을 통과했고 평가 당시 source hash가 유지됐다. Fetch 후 PR head와 로컬 HEAD가 동일함을 확인했다. Hook·push·CI의 최종 반영은 [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)에서 추적한다. 이번 계획의 완료 범위는 native 평가 보완·오류 진단·제한된 재평가와 근거 기록이며, 모델 행동·채점 신뢰성 확보까지 완료한 것은 아니다. 이 검증은 새 Main Loop로 계산하지 않는다.
