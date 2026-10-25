# PR #256 — 실제 모델 Eval 실행 계획 (초안 v1)

> 2026-10-25 · [Prepare](bootstrap-eval-plan-prepare-2026-10-25.md) → [Research](bootstrap-eval-plan-research-2026-10-25.md)
>
> **단계:** 초안. 리뷰 후 필요 시 이 파일에 최소 수정한다. 이번 요청은 계획·검토·인계이지 실제 모델 실행이 아니다.

## 목표와 판정

- **Claim A — Routing:** 한국어 Skill의 frontmatter만 제공해도 설계·리뷰 대상은 선택하고(3건), 일반 패키지 업그레이드·도구 단일 설치·CI 전용 작업에서는 선택하지 않는지(3건) 관찰한다.
- **Claim B — Behavior:** 선택된 Skill 전문으로 응답할 때 5개 사례에서 버전·lock, 설치 권한, 전역 격리, 위험 작업 제안, 기존 CLI 재사용, 부분 실패 및 출력 범위를 지키는지 본다.
- **Not claimed:** IDE/에이전트의 native 다중 Skill routing 성공, 실제 설치·변경을 막는 호스트 보안, 모든 모델·OS 일반화 또는 CI merge gate.

## 실행 전제와 순서

1. **Snapshot:** 실행 직전 `git rev-parse HEAD`, `git status --short`로 실제 Skill/cases/config 및 runner revision을 고정·기록한다. 이미 있는 변경을 정리·덮어쓰지 않는다.
2. **로컬 preflight:** `node --version`(>=22.22.0), `npx --version`, `uv --version`, `ollama list` 등 프로젝트 도구와 선택할 runtime/grader 모델이 이미 있는지 확인한다. 서비스 접근성·JSON/schema 출력 지원 여부는 실행 전 확인한다. 부재 시 `blocked`, 무단 다운로드/설치 금지.
3. **영향 범위 승인:** `uv run --locked ...`가 프로젝트 환경을 변경할 수 있고 `npx --yes promptfoo@0.122.0`가 cache에 없으면 네트워크 설치를 유발할 수 있음을 알린다. 저장 위치·네트워크·자원 사용을 점검해 필요하면 별도 사용자 승인, 승인 없으면 실행하지 않는다. 전역 환경·HOME·hooks 변경 금지.
4. **실행 모델 선택:** 이미 설치된 모델 한 개를 대표 runtime으로 선정하고 실제 존재하는 로컬 grader를 선택한다. 기존 공통 runner 기본값을 쓸 수 있으면 그대로 쓴다. 다르면 **해당 실행 프로세스에서만** `PROMPTFOO_RUNTIME_MODEL` / `PROMPTFOO_GRADER_PROVIDER`를 지정한다. 새 영구 설정 파일은 만들지 않는다.
5. **Smoke(선택적):** 기존 runner의 fixture/plumbing 및 대표 1건에서 model/transport/schema가 정상인지 확인한다. 이 성공을 행동 검증으로 보고하지 않는다.
6. **Routing 6건:** `npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=trigger`; positive/near-miss 구분, 실제 선택 JSON 및 근거 확보.
7. **Behavior 5건:** `npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=behavior`; raw 응답, 영어 rubric 기준별 판정, 금지된 설치·자체 구현 제안, 과도한 설정 증가를 함께 본다. 설치·파일 변경은 전혀 수행하지 않는다.
8. **결과 분류:** 각 `case_id`별 expected/observed, pass/fail, grader reason, raw excerpts 및 오류 타입(model/transport/parser/fixture/grader)을 구분. 예기치 않은 실패나 PASS는 대표 사례를 사람 기준으로 재판독한다.
9. **필요 시 비교:** 한국어 설명 때문에 영어 positive가 누락되거나 grader 오판이 의심되는 경우, 동일한 fixture/설정에서 좁은 조건 비교 또는 문제 사례 재실행만 한다. 변경한 설정과 trial 별 입력을 보존; 점수를 적당히 평균내지 않는다.
10. **종료:** 결과 요약/미검증·잔여 위험을 PR #256의 `inbox/github-256`에 기록. 실제 적용 개선은 별도 리뷰 이후 결정하고, PR #258 구현과 섞지 않는다.

## 예상 기록 계약

- 실행 환경: OS, repo/ref/HEAD, dirty 상태, model/runtime·grader 정확한 ID, Ollama/Node/uv/Promptfoo 버전, 실행 명령/옵션·날짜.
- 실행 결과: case별 원문 또는 안전하게 축약한 관찰 결과, routing TP/FN/FP/TN, behavior 기준 충족 여부와 채점기 판정 차이, provider 오류, 승인/부작용.
- 결론: `observed`와 `inferred`, `not_run`, `blocked` 분리. 기존 영문 10-case 결과는 역사적 참고이고 현재 11-case pass로 기재하지 않는다.
- 저장: 로그는 기본적으로 runner의 로컬 임시 영역에만 두고, PR에는 재현 가능한 판단 요약과 근거가 되는 최소 발췌만 남긴다. 모델 응답·경로·환경 출력에 민감 정보가 있으면 커밋 전에 제거한다.

## Review가 확인할 미해결 사항

- 로컬 설치/다운로드 없는 경로가 가능하다고 전제하는가? `npx --yes`와 `uv run`의 경계를 검토해야 한다.
- 영어 grader의 오판을 어떻게 교정·분리할지, 지나치게 비싼 전수 수동 리뷰 없이 충분한가?
- 격리된 Skill 하나만의 routing이 실제 다중 Skill selection과 어떻게 다른가?
