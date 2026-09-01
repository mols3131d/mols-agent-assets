# Skill Review

Agent Skill review에만 필요한 축을 다룬다. 공통 review 기준은 `../common/review.md`를 따른다.

## Review axes

- **Responsibility** — capability가 하나의 coherent owner로 묶여 있는가?
- **Activation** — intended request는 선택될 수 있고 realistic near-miss는 구분되는가?
- **Description** — selection 전에 필요한 정보가 metadata에 있으며 구현 상세 catalog로 비대하지 않은가?
- **Progressive disclosure** — 항상 로드되는 context는 모든 activation에 필요한가? conditional resource는 직접 발견 가능한가?
- **Instruction precision** — failure cost에 비해 과도하게 제한하거나 반대로 중요한 경계를 빠뜨리지 않았는가?
- **Package** — reference, script, output asset이 각각 실제 loading/runtime benefit을 갖는가?
- **Authority** — portable intent, source representation, target behavior, local delta가 섞이지 않았는가?
- **Regression** — 기존 책임, 유효 behavior, 계속 지원되는 target assumption을 훼손하지 않았는가?

Static review로 runtime trigger precision, behavioral parity, target compatibility를 확정하지 않는다.
