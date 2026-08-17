# Content Types

## 역할

content type은 Markdown front matter의 field 구조와 Front Matter 패널의 입력 UI를 정의한다.

```jsonc
{
  "frontMatter.taxonomy.contentTypes": [
    {
      "name": "guide",
      "fields": []
    }
  ]
}
```

## Active content type 선택

권장 식별 순서는 다음과 같다.

```text
fmContentType → type → default
```

```yaml
---
type: internal-document
fmContentType: guide
---
```

- 회사 시스템은 `type: internal-document`를 사용한다.
- Front Matter CMS는 `fmContentType: guide`를 우선 사용한다.
- `fmContentType`이 없으면 기존 호환을 위해 `type`을 fallback으로 사용한다.
- 둘 다 없거나 일치하는 content type을 찾지 못하면 `default`가 fallback이 될 수 있다.

> `contentTypes`는 Markdown 식별 필드가 아니다. `pageFolders`에서 허용할 content type 목록을 지정하는 설정이다.

## 주요 속성

| 속성 | 역할 | 기본 |
| --- | --- | --- |
| `name` | content type ID | 필수 |
| `fields` | field definitions | `[]` |
| `clearEmpty` | 빈 field를 front matter에서 제거 | `false` |
| `pageBundle` | 파일 대신 folder + index 파일 생성 | `false` |
| `defaultFileName` | 생성 시 기본 파일명 | `index` |
| `fileType` | 생성 확장자 | `md` |
| `filePrefix` | 생성 파일명 prefix | `null` |
| `previewPath` | type별 preview path | `null` |
| `template` | 생성 시 사용할 Markdown template | `null` |
| `postScript` | 생성 직후 실행할 script ID | `null` |
| `allowAsSubContent` | 하위 콘텐츠 생성 허용 | `false` |
| `isSubContent` | 하위 콘텐츠 전용 타입 | `false` |
| `slugTemplate` | slug 생성 규칙 | `{{title}}` |

## 권장 default

`default`는 알 수 없는 문서도 열 수 있는 느슨한 fallback으로 둔다.

```json
{
  "name": "default",
  "pageBundle": false,
  "previewPath": null,
  "clearEmpty": true,
  "fields": [
    {
      "title": "Title",
      "name": "title",
      "type": "string",
      "single": true
    },
    {
      "title": "Description",
      "name": "description",
      "type": "string"
    },
    {
      "title": "Tags",
      "name": "tags",
      "type": "tags"
    }
  ]
}
```

default에 `required`를 과도하게 설정하면 기존 Markdown과 외부 문서가 모두 오류로 보일 수 있다.

## 전용 타입

```json
{
  "name": "guide",
  "clearEmpty": true,
  "fields": [
    {
      "title": "Title",
      "name": "title",
      "type": "string",
      "single": true,
      "required": true
    },
    {
      "title": "Description",
      "name": "description",
      "type": "string",
      "required": true
    },
    {
      "title": "Status",
      "name": "status",
      "type": "choice",
      "choices": [
        "draft",
        "stable",
        "deprecated"
      ],
      "required": true
    }
  ]
}
```

Markdown:

```yaml
---
fmContentType: guide
title: DuckDB 운영 가이드
description: 운영 환경에서 DuckDB를 사용하는 기준
status: stable
---
```

## Folder와 연결

```jsonc
{
  "frontMatter.content.pageFolders": [
    {
      "title": "Docs",
      "path": "[[workspace]]/docs",
      "contentTypes": [
        "default",
        "guide"
      ]
    }
  ]
}
```

- 생성을 허용할 타입을 folder별로 제한한다.
- Markdown의 `fmContentType` 값을 대신하는 field가 아니다.
- folder에 하나의 content type만 허용하면 생성 workflow를 단순화할 수 있다.

## Template 연결

```json
{
  "name": "guide",
  "template": "[[workspace]]/.frontmatter/templates/guide.md",
  "fields": []
}
```

Template에서 `fmContentType`을 고정하면 누락을 줄일 수 있다.

```yaml
---
fmContentType: guide
title: ""
description: ""
status: draft
---

# {{title}}
```

## 작업 규칙

- 기존 `type`의 의미를 먼저 확인한다.
- 다른 도구가 `type`을 소유하면 `fmContentType`을 사용한다.
- content type의 `name`은 안정적인 kebab-case ID를 권장한다.
- display label이 필요하면 field의 `title`을 사용한다.
- 전용 type에는 명확한 validation을, `default`에는 최소 field만 둔다.

## 공식 출처

- [Content types](https://frontmatter.codes/docs/content-creation/content-types)
- [Content folders](https://frontmatter.codes/docs/content-creation/content-folders)
- [Updates](https://frontmatter.codes/updates)
