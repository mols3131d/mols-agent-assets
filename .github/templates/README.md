# GitHub Review and Comment Authoring Templates

GitHub에는 PR Review와 comment의 본문을 자동 채우는 native template 기능이 없습니다. 이 디렉터리는 해당 surface를 일관되게 작성하기 위한 **repository-local authoring template**만 관리합니다.

Issue와 Pull Request는 이 디렉터리의 템플릿을 사용하지 않습니다.

- Issue → [GitHub native Issue template](../ISSUE_TEMPLATE/issue.md)
- Pull Request → [GitHub native PR template](../pull_request_template.md)

GitHub object의 작성 의미, validation·importance·workflow status와 provenance는 [GitHub 정책](../../docs/development/github.md)이 소유합니다. 이 README는 Review·Comment 템플릿의 notation과 공통 작성 convention만 설명하며, 각 파일이 자신의 field와 rendering structure를 소유합니다.

## Templates

| Surface | Template | 용도 |
| --- | --- | --- |
| PR Review | [`pull-request-review.md`](pull-request-review.md) | 전체 판단과 finding 기록 |
| PR conversation comment | [`pull-request-comment.md`](pull-request-comment.md) | 결론, 상태와 후속 작업 전달 |
| PR inline review comment | [`pull-request-inline-comment.md`](pull-request-inline-comment.md) | 특정 line의 finding 전달 |

## Authoring notation

다음 Jinja2-style 표기는 **Review·Comment 작성 보조용**입니다. GitHub가 렌더링하거나 실제 Jinja2 runtime이 실행하는 것은 아닙니다.

| Notation | 의미 |
| --- | --- |
| `{{ value }}` | 확인된 실제 값으로 치환 |
| `{% if condition %} ... {% endif %}` | 조건이 맞을 때만 유지 |
| `{% for item in items %} ... {% endfor %}` | 실제 항목 수만큼 반복 |

- 최종 GitHub text에는 미치환 notation, 작성 지침 comment와 빈 optional section을 남기지 않습니다.
- GitHub object title이 최상위 제목이므로 주요 본문 section은 `##`부터 시작합니다.
- 일반 heading에 장식용 emoji를 사용하지 않습니다. Semantic marker와 상태·중요도는 GitHub 정책을 따릅니다.
- 작성 주체와 revision이 필요한 경우 [GitHub 정책](../../docs/development/github.md)의 본문 끝 fenced YAML 표현을 사용합니다.
