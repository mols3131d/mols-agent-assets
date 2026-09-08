---
description: mols-review-dualvantage family의 목적, 본질, 역할 분리와 유지보수 원칙을 판단할 때 사용합니다.
---

# Mols Review DualVantage

`mols-review-dualvantage`는 하나의 관점이 놓치기 쉬운 문제와 하나의 검토 방식이 만드는 편향을 줄이기 위해, **서로 다른 두 review vantage를 독립적으로 만든 뒤 별도의 meta-review에서 근거와 수정 가치를 판정하는 review family**다.

이 문서는 실행 prompt를 복제하지 않는다. 각 subagent의 구체적인 tool, target, output 형식과 runtime 동작은 대응하는 Agent Asset이 소유한다. 여기서는 family를 유지보수할 때 보존해야 할 목적, 본질과 책임 경계만 정의한다.

## 목적

DualVantage의 목적은 reviewer 수를 늘리는 것이 아니라 **서로 다른 실패 모드를 가진 검토 관점을 분리하고, 그 결과를 evidence gate를 통과한 최종 판단으로 압축하는 것**이다.

단일 reviewer는 같은 context와 reasoning path 안에서 초기 해석에 고정되기 쉽다. 반대로 여러 reviewer를 단순히 추가하면 중복 탐색, speculative finding, coordination cost가 커질 수 있다. DualVantage는 이 둘 사이에서 다음 구조를 취한다.

```text
                    mols-review-dualvantage
                         meta-review
                             │
              same bounded review brief
                 ┌───────────┴───────────┐
                 ▼                       ▼
          verifier vantage       challenger vantage
          evidence-first         challenge-first
                 │                       │
                 └───────────┬───────────┘
                             ▼
                  validate / reconcile
                             ▼
                     final assessment
```

핵심은 **parallel specialist discovery → evidence-gated adjudication → final assessment**다.

## 본질

### 두 개의 관점, 하나의 판정

`dual`은 agent가 단순히 두 개라는 뜻이 아니다. 같은 대상을 서로 다른 질문으로 바라보는 두 개의 독립적인 vantage를 뜻한다.

- Verifier는 "실제로 입증할 수 있는 material defect가 있는가"를 묻는다.
- Challenger는 "현재 설명이나 구현이 의존하는 전제를 깨는 reachable counterexample이 있는가"를 묻는다.
- Root reviewer는 "이 candidate를 최종 finding으로 주장할 만큼 근거와 수정 가치가 있는가"를 묻는다.

세 역할은 같은 일을 강도만 달리해서 반복하지 않는다.

### Discovery와 judgment를 분리한다

Verifier와 Challenger의 출력은 finding이 아니라 **candidate claim**이다. Specialist가 자신이 찾은 문제의 최종 유효성까지 결정하면 discovery bias와 confirmation bias가 그대로 최종 결과에 들어갈 수 있다.

Root reviewer는 candidate의 scope, evidence, reasoning, reachability, attribution, counter-evidence, materiality와 duplication을 검토한다. 이 단계는 새 결함을 찾는 세 번째 full review가 아니다.

### 합의보다 근거를 우선한다

두 specialist가 같은 결론에 도달해도 그것 자체는 evidence가 아니다. 반대로 두 specialist가 다른 결론을 내렸다는 이유만으로 어느 쪽도 약해지지 않는다.

최종 판정은 reviewer 수나 합의율이 아니라 **observable evidence와 applicable contract가 claim을 얼마나 지지하는지**에 의해 결정한다.

### 독립성은 관점 다양성을 위한 장치다

Verifier와 Challenger는 가능하면 같은 bounded brief에서 독립적으로 시작한다. 한 specialist의 결론이나 speculation을 다른 specialist에게 미리 전달하지 않는다.

독립성의 목적은 secrecy가 아니라 anchoring과 path dependence를 줄이는 것이다. 두 specialist가 같은 hidden reasoning path를 공유하면 역할 이름만 달라도 DualVantage의 핵심 이점은 사라진다.

## 역할 경계

### `mols-review-dualvantage`

Family의 root reviewer이자 meta-review owner다.

소유하는 책임:

- bounded review brief와 scope
- 두 specialist의 독립 delegation
- candidate claim validation
- reviewer 간 conflict reconciliation
- materiality와 fix-worthiness 판단
- duplicate/root-cause consolidation
- final assessment

소유하지 않는 책임:

- verifier가 놓친 correctness bug를 새로 탐색하는 것
- challenger가 놓친 failure scenario를 새로 발명하는 것
- 전체 artifact를 세 번째로 다시 review하는 것

Coverage가 부족하면 직접 메우기보다 coverage gap으로 드러내는 것이 기본이다.

### `mols-review-dualvantage-verifier`

Evidence-first, precision-oriented specialist다.

핵심 책임은 source, contract, test, configuration, current state와 필요한 focused validation에서 **실제로 뒷받침되는 material correctness claim**을 만드는 것이다.

Verifier는 "가능성이 있다"보다 "무엇을 관찰했고, 그 evidence가 어떤 reachable defect를 지지하는가"를 우선한다.

### `mols-review-dualvantage-challenger`

Challenge-first, recall-oriented specialist다.

핵심 책임은 hidden assumption, boundary condition, retry/recovery, stale state, ordering, compatibility와 같은 surface에서 **검증 가능한 reachable failure hypothesis**를 만드는 것이다.

Challenger는 speculative risk list를 만드는 역할이 아니다. 각 hypothesis는 existing defense를 고려하고, caller가 반박하거나 확인할 수 있는 falsification target을 가져야 한다.

## 유지보수 원칙

### 1. 역할 차이는 질문의 차이여야 한다

Verifier와 Challenger가 같은 checklist를 다른 문구로 수행하기 시작하면 둘 중 하나를 분리할 이유가 약해진다. 두 역할은 탐색 질문과 실패 모드가 실제로 달라야 한다.

### 2. Root reviewer를 더 강한 세 번째 reviewer로 만들지 않는다

Root reviewer의 품질은 더 많이 탐색하는 데서 나오지 않는다. 이미 나온 candidate를 더 엄격하게 검증하고 불필요한 claim을 버리는 데서 나온다.

새 defect hunting이 필요하다면 specialist 책임을 개선하거나 별도의 명시적 review surface로 다룬다.

### 3. Candidate claim은 evidence가 아니다

Subagent output 자체를 사실 근거로 인용하지 않는다. Claim을 최종 finding으로 올리려면 underlying source, contract, runtime state 또는 validation evidence를 확인한다.

### 4. Materiality를 correctness와 분리해 판단한다

기술적으로 사실인 지적이 모두 수정 요구가 되는 것은 아니다. 최종 finding은 실제 correctness, reliability, security, compatibility 또는 운영 판단에 의미 있는 영향을 가져야 한다.

낮은 영향이지만 참고 가치가 있는 사실은 note가 될 수 있다. 근거가 약해서 확정할 수 없는 claim을 note로 보존하지 않는다.

### 5. 기본 workflow는 single-pass다

동일 specialist를 반복 호출해 토론시키거나 refinement loop를 만드는 것을 기본 동작으로 삼지 않는다. Disposable subagent runtime에서는 재호출마다 context 전달과 coordination 비용이 다시 발생한다.

기본값은 각 specialist의 독립 1회 탐색과 root reviewer의 1회 adjudication이다. 추가 pass는 실제로 별도 가치가 확인될 때만 명시적으로 도입한다.

### 6. 병렬성보다 독립성이 먼저다

Runtime이 병렬 execution을 지원하면 두 specialist를 병렬로 실행하는 것이 효율적이다. 그러나 DualVantage의 본질은 wall-clock parallelism이 아니라 **independent perspective**다.

Runtime이 병렬 execution을 제공하지 않는다면 병렬로 수행했다고 주장하지 않는다. 순차 실행에서도 한 specialist의 결과를 다른 specialist의 brief에 섞지 않아 관점 독립성을 보존할 수 있다.

### 7. Tool 권한은 역할에 맞춘다

Verifier는 evidence를 확인하기 위해 focused validation capability가 필요할 수 있다. Challenger는 기본적으로 read/search만으로 hypothesis를 만들고, 실행이나 mutation을 통해 공격을 수행하는 역할이 아니다.

Root reviewer는 meta-review에 필요한 read/search와 delegation만 가져야 하며 implementation이나 broad execution capability를 갖는 이유가 없다.

### 8. 출력량보다 signal density를 우선한다

각 specialist가 많은 candidate를 내는 것이 목표가 아니다. 같은 root cause를 여러 항목으로 나누거나 low-confidence possibility를 늘리면 root reviewer의 비용과 false-positive pressure가 증가한다.

Material candidate가 없으면 없다고 반환할 수 있어야 한다.

## 최종 판정의 의미

Root reviewer는 내부적으로 candidate를 다음처럼 다룬다.

- `ACCEPT` — 근거, 추론, reachability/attribution과 materiality가 충분한 최종 finding
- `NOTE` — 기술적으로 유효하지만 material finding으로 올릴 정도는 아닌 참고 사항
- `DROP` — 틀렸거나, 근거가 부족하거나, unreachable/out-of-scope이거나, 실제 수정 가치가 없는 candidate
- `MERGE` — 다른 candidate와 같은 root cause 또는 같은 수정으로 해결되는 중복

외부 assessment의 기본 surface는 `ACCEPT`된 findings와 실제 참고 가치가 있는 notes다. `DROP`과 `MERGE`는 review 과정의 내부 판단이며 기본적으로 노출할 필요가 없다.

## 성공 기준

DualVantage가 잘 작동한다는 것은 reviewer가 많은 finding을 생성했다는 뜻이 아니다. 다음이 더 중요한 기준이다.

- 두 specialist가 실제로 다른 failure mode를 탐색한다.
- final finding이 underlying evidence로 독립 검증 가능하다.
- speculative 또는 low-value claim이 meta-review에서 제거된다.
- reviewer agreement를 correctness proof로 사용하지 않는다.
- 중요한 conflict는 evidence와 contract로 해소된다.
- specialist가 다루지 못한 영역은 coverage gap으로 정직하게 남는다.
- 최종 결과가 caller가 실제로 수정하거나 판단해야 할 문제에 집중한다.

## 변경할 때 보존할 것

Model, vendor, tool 이름, runtime API와 output schema는 바뀔 수 있다. 다음은 구현이 바뀌어도 보존해야 할 family의 핵심이다.

1. 서로 다른 두 review vantage를 분리한다.
2. 두 vantage의 discovery를 가능한 한 독립적으로 유지한다.
3. specialist output을 candidate claim으로 취급한다.
4. 최종 판단은 별도의 evidence gate가 소유한다.
5. evidence gate는 새 full review가 아니라 validation과 materiality 판단에 집중한다.
6. majority vote나 reviewer agreement를 evidence로 사용하지 않는다.
7. false-positive suppression과 actionable signal을 finding 수보다 우선한다.

이 조건이 사라지면 파일 이름이나 agent 수가 유지되어도 더 이상 DualVantage라고 보기 어렵다.
