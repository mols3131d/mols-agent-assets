# Validation

## 활성화

```json
{
  "frontMatter.validation.enabled": true
}
```

기본값은 `true`다. Front Matter CMS는 현재 Markdown의 active content type으로 JSON Schema를 생성하고 VS Code Diagnostics에 문제를 표시한다.

## 내장 검증 범위

| 규칙 | 예시 | 지원 |
| --- | --- | --- |
| 필수 field | `required: true` | 지원 |
| 기본 타입 | string, number, boolean, array, object | 지원 |
| choice enum | 허용 목록 밖의 값 | 지원 |
| number 범위 | `min`, `max` | 지원 |
| datetime 형식 | date-time string | 지원 |
| nested fields | object 내부 required/type | 지원 |
| block | object 배열과 field group 구조 | 지원 |
| multiple | 단일 값과 배열 구분 | 지원 |

## 예시

Schema:

```json
{
  "name": "runbook",
  "fields": [
    {
      "title": "Title",
      "name": "title",
      "type": "string",
      "required": true
    },
    {
      "title": "Severity",
      "name": "severity",
      "type": "choice",
      "choices": [
        "low",
        "medium",
        "high"
      ],
      "required": true
    },
    {
      "title": "Retry count",
      "name": "retryCount",
      "type": "number",
      "numberOptions": {
        "min": 0,
        "max": 10
      }
    }
  ]
}
```

다음 값은 오류 대상이다.

```yaml
---
fmContentType: runbook
title: ""
severity: urgent
retryCount: "three"
---
```

- 빈 `title`
- enum에 없는 `urgent`
- number가 아닌 `"three"`

## 내장 schema의 한계

현재 content type 정의만으로 다음 규칙을 표현하기 어렵다.

- 문자열 `minLength`, `maxLength`
- regex 또는 `pattern`
- 특정 prefix/suffix
- 배열의 정확한 개수
- 두 field 사이의 관계
- 조건부 required
- 파일·이미지 경로의 실제 존재
- URL 접근 가능 여부
- unknown field 금지
- 프로젝트 전체 unique 값
- 여러 파일 사이의 참조 무결성

`when`은 UI 표시 조건이지 위 규칙을 위한 일반 validation 언어가 아니다.

## Active type 관련 오류

```text
fmContentType 값이 유효함
  → 해당 content type으로 검증

fmContentType 없음 + type 값이 유효함
  → type을 fallback으로 사용

식별 값 없음 또는 미등록 타입
  → default schema가 적용될 수 있음
```

잘못된 문서가 `default`로 조용히 fallback되는 것을 막으려면 별도 CI에서 `fmContentType`의 허용 값을 검사한다.

## UI 검증과 CI 검증

| 목적 | 권장 |
| --- | --- |
| 작성 중 빠른 feedback | Front Matter CMS validation |
| commit 차단 | custom validator + pre-commit |
| repository 전체 검사 | CI |
| regex/cross-field 규칙 | JSON Schema, Zod, Python validator |
| link/path 실제 확인 | 별도 script |

## 외부 validator를 추가할 시점

다음 중 하나면 추가한다.

- `fmContentType`이 반드시 있어야 한다.
- title 길이 제한이 필요하다.
- status에 따라 다른 field가 필수다.
- 경로나 관계 대상이 실제로 존재해야 한다.
- 모든 Markdown을 CI에서 일괄 검사해야 한다.

## 검증 체크리스트

1. `frontMatter.validation.enabled` 확인
1. 문서의 `fmContentType` 또는 `type` 확인
1. content type `name`과 정확히 일치하는지 확인
1. field `type`과 실제 YAML 타입 비교
1. `choice` 값과 enum 비교
1. `required` field의 빈 문자열·빈 배열 확인
1. VS Code Problems 패널 확인
1. 강한 정책은 CI validator로 보완

## 공식 출처

- [Version 10.10.0 release notes](https://frontmatter.codes/updates/v10.10.0)
- [Settings overview](https://frontmatter.codes/docs/settings/overview)
- [ContentTypeSchemaGenerator source](https://github.com/estruyf/vscode-front-matter/blob/main/src/helpers/ContentTypeSchemaGenerator.ts)
