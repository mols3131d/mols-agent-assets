# PR #256 — 실제 모델 Eval 실행 계획 (검토 반영 v2)

> 2026-10-25 · [Prepare](bootstrap-eval-plan-prepare-2026-10-25.md) → [Research](bootstrap-eval-plan-research-2026-10-25.md)
>
> **단계:** [Review 1](bootstrap-eval-plan-review-2026-10-25.md)과 [재귀 채점 검토](bootstrap-eval-plan-child-grader-2026-10-25.md)를 반영한 실행 계획. 이번 요청은 계획·검토·인계이지 실제 모델 실행이 아니다.

## 목표와 판정

- **Claim A — 격리 Routing:** 한국어 Skill의 frontmatter만 제공하는 **단독 후보** 실험에서 설계·리뷰 요청은 선택하고(3건), 단일 패키지/도구 설치·CI 전용 요청은 선택하지 않는지(3건) 관찰한다. 다중 후보·native agent routing은 별도 주장으로 남긴다.
- **Claim B — Behavior:** 선택된 Skill 전문으로 응답할 때 5개 사례에서 버전·lock, 설치 권한, 전역 격리, 위험 작업 제안, 기존 CLI 재사용, 부분 실패 및 출력 범위를 지키는지 본다.
- **Not claimed:** IDE/에이전트의 native 다중 Skill routing 성공, 실제 설치·변경을 막는 호스트 보안, 모든 모델·OS 일반화 또는 CI merge gate.

## 실행 전제와 순서

1. **Snapshot:** 실행 직전 `git rev-parse HEAD`, `git status --short`로 실제 Skill/cases/config 및 runner revision을 고정·기록한다. 이미 있는 변경을 정리·덮어쓰지 않는다.
2. **로컬 preflight:** `node --version`(>=22.22.0), `npx --version`, `uv --version`, `ollama list` 등 프로젝트 도구와 선택할 runtime/grader 모델이 이미 있는지 확인한다. 서비스 접근성·JSON/schema 출력 지원 여부는 실행 전 확인한다. 부재 시 `blocked`, 무단 다운로드/설치 금지.
3. **영향 범위 승인:** `uv run --locked ...`의 프로젝트 Python 환경 동기화와 `npx --yes promptfoo@0.122.0`의 캐시 미존재 시 다운로드·쓰기·네트워크 접근을 **모델 평가 실행 권한과 구분**한다. 기존 환경/캐시가 충족하지 않으면 관련 위치·영향에 대한 별도 사용자 승인을 얻기 전 설치 단계 중단. `npx --yes`는 승인 자체가 아니다. HOME·전역·hook 변화는 기본 경로에서 금지.
4. **실행 모델 선택:** 이미 설치된 모델 한 개를 대표 runtime으로 선정하고 실제 존재하는 로컬 grader를 선택한다. 기존 공통 runner 기본값을 쓸 수 있으면 그대로 쓴다. 다르면 **해당 실행 프로세스에서만** `PROMPTFOO_RUNTIME_MODEL` / `PROMPTFOO_GRADER_PROVIDER`를 지정한다. 새 영구 설정 파일은 만들지 않는다.
5. **Smoke(선택적):** 기존 runner의 fixture/plumbing 및 대표 1건에서 model/transport/schema가 정상인지 확인한다. 이 성공을 행동 검증으로 보고하지 않는다.
6. **Routing 6건:** `npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=trigger`; positive/near-miss 구분, 실제 선택 JSON 및 근거 확보.
7. **Behavior 5건:** `npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=behavior`; raw 응답과 LLM grader reason/score를 보존해 검토한다. 사람이 각 3개 assertion×5 case=**15개 기준을 충족/미충족/불명**으로 별도 판정하고, 금지 설치·자체 구현·과도한 설정 확대를 확인한다. 모델 답변은 실제 설치/파일 변경을 수행하지 않는다.
8. **결과 분류:** 각 `case_id`별 expected/observed, PASS/FAIL/UNKNOWN, grader reason, raw 발췌 및 오류 타입(model/transport/schema/fixture/grader)을 분리한다. **Provider/JSON 실패는 negative selection도 Skill 안전 실패도 아니다.** LLM 점수 `0.8` 통과가 필수 안전 기준 누락을 덮지 못하도록 수동 판정과 충돌을 별도 기록한다.
9. **필요 시 비교:** 영어 positive를 놓치거나 grader 오판·모델 결과 불안정이 의심되는 **문제 case만** 동일 조건에서 제한적으로 재실행한다. 여러 모델이 이미 설치되어 있고 실제 비교 가치가 있을 때만 다른 모델을 추가한다. grader가 target과 같거나 다르면 모델 ID를 모두 기록; 독립적 판정인 양 주장하지 않는다. trial을 평균 PASS 하나로 축약하지 않는다.
10. **종료:** 결과 요약/미검증·잔여 위험을 PR #256의 `inbox/github-256`에 기록. 실제 적용 개선은 별도 리뷰 이후 결정하고, PR #258 구현과 섞지 않는다.

## 예상 기록 계약

- 실행 환경: OS, repo/ref/HEAD, dirty 상태, model/runtime·grader 정확한 ID, Ollama/Node/uv/Promptfoo 버전, 실행 명령/옵션·날짜.
- 실행 결과: 각 case의 expected/observed, routing TP/FN/FP/TN/**error**, behavior 15개 criterion별 사람 판단과 grader score/reason·불일치, provider 오류·승인/부작용. 안전상 필수 criterion 불충족은 전체 점수와 별개로 표시.
- 결론: `observed`/`inferred`/`not_run`/`blocked` 분리. **6/6·5/5라도 이 격리 harness에 한한 관찰**이며 실제 native routing, 설치 안전성, 통계적 일반화를 주장하지 않는다. 이전 영문 10-case는 역사적 참고일 뿐 최신 11-case pass 아님.
- 저장: 로그는 기본적으로 runner의 로컬 임시 영역에만 두고, PR에는 재현 가능한 판단 요약과 근거가 되는 최소 발췌만 남긴다. 모델 응답·경로·환경 출력에 민감 정보가 있으면 커밋 전에 제거한다.

## 계획 자체의 완료 조건 및 후속 판단

- **계획 준비 완료:** 사전 설치·권한 경계, 기존 runner 명령, 11-case 실행 구분, grader 보정, 결과 기록·중단/재실행·인계 조건이 문서에 있고 Review에서 반례를 처리한 상태.
- **실제 평가 성공 판정(별도 실행 후):** 출력 오류 없이 해당 모델의 Routing 6개 기대 결과, Behavior 5개에서 필수 criteria가 모두 충족됐다는 raw 응답+사람 교차 판단의 근거가 있을 때만 **이 모델/이 fixture에 한해** 만족했다고 쓴다. 하나라도 어긋나면 해당 차원을 미충족으로 표기하고 원인을 분리한다. 의도된 불합격도 capability 측정 데이터로 보존한다.
- **PR 입장:** 실제 Eval 결과는 병합 판단에 참고하되 무근거 수치 문턱이나 새 blocking CI를 추가하지 않는다. 중대한 위험 응답이 발견되면 수정안을 검토하고 다시 평가한다.

## Review가 확인할 미해결 사항

- 로컬 설치/다운로드 없는 경로가 가능하다고 전제하는가? `npx --yes`와 `uv run`의 경계를 검토해야 한다.
- 영어 grader의 오판을 어떻게 교정·분리할지, 지나치게 비싼 전수 수동 리뷰 없이 충분한가?
- 격리된 Skill 하나만의 routing이 실제 다중 Skill selection과 어떻게 다른가?
