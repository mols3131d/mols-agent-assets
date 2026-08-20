# Promptfoo Eval 도입 계획서

## 목표

기존 `evals/` behavioral contract를 유지하면서 Promptfoo를 교체 가능한 runtime eval backend로 연결한다.

이번 계획의 목표는 framework를 크게 도입하는 것이 아니라, **현재 eval fixture를 실제 runtime에서 반복 검증할 수 있는 최소 경로를 만드는 것**이다.

## 완료 상태

도입이 완료됐다고 판단하려면 다음 상태가 필요하다.

- `evals/`가 계속 behavioral contract의 authority다.
- Rulesync projection과 runtime behavior 검증이 분리되어 있다.
- 기존 fixture를 Promptfoo 전용 형식으로 복제하지 않는다.
- 최소 한 개 Skill이 end-to-end로 평가된다.
- deterministic grader와 model grader의 책임이 분리된다.
- API key 없이 실행 가능한 개발 경로가 최소 하나 존재한다.
- generated eval result는 기본적으로 일회성이다.
- Promptfoo를 제거해도 canonical asset과 fixture가 유지된다.

## Target Architecture

```text
Canonical Agent Asset
src/rulesync/.rulesync/
        │
        ▼
Rulesync Projection
        │
        ▼
Target Usage Surface ───────────────┐
                                    │ consumed by
                                    ▼
Behavioral Contract             Target Runtime
 evals/**/*.json                    ▲
        │                           │ invoked by
        ▼                           │
Eval Normalizer                Runtime Adapter
        │                           ▲
        └──────────► Promptfoo ─────┘
                         │
                         ├─ deterministic grader
                         ├─ local/model grader
                         └─ trial/result aggregation
```

Rulesync와 Promptfoo 사이에 직접적인 authority coupling을 만들지 않는다. Promptfoo는 runtime을 orchestration하고 평가하지만, target-specific asset surface는 Rulesync projection이 제공한다.

## 단계

### Phase 1 — Minimal PoC

대상은 기존 fixture가 충분히 풍부한 Skill 하나로 제한한다. 우선 후보는 `mols-rpi`다.

범위:

- 대표 positive trigger case
- representative negative trigger case
- behavior 또는 orchestration case
- 가능하면 adversarial case

PoC에서는 전체 fixture coverage를 목표로 하지 않는다.

검증할 질문:

- 현재 JSON fixture를 중복 없이 읽을 수 있는가?
- Promptfoo adapter가 작은가?
- 결과가 사람이 원인을 추적할 수 있는 형태인가?
- framework-specific semantics가 fixture에 역류하지 않는가?

### Phase 2 — Eval Normalization Boundary

현재 fixture의 다양한 shape를 하나의 내부 case representation으로 정규화한다.

예상 입력:

- `cases[]`
- `evals[]`
- raw trigger list

정규화 계층은 최소한 다음 정보만 공통화한다.

- case identifier
- input/prompt
- mode 또는 category
- expected behavior / assertions
- optional environment or fixture data

처음부터 repository-wide schema migration을 하지 않는다. 실제 반복되는 공통 contract가 확인될 때만 canonical schema 통합을 별도 결정한다.

### Phase 3 — Runtime Adapter

Promptfoo provider 자체를 repository runtime abstraction으로 사용하지 않는다.

필요한 runtime은 얇은 adapter 뒤에 둔다.

예:

```text
Promptfoo
    ↓
runtime adapter
├─ native CLI
├─ local model
├─ HTTP endpoint
└─ API provider
```

초기에는 하나의 실제 runtime만 지원한다.

추가 runtime은 다음 조건이 있을 때만 확장한다.

- target-specific behavior를 비교할 실제 필요가 있음
- regression 또는 portability risk가 확인됨
- 유지보수 비용보다 얻는 검증 가치가 큼

### Phase 4 — Grader Separation

grader는 가능한 가장 싼 증거부터 선택한다.

| 계약 | 기본 grader |
| --- | --- |
| exact field / label / exit code | deterministic |
| file mutation / prohibited action | deterministic |
| structured output contract | deterministic / schema |
| semantic behavior | model rubric |
| ambiguous policy judgment | human 또는 explicit review |

Model grader를 deterministic contract의 대체재로 사용하지 않는다.

초기 model grader는 local model을 우선 검토하고, API grader는 품질 차이가 실제로 문제일 때만 추가한다.

### Phase 5 — Rulesync Projection Evaluation

PoC가 안정화된 뒤 실제 target surface를 대상으로 검증한다.

흐름:

1. canonical asset 준비
1. temporary workspace 생성
1. Rulesync target projection
1. Promptfoo가 runtime adapter를 통해 target runtime 실행
1. target runtime이 projection된 usage surface를 소비
1. Promptfoo가 결과 평가
1. temporary output 폐기

이 단계에서 처음으로 projection parity와 runtime parity를 함께 관찰한다.

Target-specific exception은 실제 차이가 증명된 경우에만 fixture metadata 또는 별도 compatibility layer로 표현한다.

### Phase 6 — Automation

초기 자동화는 local/manual 실행을 기본으로 한다.

권장 순서:

1. local developer command
1. manual workflow 또는 explicit eval job
1. selected smoke eval
1. 필요하면 scheduled/full regression

Stochastic model eval은 초기에 PR blocking gate로 만들지 않는다.

Merge-critical contract는 가능한 deterministic test로 승격하고, stochastic eval은 behavior confidence와 regression 탐지에 사용한다.

## Repository Integration 원칙

### Source Layout

기존 경계를 유지한다.

```text
evals/                  behavioral contract
 tests/                  deterministic verification
 scripts/                repository execution adapter when justified
 src/rulesync/.rulesync/ canonical agent assets
```

Promptfoo 때문에 deployable Skill package 안에 eval 전용 파일을 넣지 않는다.

### Configuration

Promptfoo-specific config는 가능한 작게 유지한다.

Config가 다음 내용을 소유하지 않게 한다.

- Skill behavior definition
- target compatibility policy
- canonical assertion wording
- reusable asset metadata

이 정보는 기존 repository authority에 남긴다.

### Results

결과는 기본적으로 generated artifact다.

필요한 경우에만 다음 정보가 포함된 evidence artifact로 승격한다.

- asset revision
- fixture revision
- runtime/target
- model/runtime configuration
- trial count
- grader type
- pass/fail/score
- material failure evidence

Raw trace와 sensitive payload는 지속 보존하지 않는다.

## Security / Privacy Defaults

초기 도입에서 다음을 기본값으로 한다.

- Promptfoo telemetry 비활성화
- cloud sharing/sync 비활성화
- untrusted custom provider 실행 금지
- secrets를 fixture 또는 result에 기록하지 않음
- runtime credential은 repository에 저장하지 않음

Promptfoo configuration과 custom provider는 trusted code로 취급한다.

## 단계별 Gate

### Gate A — PoC 적합성

통과 조건:

- 기존 fixture를 직접 재사용
- adapter가 최소 구조로 유지됨
- 결과가 재현·해석 가능
- Promptfoo 제거 가능성이 보존됨

실패 시:

- Promptfoo 도입 중단
- fixture는 그대로 유지
- pytest/custom runner 대안 재평가

### Gate B — Runtime 가치

통과 조건:

- static/deterministic validation으로 잡지 못하는 실제 behavior defect를 탐지하거나
- portability/runtime parity에 의미 있는 evidence를 제공함

실패 시:

- runtime eval 범위를 확대하지 않음
- Promptfoo를 optional local tool로 제한하거나 제거

### Gate C — Automation 가치

통과 조건:

- 실행 안정성이 충분함
- 비용과 latency가 수용 가능함
- false positive/negative가 admission workflow를 해치지 않음

실패 시:

- manual 또는 scheduled eval로 유지
- merge gate에 편입하지 않음

## 초기 작업 단위

첫 implementation은 다음 정도로 제한한다.

1. Promptfoo dependency 또는 reproducible invocation 결정
1. telemetry/cloud-off 기본값 정의
1. `mols-rpi` fixture 일부를 읽는 normalizer 작성
1. 하나의 runtime adapter 연결
1. deterministic + semantic grader 각각 최소 하나 적용
1. local 실행 command 제공
1. generated result 저장 정책 확인
1. PoC 결과를 기준으로 다음 gate 판단

## 성공 지표

정량 KPI를 먼저 발명하지 않는다.

초기에는 다음 질적 지표로 충분하다.

- 새 behavior regression을 실제로 잡는가?
- fixture duplication이 생기지 않는가?
- failure 원인 추적이 쉬운가?
- runtime 추가가 adapter 수준에서 끝나는가?
- Promptfoo 없이도 repository semantics가 온전한가?
- 실행 비용 때문에 검증을 회피하게 되지 않는가?

## 후속 결정

PoC 이후 별도로 판단한다.

- canonical eval schema 통합 여부
- 어떤 runtime을 reference target으로 둘지 여부
- local model grader의 품질 충분성
- multi-trial 기본 횟수
- nightly/full eval 필요성
- PR smoke eval 필요성
- result retention 및 trend reporting 필요성

이 결정들을 이번 도입의 선행 조건으로 만들지 않는다.

## 권장 실행 순서

**PoC → normalization → single runtime → grader separation → Rulesync target projection → automation** 순으로 진행한다.

가장 중요한 제약은 단순하다.

> Promptfoo를 도입하되, Promptfoo가 repository의 eval 의미를 소유하게 만들지 않는다.
