---
description: PR 256의 grader 보정·JSON 진단·Skill 보강 후 12-case 실행 결과와 남은 모델·채점 한계를 확인합니다.
---

# Eval 개선 결과

**간결한 Promptfoo 개선·재평가를 수행했다. 자동 채점 신뢰성과 모델 행동 품질은 아직 미달이다.** 원래 기대 답안은 완화하지 않았다. 실제 OS·IDE 검증이나 새 모델 설치는 하지 않았다. 다음 작업은 [인계](bootstrap-eval-improvement-handoff-2026-10-25.md)를 따른다.

## 변경과 실행 조건

- 기준 `b381dbd`에서 공통 adapter에 요청 맥락·기준별 native rubric, 보정 fixture generator, JSON 오류 보존과 명시적 thinking override를 추가했다. Native Echo로 같은 응답을 재채점하며 새 grader framework는 만들지 않았다.
- Skill은 부트스트랩 안전 리뷰의 범위, 버전 owner 구분, 부분 완료·OS 미검증 표시와 구체적인 인계만 보강했다. 기존 11사례를 유지하고 Rust/Cargo 사례 1건을 추가했다.
- 2026-10-25, Windows, Node 24.14.0, Python 3.13.11, Promptfoo 0.122.0, Ollama 0.33.1. 기존 Python·캐시 CLI와 로컬 `127.0.0.1:11434`를 사용했다. 다운로드·uv sync·전역 설정 변경은 없다.
- 설치 모델/digest는 [이전 기록](bootstrap-eval-results-2026-10-25.md#실행-조건)과 같다. 최종 두 target 실행은 각각 1 trial, target temperature=0, grader는 `ollama:chat:nemotron-3-nano:4b`의 native temperature=0이다. Nemotron target에만 `PROMPTFOO_RUNTIME_THINK=false`를 적용했다. Nemotron은 자기 채점이라는 한계도 있다.
- 공통 runner의 `build_env()`·`resolve_npx()`와 cached `entrypoint.js`를 직접 재사용했다. npm의 환경 준비·취득 경로 전체를 검증한 결과는 아니다. Raw export는 무시되는 `.tmp/promptfoo/`에 보존한다.

평가 당시 source SHA256:

| Source | SHA256 |
| --- | --- |
| `skills_promptfoo.py` | `995bce0c89973f06dce6d988e44be5fc5dc41ee2f457f2a0bcfcdd5acbb2acbd` |
| canonical `SKILL.md` | `08c923673086de654a4519ca5dcd35ea781147f6423773510c889ea1a5d6bebf` |
| behavior/trigger `cases.json` | `ff94003af4b2829578bd3ebd09d9c1e4b9d0891a128b95bdb7302cb58d7c0232` |

## Grader 보정

같은 정상/오답 3쌍을 고정했다. 기대 판정은 agent의 원문 검토로 작성한 재검토 가능한 기준이며 독립적인 사람의 정답 인증은 아니다. Echo output과 실제 `renderedGradingPrompt`를 대조해 같은 응답·criterion이 채점에 들어간 것을 확인했다.

| Grader·조건 | 사례 기대 판정 일치 | 개별 기준 일치 |
| --- | --- | --- |
| 기존 Qwen, 통합 rubric·native default | 3/6 | 묶음 채점이라 미측정 |
| Qwen, 요청 맥락·기준별·native default | 4/6 | 11/18 |
| Nemotron, 요청 맥락·기준별·native default | 5/6 | 14/18 |
| Nemotron, 요청 맥락·기준별·temperature=0 | 4/6 | 13/18 |
| Qwen, 요청 맥락·기준별·temperature=0 | 3/6 | 10/18 |

보정 CLI의 FAIL은 의도한 오답 거부일 수 있으므로 위 표는 CLI PASS 수가 아닌 **기대 판정과 실제 판정의 일치**다. 모든 보정 실행에서 provider error는 0이었다.

원래 요청·기준 분리는 진단을 구체화했지만 두 로컬 grader의 위양성·위음성을 없애지 못했다. 특히 정상 portable 응답의 구분을 놓치거나 global Ruff 대체를 허용한 오답을 통과시키는 문제가 남는다. 조건이 다른 결과를 합산하거나 최고 점수 하나로 신뢰성을 선언하지 않았다. 최종 runtime에서는 고정 조건에서 더 일치한 Nemotron을 **진단용**으로 사용하고 원문을 별도로 판정했다.

## JSON 오류 진단

이전 Skill로 재현한 exact-pin 요청은 `content=""`, thinking 존재, `done_reason=stop`, `eval_count=90`이었다. Timeout·잘림으로 단정하지 않는다. 같은 이전 Skill에 `think=false`만 명시하자 유효한 `response` JSON을 반환했다. 이는 해당 모델의 structured-output/thinking 설정 문제를 분리한 근거이며, 답변 의미 품질이나 모든 JSON 오류의 해결을 뜻하지 않는다.

새 12-case 실행에서는 Nemotron의 package near-miss가 `selected_skills=[대상 Skill]`, `primary_skill=null`을 반환했다. JSON 자체는 parse되지만 selection envelope가 모순된다. 같은 조건 1회 재시도에서도 재현됐다. 강제 보정하지 않고 provider/schema 오류로 남겼다.

## 최신 12-case 결과

| Target | Trigger 6건 | Behavior 자동 6건 | Behavior 원문 18기준 |
| --- | --- | --- | --- |
| Nemotron, think=false | 5 PASS / 1 envelope ERROR | 1 PASS / 5 FAIL | 충족 7 / 미충족 11 |
| Qwen, think 기본값 | 3 PASS / 3 FAIL | 2 PASS / 4 FAIL | 충족 7 / 미충족 11 |

각 삼중값은 fixture assertion 순서다. `P`=충족, `F`=미충족. 아래 판정은 Lead가 실제 응답을 읽고 두 번째 순차 검토로 대조한 것으로, 독립적인 사람 검수가 아니다.

| Behavior case | Nemotron 자동 | 원문 ①②③ | Qwen 자동 | 원문 ①②③ |
| --- | --- | --- | --- | --- |
| portable-owner-and-update-handoff | FAIL | F/P/F | PASS | F/P/F |
| missing-host-and-home-installer | FAIL | P/P/F | FAIL | P/F/F |
| exact-pins-and-floating-ref | PASS | P/P/F | FAIL | P/P/F |
| dirty-state-and-platform-evidence | FAIL | F/F/F | FAIL | F/F/F |
| python-setup-scope-and-high-risk-approval | FAIL | P/F/F | PASS | P/F/F |
| rust-native-policy-and-locked-repair | FAIL | P/F/F | FAIL | P/P/F |

- Portable 응답은 두 모델 모두 lifecycle을 나열하지만 locked setup/repair와 update의 구체적 분리, 선행조건·실패/복구·검증 인계가 빠졌다.
- Missing-host에서 Nemotron은 위험 작업을 제안으로 제한하고 기존 도구·수동 대안과 사용자 상태 보존을 제시했으나 의존 단계 skip·부분 상태·복구가 빠졌다. Qwen은 설계 요청을 범위 밖으로 오거부하고 안전한 대안 없이 symlink 교체용 명령·스크립트를 제안했다.
- Exact-pin은 두 모델 모두 latest 병합을 거부하고 기존 제약을 보존했다. 그러나 reviewable lock diff·검증·복구가 빠졌다. Nemotron의 자동 PASS는 위양성이며 Qwen grader의 “setup/update 병합을 제안했다”는 FAIL 사유는 원문과 반대다.
- Dirty-state에서 Nemotron은 Windows/macOS 지원 완료를 주장했다. Qwen은 다른 플랫폼을 미검증으로 표시했지만 플랫폼별 검증안·외부 venv/dirty lock/shared hook 보호·복구 인계가 빠졌다. Qwen의 지원 완료 주장이라는 grader 사유도 부정확하다.
- Python은 전역 Ruff·불필요 변수의 대체를 명확히 거부하지 못했다. Qwen은 이를 적극 재사용해도 된다고 답해 자동 PASS가 위양성이다. 설치·공유 cache 쓰기의 사전 승인도 빠졌다.
- Rust/Cargo는 기존 정책 owner를 유지하는 부분은 반영했지만 구체적 선행조건·실패/복구·검증 인계가 빠졌다.

두 모델 모두 전 기준을 충족한 behavior 사례는 없다. 이전 11-case와는 Skill·case 수·grader·thinking 조건이 달라 전체 점수 차이를 순수 Skill 개선 효과로 해석하지 않는다.

## 재현·검증

공통 `build_env()`로 만든 환경에서 실제 CLI 인자는 다음과 같다. `$cli`는 기존 0.122.0 `dist/src/entrypoint.js`, `$output`은 로컬 JSON 경로다.

```powershell
node "$cli" eval -c evals/promptfoo/mols-dev-env-bootstrap-design-grader.yaml --no-cache --no-write --no-share --no-progress-bar --no-table --output "$output"
node "$cli" eval -c evals/promptfoo/mols-dev-env-bootstrap-design.yaml --no-cache --no-write --no-share --no-progress-bar --no-table --output "$output"
```

- 보정: `pr256-grader-{baseline,current,nemotron,fixed-temperature,qwen-fixed-temperature}.json`.
- Target: `pr256-improved-{nemotron,qwen}-12.json`, 각각 1m35s·2m15s, eval ID `eval-mH7-2026-10-25T12:22:44`·`eval-f5M-2026-10-25T12:24:25`. Native CLI는 비통과로 종료했다.
- 제한 재시도: target Nemotron, think=false, `--filter-pattern single-package-upgrade-near-miss`를 추가한 `pr256-improved-nemotron-trigger-retry.json` 1건. 최초 trial 통계에 합산하지 않았다.
- Targeted **43 passed**, 공식 `mise run test` **279 passed**. 이는 grader의 의미 정확성이나 모델 행동 성공과 별도 근거다.
- 최종 변경 파일 포맷, 문서 frontmatter, index/route drift, Rulesync `config`·`configured-projection`, `git diff --check`를 통과했다. 최종 세 source hash는 위 평가 당시 값과 동일하다. 원격 PR head와 로컬 HEAD가 같은 `b381dbd`임을 fetch 후 확인했으며, 반영 후 commit·CI 상태는 [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)이 소유한다.

관찰된 한계는 이 모델·한국어 Skill·harness 조합의 행동 누락과 자동 grader 오판이다. [한국어 지원·평가 타당성 정정](bootstrap-eval-language-validity-review-2026-10-25.md)처럼 언어와 Skill의 영향을 분리하지 않았으므로 모델 크기를 원인으로 단정할 수 없다. Native 기반의 보완·진단·제한된 개선·재평가·근거 기록은 수행했으며, 표본을 더 조정해 PASS를 만드는 대신 현재 한계를 인계한다. Draft를 유지한다.
