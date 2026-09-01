# Common Review

공통 리뷰는 자산 유형과 무관한 설계 품질만 본다. 유형별 failure mode는 각 `review.md`가 소유한다.

## Review axes

- **Responsibility** — 실제 책임과 owner가 명확한가?
- **Applicability** — 적용 범위를 가장 직접적인 mechanism으로 표현했는가?
- **Authority** — canonical source, target behavior, local delta가 섞이지 않았는가?
- **Granularity** — 분리된 surface마다 독립적인 적용, loading, reuse, ownership 가치가 있는가?
- **Context** — routing/reference가 context를 실제로 좁히며 stale·중복·불필요한 context가 없는가?
- **Core and delta** — reusable core를 전체 fork나 hidden configuration으로 반복하지 않는가?
- **Options** — caller가 의미 있게 선택할 값만 노출하고 기본·자동·생략 semantics가 분명한가?
- **Structure** — naming과 placement가 탐색을 돕되 자연스러운 구조를 왜곡하지 않는가?
- **Regression** — 기존의 유효한 behavior, scope, local delta를 보존했는가?
- **Failure visibility** — unknown, unavailable capability, unsupported compatibility를 성공처럼 숨기지 않는가?

## Findings

Finding은 구체적인 defect, ambiguity, unnecessary cost, unsupported claim, regression risk에 연결한다. 반복 symptom보다 root cause를 우선하고, 숫자나 형식을 맞추기 위해 finding을 만들지 않는다.

정적 리뷰로 runtime selection, application, delegation, parity, compatibility를 증명하지 않는다.
