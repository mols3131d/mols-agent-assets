# LLM 평가 실행 비용 최적화 — 작업 인계

**상태:** Draft PR #292의 구현 준비. 이 문서는 `.inbox/` 작업 자료이며 정책 정본이나 완료 근거가 아니다.

## 목표와 경계

실제 LLM·채점기가 필요한 검증만 선택적으로 실행하고, 기본 개발·CI 경로는 외부 LLM 호출 없이 유지한다. 비용을 줄이면서 필요한 model/runtime regression evidence는 보존한다.

- 기본: 정적 검사·mock·deterministic test·fixture smoke. 실모델 품질을 증명하지 않는다.
- 필요시: 로컬 실모델 eval. 원격 provider는 별도 승인·범위 제한 후 대상 모델을 검증한다.
- **우선순위:** 현재 저장소에서 모델 실행이 있는 주 경로는 `mise run eval`(Promptfoo)이다. `tests/`는 주로 결정론적 test이므로 기존 pytest 테스트 전체에 marker를 붙이지 않는다.
- 작업 범위는 이 저장소의 평가 실행 경로 개선이다. 일반적인 LLM 테스트 프레임워크나 새 gateway 구축은 목표가 아니다.

## 현재 근거와 작업 시작점

| 범위 | 현재 상태 | 구현·검증 출발점 |
| --- | --- | --- |
| pytest | `mise run test` → pytest. 현재 `pyproject.toml`에 LLM 비용 marker 미등록 | `pyproject.toml`, `tests/conftest.py`, `tests/scripts/agent_assets/` |
| Promptfoo runner | `mise run eval -c ...` → 고정 `promptfoo@0.122.0`. 기본 Ollama, runtime/grader는 별도 provider 설정 | `mise.toml`, `scripts/agent_assets/promptfoo_run.py`, `promptfoo_env.py`, `.env.example` |
| Fixture와 선택 | generator가 `skill/suite/mode/case_id` metadata와 선택적 `case_ids`를 제공 | `scripts/agent_assets/skills_promptfoo.py`, `evals/skills/*/cases.json` |
| 모델 없는 smoke | `mols-loops-smoke.yaml`: fixture provider, `semantic: false` | `evals/promptfoo/mols-loops-smoke.yaml` |
| native model eval | `mols-loops.yaml`, `mols-stdd.yaml`, `mols-dev-env-bootstrap-design.yaml`: target provider; behavior에 semantic grader 가능 | 해당 `evals/promptfoo/*.yaml` |
| custom model eval | `mols-test-design.yaml`: custom Ollama; 일부 behavior는 참조 선택 모델 호출이 선행됨 | `evals/promptfoo/mols-test-design.yaml`, `test_test_design_reference_eval.py` |
| grader 평가 | `mols-dev-env-bootstrap-design-grader.yaml`의 target은 `echo`지만 `llm-rubric` assertion은 grader 모델을 호출할 수 있음 | `generate_grader_tests`, `test_skills_promptfoo_grader.py` |
| 기존 안전성 테스트 | runner/provider/metadata/grader의 호출을 monkeypatch한 결정론적 테스트 존재 | `test_promptfoo_run.py`, `test_skills_promptfoo.py`, `test_skills_promptfoo_contract.py` |

**확인된 갭:** 기본 `promptfoo_run.py`는 외부 provider 사용 opt-in, 선택 case 상한, model/grader 비용 상한을 강제하지 않는다. `PROMPTFOO_DISABLE_REMOTE_GENERATION`, telemetry/sharing 설정과 `--no-write`는 target·grader API 호출의 차단 수단이 아니다. `--no-cache`는 오히려 캐시 재사용 없이 실제 요청을 반복할 수 있다.

**정본:** [Testing](../../docs/development/testing.md) (deterministic), [Evaluation](../../docs/development/evaluation.md) (behavior claim), [CI](../../docs/development/ci.md) (blocking/deferred), [Promptfoo 실행 안내](../../evals/README.md)와 [도구 문서](../../docs/tools/promptfoo.md). 저장소 작업은 루트 `AGENTS.md`·`CHATBOT.md`, GitHub/VCS 정책을 먼저 적용한다. Agent Asset eval fixture·config·grader를 변경할 때는 [저장소 전용 Agent Asset 워크플로](../../.rulesync/skills/repository-agent-asset-workflow/SKILL.md)에서 적용 절차를 선택하고, [Agent Asset Management](../../docs/development/agent-assets/agent-asset-management.md)에 따라 문서 영향과 유지보수 책임을 검토한다.

## 선택 전략 — 목적과 호출 경계를 구분

1. **pytest:** 실제 LLM 요청을 하는 pytest 테스트가 존재하거나 추가될 때만 `llm_local`/`llm_remote` 등 최소 marker를 등록한다. 기본 test task는 해당 테스트를 제외하고 marker 오타는 `strict_markers`로 실패시키되, **미표기 테스트의 원격 접속을 marker만으로 방지할 수 없다**. 테스트 전송 경계를 mock/차단 테스트로 검증한다.
2. **Promptfoo:** 기존 `suite`, `case_ids`, `--filter-metadata`를 먼저 이용한다. 불필요하게 새 fixture 복제·task 별칭·`profile` 분류를 추가하지 않는다. 대표 subset을 안정적으로 지정할 방법이 부족할 때만 metadata 필드를 신설한다.
3. **필터 안전:** Promptfoo `--filter-metadata`의 값은 **부분 문자열 일치**를 지원한다. `mode=activation`이 `activation-negative`까지 잡을 수 있다. 유료·원격 평가 전에는 **선택된 case ID와 개수**를 별도로 검증하고 0건/예상 초과/불명확한 선택은 실패시킨다. 필요하면 정확한 `case_ids` allowlist를 우선한다.
4. **요청 경계:** `fixture / local model / remote model`의 evidence와 `network: none / loopback / external`을 분리한다. `ollama:` provider라도 `OLLAMA_BASE_URL`이 외부 주소면 원격 전송이다. grader 및 custom Python provider도 별도로 분류한다. 모르는 provider/endpoint는 기본적으로 허용하지 않는다.

### 실행 예시와 주의

```bash
# 현재 사용 가능한 비모델 smoke (grader도 deterministic으로 고정)
mise run eval -c evals/promptfoo/mols-loops-smoke.yaml

# 현재 가능한 suite 필터. 이 명령은 실제 Ollama 호출을 수행하므로
# 사용자가 모델 실행을 승인하고 환경을 확인한 경우에만 실행한다.
mise run eval --no-cache --no-write -c evals/promptfoo/mols-test-design.yaml --filter-metadata suite=trigger
```

`pytest -m`은 `mise run eval`의 선택을 제어하지 않는다. 비용 방어는 테스트 마킹과 별도 실행 preflight에서 다룬다. 신규 예시 명령은 구현·해당 pin 버전 검증 전까지 사용 가능하다고 안내하지 않는다.

## 구현 순서

1. **경로 인벤토리:** `evals/promptfoo/`의 모든 config와 generator·custom provider·grader에 대해 실제 target 요청, rubric 요청 수(criterion별), 참조 선택, 반복·retry, 외부 전송 경로를 분류한다. Fixture/echo라는 이름만으로 무료라고 판단하지 않는다.
2. **선택 최적화:** 기존 `case_ids` 또는 검증된 필터를 통한 소규모 대표 실행을 먼저 구현한다. 0건 선택이나 과다 선택을 결과에 드러낸다. pytest에는 실제 LLM 통합 테스트가 있을 때만 marker·default exclusion을 추가한다.
3. **원격 호출 가드:** repository-owned runner에서 선택 config·target provider·grader·custom provider·endpoint를 검사하고 미승인 외부 호출을 실행 **전에** 차단한다. 알 수 없는 동적 provider/config가 있으면 안전하게 실패하거나 검증 가능한 별도 실행 경계로 인계한다. **직접 Promptfoo CLI, 임의 외부 스크립트까지 이 wrapper가 보호한다고 주장하지 않는다.**
4. **호출량 제한:** target 요청 수뿐 아니라 `llm-rubric` criterion 수, 참조 선택 요청, repeat, 자동 retry의 상한을 검토한다. `maxConcurrency=1`은 요청 수 제한이 아니다. 실제 집행 가능한 호출/토큰 한도를 적용하고 불가능한 경로는 원격 실행에서 제외하거나 불확실성을 명시한다. 예상 금액은 **추정치**로만 보고하며 provider-level spending cap이 없는 경우 금액의 hard cap을 보증하지 않는다.
5. **비용·신뢰성 균형:** deterministic oracle로 충분한 경우 LLM grader를 피하되 semantic quality case는 유지한다. 캐시는 중복 진단에는 활용할 수 있지만 독립 시행이 필요한 regression의 반복 결과로 간주하지 않는다. 다른 저가 모델 결과를 실제 target model의 PASS로 대체하지 않는다.
6. **검증·문서:** 기존 네트워크 없는 monkeypatch 테스트를 확장한다. 실행 정책과 CLI 선택 방법은 소유하는 정본 문서에만 반영하고, `.inbox/`는 작업 중 근거로 남긴다. CI gate 의미는 기존 정책에 따라 보존한다.

## 구현 에이전트가 검증할 시나리오

| 시나리오 | 기대 결과 |
| --- | --- |
| 기본 `mise run test` | 기존 deterministic 테스트 유지, 비승인 LLM 호출 없음 |
| 등록되지 않은 pytest marker / 잘못된 선택 | 조용한 누락 없이 오류 또는 명시적 진단 |
| Promptfoo case 선택 0건·의도하지 않은 추가 선택 | 실제 모델 실행 전 중단·원인 표시 |
| target은 로컬, grader만 외부 API | 별도 원격 승인 없으면 중단 |
| target은 echo/fixture, assertion만 LLM rubric | 실제 채점기 호출 경계로 판정하여 정책 적용 |
| `ollama:` + 외부 `OLLAMA_BASE_URL` | loopback으로 오인하지 않음 |
| custom provider / 미지 provider / config override | 검사 불가능하면 fail-closed; 직접 CLI 경계는 한계 명시 |
| 1 case에서 reference selection + behavior + grader | 실제 요청의 multiplicity를 사전 계산하거나 검증되지 않은 계산은 미확정으로 보고 |
| retry/repeat/다중 criterion/캐시 | 호출 수·비용 과소 계산 없이 제한, 독립 실행 근거 구분 |
| 실제 모델 미실행 | mock/fixture/구조 검증만 PASS, model quality는 Not Verified |

## 완료 조건

- [ ] 실제 비용 유발 경로와 선택 가능한 최소 사례를 문서·config로 확인하고, 저비용 기본 경로를 유지한다.
- [ ] pytest(실제 LLM 테스트가 있는 경우)와 Promptfoo가 각각 native marking/filtering을 통해 필요한 사례만 선택한다. 0건·초과 선택은 조용히 통과하지 않는다.
- [ ] repository-owned 평가 실행 경로에서 미승인 원격 target·grader·custom/외부 endpoint가 **호출 전** 차단된다. 차단 범위 밖 실행은 명시적으로 문서화한다.
- [ ] 호출 수 상한 또는 통제 가능한 예산 경계를 실제로 검증한다. 계정/명의 변경, provider 자동 fallback, 권한 없는 유료·외부 데이터 전송은 없다.
- [ ] 새 필터·가드·예외를 network-free 테스트로 검증하고 기존 fixture smoke·CLI 경로를 보존한다.
- [ ] mock/fixture, 로컬 runtime, 실제 target runtime의 evidence가 구분되고 필수 merge evidence는 약화하지 않는다.
- [ ] 관련 정본 문서·CLI 가이드·검증 근거를 갱신하고 PR Gate를 확인한다.

## 실행·인계 제약

- **지금은 PR 준비/검토 단계:** 실제 구현이나 모델 실행은 수행하지 않았다. 다음 작업자는 PR head·기존 변경·저장소 정책을 다시 확인하고 그때 사용 가능한 tools로 구현한다.
- 결제, 원격 모델 호출, 모델 다운로드, 계정·연결·명의 전환은 이 문서만으로 승인되지 않는다. 비공개 대화·Notion 문서·비밀값을 GitHub에 복제하지 않는다.
- 과도한 새 gateway, provider별 fixture 복제, 정적 검사로 충분한 영역의 model evaluation 추가는 제외한다.
- upstream CLI/SDK 기능은 고정된 `promptfoo@0.122.0`과 비교해 확인해야 한다. 관련 공식 자료: [pytest markers](https://docs.pytest.org/en/stable/how-to/mark.html), [Promptfoo test metadata](https://www.promptfoo.dev/docs/configuration/test-cases/), [Promptfoo CLI](https://www.promptfoo.dev/docs/usage/command-line/), [Promptfoo retry](https://www.promptfoo.dev/docs/configuration/rate-limits/).
