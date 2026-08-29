# GitHub Authoring Templates

이 directory는 Issue, Pull Request, PR Review와 PR comment에 사용하는 repository-local authoring template을 관리합니다. GitHub가 자동 해석하는 native template 위치가 아니라 사람과 agent가 공통 형식을 재사용하기 위한 source입니다.

GitHub object의 권한, review 의미, merge 조건과 검증 정책은 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다. 이 directory는 repository-wide instruction이나 activation을 소유하지 않습니다.

## Templates

| Surface | Template |
| --- | --- |
| Issue | [`issue.md`](issue.md) |
| Pull Request | [`pull-request.md`](pull-request.md) |
| PR Review | [`pull-request-review.md`](pull-request-review.md) |
| PR conversation comment | [`pull-request-comment.md`](pull-request-comment.md) |
| PR inline review comment | [`pull-request-inline-comment.md`](pull-request-inline-comment.md) |

## Authoring notation

Jinja2-style 표기를 authoring notation으로 사용합니다. 실제 Jinja2 runtime이나 renderer를 요구하지 않습니다.

- `{{ value }}` — 확인된 실제 값으로 치환합니다.
- `{% if condition %} ... {% endif %}` — 조건이 맞을 때만 남깁니다.
- `{% for item in items %} ... {% endfor %}` — 실제 항목 수만큼 펼칩니다.

최종 GitHub text에는 미치환 notation과 작성 지침 comment를 남기지 않습니다.

## Writing rules

- 결론과 판단에 필요한 핵심 정보를 먼저 둡니다.
- 작업 과정이나 시행착오보다 최종 결과와 근거를 기록합니다.
- GitHub UI, CI 또는 canonical artifact가 이미 소유하는 정보는 필요 없이 복제하지 않습니다.
- 독립적으로 훑어야 하는 변경, 근거, 경로와 상태는 긴 문단보다 list를 우선합니다.
- optional section과 metadata는 판단 비용을 줄일 때만 사용하고 빈 section은 제거합니다.
- 모르는 값은 추측하거나 임의의 긍정 상태로 채우지 않습니다.
- 검증 상태는 `✅ Pass`, `❌ Fail`, `⚪ Not Verified`처럼 marker와 text label을 함께 사용합니다.
- repository 내부 path와 artifact는 가능한 한 repository-relative reference를 사용합니다.
- 요구사항이나 결정의 source가 따로 있으면 내용을 다시 쓰기보다 해당 artifact를 연결합니다.

GitHub object title이 이미 최상위 제목 역할을 하므로 본문의 주요 section은 `##`부터 시작합니다.

## Metadata

GitHub가 제공하지 않는 provenance가 실제 판단에 필요할 때만 본문의 마지막에 하나의 `yaml` code block으로 둡니다. Front Matter나 GitHub object metadata로 취급하지 않으며 별도 `Metadata` heading을 만들지 않습니다.

Metadata field는 서로 독립적이며 필요한 field만 사용합니다.

### `author`

`author`는 실제 작성 주체가 GitHub에 표시되는 계정과 다를 때 agent 주도 작성을 식별하는 optional list입니다.

- 사람만 작성했거나 사람이 주도하고 agent가 보조했다면 생략합니다.
- agent가 주도했지만 GitHub 작성자만으로 실제 작성 주체를 구별할 수 없을 때 기록합니다.
- 각 항목은 `<user-id>:<provider>-<service>` 형식의 scalar string을 사용합니다.

### `revision`

`revision`은 Pull Request description이나 PR Review가 기준으로 삼은 exact repository revision pair를 식별하는 optional map입니다.

- 사용하면 `base`와 `head`를 함께 기록합니다.
- 두 값 모두 full commit SHA를 사용하며 움직이는 branch ref는 기록하지 않습니다.
- PR description을 새 base/head 기준으로 갱신하면 `revision`도 함께 갱신합니다.
- Review의 `revision`은 해당 review가 실제 검토한 pair를 고정하며 이후 PR head가 바뀌어도 과거 review 값은 바꾸지 않습니다.

```yaml
author:
  - <user-id>:<provider>-<service>
revision:
  base: <full-base-commit-sha>
  head: <full-head-commit-sha>
```

> [!NOTE]
> `.github/templates/`는 GitHub가 자동으로 적용하는 native Issue/PR template 경로가 아닙니다.
