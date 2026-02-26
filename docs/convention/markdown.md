---
title: 마크다운 관행
description: MOLS Agent의 마크다운 사용 규칙
categories:
  - convention
draft: false
date: 2026-02-26
lastmod: 2026-02-26T21:08:43.161Z
tags:
  - markdown
  - convention
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: false
---

# 마크다운 관행

MOLS Agent 프로젝트의 마크다운 문서 작성 표준을 정의합니다.# 

## Frontmatter

모든 문서는 Hugo 호환 형식을 따르며, 추가적인 에이전트 제어 필드를 포함합니다.

```yaml
---
title: "Title"
description: "문서의 설명"
categories: ["category1", "category2"]
draft: false
date: 2026-02-27
lastmod: 2026-02-27
tags: ["tag1", "tag2"]
agent-readable: true
agent-editable: false
agent-moveable: false
agent-deletable: false
agent-friendly: false
---
```

## 필드 명세 (Field Specification)

### 기본 메타데이터
- **`title`**: 문서의 제목입니다.
- **`description`**: 문서에 대한 간략한 설명입니다 (권장: 250자 이내).
- **`categories`**: 문서의 대분류를 지정합니다 (예: `convention`, `workspace`, `assets`).
- **`draft`**: `true`일 경우 초안 상태로 간주됩니다.
- **`date`**: 문서가 처음 생성된 날짜입니다 (`YYYY-MM-DD`).
- **`lastmod`**: 문서가 마지막으로 수정된 날짜 및 시간입니다.
- **`tags`**: 검색 및 식별을 위한 키워드 리스트입니다.

### 에이전트 제어 (Agent Control)
> **참고**: 아래 필드들은 에이전트가 문서를 어떻게 다룰지를 결정합니다.

- **`agent-readable`**: 에이전트가 이 문서를 읽을 수 있는지 여부를 결정합니다.
- **`agent-editable`**: 에이전트가 이 문서의 내용을 직접 수정할 수 있는지 여부입니다.
- **`agent-moveable`**: 에이전트가 이 문서의 파일 위치를 변경할 수 있는지 여부입니다.
- **`agent-deletable`**: 에이전트가 이 문서를 삭제할 수 있는지 여부입니다.
- **`agent-friendly`**: 이 문서가 토큰 최적화 등 에이전트가 이해하기 특별히 좋은 구조로 작성되었는지 여부입니다.


## Link

- 링크는 워크스페이스의 루트를 기준으로 적는다. - `/<dir1>/.../<file>`