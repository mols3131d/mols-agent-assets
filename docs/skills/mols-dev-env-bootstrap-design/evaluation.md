---
description: mols-dev-env-bootstrap-design의 positive·near-miss routing과 설계 인계 behavior를 로컬 모델로 평가하고 실제 bootstrap 검증과 구분할 때 사용하는 계약입니다.
---

# Bootstrap Design Evaluation

이 Skill의 [case fixture](../../../evals/skills/mols-dev-env-bootstrap-design/cases.json)가 behavioral contract를 소유하며, [Promptfoo config](../../../evals/promptfoo/mols-dev-env-bootstrap-design.yaml)는 기존 [공통 evaluator](../../../scripts/agent_assets/skills_promptfoo.py)에 연결한다. 별도 Skill 전용 provider나 grader는 만들지 않는다.

## What this measures

| Suite | Input | Criteria |
| --- | --- | --- |
| Trigger | 사용자 요청 + canonical Skill frontmatter만 | 설계·리뷰 요청 3개의 selection, 일반 package update·단일 도구 설치·CI-only 요청 3개의 rejection |
| Behavior | 사용자 scenario + full canonical Skill | portable owner, bounded update, host/HOME 권한, 부분 실패, dirty state와 플랫폼 evidence를 설계 인계에 반영 |

Trigger는 expected selection과 deterministic하게 비교하며 Skill body를 제공하지 않는다. Behavior는 activation을 이미 마친 상태로 보고 output contract와 case별 semantic rubric을 평가한다. 각 criterion을 원래 사용자 요청과 함께 별도 native `llm-rubric`으로 판정한다. 모든 필수 assertion이 만족돼야 사례를 PASS로 해석하며 metric 평균으로 누락을 상쇄하지 않는다. Rubric은 관찰할 수 있는 응답을 평가하며 실제 도구 실행이나 HOME 변경 여부를 증명하지 않는다.

이 suite는 **capability 평가**다. 작은 단일 trial의 성공률을 regression gate나 다른 model/runtime의 보장으로 사용하지 않는다. Negative 요청에서 해당 Skill을 선택하지 않는 것은 의도한 성공이지 평가 누락이 아니다.

현재 fixture는 **12건**(trigger 6, behavior 6)이다. 기존 11건에 다른 생태계의 정책·잠금·도구 owner를 따르는 Rust/Cargo 설계 인계 사례 1건을 추가했다. 실제 도구 설치 및 승인 준수는 이 프롬프트 평가만으로 입증되지 않는다.

## Portability coverage

평가는 [범용 재사용 범위](README.md#portability)에 맞춰, 서로 다른 저장소·기술 스택·도구 조합에서도 대상 프로젝트의 기존 정책과 native owner를 따르며 설계 계약을 유지하는지 확인해야 한다. 이 저장소에 적용한 결과만으로 범용성의 성공 여부를 판정하지 않는다.

현재 사례에는 Python/uv, Node/Volta/pnpm, Rust/Cargo 설계 시나리오가 포함된다. 이는 대표 입력 사례이며 다른 저장소의 실제 실행이나 모든 스택·도구 조합의 호환성을 검증한 결과는 아니다. 지원·성능 주장은 실제 평가한 조합과 claim에 맞는 근거로 한정한다. 추가 사례는 필요한 재사용 범위나 관찰된 실패에 근거해 선택한다.

Promptfoo/Ollama, 실행용 Node/Python과 이 저장소의 npm 진입점은 현재 평가 harness의 구성이다. 배포된 Skill을 적용하는 다른 프로젝트의 필수 도구나 설치 절차로 전제하지 않는다.

## Run locally

이미 사용 가능한 Ollama 모델을 선택한 뒤 repository root에서 실행한다. 기본 runtime/grader 이름에 해당하는 모델이 설치되어 있다고 가정하지 않는다.

```bash
npm run eval:promptfoo:mols-dev-env-bootstrap-design
```

`PROMPTFOO_RUNTIME_MODEL`과 `PROMPTFOO_GRADER_PROVIDER`를 명시하고, 필요하면 `-- --filter-metadata suite=trigger` 또는 `suite=behavior`로 분리한다. 네트워크 모델 다운로드는 이 평가의 자동 선행 작업이 아니다. 현재 공통 runner가 선택한 Promptfoo version·local/no-sharing 설정을 재사용한다.

Ollama grader에는 native `temperature=0`을 지정한다. Structured JSON에서 thinking만 반환하고 content가 비는 모델은 해당 실행에 한해 `PROMPTFOO_RUNTIME_THINK=false`를 지정할 수 있다. 기본 thinking 동작은 변경하지 않으며, 이 설정을 바꾼 결과는 이전 조건과 구분한다. Transport/envelope 오류와 content JSON 오류는 별도로 기록하고 잘못된 content와 종료 metadata를 보존한다.

## Grader calibration

[고정 응답 6개](../../../evals/skills/mols-dev-env-bootstrap-design/grader-cases.json)는 기존 사례의 요청·기준을 참조하는 정상/오답 3쌍이다. [Echo config](../../../evals/promptfoo/mols-dev-env-bootstrap-design-grader.yaml)는 같은 공통 assertion generator를 재사용하며 target inference 없이 grader만 실행한다. 기대 판정은 보고용 metadata에만 두며 grader에 제공하지 않는다.

```bash
npm run eval:promptfoo:mols-dev-env-bootstrap-design:grader
```

이 보정 실행의 CLI FAIL은 의도한 오답 거부일 수 있다. `expected_criteria`와 semantic `componentResults`의 기준별 판정을 비교하고 오류는 별도로 분류한다. 정상도 오답도 확인해야 하며, 보정 표본과 기대 판정은 재검토 가능한 agent 작성 자료다. 독립적인 사람 검수나 미사용 사례의 성능 보장이 아니다.

Grader 변경 전후는 서로 다른 측정이다. 자동 판정과 원문 검토를 함께 기록하며 알려진 위양성·위음성이 남으면 자동 점수만으로 통과나 merge readiness를 선언하지 않는다.

## Current 12-case evidence

2026-10-25, 요청 맥락·기준별 grading과 native Ollama grader temperature=0으로 최신 fixture를 두 모델에서 실행했다. [개선 계획·실행 결과](../../../inbox/github-256/bootstrap-eval-improvement-results-2026-10-25.md)에 보정 표본 비교, 정확한 조건과 source hash, 개별 원문 판정을 남겼다.

| Target | Trigger | Behavior 자동 | Behavior 원문 18기준 |
| --- | --- | --- | --- |
| `nemotron-3-nano:4b`, think=false | 5 PASS / 1 selection envelope ERROR | 1 PASS / 5 FAIL | 충족 7 / 미충족 11 |
| `qwen2.5-coder:7b`, think 기본값 | 3 PASS / 3 FAIL | 2 PASS / 4 FAIL | 충족 7 / 미충족 11 |

Grader는 두 실행 모두 `ollama:chat:nemotron-3-nano:4b`다. 고정 보정 표본의 기대 판정 일치는 Nemotron 13/18, Qwen 10/18 기준으로 **자동 승인에 충분하지 않다**. 최신 자동 behavior PASS도 모두 필수 누락이 있어 원문 검토와 분리했다. 전 기준을 충족한 behavior 사례는 두 모델 모두 없다.

이전 exact-pin empty JSON은 이전 Skill에 `think=false`를 명시한 통제 요청에서 해소됐다. 최신 실행의 다른 trigger에서 생긴 selection 불일치는 같은 조건 재시도에도 재현돼 schema 오류로 보존했다. 이전 11-case와 설정·case 수·grader가 달라 전체 점수를 직접 비교해 Skill 개선 효과를 주장하지 않는다.

## Language and Skill validity evidence

한국어 지시와 영어 루브릭의 언어 불일치 영향을 분리하기 위해, 대표 실패 사례 3건에 대해 **한국어/영어 × Skill 미적용/적용** 36건을 3개 로컬 모델(`qwen2.5-coder:7b`, `nemotron-3-nano:4b`, `qwen3.5:4b`)에서 교차 실행하고 2인의 블라인드 평가를 수행했다 ([상세 결과](../../../inbox/github-256/bootstrap-eval-language-comparison-results-2026-10-31.md)).

- **언어 격차 미미:** Skill 적용 시 영어(29.6%)와 한국어(25.9%)의 기준 충족률 차이는 3.7%p(27개 중 1개 기준 차이)에 불과해, 낮은 통과율의 주원인이 언어 불일치가 아님을 확인했다.
- **Skill 개선 효과:** 한국어 환경에서 Skill 적용 시 기준 충족률이 11.1~18.5%에서 25.9%로 향상(+7.4~14.8%p)되어 Skill 지침의 안전·범위 경계 강화 효과를 확인했다.
- **소형 모델 한계:** 다중 제약·부정 조건을 동시에 충족해야 하는 복합 루브릭 특성상 4B~7B 모델에서는 전 기준 충족 사례가 없었으며, 이는 모델의 instruction-following 역량 경계로 보존한다.

## Previous 11-case evidence

2026-10-25, HEAD `81eb4579eac6b25b45878b31d86697863b3c25bd`의 한국어 Skill과 최신 fixture를 두 로컬 모델로 각각 1회 실행했다. Grader는 `ollama:chat:qwen2.5-coder:7b`로 고정했다. [실행 조건·사례별 근거](../../../inbox/github-256/bootstrap-eval-results-2026-10-25.md)에 원문 판정과 오류·채점 차이를 기록했다.

| Target | Trigger | Behavior 자동 | Behavior 원문 기준 15개 |
| --- | --- | --- | --- |
| `nemotron-3-nano:4b` | 6/6 | 3 PASS / 1 FAIL / 1 ERROR | 충족 3 / 미충족 9 / 불명 3 |
| `qwen2.5-coder:7b` | 3/6: negative 3건 모두 오선택 | 3 PASS / 2 FAIL | 충족 4 / 미충족 11 |

자동 behavior PASS는 두 모델 모두 3건씩 위양성이었다. 필수 기준을 모두 충족한 behavior case는 없었다. OS 지원 증거 과장, 전역 Ruff 대체 수용, 설치 승인·부분 실패·복구 누락이 관찰됐다. Nemotron exact-pin case의 JSON parse error는 동일 조건 1회 재시도에서도 재현됐으며 모델의 의미 실패와 분리했다.

이 결과는 작은 모델의 isolated prompt capability와 현재 grader의 한계를 보여 준다. 자동 점수로 안전성이나 merge readiness를 판단하지 않으며 native multi-Skill routing, 실제 설치·승인 이행 또는 OS 지원을 보장하지 않는다.

## Historical 10-case evidence

2026-10-25에 로컬 Ollama와 Promptfoo 0.122.0으로 실제 runtime을 실행했다. 첫 `qwen2.5-coder:7b` trigger trial은 positive 3/3, near-miss 0/3이었다. Broad topic keyword가 별도 activation처럼 읽히지 않도록 canonical description의 lifecycle-design 조건을 좁혔다.

수정 후 같은 모델의 10-case capability run은 trigger positive 3/3, near-miss 0/3, behavior 2/4였다. Missing-host/HOME 및 dirty-state/platform scenario에서 구체적인 처분을 빠뜨렸으며, description refinement만으로 routing 문제가 해결됐다고 주장하지 않는다.

같은 case·Skill·Promptfoo harness에서 runtime만 `nemotron-3-nano:4b`로 바꾸고 grader `ollama:chat:qwen2.5-coder:7b`를 유지한 trial은 trigger 6/6, behavior 3/4, 전체 9/10이었다. Exact-pin case의 응답은 setup/update 분리와 pin 유지를 명시했는데 grader reason은 이를 누락했다고 잘못 설명했다. 다만 응답에 lock diff 검토·검증·복구 인계가 없어 세 번째 criterion은 충족하지 못하므로 이 case를 pass로 덮어쓰지 않는다. Model마다 routing/행동 성능이 다르며 전체 capability gap이 해소됐다는 결론은 내리지 않는다.

- Model runtime output과 model-grader 판정은 별개의 evidence다. 비어 있거나 parse되지 않은 output은 transport/schema 문제인지 먼저 구분한다.
- Common evaluator fixture projection test와 Rulesync structural validation은 이 runtime 결과를 대신하지 않는다.
- 실제 Windows/macOS/Linux/WSL bootstrap, HOME installer containment, native Skill discovery/harness selection은 이 isolated prompt capability suite의 측정 대상이 아니다.
- 재현 가능한 실패는 capability gap으로 남긴다. Expected answer를 바꾸거나 near-miss를 제거해서 통과율을 올리지 않는다.
