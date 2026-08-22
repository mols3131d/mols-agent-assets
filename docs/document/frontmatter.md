---
description: Markdown 문서의 frontmatter 적용 범위, 예외, directory entrypoint metadata 원칙과 관련 도구를 확인할 때 사용합니다.
---

# Frontmatter

문서 frontmatter의 current field와 required 여부는 root [`frontmatter.json`](../../frontmatter.json)을 따릅니다.

## Scope

일반 repository documentation에는 문서 frontmatter contract를 적용합니다. 다만 파일 형식만으로 일괄 적용하지 않고 자산의 역할을 먼저 판정합니다.

- `AGENTS.md`, `SKILL.md`, subagent, agent file 같은 **Agent Asset은 일반 문서 frontmatter를 강제하지 않습니다.** Frontmatter를 금지한다는 뜻이 아니며, 해당 자산의 표준·framework·vendor·repository 관행이 metadata contract를 소유합니다.
- `__*__` 같은 **systemic asset은 일반 문서 frontmatter contract의 예외**이며 해당 systemic contract를 따릅니다.
- Agent Asset을 설명하는 일반 documentation은 Agent Asset 자체가 아니므로 문서 frontmatter contract를 따릅니다.

## Directory Entrypoint

`README.md`처럼 directory의 entrypoint 역할을 하는 문서는 frontmatter에 **해당 directory의 metadata**를 담습니다.

`description`은 README 파일 자체를 설명하기보다 directory의 책임, 범위 또는 이 entrypoint를 언제 사용하는지 나타내야 합니다.

Front Matter CMS의 설정, 공식 옵션, source routing은 [Front Matter CMS](../references/tooling/front-matter-cms.md)를 참고합니다.
