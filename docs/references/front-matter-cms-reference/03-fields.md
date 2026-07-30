# Fields

## 공통 속성

| 속성 | 역할 |
| --- | --- |
| `name` | Markdown front matter key |
| `type` | field type |
| `title` | 패널에 표시할 label |
| `description` | field 설명 |
| `default` | 생성 시 기본값 또는 placeholder |
| `required` | 값 필수 |
| `hidden` | 패널에서는 숨기되 Front Matter에서 유지 |
| `actions` | field 값을 생성·갱신하는 custom action |

`name`과 `type`만 필수다. 사람도 읽는 설정이라면 `title`, 복잡한 값이면 `description`을 함께 둔다.

## 자주 쓰는 field

| Type | 적합한 값 | 주요 옵션 | 검증 포인트 |
| --- | --- | --- | --- |
| `string` | title, description, owner | `single`, `wysiwyg` | 문자열 타입 |
| `number` | weight, priority | `numberOptions` | 숫자, min/max |
| `datetime` | date, lastmod | `isPublishDate`, `isModifiedDate`, `dateFormat` | date-time |
| `boolean` | enabled, published | 없음 | boolean |
| `choice` | status, kind | `choices`, `multiple` | 허용 값 |
| `list` | aliases, commands | 없음 | 문자열 배열 |
| `tags` | 느슨한 분류 | `taxonomyLimit`, `singleValueAsString` | 문자열 배열 |
| `categories` | 상위 분류 | `taxonomyLimit`, `singleValueAsString` | 문자열 배열 |
| `taxonomy` | 프로젝트 고정 분류 | `taxonomyId`, `taxonomyLimit` | 설정에 따라 허용 값 |
| `image` | preview, cover | `multiple`, `isPreviewImage` | string 또는 string 배열 |
| `file` | attachment | `multiple` | string 또는 string 배열 |
| `slug` | URL slug | `editable`, `default` | 문자열 |
| `fields` | 중첩 object | `fields` 또는 `fieldGroup` | nested schema |
| `block` | object 배열 | `fieldGroup` | array of objects |
| `contentRelationship` | 다른 문서 참조 | `contentTypeName`, `contentTypeValue`, `multiple` | string 또는 배열 |
| `dataFile` | 외부 data 목록 선택 | `dataFileId`, `dataFileKey`, `multiple` | 선택 값 |
| `draft` | dashboard 상태 | `frontMatter.content.draftField`와 연동 | boolean 또는 custom status |

## String

`single: true`는 한 줄 입력 UI다. 값의 개수나 문자열 길이를 제한하지 않는다.

```json
{
  "title": "Title",
  "name": "title",
  "type": "string",
  "single": true,
  "required": true
}
```

`wysiwyg`는 `true`, `"html"`, `"markdown"`을 사용할 수 있다. 일반 metadata에는 과도하게 사용하지 않는 편이 좋다.

## Number

```json
{
  "title": "Priority",
  "name": "priority",
  "type": "number",
  "numberOptions": {
    "min": 1,
    "max": 5,
    "step": 1,
    "isDecimal": false
  }
}
```

- `min`, `max`: validation에 사용된다.
- `step`: 입력 단위다. 강한 배수 검증으로 의존하지 않는다.
- `isDecimal`: 소수 입력 허용 여부다.

## Datetime

```json
{
  "title": "Last modified",
  "name": "lastmod",
  "type": "datetime",
  "default": "{{now}}",
  "isModifiedDate": true,
  "dateFormat": "yyyy-MM-dd"
}
```

`isPublishDate`와 `isModifiedDate`는 dashboard와 자동 날짜 갱신에서 의미를 가진다.

## Choice

고정 enum에는 `choice`를 우선한다.

```json
{
  "title": "Status",
  "name": "status",
  "type": "choice",
  "choices": [
    {
      "id": "draft",
      "title": "Draft"
    },
    {
      "id": "stable",
      "title": "Stable"
    }
  ],
  "required": true
}
```

저장되는 값은 `id`다. label과 저장 값을 분리할 때 object form이 유용하다.

## Tags, categories, taxonomy

```json
{
  "title": "Audience",
  "name": "audience",
  "type": "taxonomy",
  "taxonomyId": "audience",
  "taxonomyLimit": 2
}
```

```jsonc
{
  "frontMatter.taxonomy.customTaxonomy": [
    {
      "id": "audience",
      "options": [
        "developer",
        "operator",
        "analyst"
      ]
    }
  ]
}
```

`taxonomyLimit`는 UI 선택 제한으로 유용하다. 정밀 CI 제약으로 사용할 경우 별도 validator를 둔다.

## Nested object: fields

Inline:

```json
{
  "title": "Owner",
  "name": "owner",
  "type": "fields",
  "fields": [
    {
      "title": "Name",
      "name": "name",
      "type": "string",
      "required": true
    },
    {
      "title": "Team",
      "name": "team",
      "type": "string"
    }
  ]
}
```

YAML:

```yaml
owner:
  name: Data Platform
  team: Analytics Engineering
```

## Reusable field group

```jsonc
{
  "frontMatter.taxonomy.fieldGroups": [
    {
      "id": "ownership",
      "fields": [
        {
          "title": "Owner",
          "name": "owner",
          "type": "string",
          "required": true
        },
        {
          "title": "Reviewers",
          "name": "reviewers",
          "type": "list"
        }
      ]
    }
  ]
}
```

content type에서 평평하게 합치기:

```json
{
  "title": "Ownership",
  "name": "ownership",
  "type": "fieldCollection",
  "fieldGroup": "ownership"
}
```

중첩 object로 사용하기:

```json
{
  "title": "Ownership",
  "name": "ownership",
  "type": "fields",
  "fieldGroup": "ownership"
}
```

## 반복 object: block

```json
{
  "title": "Owners",
  "name": "owners",
  "type": "block",
  "fieldGroup": [
    "owner"
  ]
}
```

YAML:

```yaml
owners:
  - name: Data Platform
    role: maintainer
    fieldGroup: owner
```

## 조건부 표시

`when`은 다른 field 값에 따라 UI를 표시하거나 숨긴다.

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

`when`은 UI 조건이다. 조건부 required나 cross-field validation을 완전히 대체하지 않는다.

## 고르는 기준

```text
자유 텍스트          → string
고정 단일 값         → choice
자유 문자열 배열     → list
공유 taxonomy        → tags/categories/taxonomy
중첩 단일 object     → fields
반복 object 배열     → block
다른 문서 참조       → contentRelationship
외부 data 목록 참조  → dataFile
```

## 공식 출처

- [Fields](https://frontmatter.codes/docs/content-creation/fields)
- [Field conditions](https://frontmatter.codes/docs/content-creation/field-conditions)
- [Field actions](https://frontmatter.codes/docs/content-creation/field-actions)
