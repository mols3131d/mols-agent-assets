---
description: repository-wide documentation principles를 재작성하기 위한 외부 조사 결과와 원칙·별도 문서·README 배치 계획입니다.
---

# Documentation Principles Research and Plan

이 문서는 `docs/documentation/principles.md`를 고도화하기 전에 조사한 내용을 보존하고, 발견한 원칙을 어디에 둘지 결정하기 위한 작업 계획입니다.

핵심 방향은 **repository-wide 판단 기준은 원칙 문서에, 독립적으로 탐색·유지할 구체 규칙은 별도 문서에, README는 scope-local한 작은 규칙의 예외적인 수용처로만 사용**하는 것입니다.

## Research Summary

외부 문서화 가이드에서 반복되는 공통점은 다음과 같습니다.

- 문서는 작성자가 설명하고 싶은 내용보다 **독자가 해결하려는 필요, 질문, 판단과 행동**에서 시작합니다.
- 문서와 section은 가능한 한 **명확한 주된 책임**을 가집니다. 별도 파일은 독립적으로 찾고 유지할 책임이 있을 때만 만듭니다.
- KISS는 무조건 짧게 쓰는 것이 아니라 **가장 작은 유효 scope를 선택하고 그 scope 안에서는 충분하고 정확하게 다루는 것**에 가깝습니다.
- 중요한 정보와 필요한 context를 먼저 제공하고, 세부 내용은 필요할 때 더 깊게 탐색하게 하는 **progressive disclosure**가 유효합니다.
- 의미의 authoritative source는 하나로 두되, 독자의 이해와 routing에 필요한 짧은 context까지 기계적으로 제거하지 않습니다.
- 오래된 문서는 누락된 문서보다 더 위험할 수 있으므로 **current truth와 maintainability**를 문서 품질의 일부로 봅니다.
- 좋은 내용도 찾을 수 없으면 가치가 낮으므로 **discoverability와 navigation**을 문서 품질로 봅니다.
- filesystem, search, generated projection 등에서 쉽게 복구할 수 있는 정보는 authored prose에 반복하지 않는 편이 drift와 유지 비용을 줄입니다.
- heading, paragraph, terminology, link text, accessibility 같은 scannability 규칙은 중요하지만 repository-wide 최상위 원칙과 구체 writing rule을 구분해야 합니다.

## Research Sources

| Source | 핵심 시사점 |
| --- | --- |
| Google Technical Writing — Audience | 독자의 기존 지식과 필요한 결과를 먼저 정의하고 그 gap을 문서가 채웁니다. |
| Google Technical Writing — Course Summary | scope와 핵심을 먼저 제시하고 명확한 heading, 한 문장 한 idea, 한 문단 한 topic을 권장합니다. |
| Microsoft Writing Style Guide — Scannable Content | 중요한 정보를 앞에 두고 chunking과 descriptive heading으로 빠른 탐색을 돕습니다. |
| Diátaxis — Foundations / Compass / Quality | 문서 구조를 작성 형식보다 user need에서 시작하고 서로 다른 목적의 documentation을 무리하게 섞지 않습니다. |
| Write the Docs — Documentation Principles | current, complete-within-scope, unique, discoverable, 가까운 source와 유지 가능성을 강조하며 필요한 반복은 허용합니다. |
| Write the Docs — Docs as Code | documentation도 version control, review와 검증 가능한 workflow 안에서 유지하는 것이 유리합니다. |
| GitLab Documentation Guidelines | topic responsibility, single source, 지속적 갱신, docs-as-code와 자동 검증을 강조합니다. |
| W3C Writing Tips | semantic heading, meaningful link text, 명확한 구조와 쉬운 표현이 탐색성과 접근성을 함께 높입니다. |

참고 URL:

- https://developers.google.com/tech-writing/one/audience
- https://developers.google.com/tech-writing/course-summaries/one
- https://learn.microsoft.com/en-us/style-guide/scannable-content/
- https://diataxis.fr/foundations/
- https://diataxis.fr/compass/
- https://diataxis.fr/quality/
- https://www.writethedocs.org/guide/writing/docs-principles/
- https://www.writethedocs.org/guide/docs-as-code/
- https://docs.gitlab.com/development/documentation/styleguide/
- https://docs.gitlab.com/development/documentation/topic_types/
- https://docs.gitlab.com/development/documentation/site_architecture/folder_structure/
- https://docs.gitlab.com/development/documentation/testing/
- https://www.w3.org/WAI/tips/writing/

## Placement Strategy

배치 우선순위는 다음과 같습니다.

1. repository 전체에 적용되는 durable 판단 기준이면 `principles.md`
1. 독립적으로 탐색·유지할 구체 책임이 있으면 별도 canonical document
1. 위 두 조건에 못 미치고 특정 scope의 entrypoint에서 함께 읽는 것이 더 자연스러운 작은 규칙만 README

README는 catch-all 문서로 사용하지 않습니다.

## 1. Principles Document

`docs/documentation/principles.md`에는 **구체적인 실행 방법이 아니라 repository-wide 판단 기준**만 둡니다.

현재 조사에서 원칙 후보는 다음과 같습니다.

1. **Reader need first** — 작성자의 설명 순서보다 독자의 질문·판단·행동에서 시작합니다.
1. **Clear responsibility** — 문서와 section은 명확한 주된 책임을 가지며, 책임 없는 문서를 관성적으로 만들지 않습니다.
1. **Smallest useful scope** — 가장 작은 유효 scope를 선택하되 선택한 scope 안에서는 충분하고 일관되게 다룹니다.
1. **Progressive disclosure** — 판단에 필요한 핵심과 context를 먼저 제공하고 세부는 필요에 따라 확장합니다.
1. **One authority, minimal repetition** — 같은 의미의 authority는 하나로 두되 이해와 routing에 필요한 짧은 context는 허용합니다.
1. **Current and trustworthy** — 문서는 현재 truth와 맞아야 하며 불확실하거나 오래된 내용을 확정적으로 유지하지 않습니다.
1. **Discoverable and navigable** — 필요한 독자가 올바른 문서를 발견·선택하고 다음 정보로 이동할 수 있어야 합니다.
1. **Maintainable by design** — 쉽게 재생성되거나 유지 가치가 낮은 정보를 authored documentation으로 만들지 않습니다.

현재 `principles.md`의 기존 원칙은 삭제 대상으로 보기보다 위 후보에 흡수·압축합니다.

- `필요한 문서만 둔다` → `Clear responsibility` / `Smallest useful scope`
- `가장 좁은 scope가 소유한다` → `Smallest useful scope` / authority
- `한 의미에는 한 authoritative owner` → `One authority, minimal repetition`
- `상위 원칙을 local에서 복제하지 않는다` → authority / scope
- `복구 가능한 inventory를 authored knowledge로 만들지 않는다` → `Maintainable by design`
- `반복되는 local rule은 승격을 검토한다` → responsibility / authority

원칙 문서에는 command, field schema, heading 규칙, 특정 filename의 세부 semantics, CI나 generator 동작 같은 실행 세부를 넣지 않습니다.

## 2. Dedicated Documents

구체 규칙이 독립적으로 탐색·유지될 책임을 가지면 별도 문서가 소유합니다.

| Responsibility | Owner / Candidate |
| --- | --- |
| README 생성 조건, entrypoint 역할, local rule 흡수 조건 | `docs/documentation/readme-authoring.md` |
| README `Index`와 generated `INDEX.tsv` 선택 | `docs/documentation/indexing.md` |
| frontmatter field와 discovery metadata | `docs/documentation/frontmatter.md` |
| repository 언어 선택 | `docs/language.md` |
| asset/family maintainer documentation contract | `docs/documentation/asset-maintainer-documentation.md` |
| deterministic validation, CI와 merge-blocking evidence | `docs/development/testing.md` |
| Markdown 표현, heading, paragraph, table/list 선택과 human-readable presentation | 우선 `mols-markdown-for-human`과 중복을 감사한 뒤 필요할 때만 별도 documentation owner를 검토 |

### Writing Guidance Candidate

조사에서 나온 다음 내용은 중요하지만 `principles.md`에 직접 넣기에는 구체적입니다.

- 중요한 정보를 먼저 쓰기
- descriptive heading
- 한 문장 한 idea, 한 문단 한 topic
- consistent terminology
- meaningful link text
- scan 가능한 chunking
- accessibility를 해치지 않는 semantic structure
- example과 alternative의 최소화 기준

이 내용은 곧바로 새 `writing.md`를 만들지 않습니다. 먼저 repository가 이미 사용하는 `mols-markdown-for-human`, `docs/language.md`, README authoring 규칙과의 중복을 검토합니다. **독립적인 repository documentation writing contract가 실제로 남을 때만** 새 문서를 만듭니다.

## 3. README Placement

README 배치는 **가급적 지양**합니다. Repository-wide 원칙이나 독립적으로 찾을 가치가 있는 규칙을 README에 숨기지 않습니다.

README에 둘 수 있는 것은 다음 조건을 모두 만족하는 작은 scope-local 규칙입니다.

- 해당 directory나 bundle에서만 의미가 있습니다.
- entrypoint를 읽는 사람이 함께 알아야 합니다.
- 독립적인 검색·유지·확장 책임이 아직 없습니다.
- 별도 파일로 만들면 navigation과 maintenance surface만 늘어납니다.
- 짧게 유지할 수 있습니다.

이번 `docs/documentation/README.md`의 duplication/lifecycle shared rule 흡수는 이 예외에 해당합니다.

다음 중 하나가 생기면 README에서 별도 owner로 분리할지 다시 검토합니다.

- 내용이 계속 커집니다.
- 다른 scope에서도 직접 참조하기 시작합니다.
- 독립적인 변경·검토·유지 책임이 생깁니다.
- README의 entrypoint 역할보다 해당 규칙 자체가 더 큰 비중을 차지합니다.

## Work Plan

1. 현재 `principles.md`와 위 원칙 후보를 대조해 의미 중복을 제거합니다.
1. 기존 여섯 원칙을 단순히 추가하지 않고, 전체를 7~8개 이하의 균형 잡힌 원칙으로 재구성합니다.
1. 각 문장이 repository 전체에 적용되는 durable 판단 기준인지 확인합니다. 구체 실행이면 해당 dedicated owner로 돌립니다.
1. writing/scannability/accessibility 세부는 `mols-markdown-for-human`, `docs/language.md`, README authoring과 먼저 대조합니다.
1. 감사 후 독립 responsibility가 남을 때만 별도 writing documentation을 제안합니다.
1. README에는 위 예외 조건을 만족하는 scope-local 작은 규칙만 남기고 새 repository-wide 규칙을 추가하지 않습니다.
1. 변경 후 KISS/DRY, authority 중복, discoverability, link integrity와 generated index 영향을 리뷰합니다.

## Acceptance

다음 조건을 만족하면 원칙 설계가 수렴한 것으로 봅니다.

- `principles.md`는 implementation detail 없이 repository-wide 판단 기준만 소유합니다.
- 각 principle은 다른 principle과 의미가 명확히 구분되며 7~8개 이하로 유지됩니다.
- 구체 writing, README, indexing, metadata, language, testing 규칙은 적절한 dedicated owner가 소유합니다.
- README는 독립 책임이 약한 작은 scope-local rule을 위한 예외적 surface로만 사용합니다.
- 같은 durable 의미를 여러 authored source가 병렬로 소유하지 않습니다.
- 사람이 읽기 쉽고 agent가 discovery/routing하기 쉬운 구조를 함께 유지합니다.
