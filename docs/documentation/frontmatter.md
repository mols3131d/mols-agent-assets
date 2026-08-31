---
description: Markdown 문서에 frontmatter를 언제 적용하고, description을 탐색·라우팅에 어떻게 쓰며, README 범위 메타데이터를 어디서 다룰지 확인할 때 사용합니다.
---

# Frontmatter

현재 사용하는 frontmatter 필드와 필수 여부는 루트의 [`frontmatter.json`](../../frontmatter.json)을 따릅니다.

## Scope

일반 문서에는 이 저장소의 frontmatter 규칙을 적용합니다. 다만 확장자만 보고 일괄 적용하지 않고 파일의 역할을 먼저 봅니다.

- `AGENTS.md`, `SKILL.md`, subagent, agent file 같은 **Agent Asset에는 일반 문서용 frontmatter를 강제하지 않습니다.** Frontmatter를 금지하는 뜻은 아닙니다. 해당 자산의 표준, framework, vendor 또는 저장소 규칙이 메타데이터 형식을 정합니다.
- `__*__` 같은 **systemic asset은 일반 문서 frontmatter 규칙의 예외**이며 해당 자산의 규칙을 따릅니다.
- Agent Asset을 설명하는 일반 문서는 Agent Asset 자체가 아니므로 문서 frontmatter 규칙을 따릅니다.

## Description

`description`은 문서를 열기 전에 후보를 구분하고 고르는 데 쓰는 **탐색·라우팅 메타데이터**입니다. `docs/INDEX.tsv`를 생성할 때도 이 값을 사용합니다.

가장 중요한 것은 **언제 이 문서를 찾는지** 드러나는가입니다. 어떤 작업, 문제, 판단과 관련되는지 먼저 밝히고, 후보를 구분하는 데 필요하다면 문서의 핵심 책임이나 인접 문서와의 차이를 짧게 덧붙입니다. 문서 선택에 도움이 되는 도메인 용어와 대상도 자연스럽게 포함합니다.

`description`은 문서를 자동으로 적용하거나 권한을 부여하지 않습니다. 문서를 고르는 데 도움을 주는 신호일 뿐이며, 실제 적용 범위와 권한은 해당 문서와 상위 규칙이 정합니다.

### Selection Check

같은 디렉터리에서 `path + description`만 봐도 현재 작업에 맞는 후보를 고를 수 있는지 확인합니다.

- 후보가 헷갈리면 실제 요청에 나올 만한 핵심 용어나 구분되는 책임 경계를 보강합니다.
- 파일명만으로 충분히 구분되고 설명이 새 정보를 주지 못한다면 억지로 길게 만들지 않습니다.
- 본문의 목차를 압축해 나열하거나 `~을 설명합니다`처럼 제목만 되풀이하는 문장은 피합니다.

대개 한 문장이면 충분합니다. 정확한 라우팅에 꼭 필요할 때만 두 문장까지 늘립니다.

## Entrypoint Metadata

디렉터리나 문서·파일 묶음의 진입점인 `README.md`에도 일반 frontmatter 규칙을 적용합니다. 다만 그 메타데이터는 **README 파일 자체가 아니라 README가 대표하는 범위**를 나타냅니다.

README를 언제 만들고 어떤 범위 메타데이터를 담을지는 [README Authoring](readme-authoring.md)이 정합니다. 자동 생성 인덱스나 다른 도구가 README 메타데이터를 어떻게 가져다 쓰는지는 해당 도구가 정하며, 이 문서에서 도구별 동작까지 정의하지 않습니다.

## Indexing Metadata

README의 `Index`는 본문 탐색을 위한 섹션이며 frontmatter를 대신하지 않습니다. `INDEX.tsv`는 자동 생성 결과이므로 사람이 직접 작성하는 frontmatter의 원본이 아닙니다.

어떤 인덱싱 방식을 사용할지는 [Document Indexing](indexing.md)의 원칙을 따릅니다.

Front Matter CMS의 설정, 공식 옵션, 원본 선택과 라우팅은 [Front Matter CMS](../references/tooling/front-matter-cms.md)를 참고합니다.
