# LLM Eval Cost Optimization — Implementation Handoff

## Goal

LLM 실행이 필요한 테스트만 명시적으로 선택하고, 대부분의 개발·CI 검증은 외부 모델 호출 없이 수행한다. 검증 수준을 희생하지 않으면서 실제 모델 호출·grader·재시도 비용을 줄이는 것이 목표다.

**상태:** 구현 준비. 이 문서는 작업 아티팩트이며 정본 정책이나 구현 완료 근거가 아니다.

## Current Baseline

- `tests/`는 repository-owned deterministic test, `evals/`는 Agent Asset behavioral eval을 소유한다. 기준: [Testing](../../docs/development/testing.md), [Evaluation](../../docs/development/evaluation.md), [CI](../../docs/development/ci.md).
- `mise run test`는 현재 pytest를 실행한다. `pyproject.toml`에는 비용·네트워크 관련 pytest marker가 등록되어 있지 않다.
- `mise run eval -c ...`는 [Promptfoo runner](../../scripts/agent_assets/promptfoo_run.py)를 사용한다. fixture-mode smoke는 실제 모델을 호출하지 않지만, Ollama/native provider를 선택한 eval은 모델 호출을 수행한다.
- [Fixture generator](../../scripts/agent_assets/skills_promptfoo.py)의 generated test metadata에는 이미 `skill`, `suite`, `mode`, `case_id`가 들어 있다. `--filter-metadata suite=trigger`는 기존 지원 경로다.
- `PROMPTFOO_RUNTIME_PROVIDER`와 `PROMPTFOO_GRADER_PROVIDER`는 서로 독립적이며 원격 provider를 가리킬 수 있다. `mols-test-design`의 조건부 reference 선택은 추가 Ollama 요청을 소비한다.
- 현재 runner 설정만으로 원격 provider 사용에 대한 명시적 opt-in 및 비용 상한 집행을 보장할 수 없다. `--no-cache`·`--no-write`·telemetry disable은 비용 차단이 아니다.

## Proposed Selection Contract

선택 **목적**과 실행 **환경**을 분리한다. Test metadata만으로 네트워크 허용을 결정하지 않는다.

| Surface | 분류·마킹 제안 | 선택 규칙 |
| --- | --- | --- |
| `tests/` — pytest | 실제 모델에 의존하는 신규·기존 테스트에만 `llm_local` 또는 `llm_remote` 등록·표기 | 기본 `mise run test`는 offline/deterministic만; opt-in `-m llm_local` 또는 `-m llm_remote` 선택. 오타는 strict markers로 실패 |
| `evals/` — Promptfoo | 기존 `suite/mode/case_id` 유지; 필요한 케이스에만 `profile=smoke\|regression\|extended`처럼 최소 목적 메타데이터 추가 | `--filter-metadata profile=smoke`, 기존 suite filter와 조합. Generator와 fixture owner 간 중복 정의를 피함 |
| Promptfoo provider/grader | `offline / local / remote` 실행 분류는 선택된 실제 provider·endpoint로 판단 | 실행 전에 target과 grader를 함께 분류·검사. `profile=smoke`라 해도 remote라면 차단 |
| Live release regression | 실제 target model/provider와 핵심 케이스를 소규모로 선택 | 다른 저가 모델의 PASS를 target runtime PASS로 간주하지 않음 |

**설계 판단:** 모든 pytest 테스트에 `offline` 마커를 소급 표기하지 않는다. 기본 unmarked deterministic 테스트는 유지하고 비용이 드는 테스트만 명시한다. Promptfoo는 pytest 마커가 적용되지 않으므로 CLI-native metadata 필터를 사용한다. 새로운 profile은 기존 `suite`·명시적 `case_ids` 필터로 충분하지 않을 때만 도입한다. 불필요한 고정 taxonomy와 wrapper task를 늘리지 않는다.

### Example invocation (proposed behavior; not yet implemented)

```bash
# Default: existing offline repository tests
mise run test

# Optional local/model tests, if introduced under pytest
uv run --locked --no-default-groups --group test pytest -m llm_local

# Existing Promptfoo selection by suite
mise run eval --no-cache --no-write -c evals/promptfoo/mols-test-design.yaml --filter-metadata suite=trigger

# Proposed Promptfoo short-list filter; requires implementation of profile metadata
mise run eval --no-cache --no-write -c evals/promptfoo/mols-loops.yaml --filter-metadata profile=smoke
```

단순한 `pytest -m`는 별도 `mise run eval` 호출을 제어하지 않는다. 둘 다 별도 비용·네트워크 정책이 필요하다.

## Implementation Plan

1. **Inventory** — 현재 Python test, Promptfoo config, generator, custom Python provider 및 grader를 정적 조사하고 실제 네트워크 접촉 경로를 열거한다. 이미 offline인 테스트를 불필요하게 변경하지 않는다.
2. **Mark/select** — 선택할 테스트만 안정적으로 표시한다. pytest `markers`·`strict_markers`와 default offline selection을 검토하고, Promptfoo에는 기존 `suite`·`case_ids`·`--filter-metadata`를 우선 재사용한다. 불필요한 전체 suite 호출을 제거한다.
3. **Fail-closed remote guard** — 기본 원격 LLM/LLM grader 실행을 거부하고 명시적 승인 시에만 허용한다. Provider ID뿐 아니라 endpoint·custom provider·grader·reference selection 경로의 우회 가능성을 점검한다. 사용 계정·연결을 자동 전환하지 않는다. CI의 offline execution은 실제 네트워크 차단이나 transport spy로 검증한다.
4. **Bound work** — 사전 case/provider/prompt/repeat 수, 추가 reference selection, grader 예상 요청 수를 보고 가능한 범위에서 제한한다. 최대 출력·retry·timeout을 점검한다. provider가 실제 hard-spend cap을 제공하지 않는다면 *추정 예산*을 절대 지출 보장으로 표시하지 않는다.
5. **Cheapest sufficient evidence** — mock/fixture/deterministic assertion으로 증명 가능한 claim에는 LLM 호출을 사용하지 않는다. 로컬 Ollama eval은 필요한 때만, target remote API는 승인된 최소 대표 사례로 제한한다. semantic grader는 필요할 때만 적용하고 known-good/bad sample을 활용한다.
6. **Regression & documentation** — `tests/`에 선택/차단/오타/비승인 provider·grader/custom provider/반복 횟수/잘못된 fallback 사례를 network-free fixture로 검증한다. `docs/development/evaluation.md`, `evals/README.md`, `docs/tools/promptfoo.md` 등 정본 owner의 변경 책임을 지키며 실행 예시를 갱신한다. CI의 admission 경계는 [CI policy](../../docs/development/ci.md)를 따른다.

## Acceptance Criteria

- [ ] 기본 repository test/PR deterministic gate에서 실제 원격 LLM·외부 grader 호출이 0임을 네트워크 차단/spy 기반으로 입증한다.
- [ ] pytest의 비용 유발 테스트는 등록된 marker로 명확히 선택·제외된다. 마커 미등록·오타로 테스트가 조용히 빠지지 않는다.
- [ ] Promptfoo는 기존 suite/case ID와 비용·목적에 맞는 대표 subset을 native filter로 선택할 수 있고, 예상 밖의 전체 케이스 실행을 예방한다.
- [ ] 미승인 remote runtime **또는 grader** 호출이 실행 전에 실패한다. custom provider·Ollama endpoint 등 우회 경계가 검토되고 중요한 경로가 검증된다.
- [ ] 원격 호출의 반복·선택·재시도·추가 model request가 명확히 기록되며, 사전 제한·중단 조건과 잔여 비용 불확실성이 문서화된다.
- [ ] 선택되지 않은 실제 모델의 품질 PASS를 주장하지 않고, `fixture`/`local`/`target runtime`의 evidence를 구분한다.
- [ ] 기존 fixture smoke, deterministic suites, 명시적 live eval의 계약이 불필요하게 깨지지 않으며 변경에 맞는 테스트와 PR Gate가 통과한다.
- [ ] 새 정책·마커·실행법은 소유하는 정본 문서와 사용 가이드에 반영되고, 비용 목적만으로 merge-critical evidence를 deferred 처리하지 않는다.

## Non-goals / Guardrails

- 범용 테스트 체계 재작성, 모든 test에 마커 강제, 추가 LLM gateway 도입, 모델/제공자 자동 변경, 무료 티어 계정 자동 확보, 실제 유료 평가 실행은 기본 범위에서 제외한다.
- 작업에는 사용자 개인 계정 정보, 비공개 Notion 보고서 본문·링크, 비밀키·실제 응답 원문 등을 기록하지 않는다.
- 원격 모델 호출·데이터 반출·모델 다운로드·유료 실행은 별도 승인과 환경 검증 없이는 실행하지 않는다.
- 현재 PR 준비 단계에서는 실제 구현·모델 실행 결과가 없으므로 완료라고 보고하지 않는다.

## Relevant Sources

- [Repository evaluation policy](../../docs/development/evaluation.md)
- [CI policy](../../docs/development/ci.md)
- [Promptfoo setup](../../evals/README.md)
- [Runner](../../scripts/agent_assets/promptfoo_run.py) · [Generator](../../scripts/agent_assets/skills_promptfoo.py)
- [pytest markers](https://pytest.org/en/latest/how-to/mark.html)
- [Promptfoo configuration and metadata filters](https://www.promptfoo.dev/docs/configuration/reference/)
- [Promptfoo CLI](https://www.promptfoo.dev/docs/usage/command-line/)
