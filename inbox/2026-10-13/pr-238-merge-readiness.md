---
description: PR #238의 Codex·Ollama Agent Asset Eval 구현 현황과 미검증 근거, 병합 전 최소 검증 및 후속 개선 과제를 판단할 때 사용하는 작업 보고서입니다.
---

# PR #238 Agent Asset Eval 병합 준비 보고서

> 기준일: 2026-10-13 · 검토 대상 구현 HEAD: `d7de1deab7a12fc31f37c34e08ee63eaad999813` · base: `5ef878fe05efe72e7d0cb10ebf7fb474ed3b3a98`  
> 이 문서는 해당 구현 스냅샷의 **작업 인계 자료**다. 문서가 PR 브랜치에 추가되면 HEAD가 바뀌므로 최신 상태는 [PR #238](https://github.com/mols3131d/mols-agent-assets/pull/238)과 GitHub Checks에서 다시 확인한다.

## 결론

**구현·정적 검증은 병합 후보 수준이지만, 실제 Eval 실행 경로는 아직 검증되지 않았다.** 현재 GitHub에서 PR은 Open/Ready 상태이고 충돌이 없으며, 위 HEAD의 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/38263279883)가 성공했다. 기존 인라인 리뷰 지적 3건도 해결됐다.

다만 이번 PR의 목표는 조사 문서가 아니라 **Ollama와 Codex에서 사용할 수 있는 평가 실행 경로의 보강**이다. CI가 확인한 것은 Python adapter·fixture·runner와 생성 결과의 결정적 계약이다. Promptfoo를 통한 실제 모델 실행과 Codex SDK provider 로딩은 아직 확인되지 않았다. 따라서 **현재 권고는 병합 전 최소 통합 실행을 확보하는 것**이다. 이것은 GitHub의 `mergeable: true` 상태와 별개의 품질 판단이다.

## 지금까지 구현된 범위

| 대상 | 구현 상태 | 확인 가능한 claim과 한계 |
| --- | --- | --- |
| 공통 평가 자산 | 기존 `cases.json`을 양쪽 backend에서 재사용 | 평가 기대값은 target에 전달되는 원문 요청에 삽입하지 않는다. |
| Ollama · `mols-loops` | Routing(Trigger)과 응답 수준 Behavior | 모델에 Skill 메타데이터/내용을 제공해 선택 JSON과 응답을 평가한다. 실제 Skill 자동 탐색 증거는 아니다. |
| Ollama · Agent Asset sibling | `mols-agent-asset` ↔ `mols-agent-asset-find` 경쟁 Routing 6건 | `selected_skills`와 `primary_skill`을 평가한다. Codex sibling 프로필과 같은 사례 및 후보 집합을 사용한다. |
| Codex Native · `mols-loops` | Skill 사용 Routing 8건, 응답 수준 Behavior 4건 | `skill-used` / `not-skill-used`는 Skill 파일 읽기 기반 **휴리스틱**이다. 주도 Skill이나 실제 도구 부작용은 증명하지 않는다. |
| Codex Native · Agent Asset sibling | 경쟁 Routing 6건 | 실제 agent runtime의 Skill 파일 읽기 여부를 관찰한다. Ollama의 선택 JSON과 같은 척도가 아니다. |
| 실행·추적 | Promptfoo `0.124.1`, Codex SDK `0.156.1` 고정, 격리된 임시 Skill workspace와 인증 Home, 선택적 output/manifest | 버전 인자·해시·인증 방식의 기록은 구현돼 있지만, 실제 설치·호출 성공을 대신하지 않는다. |

최근 리뷰·개선 루프에서는 Ollama가 일부 case에서만 경쟁 Skill을 보던 불일치를 수정했다. 이제 두 Ollama Routing 프로필은 각 사례마다 동일한 후보 집합을 제공하며 후보 메타데이터를 canonical `SKILL.md`에서 읽는다. 누락·중복 후보를 포함한 deterministic 회귀 테스트도 추가됐다.

관련 구현: [평가 실행 가이드](../../evals/README.md), [Promptfoo 설정](../../evals/promptfoo/), [평가 adapter](../../scripts/agent_assets/skills_promptfoo.py), [Native runner](../../scripts/agent_assets/native_eval_run.py). 초기 조사 맥락은 [기존 research](../2026-09-16/agent-asset-eval/research.md)를 참조한다.

## 확보한 근거와 비어 있는 근거

| 상태 | 항목 | 근거 또는 미확인 이유 |
| --- | --- | --- |
| ✅ Pass | 병합 충돌 | 검토 시점 GitHub `mergeable: true`, PR은 Draft가 아님. |
| ✅ Pass | PR Gate | 구현 HEAD `d7de1de`의 run `38263279883` 성공. Source contracts, deterministic tests, projection, Rulesync 검증 단계 통과. |
| ✅ Pass | 정적 계약·회귀 검증 | 두 Ollama 프로필의 후보 집합/Skill 메타데이터, native runner 인증 격리·명령 구성·결과 manifest 등 repository-owned 테스트. |
| ✅ Pass | 이전 인라인 리뷰 | 3개 thread 모두 resolved. 리뷰 제출 4건은 `COMMENTED`이며 승인(`APPROVED`)과 동일하지 않다. |
| ⚪ Not Verified | Promptfoo fixture-mode 통합 | 설치된 Promptfoo CLI를 통한 `eval-mols-loops-smoke`의 실제 실행 근거 없음. |
| ⚪ Not Verified | Ollama 모델 통합 | `mols-loops` 및 sibling Routing, Behavior grader의 실제 모델 요청·응답과 오류 분류 근거 없음. |
| ⚪ Not Verified | Codex Native 통합 | 인증된 `openai:codex-sdk` provider 로딩, Skill 읽기 positive/negative control 및 trace 미확인. |
| ⚪ Not Verified | Semantic 품질·실행 궤적 | `llm-rubric` calibration, 실제 tool/permission/side-effect 관찰, 반복 trial의 안정성 미검증. |
| ⚪ Not Verified | 최종 GitHub 통합 조건 | 이 보고서 추가로 HEAD가 이동한 뒤 새 PR Gate와 GitHub의 실제 required review/Ruleset 조건은 재확인 필요. |

이 표에서 `Pass`는 **적힌 항목만 통과했다**는 뜻이다. 특히 deterministic 테스트 성공을 Ollama/Codex의 model behavior PASS로 확대하지 않는다.

## 병합 전 제안 작업 — 우선순위와 종료 조건

### P0 · 실행 경로가 실제로 동작하는지 확인

1. **Promptfoo fixture-mode smoke** — 로컬에서 `mise run eval-mols-loops-smoke`를 실행한다. 설치/CLI, Python provider, fixture 생성 및 assertion 연결이 오류 없이 동작하는지 확인하고 실행 환경과 exit code를 기록한다. 실패하면 provider/API·버전 문제와 fixture 오류를 먼저 분리한다.
2. **Ollama 실제 평가** — 실행 중인 Ollama에 선택한 모델이 있는 상태에서 `mise run eval-asset-routing-ollama` 및 `mise run eval-mols-loops-ollama`를 실행한다. 긍정·부정·경쟁 선택 사례를 표본 확인하고 provider/HTTP 오류, 모델이 반환한 유효하지 않은 JSON, 실제 잘못된 선택, grader 실패를 구분한다. **모든 case의 고득점을 무조건 병합 조건으로 만들지 않는다.** 평가 harness가 실제로 결과를 얻고 실패 원인을 식별할 수 있어야 한다.
3. **Codex Native Routing 최소 실행** — 인증된 환경에서 `mols-loops`와 `asset-routing`을 각각 `--suite trigger --repeat 1 --output ...`으로 실행한다. SDK/provider가 로드되는지, staged canonical Skill이 관찰되는지, 최소 한 개의 **positive Skill-use control**이 정상 검출되는지, negative case 및 raw trace가 의미 있게 기록되는지 확인한다. `not-skill-used`만 PASS인 결과는 성공 근거가 아니다.
4. **결과 판독 및 결함 처리** — 실행 산출물에서 모델 선택 오류와 harness/fixture/telemetry 오류를 분류한다. 의도한 평가를 측정하지 못하는 재현 가능한 통합 결함은 수정하고 deterministic regression을 남긴다. 반대로 실제 모델의 낮은 capability 점수만으로 평가 도구의 구현 실패라고 단정하지 않는다.

아래 명령은 저장소 루트에서 실행한다. Ollama는 먼저 서버를 실행하고 기본 `qwen2.5` 모델을 준비한다. 모델·grader를 바꾸면 그 값을 기록한다.

```bash
# 1. Promptfoo wiring (모델 호출 없음)
mise run eval-mols-loops-smoke

# 2. Ollama 모델 평가
ollama pull qwen2.5
mise run eval-asset-routing-ollama
mise run eval-mols-loops-ollama

# 3. Codex Native Routing (인증 필요)
uv run --locked --no-default-groups python -m scripts.agent_assets.native_eval_run mols-loops --suite trigger --repeat 1 --output .tmp/evals/mols-loops-trigger.json
uv run --locked --no-default-groups python -m scripts.agent_assets.native_eval_run asset-routing --suite trigger --repeat 1 --output .tmp/evals/asset-routing-trigger.json
```

Codex는 `OPENAI_API_KEY` / `CODEX_API_KEY` 또는 인증된 전용 `CODEX_EVAL_HOME` 중 한 방식을 사용한다. API key와 명시적 Home을 함께 지정하면 runner가 거부한다. API key·인증 파일·개인 Home 경로는 PR이나 결과 보고서에 넣지 않는다. `.tmp/evals/` 산출물과 manifest는 로컬의 임시 증거이며 무분별하게 commit하지 않는다.

**P0 완료 판정:** Promptfoo 자체가 실행되고, Ollama와 Codex 각각에서 실제 provider 호출·의미 있는 출력·positive/negative control의 판독 근거를 확보했으며, 발견된 harness 결함을 수정했거나 명시적으로 분류했을 것. 결과의 model/runtime, fixture·Skill revision, 선택한 model과 grader, exit code, 오류 유형을 PR에 요약한다. 실제 관찰 없이 PASS를 기록하지 않는다.

### P0 · 최신 변경에 대한 통합 게이트와 승인

- P0에서 코드·config를 고쳤다면 해당 HEAD에서 PR Gate를 다시 통과시키고 이전 review thread가 다시 열리지 않았는지 확인한다. 코드 변경이 없더라도 이 보고서를 포함한 최종 HEAD의 체크를 확인한다.
- 실제 GitHub의 required checks/reviews/Ruleset 충족 여부를 확인한다. `mergeable: true`만으로 모든 병합 조건이 충족됐다고 판단하지 않는다.
- PR 설명의 Validation/Risks를 실제 확보한 근거로 갱신하고, 병합할 범위와 남겨 둘 deferred evidence를 명시한다.
- 저장소 정책에 따라 **사람의 명시적 승인 후** `main`으로 squash merge한다. 이 보고서는 승인이나 merge 실행을 대신하지 않는다.

### P1 · 실제 결과를 본 뒤 범위를 결정할 개선

- **Behavior grader calibration:** 인간 판단 또는 known-good/known-bad 응답과 `llm-rubric` 판정을 비교한다. Grader transport·판정 오류를 model failure로 계산하지 않는다. 최종 목표가 response-only capability 확인이라면 반복 calibration 규모를 최소화하고, 중요한 점수를 regression 기준으로 삼을 때 확대한다.
- **반복·회귀 검증:** Routing이나 Behavior 결과 변동이 관찰될 때에만 같은 model·fixture·설정으로 trial을 반복하고 안정적인 failure를 regression으로 승격한다.
- **Observable trajectory:** 실제 승인, tool call, 외부 side effect가 필수 계약인 사례에 한정해 별도의 state/trace grader를 제안한다. 현재 응답 수준 rubric으로 실행 결과를 증명한다고 주장하지 않는다.
- **Ollama native telemetry 요구 여부:** 현재 Ollama는 `Skill 메타데이터 기반 모델 Routing`을, Codex는 `실제 Skill 파일 읽기`를 평가한다. **둘 모두 실제 agent Skill discovery를 관찰해야 한다**는 요구라면 현재 Ollama 구현은 미충족이다. 그 경우 대상 Ollama agent harness와 관찰 가능한 trace/Skill loading 계약을 먼저 정하고, 별도 구현·검증이 필요하다. 단순히 동일 case ID를 쓴다는 이유로 측정 동등성을 선언하지 않는다.

P1을 병합 전으로 당길지는 **그 결과가 실제 병합 판단을 바꾸는지**에 따라 결정한다. 평가 결과를 안정적인 regression 보장으로 홍보하려면 관련 근거를 확보해야 하지만, 아직 측정하지 않은 capability 개선 과제는 deferred로 둘 수 있다.

## 최종 병합 판단 체크리스트

- [ ] Promptfoo fixture smoke 실제 실행 기록 확보
- [ ] Ollama `mols-loops` 및 sibling Routing/Behavior 대표 실행 결과와 실패 분류 확보
- [ ] Codex Native 두 Routing 프로필의 실제 provider 로딩 및 positive/negative Skill-use 증거 확보
- [ ] 모델 품질 문제와 eval harness 결함을 구분하고 병합을 막는 재현 가능한 결함 해소
- [ ] 최종 HEAD의 PR Gate·required checks·review 상태 확인
- [ ] PR 설명에 확인된 결과/미검증 범위 반영, 사람의 명시적 merge 승인

**인계 판단:** 지금 필요한 일은 새로운 추상화나 fixture 수 확대보다 **실제 실행 증거 확보 → 결함 분류 → 최소 수정 → 최종 게이트 확인**이다. 새 증거가 나오기 전에는 병합 가능성을 'CI 충족'과 '기능 동작 미검증'으로 분리해 표현한다.

## 근거와 정본

- [PR #238](https://github.com/mols3131d/mols-agent-assets/pull/238) · [검토 스냅샷 PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/38263279883)
- [Eval 실행 경로](../../evals/README.md) · [Eval 정책](../../docs/development/evaluation.md) · [CI 병합 근거 정책](../../docs/development/ci.md) · [GitHub merge 정책](../../docs/development/github.md)
- [초기 조사 문서](../2026-09-16/agent-asset-eval/research.md)

이 보고서는 시점이 고정된 **inbox 작업 문서**이며 정책이나 자동 승인 조건을 새로 정의하지 않는다. PR과 정본 파일 및 최신 Checks가 실제 상태의 소유자다.
