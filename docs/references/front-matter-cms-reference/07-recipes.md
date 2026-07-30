# Recipes

## 1. 최소 default schema

기존 Markdown을 방해하지 않는 fallback.

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

## 2. 회사 `type`과 공존

```yaml
---
type: internal
fmContentType: guide
title: 운영 가이드
---
```

- `type`: 회사 convention
- `fmContentType`: Front Matter CMS schema 선택

## 3. 엄격한 guide schema

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
    },
    {
      "title": "Tags",
      "name": "tags",
      "type": "tags",
      "taxonomyLimit": 5
    }
  ]
}
```

## 4. 조건부 field

```json
{
  "title": "Deprecation reason",
  "name": "deprecationReason",
  "type": "string",
  "when": {
    "fieldRef": "status",
    "operator": "equals",
    "value": "deprecated",
    "caseSensitive": false
  }
}
```

`deprecationReason`을 조건부 required로 강제하려면 별도 validator를 추가한다.

## 5. 공통 field 재사용

```jsonc
{
  "frontMatter.taxonomy.fieldGroups": [
    {
      "id": "document-lifecycle",
      "fields": [
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
        },
        {
          "title": "Last reviewed",
          "name": "lastReviewed",
          "type": "datetime"
        }
      ]
    }
  ]
}
```

각 content type:

```json
{
  "title": "Lifecycle",
  "name": "lifecycle",
  "type": "fieldCollection",
  "fieldGroup": "document-lifecycle"
}
```

## 6. Folder별 타입 제한

```jsonc
{
  "frontMatter.content.pageFolders": [
    {
      "title": "Guides",
      "path": "[[workspace]]/docs/guides",
      "contentTypes": [
        "guide"
      ]
    },
    {
      "title": "Runbooks",
      "path": "[[workspace]]/docs/runbooks",
      "contentTypes": [
        "runbook"
      ]
    }
  ]
}
```

## 7. 생성 template

```markdown
---
fmContentType: guide
title: ""
description: ""
status: draft
tags: []
---

# {{title}}

## 개요

## 절차

## 참고
```

## 8. 숫자 범위

```json
{
  "title": "Priority",
  "name": "priority",
  "type": "number",
  "numberOptions": {
    "min": 1,
    "max": 5,
    "step": 1
  },
  "required": true
}
```

내장 validation은 min/max를 검사한다. 정확한 정수 배수 규칙이 중요하면 외부 validator로 보완한다.

## 9. Split config

```text
.frontmatter/config/
├── content/pagefolders/
│   ├── guides.json
│   └── runbooks.json
└── taxonomy/
    ├── contenttypes/
    │   ├── guide.json
    │   └── runbook.json
    └── fieldgroups/
        └── document-lifecycle.json
```

`frontmatter.json`에는 split한 setting을 다시 정의하지 않는다.

## 10. 적용 전 확인

```text
[ ] 기존 type 의미 확인
[ ] fmContentType 사용 여부 결정
[ ] default는 fallback으로 유지
[ ] folder와 content type 연결
[ ] template에 식별자 포함
[ ] required/choice/min/max 확인
[ ] Problems 패널에서 validation 확인
[ ] regex/cross-field/CI 필요 여부 판단
```

## 공식 출처

- [Content types](https://frontmatter.codes/docs/content-creation/content-types)
- [Fields](https://frontmatter.codes/docs/content-creation/fields)
- [Field conditions](https://frontmatter.codes/docs/content-creation/field-conditions)
- [Content folders](https://frontmatter.codes/docs/content-creation/content-folders)
- [Placeholders](https://frontmatter.codes/docs/content-creation/placeholders)
