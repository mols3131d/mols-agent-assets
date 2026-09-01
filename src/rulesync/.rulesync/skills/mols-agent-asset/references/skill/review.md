# Skill Review

Agent Skill review에만 필요한 축을 다룬다. 공통 review 기준은 `../common/review.md`를 따른다.

## Review axes

- **Fit** — task intent에 따라 선택할 coherent capability인가? 구조만으로 적용 가능한 지침을 불필요하게 Skill routing에 맡기지 않았는가?
- **Responsibility** — representation이 아니라 semantic responsibility 기준으로 하나의 owner에 응집되어 있는가?
- **Activation** — intended request는 후보가 될 수 있고 realistic near-miss는 구분되는가?
- **Description** — coarse discovery에 필요한 정보가 metadata에 있으며 구현 상세 catalog로 비대하지 않은가?
- **Local routing** — entrypoint가 실제 applicability와 필요한 next context를 좁히는가? metadata 판단을 장황하게 반복하지 않는가?
- **Progressive disclosure** — 항상 로드되는 context는 모든 activation에 필요한가? conditional resource는 필요 시 직접 발견 가능한가? 분리 자체보다 loading benefit이 분명한가?
- **Granularity** — reference와 supporting surface마다 독립 loading, reuse 또는 ownership 가치가 있는가? 거의 항상 함께 읽는 내용이 과도하게 분리되지 않았는가?
- **Variants** — target/mode별 fork가 reusable core를 복제하지 않는가? public argument는 caller가 의미 있게 선택할 behavior만 노출하고 omission/default/auto semantics가 명확한가?
- **Instruction precision** — failure cost에 비해 과도하게 제한하거나 반대로 중요한 경계를 빠뜨리지 않았는가?
- **Package** — reference, script, output asset이 각각 실제 loading/runtime benefit을 갖고 자연스러운 package surface에 있는가?
- **Authority** — portable intent, source representation, target behavior, local delta가 섞이지 않았는가?
- **Regression** — 기존 책임, valid behavior, 계속 지원되는 target assumption을 훼손하지 않았는가?

항상 적용되어야 하는 project authority나 safety boundary가 Skill selection 실패로 누락될 수 있는 구조는 finding이다.

Static review로 runtime trigger precision, behavioral parity, target compatibility를 확정하지 않는다.
