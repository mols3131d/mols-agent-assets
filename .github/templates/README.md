# GitHub Authoring Templates

이 디렉터리는 이 repository의 Issue, Pull Request, PR Review와 PR comment를 작성할 때 사용하는 **본문 템플릿의 canonical library**입니다.

템플릿은 사람과 agent가 함께 사용합니다. GitHub object의 권한, review 의미, merge 조건과 검증 정책은 이 디렉터리가 아니라 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다.

| Surface | Template |
| --- | --- |
| Issue | [`issue.md`](issue.md) |
| Pull Request | [`pull-request.md`](pull-request.md) |
| PR Review | [`pull-request-review.md`](pull-request-review.md) |
| PR comment | [`pull-request-comment.md`](pull-request-comment.md) |
| PR inline comment | [`pull-request-inline-comment.md`](pull-request-inline-comment.md) |

## Template notation

Jinja2와 비슷한 표기를 **authoring notation**으로 사용합니다. 실제 Jinja2 runtime이나 renderer를 요구하지 않습니다.

- `{{ value }}` — 실제 값으로 치환합니다.
- `{% if condition %} ... {% endif %}` — 조건이 맞을 때만 내용을 남깁니다.
- `{% for item in items %} ... {% endfor %}` — 실제 항목 수만큼 펼칩니다.
- `| default(...)` 같은 filter 표기는 합리적인 기본값의 의도를 나타냅니다.

## Rendering contract

최종 GitHub text를 작성할 때는 다음을 지킵니다.

1. 해당 surface의 템플릿을 기본 구조로 사용합니다.
1. 사실과 확인된 상태만 채웁니다. 모르는 값을 채우기 위해 추측하지 않습니다.
1. 적용되지 않는 optional block은 제거합니다.
1. 미치환 `{{ ... }}`, `{% ... %}`와 작성 지침 comment를 남기지 않습니다.
1. 템플릿의 section이 실제 내용 없이 빈 껍데기가 되면 제거합니다.
1. YAML code block은 사람이 빠르게 훑는 **본문 metadata 요약**입니다. GitHub의 label, assignee, review action, branch 같은 실제 object metadata를 대신하지 않습니다.

Template structure는 기본값입니다. 내용이 아주 짧아 일부 section이 불필요하면 제거할 수 있지만, 핵심 결론·근거·검증·요청처럼 해당 surface의 의미를 바꾸는 정보는 생략하지 않습니다.
