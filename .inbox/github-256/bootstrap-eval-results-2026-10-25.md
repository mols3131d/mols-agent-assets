---
description: PR 256의 최신 한국어 Skill과 11개 사례를 두 로컬 모델로 실행한 결과, 개별 행동 기준 판정과 grader 위양성을 확인할 때 사용합니다.
---

# PR #256 — 최신 11-case 모델 평가

**실제 실행 완료, 행동 품질 미달.** Nemotron의 선택은 6/6, Qwen은 3/6이었다. 행동은 두 모델 모두 모든 필수 기준을 충족한 사례가 없었다. 자동 behavior PASS는 각각 3건이지만 모두 위양성이므로 Draft를 유지한다. Skill·fixture·runner는 수정하지 않았다.

## 실행 조건

- 2026-10-25, Windows, base `b29aa490d0c251d5ca478fa5c787b90258f09d79`, 평가 HEAD `81eb4579eac6b25b45878b31d86697863b3c25bd`.
- [Skill](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md), [11-case fixture](../../evals/skills/mols-dev-env-bootstrap-design/cases.json), [Promptfoo config](../../evals/promptfoo/mols-dev-env-bootstrap-design.yaml)를 그대로 사용했다. 모델별 전체 suite 1회, Nemotron의 JSON 오류 1건만 동일 조건으로 1회 재시도했다.
- Node `24.14.0`, Python `3.13.11`, PyYAML `6.0.3`, Promptfoo `0.122.0`, Ollama `0.33.1`. Target temperature는 기존 provider의 `0`, timeout은 기본 `120s`, concurrency는 기존 config의 `1`이었다. Grader는 두 실행 모두 `ollama:chat:qwen2.5-coder:7b`이며, Qwen 실행은 자기 채점이라는 한계가 있다.
- Target과 grader는 `http://127.0.0.1:11434`의 기존 설치 모델을 사용했다. 관련 경로·provider 환경변수 override는 사전 점검에서 발견되지 않았다. 다운로드, `uv sync`, 모델 pull, 전역 설정·훅 변경은 실행하지 않았다.
- 현재 worktree에 Python 환경이 없어 기존 다른 checkout의 Python 환경을 동기화 없이 사용했다. 공통 [runner](../../scripts/agent_assets/promptfoo_run.py)의 `build_env()`·`resolve_npx()`와 기존 [provider](../../scripts/agent_assets/skills_promptfoo.py)를 재사용하고, npx 취득 단계 대신 캐시된 동일 버전 CLI를 직접 실행했다. 따라서 npm 진입점의 설치·환경 준비 경로를 검증한 결과는 아니다. 결과·로그의 지정 경로는 무시되는 `.tmp/promptfoo/`였다.

| 모델 | 설치 digest |
| --- | --- |
| `nemotron-3-nano:4b` | `6cc467f054393a55e98a74098abde0c762ffb6d1d8cd64becf30458f38886197` |
| `qwen2.5-coder:7b` | `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364` |

실행 환경은 공통 `build_env()`에 `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, 위 Ollama 주소와 target/grader를 명시했다. 실제 CLI 인자는 다음과 같다. `$cli`는 기존 Promptfoo `dist/src/entrypoint.js`이며, `$output`은 모델별 로컬 JSON export다.

```powershell
node "$cli" eval -c evals/promptfoo/mols-dev-env-bootstrap-design.yaml --no-cache --no-write --no-share --no-progress-bar --no-table --output "$output"
```

Nemotron 재시도에는 같은 인자에 `--filter-pattern exact-pins-and-floating-ref`만 추가했다. 로컬 export는 `.tmp/promptfoo/pr256-{nemotron-11,nemotron-exact-retry,qwen-11}.json`이다. 공개 fixture만을 사용했지만 raw export와 상세 로그는 commit하지 않았다.

## 선택 6건

`선택`은 대상 Skill 하나가 primary인 JSON, `비선택`은 빈 목록과 null primary다. 모든 응답은 이 schema를 충족했다.

| Case | 예상 | Nemotron 실제 | Qwen 실제 |
| --- | --- | --- | --- |
| first-setup-and-repair-design | 선택 | 선택 | 선택 |
| explicit-bounded-update-design | 선택 | 선택 | 선택 |
| partial-failure-and-installer-review | 선택 | 선택 | 선택 |
| single-package-upgrade-near-miss | 비선택 | 비선택 | 선택 |
| one-off-tool-install-near-miss | 비선택 | 비선택 | 선택 |
| ci-only-pipeline-near-miss | 비선택 | 비선택 | 선택 |

단일 Skill 후보의 metadata 선택 실험이다. 실제 다중 Skill 경쟁이나 native discovery를 검증하지 않는다.

## 행동 5건과 15개 기준

각 삼중값은 [fixture](../../evals/skills/mols-dev-env-bootstrap-design/cases.json)의 assertion 순서이며, `P`=충족, `F`=미충족, `U`=응답 부재로 판정 불가다. Lead가 원문을 읽고 별도 읽기 전용 에이전트의 판정과 대조했다. 자동 점수를 수동 판정으로 덮어쓰지 않았다.

| Case | Nemotron 자동 | 기준 ①②③ | Qwen 자동 | 기준 ①②③ |
| --- | --- | --- | --- | --- |
| portable-owner-and-update-handoff | PASS | F/P/F | PASS | P/F/F |
| missing-host-and-home-installer | FAIL | P/F/F | PASS | P/F/F |
| exact-pins-and-floating-ref | ERROR | U/U/U | FAIL | F/P/F |
| dirty-state-and-platform-evidence | PASS | F/F/F | FAIL | F/F/F |
| python-setup-scope-and-high-risk-approval | PASS | P/F/F | PASS | P/F/F |

- **Nemotron: 3 P / 9 F / 3 U.** Portable은 기존 Volta/pnpm·Node 24를 유지하지만 repair/update 구분과 실패·복구·검증을 생략했다. Missing-host는 HOME symlink 교체와 다음 실행의 구 Agent 삭제를 기본 경로로 권고했다. Dirty-state는 “Windows/macOS support complete”, Python은 “relies on global Ruff”라고 답했다. Python의 설치·공유 cache 쓰기 승인 조건도 빠졌다.
- **Qwen: 4 P / 11 F.** Portable은 pnpm lock으로 Node를 갱신하는 잘못된 owner를 제시하고 “부분 성공을 전체 준비 완료로 보고합니다”라고 답했다. Missing-host는 이미 활성화된 설계 리뷰를 범위 밖으로 거부했다. Exact-pins는 기존 제약을 유지하지만 setup/update 분리와 diff·검증·복구 인계가 없다. Dirty-state는 Ubuntu 결과로 Windows/macOS 지원 완료를 허용했다. Python은 불필요한 `BOOTSTRAP_*` 변수와 전역 Ruff 대체를 거부하지 않았고 설치 승인 조건도 빠졌다.

Missing-host의 첫 기준은 host package·sudo·remote shell 설치를 제안하지 않았으므로 두 모델 모두 P다. Git/Bash를 언급하지 않았다는 이유만으로 이 부정 조건을 실패 처리하지 않았다.

## 오류와 채점 한계

| 실행 | 자동 집계 | 시간·종료 코드 |
| --- | --- | --- |
| Nemotron 전체 (`eval-a9t-2026-10-25T11:16:22`) | 9 PASS / 1 FAIL / 1 ERROR | 1m 36s / 1 |
| Nemotron exact-pins 재시도 (`eval-5dS-2026-10-25T11:19:39`) | 1 ERROR | 9s / 100 |
| Qwen 전체 (`eval-m2X-2026-10-25T11:19:52`) | 6 PASS / 5 FAIL / 0 ERROR | 57s / 1 |

Nemotron exact-pins는 두 번 모두 `Ollama runtime failed: Expecting value: line 1 column 1 (char 0)`와 빈 output을 반환했다. Provider/schema 오류로 분리하며 의미 실패나 성공으로 계산하지 않는다. 현재 export만으로 Ollama 원응답의 정확한 parse 실패 원인까지 확정할 수 없다.

두 모델의 자동 behavior PASS 3건씩은 모두 필수 기준을 놓쳤다. Nemotron portable grader는 응답에 없는 setup/update 구분을 있다고 서술했고, dirty/platform 및 global Ruff의 직접 위반도 통과시켰다. Qwen grader는 범위 밖 거부에 존재하지 않는 안전 대안·부분 복구를 있다고 판정했다. Qwen exact-pins의 FAIL 방향은 맞지만 “Python 범위·lock 유지를 명시하지 않았다”는 사유는 원문과 반대다.

Grader의 실제 입력은 output과 rubric이며 원 scenario·Skill은 포함되지 않았다. 다만 플랫폼 증거·전역 Ruff 위반은 rubric만으로도 판정 가능하므로 context 부족만으로 오판 전체를 설명할 수 없다. Grader 점수만으로 안전성이나 merge readiness를 판단하지 않는다.

## 검증과 다음 판단

- 기존 provider/runner targeted test **11 passed**. 이는 모델 행동 성능과 별도 근거다.
- Skill·fixture·runner 및 `uv.lock`·프로젝트 설정을 변경하지 않았다. 과거 영문 10-case 결과는 이번 결과에 합산하지 않았다.
- 실제 도구 설치·승인 이행·HOME containment·OS별 bootstrap은 측정하지 않았다. [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)의 구현 검증과 분리한다.
- **이번 Eval 인계는 완료했다.** 다음 과제는 대표 위양성으로 grader를 보정하고, 반복된 행동 누락을 작은 모델의 capability 한계와 Skill 표현 문제로 구분하는 제한된 개선이다. Expected answer를 완화하거나 case를 제거해 통과율을 높이지 않는다.
