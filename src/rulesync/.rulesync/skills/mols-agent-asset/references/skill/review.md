# Skill Review

Skill 리뷰는 선택 경계와 loading 효율을 중심으로 본다. 공통 기준은 `../common/review.md`를 따른다.

## Review axes

- **Fit** — task intent에 따라 선택할 capability인가? 구조만으로 적용 가능한 지침을 불필요하게 Skill routing에 맡기지 않았는가?
- **Responsibility** — 하나의 선택 단위로 응집된 책임인가?
- **Activation** — intended request는 후보가 되고 realistic near-miss는 구분되는가?
- **Routing** — metadata는 coarse discovery에 집중하고, entrypoint는 실제 applicability와 다음 context를 좁히는가?
- **Context** — 항상 로드되는 내용은 매 activation에 필요한가? conditional detail은 필요할 때 직접 발견 가능한가?
- **Granularity** — reference마다 독립 loading/reuse 가치가 있으며, 거의 항상 함께 읽는 내용을 과도하게 쪼개지 않았는가?
- **Variants** — target/mode별 fork가 core를 복제하지 않는가? public option은 의미 있는 선택만 노출하는가?
- **Package** — instruction, reference, script, output asset이 각자의 역할과 실제 benefit을 갖는가?
- **Authority** — portable intent, source representation, target behavior, local delta가 섞이지 않았는가?
- **Regression** — 기존 책임과 유효한 behavior를 보존했는가?

항상 적용되어야 하는 authority나 safety boundary가 Skill selection 실패로 누락될 수 있으면 finding이다. 정적 리뷰로 runtime trigger precision, behavioral parity, target compatibility를 확정하지 않는다.
