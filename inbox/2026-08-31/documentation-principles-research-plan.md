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
| Google Developer Documentation Style Guide | 독자와 현재 상태에 집중하고, clear·concise·unambiguous한 표현과 timeless documentation을 강조합니다. |
| Microsoft Writing Style Guide | audience와 intent를 먼저 정하고, 중요한 정보를 먼저 보여주며 scan 가능한 content를 권장합니다. |
| Diátaxis | documentation을 user need에 맞는 책임으로 분리하고 accuracy·completeness·consistency·usefulness·precision과 human fit을 함께 품질로 봅니다. |
| Write the Docs — Documentation Principles | current, complete-within-scope, unique, discoverable, 가까운 source와 유지 가능성을 강조하며 필요한 반복은 허용합니다. |
| Write the Docs — Docs as Code | documentation도 version control, review와 검증 가능한 workflow 안에서 유지하는 것이 유리합니다. |
| GitLab Documentation Guidelines | topic responsibility, single source, 지속적 갱신, search/scan 가능성과 자동 검증을 강조합니다. |
| W3C Writing for Web Accessibility | 의미 있는 heading·link text, 명확한 instruction, clear·concise content가 접근성과 탐색성을 함께 높입니다. |

참고 URL:

- https://developers.google.com/style/
- https://developers.google.com/style/translation
- https://developers.google.com/style/timeless-documentation
- https://learn.microsoft.com/en-us/style-guide/content-planning
- https://learn.microsoft.com/en-us/style-guide/scannable-content/
- https://diataxis.fr/
- https://diataxis.fr/quality/
- https://www.writethedocs.org/guide/writing/docs-principles/
- https://www.writethedocs.org/guide/docs-as-code/
- https://docs.gitlab.com/development/documentation/styleguide/
- https://docs.gitlab.com/development/documentation/topic_types/
- https://www.w3.org/WAI/tips/writing/

## Placement Strategy

배치 우선순위는 다음과 같습니다.

1. repository 전체에 적용되는 durable 판단 기준이면 `principles.md`
1. 독립적으로 탐색·유지할 구체 책임이 있으면 별도 canonical document
1. 위 두 조건에 못 미치고 특정 scope의 entrypoint에서 함께 읽는 것이 더 자연스러운 작은 규칙만 README

README는 catch-all 문서로 사용하지 않습니다.

## 1. Principles Document

`docs/documentation/principles.md`에는 **구체적인 실행 방법이 아니라 repository-wide 판단 기준**만 둡니다.

RPI Research 결과 원칙은 다음 일곱 축으로 수렴시킵니다.

1. **Reader need first** — 작성자의 설명 순서보다 독자의 질문·판단·행동에서 시작합니다.
1. **Clear responsibility and scope** — 문서마다 주된 책임과 가장 작은 유효 scope를 두고, 선택한 scope 안에서는 필요한 의미를 충분히 다룹니다.
1. **Progressive disclosure** — 판단에 필요한 핵심과 context를 먼저 제공하고 세부는 필요에 따라 확장합니다.
1. **One authority, minimal repetition** — 같은 의미의 authority는 하나로 두되 이해와 routing에 필요한 짧은 context는 허용합니다.
1. **Current and trustworthy** — 문서는 현재 truth에 맞고 정확·일관·검증 가능해야 하며, 불확실하거나 오래된 내용을 확정적으로 유지하지 않습니다.
1. **Discoverable and navigable** — 필요한 독자가 올바른 문서를 발견·선택하고 다음 정보로 이동할 수 있어야 합니다.
1. **Maintainable by design** — 쉽게 재생성되거나 유지 가치가 낮은 정보를 authored documentation으로 만들지 않고, local 반복이 공통 책임이 되면 owner를 재검토합니다.

현재 `principles.md`의 기존 원칙은 위 일곱 축에 흡수합니다.

- `필요한 문서만 둔다` → `Clear responsibility and scope`
- `가장 좁은 scope가 소유한다` → `Clear responsibility and scope`
- `한 의미에는 한 authoritative owner` → `One authority, minimal repetition`
- `상위 원칙을 local에서 복제하지 않는다` → `One authority, minimal repetition`
- `복구 가능한 inventory를 authored knowledge로 만들지 않는다` → `Maintainable by design`
- `반복되는 local rule은 승격을 검토한다` → `Maintainable by design`

원칙 문서에는 command, field schema, heading 규칙, 특정 filename의 세부 semantics, CI나 generator 동작 같은 실행 세부를 넣지 않습니다.

## 2. Dedicated Documents

구체 규칙이 독립적으로 탐색·유지될 책임을 가지면 별도 문서가 소유합니다.

| Responsibility | Owner |
| --- | --- |
| README 생성 조건, entrypoint 역할, local rule 흡수 조건 | `docs/documentation/readme-authoring.md` |
| README `Index`와 generated `INDEX.tsv` 선택 | `docs/documentation/indexing.md` |
| frontmatter field와 discovery metadata | `docs/documentation/frontmatter.md` |
| repository 언어 선택 | `docs/language.md` |
| asset/family maintainer documentation contract | `docs/documentation/asset-maintainer-documentation.md` |
| deterministic validation, CI와 merge-blocking evidence | `docs/development/testing.md` |
| Markdown 표현, heading, paragraph, table/list 선택과 human-readable presentation | `mols-markdown-for-human` |

### Writing Guidance Audit

추가 조사와 repository asset 대조 결과 **새 `docs/documentation/writing.md`는 만들지 않습니다.**

`mols-markdown-for-human`이 이미 다음을 소유합니다.

- BLUF와 중요한 정보 우선 배치
- descriptive heading과 얕은 hierarchy
- 한 문단 한 핵심과 scan 가능한 구조
- list/table/callout 등 정보 구조에 맞는 표현 선택
- consistent terminology
- KISS/DRY와 불필요한 section·중복 제거
- 독자의 질문·판단·다음 행동에 맞춘 구조화

사람과 agent 모두에게 적용할 repository-wide 판단 기준만 `principles.md`에 남기고, 구체 Markdown presentation은 Skill과 기존 dedicated policy가 계속 소유합니다. 별도 writing policy가 필요해지는 경우는 Skill로 소유할 수 없는 repository-specific writing contract가 실제로 생길 때뿐입니다.

## 3. README Placement

README 배치는 **가급적 지양**합니다. Repository-wide 원칙이나 독립적으로 찾을 가치가 있는 규칙을 README에 숨기지 않습니다.

README에 둘 수 있는 것은 다음 조건을 모두 만족하는 작은 scope-local 규칙입니다.

- 해당 directory나 bundle에서만 의미가 있습니다.
- entrypoint를 읽는 사람이 함께 알아야 합니다.
- 독립적인 검색·유지·확장 책임이 아직 없습니다.
- 별도 파일로 만들면 navigation과 maintenance surface만 늘어납니다.
- 짧게 유지할 수 있습니다.

다음 중 하나가 생기면 README에서 별도 owner로 분리할지 다시 검토합니다.

- 내용이 계속 커집니다.
- 다른 scope에서도 직접 참조하기 시작합니다.
- 독립적인 변경·검토·유지 책임이 생깁니다.
- README의 entrypoint 역할보다 해당 규칙 자체가 더 큰 비중을 차지합니다.

현재 `docs/documentation/README.md`의 working artifact·Git history·archive 관련 짧은 안내는 독립 lifecycle policy를 다시 만들기보다 entrypoint에서 필요한 최소 routing context로 유지합니다. 반면 authority·duplication의 repository-wide 판단은 `principles.md`가 canonical owner가 되도록 README에서 중복을 줄입니다.

## RPI Implementation Plan

1. `principles.md`를 기존 6개 항목에 덧붙이지 않고 일곱 축으로 전면 재구성합니다.
1. 각 principle은 한 문단 이내로 유지하고 implementation detail을 제거합니다.
1. `docs/documentation/README.md`에서 principles와 중복되는 authority·duplication 문장을 제거하고, working artifact lifecycle의 최소 entrypoint context만 남깁니다.
1. `readme-authoring.md`, `indexing.md`, `frontmatter.md`, `language.md`, `testing.md`, `mols-markdown-for-human`의 책임은 확대하지 않고 현재 owner를 유지합니다.
1. 새 writing policy는 만들지 않습니다.
1. `docs/INDEX.tsv`는 source description 변경이 생길 때만 projection을 정합화합니다.
1. 변경 후 문서 의미 보존, KISS/DRY, authority 중복, discoverability, link integrity와 PR Gate를 리뷰합니다.
1. Review에서 실제 책임 누락이나 과도한 추상화가 발견될 때만 다음 Loop를 엽니다.

## Acceptance

다음 조건을 만족하면 원칙 설계가 수렴한 것으로 봅니다.

- `principles.md`는 implementation detail 없이 repository-wide 판단 기준만 소유합니다.
- 원칙은 일곱 축 안에서 서로 역할이 구분되고, 기존 ownership 의미를 잃지 않습니다.
- 구체 writing, README, indexing, metadata, language, testing 규칙은 적절한 dedicated owner가 소유합니다.
- 새 writing policy를 중복 생성하지 않습니다.
- README는 독립 책임이 약한 작은 scope-local rule과 entrypoint routing context를 위한 예외적 surface로만 사용합니다.
- 같은 durable 의미를 여러 authored source가 병렬로 소유하지 않습니다.
- 사람이 읽기 쉽고 agent가 discovery/routing하기 쉬운 구조를 함께 유지합니다.
