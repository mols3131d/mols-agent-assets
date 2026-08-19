---
name: template-driven-markdown
description: Create Markdown documents from repository templates and design reusable templates that agents can reliably complete. Use `.frontmatter/templates/` as the template source, treat template structure as a contract, and distinguish agent-owned slots from Front Matter CMS placeholders.
---

# Template-Driven Markdown

Template-driven writing은 **template이 문서 구조와 writable area를 정의하고 agent는 선언된 영역만 채우는 방식**입니다.

이 문서는 두 작업을 다룹니다.

1. Existing template에서 Markdown document 생성
1. 반복 사용 가능한 template 생성·개선

## Source

Template은 `.frontmatter/templates/`와 그 하위 directory에서만 찾습니다. Skill 내부에 fallback template을 복제하지 않습니다.

Front Matter CMS는 optional selection context입니다. Extension이 없어도 template workflow 자체는 동작해야 합니다.

## Template Contract

Template은 다음 두 영역을 사용합니다.

```markdown
# Template Instructions

Template을 채우는 방법과 constraint.

--- TEMPLATE CONTENT ---

실제 output template.
```

`Template Instructions`와 boundary marker는 generated document에 포함하지 않습니다. `Template Content`의 fixed text, heading order, front matter key와 reserved placeholder는 사용자가 template 자체 변경을 요청하지 않는 한 보존합니다.

## Placeholders

| Syntax | 용도 | 처리 |
| --- | --- | --- |
| `<<slot:key>>` | 짧은 scalar value | 적절한 값으로 대체 |
| `<<slot:key|default>>` | default가 있는 scalar | context가 더 나은 값을 주지 않을 때만 default 사용 |
| `<<block:key>>` | paragraph/list/section 등 multiline content | instructions에 따라 작성하거나 optional이면 제거 |
| `{{...}}` | Front Matter CMS 등 다른 runtime의 reserved placeholder | 명시 요청 없이는 그대로 보존 |

`slot` key는 안정적인 kebab-case를 사용합니다. Boolean/number slot은 template이 의도한 YAML type을 문자열로 바꾸지 않습니다.

모든 slot/block의 의미, required/optional 여부와 omission rule은 `Template Instructions`가 설명해야 합니다.

## Creating Templates

1. 반복되는 문서 목적과 stable structure를 식별합니다.
1. Fixed content와 variable content를 분리합니다.
1. 짧은 값은 `slot`, 판단이 필요한 multiline content는 `block`으로 둡니다.
1. 각 placeholder의 의미와 optionality를 instructions에 명시합니다.
1. Fixed heading, policy text와 front matter key는 Template Content에 둡니다.
1. `.frontmatter/templates/` 아래에 저장합니다.

다음을 피합니다.

- sentence fragment마다 placeholder를 만드는 과분할
- `TODO`, 빈 heading 또는 모호한 braces를 placeholder로 사용
- agent-owned value에 `{{...}}` 사용
- optionality를 암묵적으로 처리
- 사실상 같은 목적의 template을 여러 개 유지

## Generating Documents

Template 선택 우선순위:

1. 사용자가 지정한 exact path/file
1. Applicable Front Matter CMS content type이 연결한 template
1. 요청한 document type과 명확히 일치하는 unique template
1. 사용 가능한 template이 하나뿐인 경우 그 template

여러 후보가 동일하게 타당하면 임의 선택하지 않고 필요한 경우 한 번의 focused selection question을 사용합니다.

생성 workflow:

1. Selected template 전체를 읽습니다.
1. Instructions와 Template Content를 분리합니다.
1. 모든 slot/block과 required/optional 조건을 확인합니다.
1. User input과 repository context에서 근거 있는 값만 수집합니다.
1. 선언된 slot/block만 채웁니다.
1. Instructions와 boundary marker를 제거하고 fixed content/reserved placeholder를 보존합니다.
1. Completion checks를 수행합니다.

필수 값이 context에 없으면 project fact, command, path, approval status, compatibility 또는 validation result를 발명하지 않습니다. Optional block은 instructions가 허용할 때만 제거합니다.

## Front Matter CMS

Root `frontmatter.json`이 존재하면 applicable content type, field shape와 linked template을 selection/validation context로 사용합니다. Product option semantics는 local copy가 아니라 current configuration과 [Front Matter CMS official-source router](../common/tooling/front-matter-cms/README.md)에서 확인합니다.

## Completion Checks

- Source template이 `.frontmatter/templates/` 아래에서 왔는가?
- `# Template Instructions`와 `--- TEMPLATE CONTENT ---`가 output에서 제거됐는가?
- unresolved `<<slot:` 또는 `<<block:` marker가 남지 않았는가?
- required area가 meaningful content로 채워졌는가?
- optional area는 valid하게 채우거나 제거했는가?
- reserved `{{...}}` placeholder가 그대로 유지됐는가?
- fixed heading, order, wording과 front matter key가 보존됐는가?
- unsupported claim을 추가하지 않았는가?

완성 후 생성한 Markdown 또는 template path와 실제 blocking input만 보고합니다.
