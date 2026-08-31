---
description: Markdown 문서의 frontmatter 적용 범위, 예외, description의 탐색·routing 역할, directory entrypoint metadata 원칙과 관련 도구를 확인할 때 사용합니다.
---

# Frontmatter

문서 frontmatter의 current field와 required 여부는 root [`frontmatter.json`](../../frontmatter.json)을 따릅니다.

## Scope

일반 repository documentation에는 문서 frontmatter contract를 적용합니다. 다만 파일 형식만으로 일괄 적용하지 않고 자산의 역할을 먼저 판정합니다.

- `AGENTS.md`, `SKILL.md`, subagent, agent file 같은 **Agent Asset은 일반 문서 frontmatter를 강제하지 않습니다.** Frontmatter를 금지한다는 뜻이 아니며, 해당 자산의 표준·framework·vendor·repository 관행이 metadata contract를 소유합니다.
- `__*__` 같은 **systemic asset은 일반 문서 frontmatter contract의 예외**이며 해당 systemic contract를 따릅니다.
- Agent Asset을 설명하는 일반 documentation은 Agent Asset 자체가 아니므로 문서 frontmatter contract를 따릅니다.

## Description

`description`은 문서를 열기 전에 후보를 구분하고 선택할 수 있게 하는 **discovery와 routing metadata**입니다. 이 repository의 generated docs `INDEX.tsv` projection에서도 사용됩니다.

가장 중요한 신호는 **언제 이 문서를 찾는가**입니다. 어떤 작업, 문제나 판단에서 관련되는지 드러내고, 후보를 구분하는 데 도움이 되면 문서가 맡는 핵심 책임이나 인접 문서와의 경계를 짧게 덧붙입니다. 문서 선택에 유용한 domain term, 대상과 주요 concern은 자연스럽게 포함합니다.

`description` 자체가 문서를 자동 적용하거나 authority를 부여하지는 않습니다. Discovery와 routing을 돕는 선택 신호이며, 실제 적용 범위와 권한은 해당 문서와 상위 contract가 소유합니다.

### Selection Check

같은 directory의 `path + description`만 보이는 상황에서 현재 작업에 맞는 후보를 고를 수 있는지 확인합니다.

- 후보가 헷갈리면 실제 요청에 나타날 만한 trigger keyword나 구분되는 책임 경계를 보강합니다.
- 파일명만으로 충분히 구분되고 설명이 선택에 새 정보를 주지 못하면 억지로 길게 만들지 않습니다.
- 본문의 목차를 압축해 나열하거나 `~을 설명합니다`처럼 제목만 다시 말하는 문장은 피합니다.

보통 한 문장으로 충분하며, 정확한 routing에 필요할 때만 두 문장까지 확장합니다.

## Entrypoints and Indexes

이 repository에서 directory와 bundle형 문서 또는 파일의 entrypoint filename은 `README.md`입니다.

Entrypoint `README.md`의 frontmatter는 **README 파일 자체보다 그 entrypoint가 대표하는 directory 또는 bundle scope의 metadata**를 담습니다.

- `description`은 그 scope를 언제 탐색하거나 사용해야 하는지와, 선택에 필요할 때 책임·경계를 나타냅니다.
- `title`을 사용할 때는 README라는 filename이 아니라 그 directory 또는 bundle의 사람이 읽는 이름을 나타냅니다.
- `이 README는 ...을 설명합니다`처럼 파일 자체를 서술하기보다 scope의 목적과 routing signal을 표현합니다.

Generated docs index가 directory metadata를 projection할 때는 해당 directory의 `README.md`만 사용합니다. Frontmatter가 없거나 일부 field가 비어 있어도 다른 filename으로 fallback하거나 metadata를 합치지 않습니다.

Bundle README도 같은 scope-metadata 원칙을 따르지만, 특정 generator나 consumer가 bundle metadata를 어떻게 사용하는지는 해당 owner가 정의합니다. 일반 frontmatter policy가 존재하지 않는 projection semantics를 만들지는 않습니다.

작은 scope에서 별도 `INDEXING.md`나 local `INDEX.tsv`가 과하면 README 안에 `Index` section을 둘 수 있습니다. 이때 table은 README body의 authored navigation이며 frontmatter metadata를 대신하지 않습니다.

`INDEXING.md`는 사람이 작성하는 directory indexing 전담 문서이며 일반 documentation frontmatter contract를 따르지만 directory metadata source는 아닙니다. `INDEX.tsv`는 generated projection이므로 authored frontmatter source가 아닙니다.

Entrypoint, inline index와 독립 index filename의 역할과 생성 조건은 [Entrypoints and Indexes](entrypoint-readme-index.md)가 소유합니다.

Front Matter CMS의 설정, 공식 옵션, source routing은 [Front Matter CMS](../references/tooling/front-matter-cms.md)를 참고합니다.
