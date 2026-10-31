# 재귀 Child — 한국어 Skill Eval의 채점 신뢰성 검토

> 2026-10-25 · 부모 [Review 1](bootstrap-eval-plan-review-2026-10-25.md)에서 push한 strict-subset 과제
>
> **Goal:** 현재 11-case Promptfoo에서 **채점기 오류·다국어 의미 오해·측정 범위 과장**을 분리해 판정하는 최소 절차를 확정. 다른 모든 parent Scope/설치·변경 금지 조건 상속. 실제 평가 실행·fixture 변경 금지.

## Child Research

**확인된 사실**

1. `scripts/agent_assets/skills_promptfoo.py` `generate_tests`는 trigger 6건의 기대 JSON과 `assert_trigger` 결과를 deterministic하게 대조한다. `case_id`별 observed JSON/expected 선택을 직접 검토할 수 있다.
2. Behavior 5건의 출력은 `assert_behavior_output`에서 **빈 문자열만 거부**하고, 실제 설계 품질은 `llm-rubric` 판정에 위임한다. 각 case의 `assertions`는 3개씩 → **15개 의미 기준**.
3. 설정에서 `rubric_threshold=0.8`이고 기준 문구는 “모든 기준을 materially 만족해야 PASS”라고 한다. 그러나 합산 점수·모델 판정 하나만으로 개별 안전 경계의 누락이 없었다고 증명할 수 없다.
4. 영문 rubric/프롬프트와 한국어 Skill·한국어/영문 혼합 시나리오의 의미 조합이 발생한다. [과거 평가 문서](../../docs/skills/mols-dev-env-bootstrap-design/evaluation.md)에 exact pin을 보존한다는 응답에 대해 grader가 반대로 판단한 오판 사례가 명시되어 있다.
5. Trigger suite는 `_routing_candidates`가 기본 빈 배열인 **격리 선택 실험**이다. 다른 실제 Skill이 후보로 없는 상태에서의 선택은 production route precision을 증명하지 못한다.
6. `_ollama_request`의 예외가 provider `error`가 되거나 응답 schema가 깨지면 대상 Skill/채점 criterion 실패가 아닌 **transport/parse/harness failure**로 분리해야 한다.

**상반 가능성**

- 어떤 케이스는 model response가 실제로 필수 경계를 빠뜨렸을 수도 있다. grader 오판이라고 가정하면 안 된다.
- 11건은 유용한 capability smoke이지만 통계적 일반화나 안전 무해성 인증용 표본이 아니다.
- 실질적으로 새로 필요한 것은 **고비용/새 채점기**가 아니라, raw output 5개에서 15개 기준을 확인하는 작고 명시적 교차 점검이다.

## Child Plan

1. 모델 본 실행 시 동일한 Skill/ref·fixture·grader provider를 고정하고 **target output + grader reason + label**을 대응시켜 저장/요약한다. 변경한 조건으로 이전 trial을 덮어쓰지 않는다.
2. **Trigger 6건:** case별 expected vs observed, `selected_skills`와 `primary_skill`이 맞는지 기록. 모델 호출 실패/형식 실패는 false positive·negative와 별도 종류로 적는다. 영어 positive와 한국어 negative를 표본 수준에서 구분해 본다.
3. **Behavior 5건:** 모델 응답을 실제로 읽고 각 사례의 **3개 assertion을 개별로 충족/미충족/판정 불가** 분류한다(총 15개). 특히 권한/전역 쓰기/lock·범위 초과 및 “실행했다고 주장”은 응답 근거를 직접 짚는다.
4. **Grader calibration:** 위 15개 수동 기준과 grader의 pass/score/reason을 대조해 false pass/false fail, 뜻이 불명확한 사례를 기록한다. 양측 불일치가 있으면 원문을 재판독하고, 합의되지 않으면 unresolved로 둔다.
5. **재실행 분기:** 동일 조건에서 provider/parse 오류는 먼저 환경 수정 후 재시도; grader가 명백히 틀린 사례는 grader 문제로 격리. Skill의 실제 실패가 재현될 때만 **그 문제 case**를 같은 모델·조건에서 소수 재실행한다. trial의 수·모델·gradering 조건을 모두 기록한다.
6. **Optional 다중 후보 선택:** 추후 native discovery에 대한 claim이 필요할 때만 기존 evaluator의 `routing_candidates` 기능으로 경쟁 Skill 후보 실험을 별도 suite/claim으로 계획한다. **이번 11건의 PASS를 native routing PASS로 표기하지 않는다.**

## Child Review / Reconcile

- **검증(정적):** 6+5의 case 수와 `_route`/`_execute_behavior`, deterministic routing/semantic behavior 계약, 과거 grader 오판의 근거를 원본에서 확인.
- **Challenge:** `0.8` 점수만 보고 PASS 결론 → **absorb**: behavior criterion 15개 별도 최소 수동 확인을 parent 계획의 성공/실패 판정에 추가.
- **Challenge:** 모든 target 모델에서 무조건 3회 반복 실행 → **reject**: 자원·시간·과적합 비용에 비해 정보 이득이 작다. 명백한 오류/의심 사례에 한정하고 반복 조건을 기록.
- **Challenge:** 영어 rubric이면 무조건 번역하거나 evaluator 수정 → **reject**: 실제 오판 근거 전에는 fixture/runner 수정 금지.
- **Challenge:** trigger 6/6 성공을 native routing으로 일반화 → **absorb**: parent의 claim을 격리 metadata selection으로 제한.
- **Residual unknown:** 실행 전까지 grader 정확도, 설치된 모델의 JSON schema 지원, response distribution은 모른다. 해결책은 추가 구현이 아니라 preflight와 실제 관찰.
- **Dispatch:** parent [계획](bootstrap-eval-plan-2026-10-25.md)과 [리뷰](bootstrap-eval-plan-review-2026-10-25.md)에 위 보완을 반영한다. Child `loops_used=2`(parent와 공유).
- **종결:** 하위 문제를 계획 수준에서 해결했다. 더 깊은 재귀는 새 독립 장애를 발견하지 못했으므로 필요하지 않다. **Child COMPLETE(계획 내용), runtime not_run**.
