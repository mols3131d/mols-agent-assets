# GitHub Authoring Templates

이 directory는 Issue, Pull Request, PR Review와 PR comment에 사용하는 **repository-local authoring template**을 관리합니다. GitHub가 자동 적용하는 native template이 아니라, 사람과 agent가 같은 구조로 빠르게 작성하고 검토하기 위한 source입니다.

> [!NOTE]
> `.github/templates/`는 GitHub가 자동으로 적용하는 native Issue/PR template 경로가 아닙니다.

GitHub object의 작성 의미, validation·importance·workflow status, provenance와 협업 정책은 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다. 이 directory는 template의 field, notation과 rendering 구조만 소유합니다.

## Templates

| Surface | Template | 용도 |
| --- | --- | --- |
| Issue | [`issue.md`](issue.md) | 문제, 원하는 결과와 완료 조건을 전달 |
| Pull Request | [`pull-request.md`](pull-request.md) | 변경 결과, 검증 근거, risk와 review focus를 전달 |
| PR Review | [`pull-request-review.md`](pull-request-review.md) | 전체 판단과 finding을 기록 |
| PR conversation comment | [`pull-request-comment.md`](pull-request-comment.md) | 결론, workflow 상태와 필요한 후속 작업을 짧게 전달 |
| PR inline review comment | [`pull-request-inline-comment.md`](pull-request-inline-comment.md) | 특정 line의 한 가지 finding을 전달 |

## Authoring notation

Jinja2-style 표기는 template 구조를 표현하기 위한 authoring notation입니다. 실제 Jinja2 runtime이나 renderer를 요구하지 않습니다.

| Notation | 의미 |
| --- | --- |
| `{{ value }}` | 확인된 실제 값으로 치환 |
| `{% if condition %} ... {% endif %}` | 조건이 맞을 때만 유지 |
| `{% for item in items %} ... {% endfor %}` | 실제 항목 수만큼 반복 |

Notation은 agent의 사고 과정이나 작업 순서를 강제하지 않습니다.

## Template conventions

- 최종 GitHub text에서는 미치환 notation, 작성 지침 comment와 빈 optional section을 제거합니다.
- Template comment에 적힌 literal value는 그대로 사용하고, 그 값의 의미와 우선순위는 [`docs/development/github.md`](../../docs/development/github.md)를 따릅니다.
- repository 내부 path와 artifact는 가능한 한 repository-relative reference를 사용합니다.
- 일반 heading에는 장식용 emoji를 사용하지 않습니다. Semantic marker가 필요한 field는 각 template contract에 따릅니다.
- GitHub object title이 이미 최상위 제목 역할을 하므로 본문의 주요 section은 `##`부터 시작합니다.

## Metadata rendering

Metadata가 필요한 template은 **본문 마지막의 fenced `yaml` block 한 곳**에만 렌더링합니다. Front Matter나 GitHub object metadata로 취급하지 않으며 별도 `Metadata` heading도 만들지 않습니다.

현재 template contract에서 사용하는 field는 `author`와 `revision`뿐입니다. 각 field의 의미와 적용 surface는 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다. Metadata가 필요 없으면 block 전체를 생략합니다.

```yaml
author:
  - <user-id>:<provider>-<service>
revision:
  base: <full-base-commit-sha>
  head: <full-head-commit-sha>
```
