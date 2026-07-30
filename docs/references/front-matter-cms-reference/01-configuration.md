# Configuration

## 핵심 구조

Front Matter CMS 설정은 일반적으로 repository의 `frontmatter.json`에 저장한다.

```text
repository/
├── frontmatter.json
├── .frontmatter/
│   ├── config/
│   └── templates/
└── docs/
```

`frontmatter.json`은 팀 공유 설정이다. `.vscode/settings.json`의 로컬 설정으로 값을 덮어쓸 수 있다.

## 우선순위

```text
분리된 .frontmatter/config 파일
  < frontmatter.json
  < .vscode/settings.json의 로컬 override
```

`frontmatter.json`에 같은 setting이 있으면 분리 파일의 값을 덮어쓴다. 한 setting을 두 위치에서 동시에 관리하지 않는 편이 안전하다.

## 최소 설정

```json
{
  "$schema": "https://beta.frontmatter.codes/frontmatter.schema.json",
  "frontMatter.framework.id": "other",
  "frontMatter.content.publicFolder": "",
  "frontMatter.validation.enabled": true,
  "frontMatter.content.pageFolders": [
    {
      "title": "docs",
      "path": "[[workspace]]/docs"
    }
  ],
  "frontMatter.taxonomy.contentTypes": [
    {
      "name": "default",
      "pageBundle": false,
      "previewPath": null,
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
  ]
}
```

## 자주 쓰는 settings

| Setting | 역할 | 권장 |
| --- | --- | --- |
| `frontMatter.framework.id` | framework/SSG 통합 선택 | 일반 Markdown이면 `other` |
| `frontMatter.content.pageFolders` | 콘텐츠 검색·생성 위치 | 반드시 명시 |
| `frontMatter.content.publicFolder` | image/media 기준 폴더 | asset workflow가 있을 때 |
| `frontMatter.taxonomy.contentTypes` | front matter schema와 입력 UI | 핵심 |
| `frontMatter.taxonomy.fieldGroups` | 재사용 field 묶음 | 중복이 생길 때 |
| `frontMatter.validation.enabled` | active content type 기반 진단 | `true` |
| `frontMatter.taxonomy.quoteStringValues` | 문자열 YAML quoting | 프로젝트 convention에 맞춤 |
| `frontMatter.content.supportedFileTypes` | 처리할 확장자 | 기본 `md`, `mdx`, `markdown` |
| `frontMatter.content.hideFm` | editor에서 front matter 숨김 | 원문 검토가 중요하면 `false` |
| `frontMatter.content.fmHighlight` | front matter 강조 | 기본 유지 |

## 설정 분리

content type이 많아지면 다음 위치로 분리할 수 있다.

```text
.frontmatter/config/
├── content/pagefolders/
│   └── docs.json
└── taxonomy/
    ├── contenttypes/
    │   ├── guide.json
    │   └── skill.json
    └── fieldgroups/
        └── common.json
```

### Content type 분리 파일

```json
{
  "$schema": "https://frontmatter.codes/config/taxonomy.contenttypes.schema.json",
  "name": "guide",
  "fields": [
    {
      "title": "Title",
      "name": "title",
      "type": "string",
      "required": true,
      "single": true
    }
  ]
}
```

### Page folder 분리 파일

```json
{
  "$schema": "https://frontmatter.codes/config/content.pagefolders.schema.json",
  "title": "docs",
  "path": "[[workspace]]/docs",
  "contentTypes": [
    "default",
    "guide"
  ]
}
```

## 두 종류의 schema를 구분한다

| Schema | 검증 대상 |
| --- | --- |
| `frontmatter.schema.json` | `frontmatter.json` 설정 구조 |
| content type 기반 validation | Markdown front matter 값 |

설정 JSON이 유효하더라도 Markdown metadata가 유효하다는 뜻은 아니다.

## 작업 규칙

1. 기존 `frontmatter.json`과 분리 config를 함께 검색한다.
1. 같은 setting이 여러 위치에 있는지 확인한다.
1. 기존 field name과 YAML 출력 형태를 보존한다.
1. 새 옵션은 공식 schema 또는 문서에서 확인한다.
1. 변경 후 VS Code의 settings diagnostic과 Markdown diagnostics를 확인한다.

## 공식 출처

- [Settings](https://frontmatter.codes/docs/settings)
- [Settings overview](https://frontmatter.codes/docs/settings/overview)
