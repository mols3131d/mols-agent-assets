---
description: Agent Asset의 behavioral evaluation을 설계·실행·해석하고 deterministic test, runtime evidence, regression contract를 구분할 때 사용하는 repository-local policy입니다.
---

# Evaluation

Evaluation은 deterministic correctness만으로 충분히 판단하기 어려운 **Agent Asset의 behavior와 품질**을 평가합니다.

`evals/`가 behavioral contract를 소유합니다. Promptfoo 같은 도구는 contract의 authority가 아니라 실행·채점 backend입니다.

## Test와 Eval

- deterministic correctness를 기계적으로 판정할 수 있으면 `tests/`에서 검증합니다.
- trigger 선택, instruction following, semantic quality, adversarial behavior, runtime/model 차이처럼 실행 결과를 평가해야 하면 `evals/`를 사용합니다.
- 같은 계약을 deterministic assertion으로 표현할 수 있다면 model grader보다 deterministic 검증을 우선합니다.
- runtime을 실제로 실행하지 않았다면 runtime behavior가 통과했다고 주장하지 않습니다.

## Ownership

- canonical Agent Asset → `src/rulesync/.rulesync/`
- deterministic verification → `tests/`
- behavioral contract와 fixture → `evals/`
- tool-specific eval config → `evals/promptfoo/`
- adapter와 runner → `scripts/evals/`
- Promptfoo 자체의 사용법과 upstream authority → [Promptfoo](../references/tooling/promptfoo.md)

`evals/` 내부 layout과 fixture ownership은 [`evals/README.md`](../../evals/README.md)가 소유합니다.

## Eval을 추가할 때

다음 중 하나가 실제로 필요할 때 eval을 추가합니다.

- Agent Asset이 올바른 상황에서 선택되거나 동작하는지 확인
- 요구한 behavior와 금지한 behavior를 구분
- adversarial 또는 ambiguous input에서 중요한 boundary 확인
- model이나 runtime이 달라져도 핵심 behavior가 유지되는지 비교
- 반복해서 발견된 failure를 regression contract로 남김

단순히 case 수를 늘리기 위해 fixture를 추가하지 않습니다. 새 case는 보호하려는 behavior나 failure mode가 분명해야 합니다.

## Evidence

Eval 결과는 증거의 강도를 구분해서 해석합니다.

1. **Deterministic evidence** — 동일 입력에서 안정적으로 판정 가능한 contract. 필요한 경우 merge-blocking verification으로 사용할 수 있습니다.
2. **Runtime behavioral evidence** — 실제 model/runtime을 실행해 관찰한 결과. 실행 환경과 asset revision을 함께 봅니다.
3. **Stochastic/model-graded evidence** — model 생성이나 grader 변동성이 있는 결과. 기본적으로 단일 PASS/FAIL을 merge admission으로 사용하지 않습니다.

반복 가능한 failure pattern이 확인되면 원인을 Asset, fixture, runtime/provider, grader로 분리합니다. 안정적인 contract로 만들 수 있을 때만 deterministic regression 또는 blocking eval로 승격합니다.

## Eval Design

- 먼저 보호할 behavior와 실패 조건을 명시합니다.
- 최소한의 representative case와 필요한 adversarial case만 둡니다.
- 문자열 일치보다 의미가 중요한 계약을 억지 deterministic regression으로 고정하지 않습니다.
- model grader가 필요하면 rubric은 판정할 behavior만 설명하고 구현 세부를 재정의하지 않습니다.
- stochastic comparison은 필요하면 여러 trial을 사용하고 model/runtime, fixture, asset revision을 함께 기록합니다.
- generated result는 기본적으로 disposable evidence로 취급합니다. durable decision이나 regression contract가 생겼을 때만 canonical surface에 반영합니다.

## Promptfoo

Promptfoo는 현재 behavioral eval 실행 backend입니다. Repository-owned fixture를 Promptfoo 전용 contract로 복제하지 않습니다.

Fixture-mode smoke는 provider/generator/assertion plumbing을 검증하는 deterministic check이며 runtime behavior evidence가 아닙니다. 실제 local-model eval과 semantic grading은 기본적으로 비차단 evidence입니다.

현재 `mols-rpi` eval surface는 다음 entrypoint를 제공합니다.

```bash
mise exec -- npm run eval:promptfoo:mols-rpi:smoke
mise exec -- npm run eval:promptfoo:mols-rpi
```

Local-model eval에는 기본적으로 Ollama를 사용합니다. 필요한 model 준비와 provider override는 실행 환경에서 명시적으로 관리합니다.

- `PROMPTFOO_RUNTIME_MODEL` — 실행 대상 model
- `PROMPTFOO_GRADER_PROVIDER` — semantic grader provider
- `OLLAMA_BASE_URL` — Ollama endpoint

Promptfoo-specific config와 adapter의 실제 구현은 `evals/promptfoo/`와 `scripts/evals/`가 소유합니다. PR Gate에서 eval surface를 어떻게 blocking verification으로 연결하는지는 [Testing](testing.md)이 소유합니다.

## Review

Eval 변경을 검토할 때 다음을 확인합니다.

- 이 case가 실제 behavior 또는 failure mode를 보호하는가?
- deterministic test로 더 싸고 안정적으로 검증할 수 없는가?
- fixture가 특정 model/provider의 우연한 표현에 과적합되지 않았는가?
- grader가 contract보다 더 넓은 품질 기준을 임의로 만들고 있지 않은가?
- 결과의 증거 수준보다 강한 결론을 주장하고 있지 않은가?
