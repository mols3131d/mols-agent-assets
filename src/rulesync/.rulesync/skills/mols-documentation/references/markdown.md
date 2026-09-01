# Markdown

Markdown으로 문서를 표현할 때만 적용한다. 독자, 목적, 정보 구조와 내용 판단은 상위 `SKILL.md`가 소유하며 이 reference는 Markdown-specific 표현 선택과 source/rendered-view 주의점만 소유한다.

## Structure

- 독립 문서는 보통 하나의 `#` 제목에서 시작하되 대상 surface나 프로젝트가 다른 구조를 요구하면 그 규칙을 따른다.
- heading은 굵은 글씨로 흉내 내지 말고 실제 heading syntax를 사용한다. 깊이는 필요한 만큼만 사용하고 의미 없는 nesting을 만들지 않는다.
- 한 문단의 prose를 문장마다 수동 줄바꿈하지 않는다. renderer나 프로젝트 formatter가 소유하지 않는 임의 줄바꿈으로 읽기 흐름을 깨지 않는다.
- list는 같은 추상화 수준과 가능한 한 같은 문법 형태를 유지한다. 절차에는 순서 있는 list, 독립 항목에는 unordered list를 우선한다.
- table은 반복되는 속성이나 선택지처럼 열을 비교할 가치가 있을 때 사용한다. 긴 서술, 절차나 구조가 서로 다른 항목에는 section이나 list가 낫다.
- command, path, field, identifier와 짧은 code는 inline code로, 여러 줄 code나 그대로 복사해야 하는 내용은 fenced code block으로 표현한다.
- link text는 목적지를 예측할 수 있게 작성한다. URL 자체가 필요한 데이터가 아니면 문장 속에 긴 URL을 그대로 노출하지 않는다.

## Optional Elements

### Semantic Markers

상태, 위험, 행동과 category를 빠르게 구분할 필요가 있으면 [Semantic Markers](semantic-markers.md)를 읽는다. Emoji나 색상은 text label을 대체하지 않으며 장식으로 반복하지 않는다.

### Text Bars

완료율이나 소수 category의 단일 수치를 간단한 text visual로 표현할 가치가 있으면 [Text Bars](text-bars.md)를 읽는다.

### Tree Structures

파일, module, section이나 ownership처럼 하나의 parent를 갖는 hierarchy를 보여줄 때는 [Tree Structures](tree-structures.md)를 읽는다. 복잡한 관계나 여러 parent가 있는 구조를 tree로 억지로 표현하지 않는다.

### Callouts

대상 renderer가 callout syntax를 지원하고 핵심 안내, 팁, 경고나 주의사항을 본문에서 빠르게 구분할 가치가 있을 때만 사용한다. GitHub에서는 `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION` callout을 사용할 수 있다. 일반 section container로 남용하지 않는다.

### Footnotes

본문 흐름을 끊는 출처, 용어 설명, 예외와 부가 기술 설명에 사용한다. 핵심 결론, 필수 절차와 중요한 제약을 footnote에 숨기지 않는다. renderer가 footnote를 지원하지 않으면 짧은 `References` section이나 inline 설명을 사용한다.

## Visual Routing

| Information | Expression |
| --- | --- |
| 짧은 상태, 위험, 행동, category | Semantic marker |
| 반복되는 속성, 선택지, 변경 전후 | Markdown table |
| 현재값 / 전체값 또는 소수 category의 단일 수치 | Text bar |
| 단일 부모 hierarchy | Tree structure |
| 복잡한 관계, 흐름, 상태와 sequence | `mols-mermaid-diagram` |
| 정량 비교, 추세, 분포와 비율 | `mols-mermaid-chart` |
| 개발 현황, evidence, gap, risk와 next action의 통합 뷰 | `mols-markdown-dashboard` |

짧은 prose나 list가 더 빠르게 이해되면 visual을 추가하지 않는다. 전문 Skill이 선택되면 그 Skill의 문법과 의미 규칙을 이 reference에 복제하지 않는다.

## Source and Rendered View

- source에서만 예쁘고 rendered view에서 의미가 깨지는 표현을 피한다.
- 반대로 renderer-specific 기능이 독자 경험을 크게 개선하고 target이 명확하면 사용할 수 있지만 fallback 필요성을 판단한다.
- Markdown의 deterministic formatting, heading/link lint, frontmatter와 index mechanics는 `mols-markdown-maintenance`가 소유한다.
