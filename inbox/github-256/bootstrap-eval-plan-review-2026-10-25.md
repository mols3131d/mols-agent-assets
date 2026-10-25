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

## Review 3 (parent)

두 번째 child 결과와 최신 실행 계획을 검토한 뒤 기록할 것. 현재 **pending**.

