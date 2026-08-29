# `mols-clarify-runtime` 고도화 RPI Review

`mols-clarify-runtime`을 **logging 중심의 runtime clarification**에서 **실제 runtime behavior를 최소 비용으로 이해하고, 필요한 경우에만 future evidence를 개선하는 Skill**로 고도화한 RPI 결과다.

이 문서는 Research와 Plan을 반복해서 검증한 Review artifact다.

- Research: [`mols-clarify-runtime-enhancement-research.md`](mols-clarify-runtime-enhancement-research.md)
- Plan: [`mols-clarify-runtime-enhancement-plan.md`](mols-clarify-runtime-enhancement-plan.md)
- Canonical Skill: `src/rulesync/.rulesync/skills/mols-clarify-runtime/`

## 결론

최종 설계는 다음 순서로 수렴했다.

```text
복원 질문 하나
    ↓
이미 남은 runtime evidence 재사용
    ↓
여전히 gap이 있는가?
    ├─ No → 현재 이해만 필요하면 stop
    │
    └─ Yes
        ↓
안전하고 허가된 가장 작은 기존 scenario 실행
        ↓
현재 이해만 필요한가?
    ├─ Yes → stop
    │
    └─ No / future evidence 요청
        ↓
가장 작은 future runtime evidence 개선
        ↓
같은 좁은 scenario로 behavior + reconstructability 재검증
```

Logging은 이 흐름의 기본값이 아니다. Result, exception, state delta, artifact, framework history, existing trace/coverage와 test execution도 runtime 이해에 사용하는 evidence다.

## Skill 분리 결정

별도 `mols-understand-runtime` Skill은 만들지 않았다.

### 유지한 이유

- 기존 `mols-clarify-runtime`의 책임 자체가 runtime understanding debt다.
- observation-only와 future evidence improvement는 `관찰 → 필요성 판정 → 개선 → 재관찰`이라는 하나의 lifecycle이다.
- 두 Skill로 분리하면 trigger가 겹친다.
- 한 작업 안에서 observation 결과에 따라 evidence 개선 필요성이 결정되므로 handoff가 새로 생긴다.
- 별도 Skill이 소유할 독립 authority, runtime capability 또는 deployment surface가 없다.

### 분리를 다시 검토할 조건

다음과 같은 실제 usage evidence가 생길 때만 재검토한다.

- observation-only 요청과 evidence-improvement 요청이 반복적으로 서로 다른 routing을 요구한다.
- 두 작업이 서로 다른 tool/permission/safety contract를 가진다.
- observation context가 너무 커서 current Skill의 activation 비용을 실질적으로 높인다.
- 독립 Skill로 분리했을 때 명확한 loading 또는 runtime benefit이 측정된다.

현재는 분리보다 하나의 owner 안에서 progressive disclosure를 사용하는 편이 KISS와 DRY에 맞다.

## 최종 package

```text
mols-clarify-runtime/
├── SKILL.md
└── references/
    ├── diagnosis.md
    ├── observation.md
    ├── evidence.md
    ├── correlation.md
    ├── logging.md
    └── validation.md
```

### 새 reference가 필요한 이유

`observation.md`
: 실제 execution을 이해하는 경우에만 필요한 test/command, result, state delta, artifact, history, coverage/trace 해석을 조건부로 소유한다. Core Skill에 넣으면 대부분의 activation에서 불필요한 context가 된다.

`correlation.md`
: retry, async, batch, fan-out/fan-in, cross-process relation에서만 필요한 logical operation/attempt와 causality를 소유한다. 일반 synchronous runtime clarification에 항상 로드할 이유가 없다.

### 추가 분리를 하지 않은 이유

`evidence.md`의 owner selection과 viability는 같은 decision에서 함께 필요하다. Sampling/retention만 별도 reference로 분리하면 한 evidence 선택을 위해 두 파일을 오가게 된다.

Security, metrics, tracing도 별도 reference로 만들지 않았다. 이 Skill은 각 domain의 구현법을 소유하지 않고 runtime clarification과의 boundary만 필요하다.

## RPI Loop

### Loop 1 — Research / responsibility

**Question**
: 현재 문제는 logging 개선인가, 더 일반적인 runtime comprehension인가?

**Evidence**
: 기존 Skill, OpenTelemetry, workflow execution history, provenance/lineage, Whyline, dynamic slicing, 최신 Agent trace 연구를 비교했다.

**Finding**
: logging은 evidence surface 하나일 뿐이며 result, exception, artifact, state delta, history, trace와 executable test도 runtime understanding에 직접 기여한다.

**Disposition**
: `observe before instrument`를 핵심 방향으로 채택했다.

**Evidence level**: `verified` for source inspection, `inferred` for design synthesis.

---

### Loop 2 — Initial observation-first design

**Question**
: 기존 test를 runtime observation으로 사용할 수 있는가?

**Finding**
: 새 test를 설계하는 것과 기존 test를 executable scenario로 사용하는 것은 책임이 다르다. Existing fixture, parameter, result와 failure report는 실제 scenario의 context를 제공한다.

**Disposition**
: `observation.md`를 추가하고 existing test, command, result, exception, state delta, artifact, native history, existing trace/coverage를 observation surface로 포함했다.

**Boundary**
: 새 test 설계와 correctness 판단은 testing/debugging 책임으로 유지했다.

**Evidence level**: `verified` for package change, `inferred` for behavior contract.

---

### Loop 3 — Current observation vs future evidence

**Question**
: 현재 한 번 이해할 evidence와 앞으로 계속 남길 evidence를 같은 것으로 취급하고 있지 않은가?

**Finding**
: 초기안은 current observation이 부족하면 곧바로 persistent change로 넘어갈 위험이 있었다.

**Disposition**
: 현재 조사에서 사용하는 observation evidence와 future execution에 유지할 runtime evidence를 구분했다. Existing evidence로 현재 질문이 풀리면 source change 없이 stop할 수 있게 했다.

**Evidence level**: `verified`.

---

### Loop 4 — No-op와 명시 요청

**Question**
: 현재 observation만으로 이해할 수 있다는 이유로 사용자의 “앞으로 로그를 남겨 달라”는 요청까지 무시할 수 있는가?

**Finding**
: 절대적인 no-op 규칙은 explicit maintained-evidence request와 충돌할 수 있었다.

**Disposition**
: 사용자가 future logging, metadata, result context 같은 유지되는 surface를 명시하면 current observation sufficiency만으로 요청을 종료하지 않게 했다.

**Evidence level**: `simulated` → bounded correction `verified` by source inspection.

---

### Loop 5 — Observation scope / overclaim

**Question**
: 한 test/run에서 관찰한 behavior를 전체 프로그램 behavior처럼 일반화할 수 있는가?

**Finding**
: 아니다. 특히 mock, stub, fake, synthetic dependency를 사용한 test는 그 대체 경계에서의 실제 execution만 보여준다.

**Disposition**
: input, environment, runtime version, concurrency 조건을 넘는 일반화를 금지했다. Mocked scenario에서 production external behavior를 추론하지 않게 했다.

**Evidence level**: `simulated` → source correction `verified`.

---

### Loop 6 — Causality / retry / async

**Question**
: 하나의 execution ID만 있으면 retry와 async flow를 충분히 이해할 수 있는가?

**Finding**
: logical operation, individual attempt, parent-child, trigger/caused-by와 link 관계를 구분해야 하는 경우가 있다. Timestamp만으로 causality를 결정할 수 없다.

**Disposition**
: `correlation.md`를 추가했다. Existing native relation을 우선하고 universal `operation_id` schema는 만들지 않았다.

**Evidence level**: `inferred` from current tracing/workflow semantics; package change `verified`.

---

### Loop 7 — Evidence viability / boundary

**Question**
: 의미상 올바른 evidence owner를 고르면 충분한가?

**Finding**
: 아니다. Sampling, filtering, truncation, retention, access와 drop 때문에 semantic owner가 실제 reconstruction에는 unavailable할 수 있다.

**Disposition**
: `Generated`, `Available`, `Complete enough`, `Durable enough`, `Correlatable`, `Trustworthy enough`를 viability check로 추가했다.

추가 boundary:

- sampled/best-effort telemetry를 반드시 복원되어야 하는 사실의 sole owner로 두지 않는다.
- metric은 per-execution reconstruction용 identifier storage로 사용하지 않는다.
- audit/security/compliance evidence는 일반 duplicate/noise 규칙으로 삭제하지 않는다.

**Evidence level**: `inferred` from authoritative telemetry/security semantics; source change `verified`.

---

### Loop 8 — Explicit surface / logging behavior

**Question**
: 사용자가 “logging을 추가해 달라”고 했는데 result가 더 좋은 owner라는 이유로 logging을 몰래 없애도 되는가?

**Finding**
: specific surface request는 요청 제약이다. Method-agnostic 요청과 다르게 취급해야 한다.

**Disposition**
: explicit logging이면 logging surface를 유지하되 detailed result/history를 복제하지 않고 boundary event, outcome 또는 stable link만 최소 projection하도록 보정했다.

Logging 자체도 다음으로 고도화했다.

- stable event semantics
- `action / outcome / reason`은 optional semantic frame
- structured logging은 JSON 여부보다 stable field meaning
- handled retry/rejection/cancellation을 무조건 ERROR로 승격하지 않음
- native span/event가 있으면 중복하지 않음

**Evidence level**: `simulated` → source correction `verified`.

---

### Loop 9 — Execution safety / re-execution cost

**Question**
: runtime 이해를 위해 항상 실제 command/request를 다시 실행해야 하는가?

**Finding**
: 아니다. 기존 result/history/artifact/trace가 현재 revision과 질문에 충분하면 재실행은 불필요한 비용과 위험이다. 또한 가장 작은 command가 destructive하거나 external consequence를 가질 수도 있다.

**Disposition**
: 최종 순서를 `existing evidence reuse → gap일 때만 smallest safe execution`으로 바꿨다.

Safety boundary:

- observation은 실행 권한을 새로 만들지 않는다.
- destructive/irreversible/external action을 관찰 목적만으로 실행하지 않는다.
- source temporary probe는 caller-visible output, external state와 domain behavior를 바꾸지 않아야 하며 timing/concurrency risk도 낮아야 한다.

**Evidence level**: `simulated` → source correction `verified`.

---

### Loop 10 — Split / context-noise / saturation

**Question**
: 더 많은 Skill 또는 reference로 분리하면 품질이 좋아지는가?

**Review axes**
: Responsibility, routing, progressive disclosure, instruction bottleneck, context noise, human comprehension debt, DRY, package integrity.

**Result**
: 추가 분리는 기각했다.

- `observation.md`와 `correlation.md`는 조건부 loading benefit이 명확하다.
- `evidence.md`의 owner와 viability는 함께 판단해야 하므로 분리 이득이 없다.
- `logging.md`는 logging 요청일 때만 읽는 기존 독립 owner를 유지한다.
- Validation에 중복되어 있던 coverage/trace 설명은 Observation reference로 환원했다.
- always-loaded `SKILL.md`에서 새로 만든 `maintained runtime evidence` 용어를 제거하고 평이한 “future execution에 유지할 runtime evidence”로 단순화했다.

새 P1/P2 finding이 나오지 않았고 이후 추가 분리는 context navigation cost만 늘리는 것으로 판단해 saturation으로 종료했다.

**Evidence level**: `verified` for package/source structure, `simulated` for routing behavior.

## Adversarial Scenario Matrix

| Scenario | Expected behavior | Result |
| --- | --- | --- |
| 기존 result/history만으로 질문에 답할 수 있다 | 재실행·logging 추가 없이 stop | ✅ Simulated pass |
| 기존 evidence는 충분하지만 사용자가 future logging을 명시했다 | logging 제약을 유지하고 최소 projection 선택 | ✅ Simulated pass |
| failing test를 관찰했다 | failure evidence만 넘기고 defect 수정은 debugging/review로 route | ✅ Simulated pass |
| 하나의 passing test만 있다 | 전체 input space로 일반화하지 않음 | ✅ Simulated pass |
| mock external service를 사용하는 test | mock boundary에서의 behavior만 주장 | ✅ Simulated pass |
| coverage에 branch transition이 보인다 | path evidence로만 사용하고 reason/correctness를 추론하지 않음 | ✅ Simulated pass |
| 한 logical operation에 retry 3회 | operation과 attempt를 구분 | ✅ Simulated pass |
| async fan-out/fan-in | parent 하나로 강제하지 않고 native causal/link relation 검토 | ✅ Simulated pass |
| sampled trace에 destructive action이 보인다 | trace를 sole durable owner로 두지 않음 | ✅ Simulated pass |
| audit log와 operational log가 같은 event를 기록 | audit/security contract 확인 없이 duplicate 삭제하지 않음 | ✅ Simulated pass |
| fixture/config/raw payload 전체를 기록하려 한다 | relevant bounded context만 남김 | ✅ Simulated pass |
| metric label에 request ID를 넣어 execution을 추적하려 한다 | monitoring/observability로 route; per-execution evidence owner 재선택 | ✅ Simulated pass |
| production-affecting command가 가장 작은 재현 경로다 | observation 명목으로 실행 권한을 가정하지 않음 | ✅ Simulated pass |
| temporary probe가 stdout contract 또는 external state를 바꾼다 | transient observation으로 사용하지 않음 | ✅ Simulated pass |
| 새 tracing/coverage framework가 있어야만 관찰할 수 있다 | clarification만을 위해 새 dependency를 도입하지 않음 | ✅ Simulated pass |

`Simulated pass`는 actual model/runtime trial을 실행했다는 뜻이 아니다. Current Skill contract에 scenario를 대입한 semantic/adversarial review다.

## Route / package integrity

- Canonical owner는 `src/rulesync/.rulesync/skills/mols-clarify-runtime/SKILL.md`다.
- `route/skills.jsonl`은 canonical `name`과 `description`의 derived projection으로 동기화했다.
- `observation.md`, `correlation.md`를 포함한 모든 Progressive Disclosure target이 package에 존재한다.
- `logging.md` → Evidence anchors, `validation.md` → Observation anchor와 package-local link를 교차 확인했다.
- Vendor-specific field, protocol 또는 concrete telemetry backend를 portable contract로 추가하지 않았다.

## 검증 상태

| Check | Status | Evidence level |
| --- | --- | --- |
| Repository/Skill source inspection | ✅ Pass | `verified` |
| Package references 존재 | ✅ Pass | `verified` |
| Derived route description sync | ✅ Pass | `verified` |
| Responsibility/routing review | ✅ Pass | `simulated` + source inspection |
| 15 adversarial scenarios | ✅ Pass | `simulated` |
| Skill split stress review | ✅ Keep one Skill | `inferred` + structure inspection |
| Repository-native `mise run generated-sync` | ⚪ Not run | connector 환경에서 local command execution 없음 |
| `mise run check` / `mise run test` | ⚪ Not run locally | GitHub PR Gate 결과를 별도로 확인 |
| Independent model/runtime trials | ⚪ Not run | 별도 executor 사용 안 함 |

## Remaining risks

### 🔵 Low — 실제 host routing은 아직 runtime trial이 아니다

Description과 negative boundary를 semantic review했지만 각 target runtime에서 실제 activation trial을 반복 실행하지 않았다.

### 🔵 Low — Runtime-specific evidence semantics는 upstream이 소유한다

Coverage, trace, test runner, workflow history가 실제 어떤 field와 retention을 제공하는지는 project/runtime마다 다르다. Skill이 이를 복제하지 않는 것이 의도된 설계다.

### 🔵 Low — Large references are conditional

`evidence.md`와 `observation.md`는 짧지 않지만 항상 로드되지 않는다. 줄 수만을 이유로 분리하면 owner selection과 observation judgment가 오히려 흩어진다. 반복 사용에서 실제 context bottleneck이 확인되면 다시 분리한다.

## Final acceptance

RPI의 핵심 목표는 달성됐다.

- ✅ Logging-first에서 evidence-first로 전환
- ✅ Existing runtime record 재사용 우선
- ✅ 필요할 때만 safe executable scenario 실행
- ✅ Existing tests를 runtime scenario로 활용하되 test design과 분리
- ✅ Result / exception / state delta / artifact / history / trace / coverage를 observation surface로 인정
- ✅ Why / Why-not, input/context, effect/outcome 복원 강화
- ✅ Retry/async causality 보강
- ✅ Evidence viability / budget / audit boundary 보강
- ✅ Explicit logging surface 요청 보존
- ✅ Single-run overclaim 방지
- ✅ Observation execution safety 보강
- ✅ Skill 분리 불필요 판정
- ✅ Progressive disclosure로 conditional detail 격리

새로운 근거가 현재 architecture나 behavior contract를 실질적으로 바꾸지 않는 상태에 도달했으므로 이번 RPI는 **saturation**으로 종료한다.
