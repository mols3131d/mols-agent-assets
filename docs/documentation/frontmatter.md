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

`description`은 문서를 열기 전에 후보를 구분하고 선택할 수 있게 하는 **discovery와 routing metadata**입니다. 이 repository의 `docs/**/INDEX.tsv` 같은 projection에서도 사용되므로 제목을 되풀이하는 요약보다 다음 두 신호를 우선합니다.

- **언제 찾는가** — 어떤 작업, 문제, 판단에서 이 문서가 relevant한지 드러냅니다.
- **무엇을 책임지는가** — 이 문서가 소유하는 핵심 범위나 다른 문서와 구분되는 boundary를 짧게 나타냅니다.

문서 선택에 도움이 되는 domain term, 대상과 주요 concern은 자연스럽게 포함합니다. 반대로 본문의 목차를 압축해 나열하거나 `~을 설명합니다`처럼 제목만 다시 말하는 문장은 피합니다. 보통 한 문장으로 충분하며, 정확한 routing에 필요할 때만 두 문장까지 확장합니다.

## Directory Entrypoint

`README.md`처럼 directory의 entrypoint 역할을 하는 문서는 frontmatter에 **해당 directory의 metadata**를 담습니다.

`description`은 README 파일 자체를 설명하기보다 directory의 책임, 범위와 이 entrypoint를 언제 사용하는지 나타냅니다.

Front Matter CMS의 설정, 공식 옵션, source routing은 [Front Matter CMS](../references/tooling/front-matter-cms.md)를 참고합니다.
