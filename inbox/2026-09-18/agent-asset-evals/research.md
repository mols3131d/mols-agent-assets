# Agent Asset별 Eval 보강 조사 보고서

- 조사일: 2026-09-18
- 범위: `src/rulesync/.rulesync/skills/`, `src/rulesync/.rulesync/subagents/`, `evals/skills/`, `evals/subagents/`
- 목적: 각 Skill과 Subagent에 대해 behavioral eval을 어떤 순서와 계약으로 보강할지 결정
- 상태: 조사 결과. 구현·canonical policy 변경 아님.

## 결론

현재 eval은 핵심 일부 자산에 집중되어 있다. canonical source 기준 Skill 26종 중 7종만 fixture를 보유하고, Subagent 9종 중 `mols-review-dualvantage` family만 fixture를 보유한다. fixture case는 Skill 218건, Subagent 9건이다.

따라서 다음 단계는 모든 자산에 동일한 수의 case를 기계적으로 추가하는 것이 아니다. 각 자산의 책임을 먼저 분류하고, 아래 공통 계약을 자산별로 최소 구현하는 방식이 적절하다.

1. 모든 routed Skill: positive, negative, near-miss routing을 우선 보강한다.
2. 행동이 중요한 Skill: 선택 이후의 observable outcome, 금지 행동, scope와 evidence handling을 behavior eval로 보강한다.
3. context/selector Skill: discovery boundary, authority, freshness, no-match, mutation boundary를 우선 평가한다.
4. orchestration Skill: dependency composition, phase/termination, handoff, non-interference를 평가한다.
5. renderer/tool-specific Skill: 결과물 구조와 의미 보존을 deterministic outcome으로 평가하고, 실제 runtime 품질은 별도 evidence로 둔다.
6. Subagent: direct invocation보다 delegation, ownership, handoff, bounded invocation, failure/termination을 중심으로 평가한다.
7. native-runtime eval은 먼저 `mols-loops` prototype을 공통 adapter와 assertion의 기준선으로 삼고, 이후 자산군별로 확장한다.

## 조사 근거

Repository evaluation policy는 다음 경계를 둔다.

- behavioral claim은 `evals/`가 소유한다.
- source/schema/generated artifact correctness는 `tests/`가 소유한다.
- Promptfoo는 contract owner가 아니라 실행·채점 backend다.
- runtime을 실제 실행하지 않았으면 runtime behavior가 검증됐다고 주장하지 않는다.
- outcome을 먼저 평가하고, trajectory는 필수 gate·authority·side effect·handoff처럼 중간 행동 자체가 계약일 때만 평가한다.
- capability와 regression을 구분한다. 불안정한 model judgment를 이름만 regression으로 바꾸지 않는다.

현재 공통 fixture validator는 JSON 유효성 중심이다. Subagent validator는 `version`, `contract`, `system_under_evaluation`, case `id/mode/prompt/assertions`를 확인하지만, Skill fixture에 대해서는 동일한 최소 contract 검사가 상대적으로 약하다. 이는 새 fixture를 늘리기 전에 스키마·메타데이터의 공통성을 먼저 검토해야 함을 뜻한다.

## 현재 커버리지

### Skills

| 상태 | 자산 |
| --- | --- |
| fixture 있음 | `caveman-ko`, `mols-agent-asset`, `mols-agent-asset-find`, `mols-clarify-code`, `mols-code-comprehension-refactor`, `mols-loops`, `mols-text-optimizer` |
| fixture 없음 | `artifact-consistency-inspector`, `coding-context`, `github-context`, `guidance-context`, `mols-agent-asset-validator`, `mols-chatbot-bootstrap`, `mols-ci-design`, `mols-clarify-runtime`, `mols-coding-context`, `mols-coding-context-python`, `mols-dialectic`, `mols-documentation`, `mols-markdown-dashboard`, `mols-markdown-maintenance`, `mols-mermaid-chart`, `mols-mermaid-diagram`, `mols-openspec-customize`, `mols-tach`, `news-table`, `notion-context`, `searcher`, `technical-document-fidelity`, `text-humanize-korean` |

기존 fixture 규모:

- `caveman-ko`: trigger 18, behavior 14
- `mols-agent-asset`: 28
- `mols-agent-asset-find`: 17
- `mols-clarify-code`: 17
- `mols-code-comprehension-refactor`: 16
- `mols-loops`: 71
- `mols-text-optimizer`: trigger 20, behavior 17

합계 218 case.

### Subagents

| 상태 | 자산 |
| --- | --- |
| fixture 있음 | `mols-review-dualvantage` family fixture 1개. `mols-review-dualvantage`, `mols-review-dualvantage-verifier`, `mols-review-dualvantage-challenger`의 협력 계약을 함께 평가 |
| fixture 없음 | `mols-dialectic-antithesis`, `mols-dialectic-synthesis`, `mols-dialectic-thesis`, `review-adversarial`, `review-lead`, `review-quality` 및 나머지 `mols-review-dualvantage` family specialist는 별도 fixture 없음 |

Subagent fixture는 총 9 case다. 현재 구조는 individual subagent보다 family/system contract를 평가하는 방향이며, 이 방향 자체는 적절하다. 다만 family 내 specialist와 caller가 어떤 claim을 각각 소유하는지 더 명시할 필요가 있다.

## 자산군별 평가 모델

### 1. 일반 routing/context Skill

대상 예:

- `coding-context`
- `github-context`
- `guidance-context`
- `mols-coding-context`
- `mols-coding-context-python`
- `mols-chatbot-bootstrap`
- `searcher`
- `notion-context`

필수 routing family:

- 명확한 positive
- 인접 책임의 negative
- 이름·키워드만 같은 near-miss
- 명시적 source/runtime 조건이 있는 conditional positive
- no-match 또는 source boundary 제한

필수 behavior family:

- 필요한 context만 로드
- 불충분한 context를 추측하지 않음
- stale·missing·ambiguous evidence를 limitation으로 유지
- target/source/runtime authority를 혼동하지 않음
- 수행하지 않은 조회·검증·변경을 주장하지 않음

우선순위: 높음. 이 자산들은 다른 Skill과의 조합에서 잘못 선택되면 이후 모든 결과가 오염되므로 routing precision이 먼저다.

### 2. Agent Asset authoring/validation Skill

대상:

- `mols-agent-asset`
- `mols-agent-asset-find`
- `mols-agent-asset-validator`
- `artifact-consistency-inspector`

이미 `mols-agent-asset`과 `mols-agent-asset-find` fixture가 있어 기준선이 있다. 보강 방향은 case 수 증가보다 sibling boundary다.

필수 routing:

- authoring vs finding/install vs validation 분리
- direct name mention이 scope bypass가 되지 않음
- no-match가 자동 authoring으로 변하지 않음
- Rulesync source와 fallback discovery의 우선순위

필수 behavior:

- canonical source와 generated projection 구분
- asset identity 불확실성에서 overwrite·merge 금지
- target mutation의 durable/temporary 차이 보존
- authority, provenance, evidence와 user request scope 보존
- validator가 판정할 수 있는 repository correctness와 behavioral eval을 중복하지 않음

우선순위: 최상. 이 자산군은 다른 eval fixture와 자산 배포 자체를 생산·검증하므로 평가가 약하면 eval 체계도 오염된다.

### 3. Workflow/orchestration Skill

대상:

- `mols-loops`
- `mols-dialectic`
- `mols-ci-design`
- `mols-clarify-runtime`

`mols-loops`는 71 case와 native-runtime prototype이 있으므로 기준선이다. 나머지는 다음 축으로 보강한다.

- 단계 순서와 required gate
- material change·scope change 시 refresh/reopen
- terminal condition과 exhaustion
- recursive authority/scope 제한
- independent perspective, reconcile와 unresolved 유지
- plan/research/review/implementation의 ownership 분리
- 실행하지 않은 stage, parallelism, evidence를 주장하지 않음

`mols-dialectic`은 debate가 아니라 thesis·antithesis·synthesis의 역할 충실성과 evidence-based transformation을 평가해야 한다. `mols-ci-design`은 local→branch→PR→deferred evidence 경계, admission과 non-blocking evidence를 평가해야 한다.

우선순위: 최상~높음. workflow Skill은 단순 문장 품질보다 중간 상태와 종료 조건이 계약이므로 trajectory assertion을 제한적으로 사용할 가치가 높다.

### 4. 문서·텍스트 변환 Skill

대상:

- `caveman-ko`
- `mols-text-optimizer`
- `mols-clarify-code`
- `mols-documentation`
- `technical-document-fidelity`
- `text-humanize-korean`

기존 `caveman-ko`, `mols-text-optimizer`, `mols-clarify-code` fixture를 기준으로 다음을 보강한다.

- 요청된 변환만 수행하고 다른 작업을 하지 않음
- 의미, 부정, 조건, 수치, identifier, code, URL, 구조 보존
- style overlay와 content/behavior change 분리
- 특정 형식, exact output, Markdown 구조 보존
- 변환 불가·불확실성에서 과장하지 않음
- specific domain owner가 있으면 generic optimizer가 선점하지 않음

이 자산군의 semantic quality는 model/human rubric이 필요할 수 있지만, 보존해야 할 literal·구조는 deterministic checker로 분리하는 것이 좋다. 문자열 전체 일치를 regression으로 고정하지 않는다.

우선순위: 높음. 이미 일부 fixture가 있으므로 sibling routing과 protected-content behavior를 확장하기 쉽다.

### 5. 결과물·도구·다이어그램 Skill

대상:

- `mols-markdown-dashboard`
- `mols-markdown-maintenance`
- `mols-mermaid-chart`
- `mols-mermaid-diagram`
- `mols-tach`
- `mols-openspec-customize`
- `news-table`

필수 behavior:

- 입력 값·단위·순서·범위 보존
- 적절한 output type 선택
- chart와 diagram, dashboard와 일반 status report의 경계 유지
- canonical source와 generated projection 구분
- renderer/schema/native validator를 우회하지 않음
- 확인하지 않은 상태·최신성·정량 결과를 주장하지 않음

가능한 deterministic outcome:

- Markdown/YAML/JSON schema validity
- rendered artifact 존재와 structural invariants
- Mermaid syntax 또는 domain-specific validation
- dashboard numerator/denominator 합계
- Tach configuration과 observed graph의 구분

우선순위: 중간~높음. output artifact가 observable하면 model grader보다 구조 검사를 우선하고, semantic usefulness만 별도 rubric으로 둔다.

### 6. 외부·현재성·컨텍스트 Skill

대상:

- `searcher`
- `news-table`
- `notion-context`
- `github-context`
- `technical-document-fidelity`

필수 routing:

- current/niche/contested fact에서 검색
- user-provided text transformation에서는 불필요한 검색 금지
- named target은 lookup 후 live context 재확인
- news curation과 evidence acquisition 분리

필수 behavior:

- source attribution과 freshness 보존
- 검색 결과를 authority로 승격하지 않음
- pagination/truncation/permission을 absence로 해석하지 않음
- citation과 claim의 범위를 맞춤
- 읽지 않은 source, 실행하지 않은 lookup을 주장하지 않음

우선순위: 높음. 최신성·권한·외부 source 경계는 hallucination과 false confidence를 직접 만든다.

## Subagent 평가 모델

Subagent는 individual text quality보다 invocation context 안의 system contract를 평가한다. 각 fixture는 다음 중 하나를 system under evaluation으로 명시한다.

- caller + specialist family
- lead + verifier/challenger
- thesis + antithesis + synthesis
- review lead + quality/adversarial reviewer

공통 case family:

1. delegation ownership — caller가 필요한 context만 전달하고 worker가 자체 탐색을 소유하는가
2. independence — sibling 결과가 초기 context를 오염시키지 않는가
3. concurrency/fallback — 가능한 경우 같은 wave에서 호출하고, 불가능하면 병렬이라고 주장하지 않는가
4. invocation budget — timeout·empty result도 호출 1회로 소비하는가
5. evidence adjudication — reviewer vote/confidence보다 source·state·reachability를 우선하는가
6. no-finding — quota를 채우려고 약한 finding을 만들지 않는가
7. handoff — confirmed/rejected/unresolved와 coverage limitation을 caller가 쓸 수 있게 전달하는가
8. termination — caller lifecycle, retry, mutation과 worker responsibility를 침범하지 않는가

`mols-review-dualvantage` fixture의 9 case는 위 축을 이미 일부 구현한다. 다음 보강은 `review-lead` family와 `mols-dialectic` family를 별도 fixture로 추가하는 것이 가장 자연스럽다.

## 우선순위 로드맵

### P0: 측정 기반과 최상위 경계

대상:

- `mols-agent-asset`
- `mols-agent-asset-find`
- `mols-agent-asset-validator`
- `mols-loops`
- `mols-review-dualvantage` family

작업:

- 기존 fixture의 schema/metadata를 최소 공통 계약으로 정리
- routing/behavior 또는 delegation/handoff를 명시적으로 분리
- `mols-loops` native-runtime lane을 공통 runner 기준선으로 확정
- source, target, runtime, model, fixture revision을 evidence metadata로 기록

완료 기준:

- 각 P0 family에 positive/negative/near-miss 또는 ownership/failure/termination case 존재
- fixture-mode와 runtime evidence가 구분됨
- deterministic outcome과 semantic rubric이 섞이지 않음

### P1: 재사용도가 높은 context·workflow·텍스트 자산

대상:

- `coding-context`
- `mols-coding-context`
- `mols-coding-context-python`
- `mols-clarify-runtime`
- `mols-dialectic`
- `caveman-ko`
- `mols-text-optimizer`
- `mols-clarify-code`
- `mols-documentation`
- `technical-document-fidelity`
- `text-humanize-korean`

작업:

- sibling boundary를 중심으로 routing fixture 추가
- protected content와 no-overreach behavior 추가
- semantic rubric은 최소 criterion 단위로 분리

### P2: artifact/tool/domain-specific 자산

대상:

- `artifact-consistency-inspector`
- `mols-ci-design`
- `mols-markdown-dashboard`
- `mols-markdown-maintenance`
- `mols-mermaid-chart`
- `mols-mermaid-diagram`
- `mols-openspec-customize`
- `mols-tach`
- `news-table`
- `notion-context`
- `searcher`
- `github-context`
- `mols-chatbot-bootstrap`
- `guidance-context`

작업:

- deterministic artifact/state grader부터 설계
- 외부 service 또는 current runtime dependency는 local capability fixture와 실제 runtime evidence를 분리
- chart/diagram, dashboard/status, search/curation, source/context ownership의 near-miss를 우선 추가

## Fixture 설계 제안

현재 fixture 형식은 자산별로 이미 약간 다르다. `cases.json`, `trigger-evals.json`, `behavior-evals.json`을 즉시 하나로 통합하기보다 다음 공통 필드를 점진적으로 맞추는 편이 안전하다.

```json
{
  "version": 1,
  "contract": "capability",
  "system_under_evaluation": ["skill-name"],
  "cases": [
    {
      "id": "stable-case-id",
      "mode": "activation | activation-negative | behavior | ...",
      "prompt": "...",
      "assertions": ["..."],
      "expected_selection": {
        "selected_skills": ["skill-name"],
        "primary_skill": "skill-name"
      },
      "evidence": {
        "grader": "deterministic | rubric | trajectory",
        "purpose": "capability | regression"
      }
    }
  ]
}
```

주의:

- `assertions`는 hidden requirement가 아니라 사용자 요청과 observable contract를 표현해야 한다.
- `expected_selection`은 routing case에서만 사용한다.
- `system_under_evaluation`은 model/runtime/harness까지 필요하면 metadata에 조건을 추가한다.
- trajectory assertion은 필수 gate, authority, side effect, handoff처럼 경로 자체가 계약일 때만 사용한다.
- source 내용을 prompt에 불필요하게 복제해 contamination을 만들지 않는다.

## Native-runtime 확장 순서

1. 기존 contract lane을 baseline으로 고정한다.
2. `mols-loops` native smoke로 provider metadata와 `skill-used`/`not-skill-used` 연결을 검증한다.
3. 같은 evaluator를 사용해 `mols-agent-asset` / `mols-agent-asset-find` sibling routing을 native lane에 추가한다.
4. `mols-review-dualvantage`와 `mols-dialectic`은 skill invocation만으로 충분하지 않으므로 delegation trace와 handoff output을 별도 관찰한다.
5. artifact-producing Skill은 workspace snapshot 또는 generated artifact를 deterministic grader가 읽는 형태로 확장한다.
6. 반복 trial이 필요한 경우 3회 정도의 fresh run으로 variability를 확인하되, trial 수를 quality quota로 취급하지 않는다.

## 산출물과 후속 구현 단위

이번 조사 후 바로 추가할 구현 단위는 다음과 같다.

1. Skill fixture 공통 validator 보강: `version`, cases, unique id, mode별 required fields, contract metadata.
2. asset family matrix를 fixture metadata 또는 별도 report로 유지하되, generated projection과 canonical source를 혼동하지 않는다.
3. `mols-agent-asset` / `mols-agent-asset-find` native routing config 추가.
4. `mols-dialectic` family fixture 추가.
5. `review-lead` / `review-quality` / `review-adversarial` family fixture 추가.
6. artifact-producing Skill은 각자의 deterministic checker가 준비된 뒤 fixture를 추가한다.
7. 각 family에서 안정된 capability case만 regression으로 승격한다.

## 리스크와 미확인 사항

- 일부 Skill은 runtime/tool/외부 service 의존성이 커서 local fixture만으로 실제 품질을 증명할 수 없다.
- Subagent의 독립성·병렬성은 runtime capability가 제공하지 않으면 평가 결과로 주장할 수 없다.
- model grader를 모든 자산에 적용하면 grader drift와 비용이 커진다. deterministic outcome을 먼저 찾아야 한다.
- 26개 Skill과 9개 Subagent를 한 번에 채우면 fixture 품질보다 수량 최적화가 되기 쉽다.
- 현재 working tree의 `.frontmatter/database/pinnedItemsDb.json`, `.frontmatter/database/taxonomyDb.json` 수정은 본 조사와 무관하며 보존했다.

## 최종 판단

`evals/skills`와 `evals/subagents`의 보강은 필요하다. 그러나 목표는 asset count와 fixture count의 일대일 대응이 아니다. 먼저 자산의 ownership boundary를 측정할 수 있는 최소 case를 만들고, 실제 failure와 runtime evidence가 쌓이는 자산만 capability에서 regression으로 승격해야 한다.

첫 구현 순서는 다음이 가장 합리적이다.

1. `mols-agent-asset` ↔ `mols-agent-asset-find` sibling routing native eval
2. `mols-dialectic` specialist family delegation/transform eval
3. `review-lead` family delegation/independence/handoff eval
4. context·text Skill의 protected-content와 no-overreach eval
5. artifact/tool-specific Skill의 deterministic artifact eval
