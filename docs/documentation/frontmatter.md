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

## Directory Entrypoint

`README.md`, `index.md`처럼 directory의 entrypoint 역할을 하는 문서는 frontmatter에 **해당 directory의 metadata**를 담을 수 있습니다.

Directory metadata를 projection할 때는 repository가 정한 entrypoint 후보의 우선순위를 따릅니다. 이 repository의 docs index는 기본적으로 `README.md`를 먼저 보고, 파일이 없거나 YAML frontmatter 자체가 없으면 `index.md`로 넘어갑니다. 앞선 entrypoint에 frontmatter가 있으면 일부 field가 비어 있어도 뒤 entrypoint와 metadata를 임의로 합치지 않습니다.

`description`은 entrypoint 파일 자체를 설명하기보다 directory를 언제 탐색해야 하는지와, 선택에 필요할 때 그 directory의 책임·범위를 나타냅니다.

Front Matter CMS의 설정, 공식 옵션, source routing은 [Front Matter CMS](../references/tooling/front-matter-cms.md)를 참고합니다.
