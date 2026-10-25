# PR #256 — 실제 모델 Eval 실행 인계 및 Finalize

> 2026-10-25 · [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)
>
> **현재 상태: 계획 수립 COMPLETE / 실제 모델 Eval NOT RUN.** 다음 실행자가 이 대화 없이 저장소만 읽어도 이어갈 수 있도록 작성했다. PR #258의 개발환경 설치기 구현과 혼합하지 않는다.

## 먼저 읽을 아티팩트

| 순서 | 아티팩트 | 용도 |
| --- | --- | --- |
| 1 | [Prepare](bootstrap-eval-plan-prepare-2026-10-25.md) | 목표/Active Scope/금지 작업, 초기 실행 조건 |
| 2 | [Research](bootstrap-eval-plan-research-2026-10-25.md) | 정본·runner·legacy 근거와 함정 |
| 3 | [실행 계획 v3](bootstrap-eval-plan-2026-10-25.md) | 실행 단계, 안전 게이트, 관찰·성공 판정·원본 보관 |
| 4 | [Review 1~3](bootstrap-eval-plan-review-2026-10-25.md) | 5회 총괄 Loop accounting, findings/처분, 수렴 |
| 5 | [재귀 child — grader](bootstrap-eval-plan-child-grader-2026-10-25.md) | 6개 Routing 결과 + Behavior 5×3=15개 기준 교차판정 |
| 6 | [재귀 child — runtime](bootstrap-eval-plan-child-runtime-2026-10-25.md) | 캐시·설치·전역 override·원격 전송 위험 판단 |

## 확정된 실행 판단

- 정본: `src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md`와 `evals/skills/mols-dev-env-bootstrap-design/cases.json`. 시작 확인 기준 PR head `b3c5024240030a39d342979ea04ff93935aee010`(이번 계획 문서 커밋으로 HEAD가 이동했으므로 **실행 직전의 실제 HEAD/SHA 및 변경 diff**를 다시 고정).
- Source 재실행기가 아닌 기존 진입점: `npm run eval:promptfoo:mols-dev-env-bootstrap-design`. 기존 YAML, `skills_promptfoo.py`, `promptfoo_run.py`를 그대로 사용.
- 기본 설정이 안전한지 **읽기 전용 preflight**: Node>=22.22.0, npx, uv/test deps, 로컬 Ollama endpoint/모델, grader provider, output schema/접근성, 프로젝트·user/shared cache write targets 확인. 특히 `OLLAMA_BASE_URL`, `PROMPTFOO_GRADER_PROVIDER`, `PROMPTFOO_CONFIG_DIR/LOG_DIR/CACHE_PATH`의 상속값은 안전한 기본값이라는 보장이 없음.
- 새 모델 pull·Promptfoo npx 다운로드·uv project env 동기화·shared cache 쓰기가 필요하면 영향과 범위를 설명하고 **별도 승인 후** 평가 실행. 승인이 없거나 로컬 endpoint를 확인할 수 없으면 `blocked / not_run` 기록. 새 전역/영구 환경변수·cache manager·installer를 만들지 않는다.
- 선택 모델은 **실제로 설치되어 있는 하나**로 시작하고, grader도 존재하는 local Ollama provider를 사용. 필요하면 기존 runner가 이미 지원하는 env key를 **명령 한 번에만** 적용한다. 모델명·grader명·버전·설정 변경을 기록하고 서로 다른 trial을 합산하지 않는다.

## 사전 승인 후 최소 실행

아래 명령은 설치·캐시·venv 등 영향이 모두 확인됐고 필요한 승인을 받은 **로컬 개발 환경에서만** 사용한다. 환경별 Shell 표현은 기존 프로젝트 계약에 맞춘다.

```bash
# 먼저 node/uv/npx/ollama 및 project state 확인, 승인 필요 여부 판정
npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=trigger
npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=behavior
```

선택 평가 **6개**: positive 3 / negative·near-miss 3. 행동 평가 **5개**: 각 3개 criteria → 총 15개 개별 수동 교차판정. 출력/채점 기록을 분리하며 `llm-rubric`의 0.8 합산 PASS가 금지된 실행 제안이나 승인 무시를 가리지 못하게 한다.

## 실행 결과가 도착하면

1. Repository/ref/HEAD, model/grader/provider, command, timestamp, 실행 셸의 민감값 없는 endpoint/캐시 영향, 실제 trial 수를 명시.
2. Routing 각 6 case는 expected vs observed (`primary_skill` 포함); provider error/parse error와 genuine selection error 분리.
3. Behavior 각 5 case는 원문 답변·3 assertions별 충족/미충족/불명, grader pass/reason/score, 사람 판단과 충돌을 기록. 금지된 설치·전역 변경 제안과 근거 없는 실제 실행 주장 확인.
4. 오류 발생 시 **target / fixture / harness / transport / grader** 소유자를 구분하고, 재실행이 실질적 불확실성을 줄일 때만 동일 모델·조건으로 해당 case를 재실행. 기준/모델/문구를 점수에 맞춰 변경하지 않음.
5. 요약 결과와 알려진 한계를 `inbox/github-256/`에 추가하고, PR #256의 모델 Eval `Not Verified` 문구를 **실제 확인된 범위만** 갱신. 실패 시에도 성능 결함과 실행 장애를 혼합하지 않음.
6. 사용자/system/Home/다른 프로젝트 상태를 지우거나 덮어쓰지 않음. 로그 raw 원문에 비밀·경로가 포함되면 GitHub에 그대로 업로드하지 않음.

## 이번 계획의 검증·잔여 위험

- **verified(정적):** 기존 fixture 11건, suite 분리, frontmatter/전문 주입 방식, native runner 사전조건·설정 기본값, 0.8 grader, `npx --yes`·`uv run` 영향의 출처, 여섯 개 이전 단계/하위 검토 문서의 존재.
- **inferred:** 위 구성으로 최소·재현성 중심 평가를 설계할 수 있고 새 framework가 필요하지 않음.
- **not_run/unknown:** 실제 Ollama 모델 보유/응답, Promptfoo 실행 성공, 11개 선택·행동 결과, grader calibration의 실제 관찰, 실제 설치·네트워크 부작용. **PR CI PASS는 이 값을 대신하지 않는다.**
- **scope:** PR #256의 Skill 평가 계획. 실제 설치기 검증은 [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258).

## Run 종료

`mols-loops` Prepare(READY WITH LIMITS) → Parent Research/Plan/Review 1 → Child grader Research/Plan/Review → Parent Review 2 → Child runtime Research/Plan/Review → Parent Review 3 → Finalize.

- **공유 `loops_used=5`, hard ceiling=30.** Review/child 각 실질 검토 1회만 계산. 새로운 child가 불필요해 수렴; 제안 작업을 실행한 것처럼 계산하지 않음.
- **Finalize: COMPLETE (계획 아티팩트).** 실제 Runtime Eval은 고유한 후속 실행 작업으로 **HANDOFF**. 재개자는 새 세션에서 현재 HEAD/지침/로컬 runtime 조건을 재확인해야 한다.
