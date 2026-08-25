# Patterns

이 디렉토리는 이 repository의 reusable pattern library를 `catalog/`에서 찾기 위한 entrypoint입니다.

Pattern의 본문과 category 구조는 [`docs/references/patterns/`](../../docs/references/patterns/)가 canonical source입니다. 이 디렉토리는 pattern 내용을 복제하거나 별도의 authority를 만들지 않습니다.

## Categories

- [`context-engineering`](../../docs/references/patterns/context-engineering/) — Agent Asset, instruction, routing, discovery와 scoped context 설계
- [`documentation`](../../docs/references/patterns/documentation/) — 개발·기술 문서와 durable documentation 구조
- [`workflow`](../../docs/references/patterns/workflow/) — agentic work의 실행 흐름, working artifact와 handoff/lifecycle surface
- [`software-engineering`](../../docs/references/patterns/software-engineering/) — repository/code 구조, architecture, implementation, testing과 reliability

새 pattern의 작성과 기존 pattern의 수정은 canonical source에서 수행합니다. Catalog는 재사용할 pattern을 발견하기 위한 얕은 진입점만 소유합니다.
