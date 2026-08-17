# Folders, Templates, Placeholders

## Content folders

`frontMatter.content.pageFolders`는 확장이 Markdown을 찾고 새 문서를 생성할 위치를 정의한다.

```json
{
  "frontMatter.content.pageFolders": [
    {
      "title": "Docs",
      "path": "[[workspace]]/docs",
      "contentTypes": [
        "default",
        "guide"
      ],
      "excludePaths": [
        "_archive/**",
        "**/*.generated.md"
      ]
    }
  ]
}
```

## 주요 folder 속성

| 속성 | 역할 |
| --- | --- |
| `title` | UI label |
| `path` | content folder, `[[workspace]]` 권장 |
| `contentTypes` | folder에서 허용할 content type |
| `excludeSubdir` | 하위 folder 제외 |
| `excludePaths` | glob 기반 파일·folder 제외 |
| `disableCreation` | 검색은 하되 신규 생성 차단 |
| `previewPath` | folder 공통 preview prefix |
| `filePrefix` | 생성 파일명 prefix |
| `defaultLocale` | 기본 locale |
| `locales` | folder별 locale 설정 |

`contentTypes`는 Markdown key가 아니다.

## Templates

Template은 새 문서의 초기 front matter와 본문을 보장한다.

Content type 연결:

```json
{
  "name": "guide",
  "template": "[[workspace]]/.frontmatter/templates/guide.md",
  "fields": []
}
```

Template:

```markdown
---
fmContentType: guide
title: ""
description: ""
status: draft
---

# {{title}}

## 개요

## 사용법
```

### Content type과 template의 역할

| 기능 | Content type | Template |
| --- | --- | --- |
| 패널 field UI | 담당 | 미담당 |
| validation schema | 담당 | 미담당 |
| 초기 metadata | default로 일부 가능 | 담당 |
| 초기 본문 구조 | 미담당 | 담당 |
| 문서 type 누락 방지 | 간접 | 직접 |

둘 중 하나를 고르는 관계가 아니다. 함께 사용한다.

## 기본 placeholders

| Placeholder | 값 |
| --- | --- |
| `{{title}}` | 문서 title |
| `{{slug}}` | 문서 slug |
| `{{now}}` | 현재 날짜·시간 |
| `{{year}}`, `{{month}}`, `{{day}}` | 현재 날짜 구성요소 |
| `{{date\|yyyy-MM-dd}}` | publish date formatting |
| `{{fm.<field>}}` | 다른 front matter field |
| `{{fileName}}` | 현재 파일명 |
| `{{slugifiedFileName}}` | slug화한 파일명 |
| `{{pathToken.relPath}}` | page folder 기준 상대 경로 |
| `{{locale}}` | locale |
| `{{filePrefix.index}}` | folder 내 순번 |

## 활용 위치

placeholder는 다음에 사용할 수 있다.

- field의 `default`
- `slugTemplate`
- `previewPath`
- `filePrefix`
- dynamic path
- template

## 예시: 날짜 기반 경로

```json
{
  "title": "Posts",
  "path": "[[workspace]]/content/{{year}}/{{month}}",
  "previewPath": "/posts/{{date|yyyy-MM}}/{{slug}}",
  "contentTypes": [
    "post"
  ]
}
```

## 예시: front matter 기반 preview

```json
{
  "title": "Docs",
  "path": "[[workspace]]/docs",
  "previewPath": "/{{fm.section}}/{{slug}}"
}
```

## Custom placeholder

Static:

```jsonc
{
  "frontMatter.content.placeholders": [
    {
      "id": "permalink",
      "value": "/docs/{{slug}}/"
    }
  ]
}
```

Field:

```json
{
  "title": "Permalink",
  "name": "permalink",
  "type": "string",
  "default": "{{permalink}}"
}
```

Dynamic placeholder는 script를 실행한다. 전체 front matter가 필요한 처리는 placeholder보다 content type의 `postScript`가 적합하다.

## 생성 workflow 권장

```text
pageFolder 선택
  → content type 선택
  → template 적용
  → placeholder 치환
  → 파일 생성
  → postScript 실행
  → validation 확인
```

## 작업 규칙

- 절대 경로 대신 `[[workspace]]`를 사용한다.
- Template에 `fmContentType`을 명시한다.
- 동적 path는 예상 결과 예시를 문서화한다.
- `excludePaths`로 generated/archive 문서를 제외한다.
- file naming 자동화가 기존 link를 깨뜨리지 않는지 확인한다.

## 공식 출처

- [Content folders](https://frontmatter.codes/docs/content-creation/content-folders)
- [Content types](https://frontmatter.codes/docs/content-creation/content-types)
- [Placeholders](https://frontmatter.codes/docs/content-creation/placeholders)
- [Slug](https://frontmatter.codes/docs/content-creation/slug)
