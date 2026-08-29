# GitHub Authoring Templates

이 directory는 Issue, Pull Request, PR Review와 PR comment에 사용하는 **repository-local authoring template**을 관리합니다. GitHub가 자동 적용하는 native template이 아니라, 사람과 agent가 같은 구조로 빠르게 작성하고 검토하기 위한 source입니다.

> [!NOTE]
> `.github/templates/`는 GitHub가 자동으로 적용하는 native Issue/PR template 경로가 아닙니다.

GitHub object의 권한, review 의미, merge 조건과 검증 정책은 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다. 이 directory는 repository-wide instruction이나 activation을 소유하지 않습니다.

## Templates

| Surface | Template | 용도 |
| --- | --- | --- |
| Issue | [`issue.md`](issue.md) | 문제, 원하는 결과와 완료 조건을 전달 |
| Pull Request | [`pull-request.md`](pull-request.md) | 변경 결과, 검증 근거와 review focus를 전달 |
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

최종 GitHub text에서는 미치환 notation, 작성 지침 comment와 빈 optional section을 제거합니다. Notation은 agent의 사고 과정이나 작업 순서를 강제하지 않습니다.

## Writing rules

- 결론과 판단에 필요한 핵심 정보를 먼저 둡니다. 작업 과정이나 시행착오보다 최종 결과와 근거를 기록합니다.
- 독립적으로 훑어야 하는 변경, 근거, 경로와 상태는 긴 문단보다 list를 우선합니다. 일반 heading에는 장식용 emoji를 사용하지 않습니다.
- GitHub UI, CI 또는 canonical artifact가 이미 소유하는 정보는 필요 없이 복제하지 않습니다. 요구사항이나 결정의 source가 따로 있으면 다시 쓰기보다 연결합니다.
- 모르는 값은 추측하거나 임의의 긍정 상태로 채우지 않습니다.
- 검증 상태는 `✅ Pass`, `❌ Fail`, `⚪ Not Verified`를 사용합니다. `Pass`는 명시한 check가 통과했다는 뜻만 가지며 semantic review나 제한된 inspection을 전체 검증으로 확대 해석하지 않습니다.
- PR Review finding과 Pull Request risk의 importance는 `🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Low`를 사용합니다. 같은 색은 같은 상대적 중요도를 뜻하지만 finding과 risk 자체는 서로 다른 개념입니다.
- PR conversation comment의 optional workflow status는 `🔴 Blocked`, `🟡 Waiting`, `🟢 Ready`를 사용합니다. 현재 진행 상태를 전달할 필요가 없는 일반 comment에서는 생략합니다.
- 색상 원은 importance나 workflow 상태처럼 반복되는 의미를 빠르게 구분할 때만 사용하며 일반 section 장식에는 사용하지 않습니다.
- 같은 finding을 review body와 inline comment에 완전히 중복하지 않습니다. Line-specific finding은 inline comment에 두고, review body에는 cross-cutting finding이나 전체 판단에 필요한 요약만 둡니다.
- repository 내부 path와 artifact는 가능한 한 repository-relative reference를 사용합니다.
- GitHub object title이 이미 최상위 제목 역할을 하므로 본문의 주요 section은 `##`부터 시작합니다.

## Metadata

Metadata는 필요한 경우 **본문 마지막의 fenced `yaml` block 한 곳**에만 둡니다. Front Matter나 GitHub object metadata로 취급하지 않으며 별도 `Metadata` heading도 만들지 않습니다.

허용하는 field는 `author`와 `revision`뿐이며 서로 독립적인 optional field입니다.

- `author` — GitHub 작성자만으로 실제 작성 주체를 구별할 수 없는 agent 주도 작성의 provenance입니다. 각 항목은 `<user-id>:<provider>-<service>` 형식을 사용합니다.
- `revision` — Pull Request description이나 PR Review가 exact diff pair에 의존할 때 사용합니다. `base`와 `head`를 함께 full commit SHA로 기록합니다. PR description을 새 pair 기준으로 갱신하면 함께 갱신하고, 이미 제출된 review의 pair는 이후 head가 바뀌어도 변경하지 않습니다.

`revision`은 Pull Request와 PR Review template에서만 사용합니다. Issue, PR conversation comment와 inline review comment에는 필요한 경우 `author`만 사용합니다. Metadata가 필요 없으면 block 전체를 생략합니다.

```yaml
author:
  - <user-id>:<provider>-<service>
revision:
  base: <full-base-commit-sha>
  head: <full-head-commit-sha>
```
