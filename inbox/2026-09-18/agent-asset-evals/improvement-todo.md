# Existing Eval 개선 투두

- 작성일: 2026-09-18
- 범위: 현재 존재하는 `evals/skills/`, `evals/subagents/`, `evals/promptfoo/` fixture와 실행 구조
- 목적: eval 없는 자산 추가가 아니라, 이미 있는 eval의 측정 품질·일관성·재현성 개선

## P0. Contract·검증 기반

- [ ] Skill fixture 공통 schema 정의
  - 대상: `evals/skills/*/*.json`
  - `version`, `contract`, `system_under_evaluation`, `cases` 공통 필드 결정
  - 기존 `cases.json`, `trigger-evals.json`, `behavior-evals.json` 호환 전략 결정
  - 완료: migration 없이 validator가 세 형식을 명시적으로 구분·검증

- [ ] Skill fixture validator 강화
  - 대상: `tests/evals/test_skill_eval_json.py`
  - unique `id`, non-empty `prompt/query/input`, mode별 required field 검증
  - trigger case: `should_trigger` 또는 `expected_selection` 일관성 검증
  - behavior case: `expected` 또는 `assertions` 존재 검증
  - 완료: 잘못된 fixture를 deterministic하게 거부

- [ ] Subagent fixture schema 확장
  - 대상: `tests/evals/test_subagent_cases.py`, `evals/subagents/mols-review-dualvantage/cases.json`
  - `mode` 허용값과 system-level contract 명시
  - delegation, ownership, handoff, termination case 분류 필드 추가
  - 완료: family fixture가 어떤 subagent 관계를 평가하는지 machine-checkable

- [ ] capability/regression 목적 metadata 추가
  - 대상: 모든 기존 fixture
  - case 또는 suite에 `purpose: capability | regression` 추가
  - 불안정한 semantic case는 capability로 유지
  - 완료: regression 승격 여부를 파일 내용에서 확인 가능

## P1. 기존 Skill fixture 품질 개선

- [ ] `caveman-ko` trigger fixture 보강
  - 대상: `evals/skills/caveman-ko/trigger-evals.json`
  - explicit activation, ordinary brevity, deactivation, lifetime, intensity near-miss 균형 확인
  - 영어·한국어·slash syntax의 중복 case 통합 검토
  - 완료: false positive/false negative 경계가 각 1개 이상 존재

- [ ] `caveman-ko` behavior fixture 구조 통일
  - 대상: `evals/skills/caveman-ko/behavior-evals.json`
  - `input/expected` 형식을 공통 `prompt/assertions` projection과 연결
  - 보존 항목을 의미·수치·부정·불확실성·정확 토큰·순서로 분리
  - 완료: semantic rubric과 deterministic protected-token check 분리

- [ ] `mols-text-optimizer` trigger fixture 정리
  - 대상: `evals/skills/mols-text-optimizer/trigger-evals.json`
  - `specific-owner-*` negative case와 generic optimization positive case의 경계 명확화
  - `caveman-style`, summary, translation, humanization 중복 경계 유지
  - 완료: generic response brevity와 target-text optimization이 혼동되지 않음

- [ ] `mols-text-optimizer` behavior fixture deterministic check 추가
  - 대상: `evals/skills/mols-text-optimizer/behavior-evals.json`
  - exact technical token, code fence, heading/list 구조, 숫자·조건·예외 보존을 구조 check로 분리
  - 전체 문자열 equality 금지
  - 완료: 의미 rubric 실패와 literal/structure 보존 실패를 구분

- [ ] `mols-agent-asset` routing/behavior 분리
  - 대상: `evals/skills/mols-agent-asset/cases.json`
  - `mode`를 activation, activation-negative, behavior 계열로 명시적으로 정리
  - authoring, validation, evaluation, rule/prompt/hook/MCP ownership 경계 분리
  - 완료: routing mismatch와 behavior failure가 별도 metric으로 집계

- [ ] `mols-agent-asset-find` routing/behavior 분리
  - 대상: `evals/skills/mols-agent-asset-find/cases.json`
  - select, use, persist, sync, negative 책임을 suite로 분리
  - no-match, source boundary, identity uncertainty, overwrite risk 보강
  - 완료: discovery 성공과 mutation 안전성이 같은 PASS로 합쳐지지 않음

- [ ] `mols-clarify-code` protected-content case 보강
  - 대상: `evals/skills/mols-clarify-code/cases.json`
  - docstring/comment-only boundary와 executable refactor near-miss 분리
  - caller contract, rationale, invariant, ordering, side effect 보존 case 추가
  - 완료: 설명 개선과 코드 변경이 명확히 분리됨

- [ ] `mols-code-comprehension-refactor` behavior grader 정밀화
  - 대상: `evals/skills/mols-code-comprehension-refactor/cases.json`
  - behavior preservation, public API preservation, performance caveat, scope restraint 분리
  - “더 읽기 쉬움” 단일 rubric을 세부 criterion으로 분해
  - 완료: readability와 correctness를 별도 평가

- [ ] `mols-loops` fixture 중복·과적합 점검
  - 대상: `evals/skills/mols-loops/cases.json`
  - 유사 prompt 반복 제거 또는 각 case의 고유 failure mode 명시
  - lifecycle, gate, loop count, scope expansion, evidence claim별 suite metadata 추가
  - 완료: 71건이 case 수가 아니라 보호하는 contract 기준으로 설명 가능

- [ ] `mols-loops` native lane case subset 재검토
  - 대상: `evals/promptfoo/mols-loops-native.yaml`, `mols-loops-native-smoke.yaml`
  - smoke는 plumbing, native eval은 실제 runtime evidence로 명확히 구분
  - trigger `skill-used/not-skill-used`와 behavior outcome metric 분리
  - 완료: fixture-mode PASS가 runtime behavior PASS로 해석되지 않음

- [ ] `mols-review-dualvantage` family fixture 보강
  - 대상: `evals/subagents/mols-review-dualvantage/cases.json`
  - verifier/challenger/root ownership을 case metadata로 명시
  - timeout, empty output, incomplete handoff, unresolved coverage 추가
  - 완료: specialist 실패를 다른 reviewer가 대신 수행했다고 판정하지 않음

## P1. 공통 evaluator·native lane

- [ ] evaluator의 suite/lane metadata 표준화
  - 대상: `scripts/agent_assets/skills_promptfoo.py`
  - `routing`, `behavior`, `delegation` suite와 `contract`, `native` lane 명명 정리
  - 기존 config와 backward compatibility 유지
  - 완료: 결과 metadata만 보고 claim과 evidence level 식별 가능

- [ ] provider metadata schema 검증
  - 대상: `scripts/agent_assets/skills_promptfoo.py`, 관련 tests
  - `skillCalls`, tool calls, trace, runtime identity의 shape 검증
  - 누락 metadata와 실제 no-call을 구분
  - 완료: false negative를 빈 metadata로 숨기지 않음

- [ ] native routing lane 확장
  - 대상: `evals/promptfoo/`, `package.json`, `mise.toml`
  - `mols-agent-asset` ↔ `mols-agent-asset-find` sibling routing 추가
  - positive, negative, near-miss, direct-name bypass 포함
  - 완료: 두 자산 간 false positive/false negative 확인 가능

- [ ] repeated trial 실행 옵션 추가
  - 대상: `mise.toml`, Promptfoo entrypoint
  - 기본 1회, 비교·flaky 확인 3회 실행 경로 제공
  - cache off, model/runtime/config metadata 고정
  - 완료: 반복 결과를 단일 deterministic PASS로 과장하지 않음

- [ ] raw result evidence 저장 경계 정의
  - 대상: `evals/promptfoo/`, `.tmp/` 및 문서
  - disposable local result와 durable regression artifact 구분
  - 결과 저장 시 model, runtime, harness, asset revision 기록
  - 완료: 결과 재현 조건 누락 없음

## P2. Case 유지보수·중복 제거

- [ ] fixture case ID naming convention 통일
  - 대상: 전체 `evals/skills/`, `evals/subagents/`
  - `positive/negative/near-miss`, suite, behavior claim이 드러나는 ID 검토
  - 의미 없는 이름 변경은 피하고 migration map 유지
  - 완료: ID만 보고 case 목적 확인 가능

- [ ] assertions를 observable claim 단위로 분해
  - 대상: `mols-agent-asset`, `mols-agent-asset-find`, `mols-loops`, DualVantage
  - 여러 독립 조건을 한 assertion 문자열에 결합하지 않음
  - outcome, prohibited action, evidence, handoff를 각각 metric으로 분리
  - 완료: 실패 시 어떤 계약이 깨졌는지 확인 가능

- [ ] negative/near-miss 균형 감사
  - 대상: 모든 routing fixture
  - positive만 많은 suite에 인접 owner, keyword-only, explicit-name bypass 추가
  - case 수보다 false positive 보호 범위 우선
  - 완료: 각 suite에 의도된 rejection 근거 존재

- [ ] semantic rubric calibration 대상 선정
  - 대상: behavior fixture 전체
  - 사람 판단과 비교할 대표 case 선정
  - rubric drift, grader failure, target failure 분리
  - 완료: model grader 결과를 단독 merge truth로 사용하지 않음

- [ ] fixture prompt contamination 감사
  - 대상: 전체 eval fixture
  - expected answer, hidden requirement, canonical source 복제 여부 확인
  - task가 실제 사용자 요청보다 많은 조건을 요구하지 않는지 확인
  - 완료: eval-only 힌트가 target input에 불필요하게 노출되지 않음

- [ ] source asset revision linkage 추가
  - 대상: 전체 fixture
  - canonical asset path, asset revision 또는 snapshot 식별자 기록
  - generated projection을 canonical source로 기록하지 않음
  - 완료: fixture가 어떤 asset contract를 평가하는지 추적 가능

- [ ] fixture별 capability/regression 승격 검토
  - 대상: 기존 218 Skill case, 9 Subagent case
  - 반복 성공·실패와 실제 failure evidence가 있는 case만 regression 후보화
  - 불안정 semantic case는 capability 유지
  - 완료: regression 목적과 근거가 명시됨

## P3. 검증·문서화

- [ ] eval inventory 자동 생성
  - 대상: `scripts/` 또는 `tests/evals/`
  - canonical asset과 eval fixture의 coverage matrix 생성
  - eval 없는 자산과 fixture 없는 suite를 별도 표시
  - 완료: 수동 목록 drift 제거

- [ ] eval coverage 보고서 추가
  - 대상: `inbox` 또는 문서 owner 검토 후 canonical 위치 결정
  - 자산별 routing/behavior/delegation coverage와 evidence level 표시
  - 완료: “eval 있음”과 “충분히 평가됨”을 구분

- [ ] Promptfoo config contract test 확대
  - 대상: `tests/scripts/agent_assets/test_skills_promptfoo_contract.py`
  - config file existence, unique provider label, suite/lane validity, selected case validity 검증
  - 완료: config 오타가 runtime 실행까지 지연되지 않음

- [ ] 전체 eval validation task 추가
  - 대상: `mise.toml`
  - fixture validation, config contract, artifact validation, focused pytest 순서 고정
  - runtime/model eval은 별도 non-blocking 단계로 유지
  - 완료: local 전체 점검 명령 하나 제공

## 권장 실행 순서

1. 공통 Skill/Subagent fixture validator
1. `mols-agent-asset` / `mols-agent-asset-find` suite 분리
1. `mols-loops` 중복·native lane 정리
1. DualVantage family handoff/failure case 보강
1. caveman/text optimizer protected-content grader 분리
1. native routing lane 확장
1. ID·metadata·inventory 자동화
1. 전체 validation과 calibration

## 완료 기준

- [ ] 모든 기존 fixture가 명시적 claim과 evidence level을 가짐
- [ ] routing, behavior, delegation 결과가 metric상 분리됨
- [ ] fixture-mode, native-runtime, semantic grader 결과가 혼동되지 않음
- [ ] deterministic outcome은 deterministic grader로 우선 판정
- [ ] trajectory는 실제 contract인 경우에만 평가
- [ ] 기존 fixture 삭제·대량 재작성 없이 migration 완료
- [ ] 전체 fixture validator와 focused tests 통과
