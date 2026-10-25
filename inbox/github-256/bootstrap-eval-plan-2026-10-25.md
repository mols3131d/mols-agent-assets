# PR #256 — 실제 모델 Eval 실행 계획 (재귀 리뷰 반영 최종 v3)

> 2026-10-25 · [Prepare](bootstrap-eval-plan-prepare-2026-10-25.md) → [Research](bootstrap-eval-plan-research-2026-10-25.md)
>
> **단계:** [Review 1·2](bootstrap-eval-plan-review-2026-10-25.md), [채점 검토 child](bootstrap-eval-plan-child-grader-2026-10-25.md), [실행 경계 child](bootstrap-eval-plan-child-runtime-2026-10-25.md)를 반영한 실행 계획. 이번 요청은 계획·검토·인계이지 실제 모델 실행이 아니다.

## 목표와 판정

- **Claim A — 격리 Routing:** 한국어 Skill의 frontmatter만 제공하는 **단독 후보** 실험에서 설계·리뷰 요청은 선택하고(3건), 단일 패키지/도구 설치·CI 전용 요청은 선택하지 않는지(3건) 관찰한다. 다중 후보·native agent routing은 별도 주장으로 남긴다.
- **Claim B — Behavior:** 선택된 Skill 전문으로 응답할 때 5개 사례에서 버전·lock, 설치 권한, 전역 격리, 위험 작업 제안, 기존 CLI 재사용, 부분 실패 및 출력 범위를 지키는지 본다.
- **Not claimed:** IDE/에이전트의 native 다중 Skill routing 성공, 실제 설치·변경을 막는 호스트 보안, 모든 모델·OS 일반화 또는 CI merge gate.

## 실행 전제와 순서

1. **Snapshot:** 실행 직전 `git rev-parse HEAD`, `git status --short`로 실제 Skill/cases/config 및 runner revision을 고정·기록한다. 이미 있는 변경을 정리·덮어쓰지 않는다.
2. **로컬 preflight(읽기 전용):** `node --version`(>=22.22.0), `npx --version`, `uv --version`, `ollama list`, 실제 Ollama 서비스 접근성을 점검한다. 실행 모델·grader 모델이 모두 이미 있는지, JSON schema 응답이 가능한지 확인한다. **상속된** `PROMPTFOO_CONFIG_DIR/LOG_DIR/CACHE_PATH/PYTHON`, `PROMPTFOO_RUNTIME_MODEL`, `PROMPTFOO_GRADER_PROVIDER`, `OLLAMA_BASE_URL`과 npm/npx·uv 캐시/프로젝트 .venv의 실제 영향을 확인하되 비밀값을 출력/커밋하지 않는다. 부재/불명확 시 `blocked`, 무단 다운로드·설치 금지.
3. **영향 범위·전송 대상 승인:** `uv run --locked ...`의 프로젝트 환경 동기화, `npx --yes promptfoo@0.122.0`의 캐시/패키지 다운로드 가능성을 평가 실행 허가와 구분한다. 모델 pull·shared 캐시 쓰기 등 신규 설치가 필요하면 위치·네트워크·디스크 영향을 설명하고 **별도 승인 전 실행 중단**한다. `--yes`는 사용자 승인 대체가 아니다. `OLLAMA_BASE_URL`은 실제 로컬 endpoint인지, `PROMPTFOO_GRADER_PROVIDER`도 로컬 Ollama인지 확인한다. 외부 전송/공유 쓰기를 안전하게 설명할 수 없으면 실행하지 않는다; HOME·전역·hook 영구 변경 금지.
4. **실행 모델 선택:** 이미 설치된 모델 한 개를 대표 runtime으로 선정하고 실제 존재하는 로컬 grader를 선택한다. runner 기본값·사용자 기존 설정이 **재현성·격리·로컬 전송 요구**와 맞으면 그대로 사용한다. 충돌할 때만 승인된 평가 **프로세스 한정** `PROMPTFOO_RUNTIME_MODEL`, `PROMPTFOO_GRADER_PROVIDER`, 필요 시 로컬 `OLLAMA_BASE_URL` 등을 최소 지정한다. 기존 전역값을 영구 변경하거나 무차별 삭제하지 않는다.
5. **Smoke(선택적):** 기존 runner의 현재 제공 기능·deterministic test로 fixture/plumbing을 확인한 뒤, 필요할 때만 대표 1건으로 model/transport/schema를 확인한다. 새 smoke mode/runner는 만들지 않는다. fixture-mode PASS는 실제 모델 behavior 근거가 아니다.
6. **Routing 6건:** `npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=trigger`; positive/near-miss 구분, 실제 선택 JSON 및 근거 확보.
7. **Behavior 5건:** `npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=behavior`; raw 응답과 LLM grader reason/score를 보존해 검토한다. 사람이 각 3개 assertion×5 case=**15개 기준을 충족/미충족/불명**으로 별도 판정하고, 금지 설치·자체 구현·과도한 설정 확대를 확인한다. 모델 답변은 실제 설치/파일 변경을 수행하지 않는다.
8. **결과 분류:** 각 `case_id`별 expected/observed, PASS/FAIL/UNKNOWN, grader reason, raw 발췌 및 오류 타입(model/transport/schema/fixture/grader)을 분리한다. **Provider/JSON 실패는 negative selection도 Skill 안전 실패도 아니다.** LLM 점수 `0.8` 통과가 필수 안전 기준 누락을 덮지 못하도록 수동 판정과 충돌을 별도 기록한다.
9. **필요 시 비교:** 영어 positive를 놓치거나 grader 오판·모델 결과 불안정이 의심되는 **문제 case만** 동일 조건에서 제한적으로 재실행한다. 여러 모델이 이미 설치되어 있고 실제 비교 가치가 있을 때만 다른 모델을 추가한다. grader가 target과 같거나 다르면 모델 ID를 모두 기록; 독립적 판정인 양 주장하지 않는다. trial을 평균 PASS 하나로 축약하지 않는다.
10. **종료:** 결과 요약/미검증·잔여 위험을 PR #256의 `inbox/github-256`에 기록. 실제 적용 개선은 별도 리뷰 이후 결정하고, PR #258 구현과 섞지 않는다.

## 예상 기록 계약

- 실행 환경: OS, repo/ref/HEAD, dirty 상태, model/runtime·grader 정확한 ID, Ollama/Node/uv/Promptfoo 버전, 실행 명령/옵션·날짜 및 로컬/원격 endpoint 분류. 실제 캐시/환경 쓰기 위치는 **민감 경로 제외한 영향 요약**만 남긴다.
- 실행 결과: 각 case의 expected/observed, routing TP/FN/FP/TN/**error**, behavior 15개 criterion별 사람 판단과 grader score/reason·불일치, provider 오류·승인/부작용. 안전상 필수 criterion 불충족은 전체 점수와 별개로 표시.
- 결론: `observed`/`inferred`/`not_run`/`blocked` 분리. **6/6·5/5라도 이 격리 harness에 한한 관찰**이며 실제 native routing, 설치 안전성, 통계적 일반화를 주장하지 않는다. 이전 영문 10-case는 역사적 참고일 뿐 최신 11-case pass 아님.
- 저장: runner/Promptfoo의 기존 정책이 기록을 자동 보존한다고 가정하지 않는다(`write=false`). 필요 시 실행자가 **승인받은 로컬 임시 위치**에 콘솔/결과를 저장하고 PR에는 익명화된 사례별 판단 요약·최소 발췌만 남긴다. 모델 응답·환경·로그의 토큰·민감 경로를 커밋 전에 제거한다.

## 계획 자체의 완료 조건 및 후속 판단

- **계획 준비 완료:** 사전 설치·권한 경계, 기존 runner 명령, 11-case 실행 구분, grader 보정, 결과 기록·중단/재실행·인계 조건이 문서에 있고 Review에서 반례를 처리한 상태.
- **실제 평가 성공 판정(별도 실행 후):** 출력 오류 없이 해당 모델의 Routing 6개 기대 결과, Behavior 5개에서 필수 criteria가 모두 충족됐다는 raw 응답+사람 교차 판단의 근거가 있을 때만 **이 모델/이 fixture에 한해** 만족했다고 쓴다. 하나라도 어긋나면 해당 차원을 미충족으로 표기하고 원인을 분리한다. 의도된 불합격도 capability 측정 데이터로 보존한다.
- **PR 입장:** 실제 Eval 결과는 병합 판단에 참고하되 무근거 수치 문턱이나 새 blocking CI를 추가하지 않는다. 중대한 위험 응답이 발견되면 수정안을 검토하고 다시 평가한다.

## Final Review 점검용 질문

- `uv run`/npx, 기존 override, grader endpoint의 설치·쓰기·외부 전송 영향을 **읽기 전용 사전 점검**으로 판별할 수 있는가? 알 수 없으면 `blocked`로 남기는가?
- 영어 grader의 오류를 5 case × 3 criterion 교차판정으로 구분하면서 불필요한 새 runner·case·환경변수는 피했는가?
- 단독 후보 metadata 선택, 실제 native 다중 Skill routing, 실제 bootstrap host 동작을 각각 독립된 claim으로 구분했는가?
