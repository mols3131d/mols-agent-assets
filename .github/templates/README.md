# GitHub Authoring Templates

이 디렉터리는 이 repository의 Issue, Pull Request, PR Review와 PR comment를 작성할 때 참고하는 **본문 authoring library**입니다.

템플릿은 사람과 agent가 함께 사용할 수 있습니다. 이 디렉터리는 repository-wide instruction이나 activation을 소유하지 않으며, GitHub object의 권한·review 의미·merge 조건·검증 정책은 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다.

> [!NOTE]
> `.github/templates/`는 GitHub가 자동으로 적용하는 native Issue/PR template 경로가 아닙니다.

| Surface | Template |
| --- | --- |
| Issue | [`issue.md`](issue.md) |
| Pull Request | [`pull-request.md`](pull-request.md) |
| PR Review | [`pull-request-review.md`](pull-request-review.md) |
| PR conversation comment | [`pull-request-comment.md`](pull-request-comment.md) |
| PR inline review comment | [`pull-request-inline-comment.md`](pull-request-inline-comment.md) |

## Template notation

Jinja2-style 표기를 authoring notation으로 사용합니다. 실제 Jinja2 runtime이나 renderer를 요구하지 않습니다.

- `{{ value }}` — 확인된 실제 값으로 치환합니다.
- `{% if condition %} ... {% endif %}` — 조건이 맞을 때만 내용을 남깁니다.
- `{% for item in items %} ... {% endfor %}` — 실제 항목 수만큼 펼칩니다.

## Rendering contract

최종 GitHub text에는 **확인된 정보와 실제로 필요한 section만** 남깁니다.

1. 해당 surface의 템플릿을 기본 구조로 사용합니다.
1. 모르는 값은 추측하거나 임의의 기본값으로 채우지 않습니다.
1. 적용되지 않는 optional block과 빈 section은 제거합니다.
1. 미치환 `{{ ... }}`, `{% ... %}`와 작성 지침 comment를 남기지 않습니다.
1. YAML code block에는 GitHub UI가 이미 충분히 보여주는 정보보다 본문을 빠르게 이해하는 데 필요한 metadata를 우선합니다.
1. YAML code block은 본문 요약일 뿐 GitHub의 label, assignee, review action 같은 실제 object metadata를 대신하지 않습니다.

GitHub object title이 이미 최상위 제목 역할을 하므로 본문의 주요 section은 `##`부터 시작합니다. 짧은 내용은 불필요한 section을 제거하되 해당 surface의 판단에 필요한 핵심 정보는 보존합니다.
