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

- 최종 GitHub text에는 [GitHub 정책](../../docs/development/github.md)의 surface별 필수 섹션을 남기고 선택 섹션만 필요에 따라 추가합니다. 미치환 notation, 작성 지침 comment나 빈 선택 섹션은 제거합니다.
- GitHub object title을 H1로 취급하고 템플릿은 H2까지만 정의합니다. H3 이하는 섹션이 길어 구분이 필요할 때 작성자가 선택합니다.
- 체크박스는 실제 추적 작업에, 표는 비교에, 진행 표시는 확인된 집계에, Mermaid는 복잡한 관계에만 선택적으로 사용합니다. 공통 기준은 [GitHub 정책](../../docs/development/github.md)을 따릅니다.
- 장식용 emoji를 heading에 사용하지 않습니다. 상태·중요도는 GitHub 정책을 따릅니다.
- 이 표기는 GitHub가 렌더링하는 작성 보조용이지 실행되는 Jinja2가 아닙니다. 본문 metadata가 필요하면 본문 끝의 단일 fenced `yaml`을 사용하고 GitHub의 native frontmatter로 오인하지 않습니다.
