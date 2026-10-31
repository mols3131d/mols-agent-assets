# PR #256 — 실제 모델 Eval 계획 루프 / Prepare

> 2026-10-25 · 계획 대상: `mols-dev-env-bootstrap-design` · [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)

## Active Scope

- **Goal:** 현재 한국어 Skill의 **실제 모델 선택(Routing)과 설계 행동(Behavior)**을 검증할 수 있는, 기존 Promptfoo/Ollama 체계를 재사용하는 실행 가능한 평가 계획을 만들고 리뷰·인계한다.
- **In:** PR #256의 `SKILL.md`, 11-case fixture, 기존 평가 adapter/runner/문서, 과거 결과 해석, 로컬 실행 조건, 판정·오류 분류·증거 저장과 후속 의사결정.
- **Out:** 이번 세션에서 로컬 Ollama/Promptfoo 평가 실행, 모델 다운로드·설치, 환경변수 영구 지정, Skill 동작 변경, CI 또는 bootstrap 구현 변경, PR #258 작업, 병합.
- **Acceptance:** (1) 최신 source 및 과거 결과의 구분; (2) 재현 가능한 최소 로컬 실행 절차; (3) Trigger/Behavior·grader·모델 변동과 비대칭 실패 판정; (4) 보안·비용·부작용 제어; (5) 모든 주요 단계의 GitHub inbox 아티팩트와 세션 간 인계; (6) 실제 미실행은 `not_run`으로 표시.

## Run configuration

- `mols-loops` Prepare → RPI Main Loop → Finalize. 사용자가 **조사·계획·검토의 재귀 반복**을 요구했으므로 필요한 하위 문제만 엄격한 부분 범위로 분리한다.
- Task Skill: `mols-agent-asset`의 Eval/Routing/Behavior/Evidence + 저장소 `docs/development/evaluation.md`.
- 기본 강도: deep(재귀 검토 요청의 취지). 경계에 비례해 반복하고 새 문제를 만들지 않는다. `loops_used`는 실질적인 Review 종료 후만 증가한다.
- 아티팩트 위치: `inbox/github-256/` 아래 날짜가 붙은 단계별 단일 Markdown 파일. Root `inbox/README.md`에 따른다.
- 사용 가능한 수행 능력: GitHub Plugin으로 live repository 소스 읽기와 문서 쓰기 가능. **GitHub Plugin이 로컬 사용자의 Ollama 모델 실행을 보장하지는 않는다.**

## 시작점 및 인계 메모

- 조사 시작 PR head: `b3c5024240030a39d342979ea04ff93935aee010` (이후 계획 아티팩트 커밋으로 tip 이동 가능).
- 정본: `src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md`(한국어), `evals/skills/mols-dev-env-bootstrap-design/cases.json`(11개).
- 기존 실행 surface: `evals/promptfoo/mols-dev-env-bootstrap-design.yaml`, `scripts/agent_assets/skills_promptfoo.py`, `scripts/agent_assets/promptfoo_run.py`; 기존 npm script가 진입점.
- 남은 최초 연구 질문: native 실행 경로의 사전조건, 평가 입력에 제공되는 맥락, 실제 grader 계약 및 실패 분류, 과거 trial의 의미, 기존 출력의 재현성/보존법.

## Readiness

**READY WITH LIMITS.** 계획 작성은 가능하나 로컬 모델 보유/실행 권한·상태는 이번 GitHub 읽기로 알 수 없다. 실행 계획에는 preflight 및 분기·미검증 처리로 다룬다. 이후 단계는 Research → Plan → Review를 문서화하고 최종 인계에서 실제 실행 전 승인/조건을 명시한다.
