# Common Review

Skill, Rule, Subagent에 공통으로 적용되는 semantic review를 다룬다. 자산 유형 고유의 failure mode는 각 유형의 `review.md`가 소유한다.

## Review axes

요청된 behavior와 maintenance boundary에 실제 영향을 줄 수 있는 축만 본다.

- **Responsibility** — representation 이름이 아니라 실제 semantic responsibility가 명확하고 한 owner에 귀속되는가?
- **Scope** — 적용 여부를 structural scope와 semantic scope 중 더 자연스러운 mechanism이 결정하는가?
- **Authority** — canonical source, target behavior, project delta, asset-local requirement가 섞이지 않았는가?
- **Granularity** — 분리된 surface마다 독립적인 applicability, loading, reuse 또는 ownership 가치가 있는가? 거의 항상 함께 쓰이는 책임을 불필요하게 쪼개지 않았는가?
- **Routing cost** — router, index, entrypoint, reference chain이 실제로 후보와 context를 좁히는가, 아니면 탐색 단계와 failure point만 늘리는가?
- **Context cost** — required context가 duplicated, stale, unreachable하거나 항상 불필요하게 로드되지 않는가? 항상 필요한 authority가 optional routing 뒤에 숨지 않았는가?
- **Core and delta** — reusable core와 local/target customization이 분리되어 있고 전체 asset fork나 hidden configuration으로 drift를 만들지 않는가?
- **Options** — public argument나 mode가 caller가 실제 제어할 가치가 있는 선택인가? default, auto, omission semantics가 숨은 behavior를 만들지 않는가?
- **Structure** — filesystem naming과 placement가 orientation을 돕되 framework convention이나 올바른 cohesion을 왜곡하지 않는가?
- **Regression** — 기존의 valid behavior, intended scope, local delta와 supported target assumptions을 보존했는가?
- **Failure visibility** — uncertainty, unavailable capability, unresolved state 또는 unsupported compatibility를 성공처럼 숨기지 않는가?

## Findings

Material finding은 concrete defect, ambiguity, unnecessary cost, unsupported claim 또는 regression risk를 식별해야 한다.

- 반복 symptom보다 root cause를 우선한다.
- 변경으로 생긴 defect와 scope 밖의 pre-existing issue를 구분한다.
- 파일 수, 계층 수, option 수처럼 숫자 자체를 finding으로 만들지 않는다. 실제 discovery, loading, ownership, correctness 또는 maintenance 비용과 연결한다.
- 형식을 채우기 위해 finding을 만들지 않는다.
- 현재 evidence로 안전하게 판단할 수 없는 behavior는 추측으로 해결하지 않는다.

Static review는 semantic·structural concern을 판단할 수 있지만 runtime selection, application, delegation, parity 또는 compatibility를 증명하지 않는다.
