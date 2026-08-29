## Summary

<!--
전체 판단과 가장 중요한 근거를 먼저 쓴다.
필요하면 다음 조치를 덧붙이되 GitHub review decision은 본문에 반복하지 않는다.
-->

{{ summary }}

{% if scope %}
## Scope

<!-- 전체 diff가 아닌 일부만 검토했거나 특별한 기준을 적용했을 때만 범위와 한계를 적는다. -->

{% for item in scope %}
- {{ item }}
{% endfor %}
{% endif %}

## Findings

<!--
확인된 문제만 finding으로 기록한다. 단순 선호나 근거 없는 가능성은 제외한다.
Finding의 review body / inline placement와 중복 경계는 `docs/development/github.md`를 따른다.
본문 finding이 없고 qualifying inline finding만 있으면 `See inline review comments for findings.`를 사용한다.
둘 다 없을 때만 `No findings identified in the reviewed scope.`를 사용한다.
Required Change는 문제를 해소하기 위해 필요한 결과나 제약을 적고, 특정 구현이 필수가 아니면 해결 방법을 과도하게 지정하지 않는다.
`finding.importance`는 `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🔵 Low` 중 하나를 그대로 사용한다. 의미와 정렬 기준은 `docs/development/github.md`를 따른다.
-->

{% if findings %}
{% for finding in findings %}
### {{ finding.importance }} · F{{ loop.index }} — {{ finding.title }}

**Impact:** {{ finding.impact }}

{% if finding.required_changes %}
**Required Change**

{% for change in finding.required_changes %}
- {{ change }}
{% endfor %}
{% endif %}

{% if finding.evidence %}
**Evidence**

{% for item in finding.evidence %}
- {{ item }}
{% endfor %}
{% endif %}

{% if finding.locations %}
**Location**

{% for location in finding.locations %}
- {{ location }}
{% endfor %}
{% endif %}

{% if finding.uncertainty %}
**Uncertainty:** {{ finding.uncertainty }}
{% endif %}

{% endfor %}
{% elif has_inline_findings %}
See inline review comments for findings.
{% else %}
No findings identified in the reviewed scope.
{% endif %}

## Validation

<!--
직접 확인한 check와 근거만 기록한다.
`check.status`는 `✅ Pass` / `❌ Fail` / `⚪ Not Verified` 중 하나를 그대로 사용하고 의미와 정렬 기준은 `docs/development/github.md`를 따른다.
-->

{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}

{% if remaining_risks %}
## Remaining Risks

{% for risk in remaining_risks %}
- {{ risk }}
{% endfor %}
{% endif %}

<!--
Agent가 최종 PR Review text를 실질적으로 작성하거나 재작성했다면 `author`는 필수입니다.
이 template은 특정 diff pair를 평가하므로 `revision`을 항상 기록합니다.
-->
```yaml
{% if author %}
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
{% endif %}
revision:
  base: {{ revision.base }}
  head: {{ revision.head }}
```
