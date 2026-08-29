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

최종 GitHub text에는 미치환 notation과 작성 지침 comment를 남기지 않습니다. Notation은 구조를 표현하는 authoring aid일 뿐 agent의 사고 과정이나 작업 순서를 강제하지 않습니다.

## Writing rules

- 결론과 판단에 필요한 핵심 정보를 먼저 둡니다.
- 작업 과정이나 시행착오보다 최종 결과와 근거를 기록합니다.
- GitHub UI, CI 또는 canonical artifact가 이미 소유하는 정보는 필요 없이 복제하지 않습니다.
- 같은 review finding을 review body와 inline comment에 완전히 중복하지 않습니다. Line-specific finding은 inline comment를 우선하고, review body에는 cross-cutting finding이나 전체 판단에 필요한 요약만 둡니다.
- 독립적으로 훑어야 하는 변경, 근거, 경로와 상태는 긴 문단보다 list를 우선합니다.
- optional section과 metadata는 판단 비용을 줄일 때만 사용하고 빈 section은 제거합니다.
- 모르는 값은 추측하거나 임의의 긍정 상태로 채우지 않습니다.
- 검증 상태는 `✅ Pass`, `❌ Fail`, `⚪ Not Verified`처럼 marker와 text label을 함께 사용합니다.
- `Pass`는 **명시한 check가 통과했다는 뜻만** 가집니다. Semantic review, self-review나 제한된 inspection 결과를 deterministic test, runtime verification 또는 전체 변경의 검증으로 확대 해석하지 않습니다.
- repository 내부 path와 artifact는 가능한 한 repository-relative reference를 사용합니다.
- 요구사항이나 결정의 source가 따로 있으면 내용을 다시 쓰기보다 해당 artifact를 연결합니다.

GitHub object title이 이미 최상위 제목 역할을 하므로 본문의 주요 section은 `##`부터 시작합니다.

## Metadata

Metadata는 필요한 경우 **본문 마지막의 fenced `yaml` block 한 곳**에만 둡니다. Front Matter나 GitHub object metadata로 취급하지 않으며 별도 `Metadata` heading도 만들지 않습니다.

허용하는 field는 `author`와 `revision`뿐입니다. 둘은 서로 독립적인 optional field이며 실제 판단에 필요한 것만 남깁니다.

- `author` — GitHub 작성자만으로 실제 작성 주체를 구별할 수 없는 agent 주도 작성의 provenance입니다. 각 항목은 `<user-id>:<provider>-<service>` 형식을 사용합니다.
- `revision` — Pull Request description이나 PR Review가 exact diff pair에 의존할 때 사용하는 provenance입니다. `base`와 `head`를 함께 full commit SHA로 기록합니다. PR description을 새 pair 기준으로 갱신하면 함께 갱신하고, 이미 제출된 review의 pair는 이후 head가 바뀌어도 변경하지 않습니다.

Issue와 일반 comment에는 exact revision pair가 판단에 특별히 필요하지 않으면 `revision`을 추가하지 않습니다. Metadata가 필요 없으면 block 전체를 생략합니다.

```yaml
author:
  - <user-id>:<provider>-<service>
revision:
  base: <full-base-commit-sha>
  head: <full-head-commit-sha>
```

> [!NOTE]
> `.github/templates/`는 GitHub가 자동으로 적용하는 native Issue/PR template 경로가 아닙니다.
