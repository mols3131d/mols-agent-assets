# Common Review

공통 리뷰는 자산 유형과 무관한 품질과 경계를 탐색한다. 유형별 failure mode는 각 `review.md`가 소유한다. 이미 정해진 계약의 준수 여부만 판정하려면 Validation을 사용한다.

## Review axes

- **Responsibility** — 실제 책임과 owner가 명확한가?
- **Applicability** — 적용 범위를 가장 직접적인 mechanism으로 표현했는가?
- **Authority** — canonical source, target behavior, local delta가 섞이지 않았는가?
- **Granularity** — 분리된 surface마다 독립적인 적용, loading, reuse, ownership 가치가 있는가?
- **Context** — routing/reference가 context를 실제로 좁히며 stale·중복·불필요한 context가 없는가?
- **Core and delta** — reusable core를 불필요한 fork나 중복으로 반복하지 않는가?
- **Structure** — naming과 placement가 탐색을 돕되 자연스러운 구조를 왜곡하지 않는가?
- **Instruction cost** — material failure를 방지하지 않는 과도한 절차·조건이 판단을 방해하지 않는가?
- **Context noise** — 항상 로드되는 저관련성 자산, 중복·stale context, signal dilution이 없는가?
- **Stability** — 실패, 이름·경로·override 변화에서 핵심 contract와 복구 경계가 유지되는가?
- **Human comprehension** — 목적, trigger, owner, 근거, 예외와 변경 영향을 과도한 해석 없이 파악할 수 있는가?
- **Regression** — 기존의 유효한 behavior, scope, local delta를 보존했는가?
- **Failure visibility** — unknown, unavailable capability, unsupported compatibility를 성공처럼 숨기지 않는가?

길이, 규칙 수, 파일 수만으로 instruction bottleneck이나 context noise를 판정하지 않는다. Human comprehension finding도 문체 취향이 아니라 잘못된 변경, 느린 검토, ownership 혼란 같은 실제 비용과 연결한다.

## Multiple perspectives

다관점 검토가 materially useful하고 환경이 지원하면 필요한 reviewer만 선택한다.

- `agents/quality.agent.md` — correctness, clarity, consistency, maintainability
- `agents/routing.agent.md` — trigger, routing, delegation, tool selection
- `agents/efficiency.agent.md` — instruction/context bottleneck, stability, comprehension
- `agents/adversarial.agent.md` — bypass, conflicting instruction, malformed or hostile case
- `agents/orchestration.agent.md` — agent boundary, handoff, ownership, termination

Reviewer는 candidate finding과 unknown을 반환하고 최종 deduplication, severity, disposition은 lead가 소유한다. Independent execution을 지원하지 않으면 auto 선택에서는 관점을 순차 분리하고 shared-context limitation을 남길 수 있지만, 사용자가 독립 실행을 명시적으로 요구했다면 독립인 것처럼 대체하지 않는다.

## Findings

Finding은 구체적인 defect, ambiguity, unnecessary cost, unsupported claim, regression risk에 연결한다. 반복 symptom보다 root cause를 우선하고, 숫자나 형식을 맞추기 위해 finding을 만들지 않는다.

정적 리뷰로 runtime selection, application, delegation, parity, compatibility를 증명하지 않는다.
