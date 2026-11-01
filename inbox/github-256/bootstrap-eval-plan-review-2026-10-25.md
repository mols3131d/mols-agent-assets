# PR #256 — Eval 계획 검토 및 루프 결정 기록

> 2026-10-25 · [초안 계획](bootstrap-eval-plan-2026-10-25.md) · `mols-loops` Review → Reconcile → Dispatch
>
> 이 문서는 단계별 Review 누적 기록이다. **상단 Review 1 완료 후 재귀 하위 문제를 위임**하며, 후속 결과는 같은 파일을 갱신한다.

## Review 1 (parent, `loops_used=1`)

### Verify

- **Pass(정적):** 목표가 Routing 6/Behavior 5, 신규 framework 없이 기존 runner 활용, 실제 설치하지 않고 실행 계획만 수립하는 범위와 일치한다.
- **Pass(원본):** `scripts/agent_assets/skills_promptfoo.py`의 `_route`는 frontmatter만, `_execute_behavior`는 선택된 Skill 전문만 주입한다. `assert_trigger`는 기대 선택과 JSON을 비교한다. `llm-rubric`은 behavior에서 영어 assertion을 판정한다.
- **Not Run:** 사용자 로컬 Ollama·Promptfoo 실행, provider output 또는 rubric calibration.

### Challenge → Reconcile

| 후보 | 판단 | 근거와 최소 대응 |
| --- | --- | --- |
| `npx --yes` 및 `uv run`이 로컬 환경을 변경할 수 있음 | **absorb / High** | 기존 runner는 npx로 Promptfoo를 호출한다. 사용자에게 평가 자체를 승인받은 것과 다운로드/설치 허가를 구분; preflight에서 설치 필요 여부 확인·허가 미획득 시 중단 |
| 단독 Skill catalog의 trigger 결과를 native multi-Skill 선택 성공이라 주장할 위험 | **absorb / Medium** | `_routing_candidates` 기본값은 빈 배열. 결과 claim을 단일 후보 메타데이터 선택으로 제한 |
| 영어 rubric + 한국어 Skill·mixed prompts, grader가 위협·거절을 잘못 판정할 가능성 | **absorb / Medium** | 과거 documentation에 grader 오판이 이미 적혀 있음. 하위 문제로 **판정 신뢰성 검증법**만 분리 조사 |
| 모든 model/runtime과 OS에 대한 전체 행렬 | **reject** | 사용자 목표를 넘는 비용/범위. 우선 기존 설치 모델 1종 + 필요 시 좁은 재실행/비교가 충분 |
| 새 case/새 runner/영구 환경변수/CI blocking gate 추가 | **reject** | 기존 fixture와 runner가 현재 설계 검증 범위의 출발점이며 추가 이득 미확인 |

### Dispatch

- **재귀 child push:** `grader-calibration` — 오직 *채점의 신뢰성과 다국어/선택 결과 해석*만 다루는 부분 범위로 Research → Plan → Review 수행한다. 원본 Skill·runner나 fixture 파일은 수정하지 않는다. Parent scope, authority, 설치 금지, artifacts 경계를 그대로 상속한다.
- **다음 단계:** child 결론으로 parent 계획을 보강한 뒤 실행 안전성/재현성 게이트를 재검토하여 최종 계획을 검증한다.
- **공유 카운터:** parent 첫 substantive Review 종료 시 `loops_used=1`. child는 같은 Run의 카운터를 이어받으며 새 Run/ceiling을 만들지 않는다.

## Review 2 (parent, `loops_used=3`)

### Verify

- Child `grader-calibration` 결과를 parent 실행 계획 v2에 반영했다. 각 criterion의 사람 판정, `0.8` grader score의 한계, 오류·판정 차이 분류와 최소 재실행 조건을 명시했다.
- 평가 실행과 모델 다운로드는 아직 하지 않았다. 현재까지는 repository source에 대한 정적 근거만 있다.

### Challenge → Reconcile

- **absorb / High:** `promptfoo_run.py::build_env`는 `PROMPTFOO_CONFIG_DIR`, `PROMPTFOO_LOG_DIR`, `PROMPTFOO_CACHE_PATH`, `PROMPTFOO_PYTHON`을 `setdefault`로 지정한다. **이미 존재하는 사용자/전역 override는 보존**하므로 cache/log/python 경로가 반드시 `.tmp/promptfoo`로 격리된다고 단정할 수 없다. 이는 실행 영향·안전 승인의 근거를 바꾼다.
- **absorb / Medium:** `npm/npx`, `uv`, Ollama endpoint도 공유 자원·네트워크·저장 공간을 사용할 수 있다. 최초 preflight와 11-case 평가의 `safe to start` 경계를 기존 도구의 경로/설치 상태에 근거해 확정해야 한다.
- **reject:** 버전 관리자, 캐시 추적기, OS별 installer wrapper를 새로 만들면 위험 제어보다 유지비가 더 커진다. 기존 도구의 조회 기능과 프로젝트 정책으로 한정한다.

### Dispatch

- **재귀 child push 2:** `runtime-side-effects` — **기존 runner의 쓰기/네트워크/전역 설정 영향과 재현성**만을 조사·계획·리뷰한다. parent의 eval 계획/PR 범위와 권한 경계를 상속하며 실행은 하지 않는다.
- **공유 카운터:** 지금까지 parent Review 1, child grader Review 1, parent Review 2 = `loops_used=3`. child는 이 카운터를 이어받는다.

## Review 3 (parent, `loops_used=5`)

### Verify

- **Pass(직접 확인):** 현재 한국어 Skill과 11개 fixture 원본(activation 3, activation-negative 3, behavior 5), 기존 Promptfoo YAML/runner, `inbox/github-256`의 Prepare·Research·계획 v3·Review 및 두 Child 문서 존재.
- **Pass(정적 조건):** 계획에 source/fixture 고정, Node/uv/Ollama preflight, npx/uv 쓰기·승인, 상속 설정과 grader/endpoint 확인, 원래 6+5 사례 실행, behavior 15개 기준 교차판정, grader 오류·모델 오류·fixture 오류 분리, 재실행 제한, raw/결과 증거 저장과 민감값 비공개, 정확한 claim 범위, 멈춤 조건 포함.
- **Not Run:** Ollama 모델 실제 동작, Promptfoo CLI 통합 실행, grader calibration의 관측치. 이들이 미실행인 것은 **이번 요청이 계획만 수립**하기 때문이며 계획 자체의 실패로 볼 수 없다.

### Challenge → Reconcile

- **설치 안 하고 바로 실행 가능한가?** `uv run --locked --group test`와 `npx --yes`는 공유 캐시/프로젝트 환경에 쓸 수 있고, 캐시 및 의존성 상태는 원격 GitHub만으로 확인 불가. **absorb 완료:** 영향 대상 확인과 별도 승인/실행 보류 경계가 계획 v3에 있음.
- **grader `0.8` 통과를 안전성 통과로 오해하는가?** **absorb 완료:** 5×3 개별 기준 판정과 raw 응답·grader reason 대조, 명백한 안전 조건 누락의 별도 보고.
- **시험이 native routing 자체를 입증하는가?** **absorb 완료:** `routing_candidates` 기본 단독 후보임을 문서화, cross-runtime/native claim 배제.
- **실행 결과를 저장할 수 있는가?** Promptfoo 설정의 `write:false`를 감안해 승인된 로컬 임시 출력/콘솔 증거에서 요약하고, 민감한 raw output은 PR에 저장하지 않는다.
- **더 많은 파일·체크·모델을 추가해야 하는가?** **reject:** 증명 대상과 연결된 새 결함 근거가 없으므로 스크립트·fixture·모델 다운로드·CI 게이트 추가 없음.

### Dispatch / Finalize candidate

- 별도 후속 Research/재귀로 해결할 **계획 수준의 material finding 없음**. 실제 로컬 모델 상태는 실행자가 preflight에서 확인해야 할 **선행 조건**이며 실행 전까지 unknown으로 보존한다.
- **수렴:** parent 3회 Review + grader Child 1회 + runtime Child 1회 = `loops_used=5`, parent/child가 동일 Run 카운터 공유. 나머지 Loop 25회를 소비하기 위한 반복은 하지 않는다.
- **Finalize로 인계:** 현재 검증된 실행 계획과 미실행 경계를 요약한 handoff 문서 작성 후, 링크·파일·revision·PR 상태의 최소 검증만 수행한다.


