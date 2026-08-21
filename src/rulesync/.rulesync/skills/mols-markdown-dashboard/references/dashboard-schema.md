# Dashboard Schema

## Root

```yaml
version: 1

dashboard:
  level: project | domain
  title: <string>
  snapshot: <date, version, or revision string>
  current_focus: <one concise sentence>
  include_total: true

items: []
risks: []       # optional
references: []  # optional
```

## Item

```yaml
- name: <Domain or Capability>
  implementation:
    status: not_started | planned | in_progress | implemented | blocked | unknown
    progress: 3/4
    gaps:
      - <remaining Requirement>
  verification:
    status: unverified | partial | passing | failing | blocked | unknown
    progress: 2/4
    gaps:
      - <unverified Target>
      - state: failing | unverified | blocked | manual
        text: <remaining Verification Target>
```

`progress`는 짧은 `n/n` 문자열을 권장한다. 다음 mapping도 허용한다.

```yaml
progress:
  completed: 3
  total: 4
```

## Verification Gap State

| Code | Prefix | Meaning |
| --- | :---: | --- |
| `unverified` | ⚪ | 아직 검증하지 않음 |
| `failing` | 🔴 | 현재 검증 실패 |
| `blocked` | 🟠 | 실행 불가 |
| `manual` | 🟡 | 수동 확인만 존재 |

문자열 하나만 쓰면 `unverified`로 처리한다. `failing` gap은 현재 결과가 있으므로 progress 분자에 포함될 수 있다.
`unverified`, `blocked`, `manual` gap의 개수는 `total - completed`와 일치해야 한다.

## Strict Input Policy

- 정의되지 않은 root, dashboard, item, progress, gap, risk 필드는 오류로 처리한다.
- schema version이 지원 범위를 벗어나면 추측해 변환하지 않는다.
- title, snapshot, current focus, item name, gap text, risk text와 reference 같은 text field는 YAML string이어야 한다.
- date처럼 YAML parser가 다른 scalar type으로 해석할 수 있는 text는 따옴표로 명시한다.
- title, snapshot, current focus, item name과 reference는 한 줄이어야 한다.
- 표 셀의 pipe와 여러 줄 gap은 renderer가 안전하게 escape한다.

## Consistency Invariants

- `implemented`는 implementation progress가 완료돼야 한다.
- `implemented`에는 implementation gap이 없어야 한다.
- `not_started`와 `planned`는 implementation completed가 `0`이어야 한다.
- `in_progress`는 implementation이 미완료여야 하며 실제 작업이 시작됐다면 completed가 `0`일 수도 있다.
- `passing`은 verification progress가 완료돼야 한다.
- `passing`에는 verification gap이 없어야 한다.
- `unverified`는 verification completed가 `0`이어야 한다.
- `partial`은 하나 이상의 current result와 하나 이상의 result 없는 Target이 있어야 한다.
- progress는 `0 <= completed <= total`, `total > 0`이어야 한다.
- item name은 dashboard 안에서 중복될 수 없다.

## Risks

```yaml
risks:
  - area: <Domain or Capability>
    text: <risk or blocker>
    impact: <development impact>
```

## References

```yaml
references:
  - <path, artifact id, command, or source label>
```

Markdown link가 필요하면 YAML string 안에 그대로 작성할 수 있다.
