# Promptfoo Eval 도입 제안서

## 결론

`Promptfoo`를 이 저장소의 **behavioral eval 실행 backend**로 도입한다.

단, Promptfoo를 eval schema나 behavioral contract의 authority로 만들지 않는다. Repository-owned eval fixture와 기대 동작은 계속 `evals/`가 소유하고, Promptfoo는 이를 실행·채점·비교하는 교체 가능한 도구로만 사용한다.

핵심 책임은 다음처럼 분리한다.

| 영역 | 책임 |
| --- | --- |
| Canonical Agent Assets | `src/rulesync/.rulesync/` |
| Projection | Rulesync |
| Behavioral Contract | `evals/` |
| Deterministic Verification | `tests/` |
| Runtime Eval Orchestration | Promptfoo |
| Target Runtime | Codex, Claude Code, local model 등 실제 executor |

## 배경

현재 저장소는 이미 eval의 위치와 증거 수준을 구분하고 있다.

- deterministic correctness는 `tests/`
- Skill trigger, behavior, adversarial fixture는 `evals/skills/<skill>/`
- cross-asset regression contract는 `evals/regression/`
- generated result는 기본적으로 일회성 artifact
- runtime을 실제로 실행하지 않은 경우 runtime pass를 주장하지 않음

따라서 필요한 것은 새로운 eval 체계를 발명하는 일이 아니라, 기존 fixture를 실제 모델과 runtime에 연결해 반복 실행할 수 있는 **runner와 grader layer**다.

## 제안

### Promptfoo의 역할

Promptfoo는 다음 기능만 소유한다.

- eval case 실행 orchestration
- provider/runtime adapter 호출
- deterministic 또는 model grader 실행
- trial 반복과 결과 집계
- local/manual/CI 환경에서 결과 출력

Promptfoo configuration에 repository의 핵심 behavioral semantics를 중복 작성하지 않는다.

### Canonical Fixture 유지

기존 `evals/**/*.json`을 그대로 repository-owned contract로 유지한다.

Promptfoo가 요구하는 형식은 runtime adapter 또는 generator가 투영한다.

```text
evals/**/*.json
      ↓
normalized eval case
      ↓
Promptfoo
      ↓
runtime adapter + grader
```

Promptfoo 제거 또는 교체 시 canonical fixture를 마이그레이션하지 않아도 되는 구조를 목표로 한다.

### Rulesync와의 관계

Rulesync는 build system이 아니라 **projection system**으로 본다.

```text
Canonical Asset
src/rulesync/.rulesync/
        ↓
Rulesync Projection
        ↓
Target Usage Surface
        ↓
Target Runtime

Behavioral Contract
     evals/
        ↓
Promptfoo
        ↓
Runtime Adapter
        ↓
Target Runtime
```

Target Runtime이 Rulesync projection을 실제로 소비하고, Promptfoo는 해당 runtime을 호출하고 결과를 평가한다.

Rulesync가 target surface로 정상 projection했다는 사실과 해당 runtime에서 behavior가 동일하다는 주장은 분리한다.

검증 계층은 다음과 같다.

1. source correctness
2. projection correctness
3. runtime behavior correctness

Promptfoo는 3번의 실행과 평가만 소유한다.

## 채택 이유

### Vendor Neutrality

Promptfoo는 여러 model/provider, local model, HTTP, Python, JavaScript, shell/custom provider를 지원한다.

따라서 특정 vendor SDK를 repository의 eval architecture에 고정하지 않고 실제 runtime을 black-box adapter로 연결할 수 있다.

### 기존 Fixture 재사용

Promptfoo는 외부 Python/JavaScript generator와 custom provider/assertion을 지원하므로 현재 `cases.json`, `trigger-evals.json`, `behavior-evals.json`을 Promptfoo 전용 YAML로 복제할 필요가 없다.

Repository-owned fixture를 한 번 normalize한 뒤 Promptfoo로 projection하는 얇은 adapter가 충분하다.

### 비용 제어

초기 도입은 API key를 필수 조건으로 하지 않는다.

가능한 실행 계층은 다음과 같다.

- deterministic assertion
- local model/Ollama grader
- subscription-authenticated native CLI
- 필요할 때만 API provider

즉 비용이 높은 runtime eval은 선택적으로 실행하고, 저비용 검증을 기본 경로로 유지할 수 있다.

### Multi-runtime Validation

동일한 canonical Skill과 eval fixture를 여러 Rulesync target projection에 적용해 runtime 차이를 비교할 수 있다.

이 구조는 특정 target에 맞춘 fixture 복제를 줄이고, projection parity와 runtime parity를 분리해서 판단할 수 있게 한다.

## 비목표

이번 도입은 다음을 목표로 하지 않는다.

- Promptfoo를 repository-wide test framework로 교체
- 기존 pytest 또는 Rulesync validation 대체
- 모든 eval fixture schema 즉시 통합
- 모든 PR에서 stochastic model eval 실행
- 특정 vendor runtime을 공식 기준 runtime으로 고정
- Promptfoo Cloud를 repository dependency로 도입
- runtime 결과를 곧바로 canonical knowledge로 보존

## 위험과 통제

### Framework Lock-in

**위험:** Promptfoo configuration에 behavioral semantics가 쌓이면 교체 비용이 커진다.

**통제:** `evals/`가 behavioral contract를 계속 소유하고 Promptfoo-specific logic은 adapter layer에 격리한다.

### Stochastic Gate

**위험:** model variability와 인증·quota·latency가 PR admission을 불안정하게 만들 수 있다.

**통제:** 초기에는 model eval을 merge-blocking gate로 사용하지 않는다. deterministic test와 fixture validation은 기존 merge gate를 유지한다.

### Security and Privacy

**위험:** custom provider와 assertion은 repository-local code execution 권한을 가진다. telemetry와 cloud 기능도 별도 통제가 필요하다.

**통제:** trusted repository code만 실행하고 telemetry/cloud sharing을 기본 비활성화한다. raw sensitive trace는 durable artifact로 보존하지 않는다.

### Target Drift

**위험:** target runtime 또는 Rulesync projection semantics가 바뀌면 과거 결과와 직접 비교하기 어려울 수 있다.

**통제:** runtime eval 결과에는 asset revision, target, model/runtime config, fixture version을 함께 기록한다.

## 도입 원칙

1. **Repository contract first** — Promptfoo보다 `evals/`가 우선한다.
2. **Projection before runtime claim** — 실제 target surface를 소비하는 runtime을 대상으로 평가한다.
3. **Deterministic before model grader** — 값싼 증거가 가능한 계약에 LLM judge를 사용하지 않는다.
4. **Portable by default** — target-specific fixture는 실제 차이가 증명된 경우에만 추가한다.
5. **Local/manual first** — stochastic eval은 안정성과 비용이 확인된 뒤 자동화 범위를 넓힌다.
6. **Disposable results** — generated result는 기본적으로 일회성으로 취급한다.
7. **Easy exit** — Promptfoo 제거 시 canonical assets와 fixture가 그대로 남아야 한다.

## 권고 결정

**도입한다.**

다만 첫 단계는 framework migration이 아니라 `mols-rpi` 같은 기존 Skill fixture 일부를 대상으로 한 최소 PoC로 제한한다.

PoC가 다음 조건을 만족할 때만 repository-level integration으로 승격한다.

- 기존 fixture를 중복 없이 재사용할 수 있음
- adapter가 작고 이해 가능함
- API key 없이 최소 한 개 runtime 또는 local model path가 동작함
- deterministic/model grader를 명확히 구분할 수 있음
- Promptfoo를 제거해도 `evals/` contract가 손상되지 않음

## 참고

- Promptfoo documentation: https://www.promptfoo.dev/docs/
- Custom providers: https://www.promptfoo.dev/docs/providers/custom-script/
- Ollama provider: https://www.promptfoo.dev/docs/providers/ollama/
- Python integration: https://www.promptfoo.dev/docs/integrations/python/
- Telemetry: https://www.promptfoo.dev/docs/configuration/telemetry/
- Rulesync documentation: https://rulesync.dyoshikawa.com/
