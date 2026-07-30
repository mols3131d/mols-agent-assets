# Front Matter CMS Reference

> 사람과 에이전트가 함께 보는 실무 레퍼런스.
>
> 검토 기준: Front Matter CMS `10.11.x`, 2026-07-30.

이 문서는 공식 문서를 그대로 복제하지 않는다. 자주 쓰는 기능, 설정 관계, 검증 범위와 실무 결정을 한국어로 재구성한다.

## 빠른 결론

- 공유 설정은 repository root의 `frontmatter.json`에 둔다.
- 회사나 다른 도구가 `type`을 사용한다면 Front Matter CMS 전용 식별자로 `fmContentType`을 사용한다.
- `default` content type은 느슨한 fallback으로 유지한다.
- 강한 제약은 전용 content type에서 `required`, `choice`, `numberOptions`로 설정한다.
- regex, 문자열 길이, cross-field 규칙, CI 검증은 별도 validator가 필요하다.
- `contentTypes`는 Markdown front matter 필드가 아니라 `pageFolders`에서 허용 타입을 제한하는 설정이다.

## 문서 구성

| 문서 | 용도 |
| --- | --- |
| [01-configuration.md](01-configuration.md) | 설정 파일, 우선순위, 분리 구성 |
| [02-content-types.md](02-content-types.md) | 타입 선택, 속성, `fmContentType` |
| [03-fields.md](03-fields.md) | field 종류와 주요 옵션 |
| [04-validation.md](04-validation.md) | 내장 검증 범위와 한계 |
| [05-folders-templates-placeholders.md](05-folders-templates-placeholders.md) | 폴더, template, placeholder |
| [06-scripts.md](06-scripts.md) | custom action, post-script, 자동화 |
| [07-recipes.md](07-recipes.md) | 복사 가능한 실무 패턴 |

## 권장 읽기 순서

```text
처음 설정
  → 01 Configuration
  → 02 Content Types
  → 03 Fields

오류·검증
  → 04 Validation

생성 흐름·자동화
  → 05 Folders/Templates
  → 06 Scripts

바로 적용
  → 07 Recipes
```

## SKILL.md에서 연결할 때

전체 내용을 SKILL.md에 복사하지 않는다. 작업별로 필요한 reference만 읽도록 연결한다.

```markdown
## References

- 설정 구조를 변경하기 전 `references/01-configuration.md`를 읽는다.
- content type을 추가·수정할 때 `references/02-content-types.md`를 읽는다.
- field 옵션이 필요할 때 `references/03-fields.md`를 읽는다.
- 검증 가능 여부를 판단할 때 `references/04-validation.md`를 읽는다.
- 복사 가능한 패턴은 `references/07-recipes.md`를 사용한다.
```

## 업데이트 기준

다음 변경이 생기면 이 레퍼런스를 다시 검토한다.

- Front Matter CMS major/minor upgrade
- `frontmatter.schema.json` 또는 content type schema 변경
- validation 진단 범위 변경
- 신규 field type 추가
- `fmContentType` 선택 규칙 변경

## 공식 출처

- [Documentation](https://frontmatter.codes/docs)
- [Settings](https://frontmatter.codes/docs/settings)
- [Updates](https://frontmatter.codes/updates)
- [Official repository](https://github.com/estruyf/vscode-front-matter)
