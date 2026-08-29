# GitHub Authoring Templates

이 directory는 Issue, Pull Request, PR Review와 PR comment에 사용하는 **repository-local authoring template**을 관리합니다. GitHub가 자동 적용하는 native template이 아니라, 사람과 agent가 같은 구조로 빠르게 작성하고 검토하기 위한 source입니다.

> [!NOTE]
> `.github/templates/`는 GitHub가 자동으로 적용하는 native Issue/PR template 경로가 아닙니다.

GitHub object의 권한, review 의미, merge 조건과 검증 정책은 [`docs/development/github.md`](../../docs/development/github.md)가 소유합니다. 이 directory는 repository-wide instruction이나 activation을 소유하지 않습니다.

## 빠르게 선택하기

| Surface | Template | 핵심 용도 |
| --- | --- | --- |
| Issue | [`issue.md`](issue.md) | 문제와 원하는 결과, 완료 조건을 명확히 전달 |
| Pull Request | [`pull-request.md`](pull-request.md) | 변경 결과, 검증 근거와 review focus를 전달 |
| PR Review | [`pull-request-review.md`](pull-request-review.md) | 전체 판단, finding과 검증 근거를 기록 |
| PR conversation comment | [`pull-request-comment.md`](pull-request-comment.md) | 결론과 필요한 후속 작업을 짧게 전달 |
| PR inline review comment | [`pull-request-inline-comment.md`](pull-request-inline-comment.md) | 특정 line의 한 가지 논점과 필요한 변경을 전달 |

## 사용 방법

1. GitHub surface에 맞는 template을 선택합니다.
1. `{{ value }}`를 확인된 값으로 채우고, 조건이 맞지 않는 optional section은 제거합니다.
1. 최종 text에서는 미치환 notation과 작성 지침 comment를 모두 제거합니다.
1. provenance가 실제 판단에 필요할 때만 본문 마지막에 metadata를 남깁니다.

## Authoring notation

Jinja2-style 표기는 구조를 표현하는 authoring notation입니다. 실제 Jinja2 runtime이나 renderer를 요구하지 않습니다.

| Notation | 의미 |
| --- | --- |
| `{{ value }}` | 확인된 실제 값으로 치환 |
| `{% if condition %} ... {% endif %}` | 조건이 맞을 때만 유지 |
| `{% for item in items %} ... {% endfor %}` | 실제 항목 수만큼 반복 |

Notation은 agent의 사고 과정이나 작업 순서를 강제하지 않습니다.

## Writing rules

### 구조와 가시성

- 결론과 판단에 필요한 핵심 정보를 먼저 둡니다.
- 작업 과정이나 시행착오보다 최종 결과와 근거를 기록합니다.
- 독립적으로 훑어야 하는 변경, 근거, 경로와 상태는 긴 문단보다 list를 우선합니다.
- optional section은 판단 비용을 줄일 때만 사용하고 빈 section은 제거합니다.
- GitHub object title이 이미 최상위 제목 역할을 하므로 본문의 주요 section은 `##`부터 시작합니다.
- 일반 heading에는 장식용 emoji를 사용하지 않습니다.

### 근거와 상태

- 모르는 값은 추측하거나 임의의 긍정 상태로 채우지 않습니다.
- 검증 상태는 `✅ Pass`, `❌ Fail`, `⚪ Not Verified`처럼 marker와 text label을 함께 사용합니다.
- PR Review의 importance는 `🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Low`처럼 색상 원 marker와 label을 함께 사용합니다.
- `Pass`는 **명시한 check가 통과했다는 뜻만** 가집니다. Semantic review, self-review나 제한된 inspection을 deterministic test, runtime verification 또는 전체 변경의 검증으로 확대 해석하지 않습니다.
- 같은 review finding을 review body와 inline comment에 완전히 중복하지 않습니다. Line-specific finding은 inline comment를 우선하고, review body에는 cross-cutting finding이나 전체 판단에 필요한 요약만 둡니다.

### 중복과 연결

- GitHub UI, CI 또는 canonical artifact가 이미 소유하는 정보는 필요 없이 복제하지 않습니다.
- repository 내부 path와 artifact는 가능한 한 repository-relative reference를 사용합니다.
- 요구사항이나 결정의 source가 따로 있으면 내용을 다시 쓰기보다 해당 artifact를 연결합니다.

## Metadata

Metadata는 필요한 경우 **본문 마지막의 fenced `yaml` block 한 곳**에만 둡니다. Front Matter나 GitHub object metadata로 취급하지 않으며 별도 `Metadata` heading도 만들지 않습니다.

허용하는 field는 `author`와 `revision`뿐이며 서로 독립적인 optional field입니다.

| Field | 사용 시점 |
| --- | --- |
| `author` | GitHub 작성자만으로 실제 작성 주체를 구별할 수 없는 agent 주도 작성의 provenance가 필요할 때 |
| `revision` | Pull Request description이나 PR Review가 exact diff pair에 의존할 때 |

- `author`의 각 항목은 `<user-id>:<provider>-<service>` 형식을 사용합니다.
- `revision`은 `base`와 `head`를 함께 full commit SHA로 기록합니다. PR description을 새 pair 기준으로 갱신하면 함께 갱신하고, 이미 제출된 review의 pair는 이후 head가 바뀌어도 변경하지 않습니다.
- `revision`은 Pull Request와 PR Review template에서만 사용합니다. Issue, PR conversation comment와 inline review comment에는 필요한 경우 `author`만 사용합니다.
- Metadata가 필요 없으면 block 전체를 생략합니다.

```yaml
author:
  - <user-id>:<provider>-<service>
revision:
  base: <full-base-commit-sha>
  head: <full-head-commit-sha>
```
