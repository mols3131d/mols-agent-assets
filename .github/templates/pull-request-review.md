## 📌 Summary

<!--
전체 판단과 가장 중요한 근거를 먼저 쓴다.
필요하면 다음 조치를 덧붙이되 GitHub review decision은 본문에 반복하지 않는다.
-->

{{ summary }}

{% if scope %}
## 🧭 Scope

<!--
전체 current diff가 아닌 일부만 검토했거나 특별한 기준을 적용했다면 범위와 한계를 적는다.
전체 current diff를 일반 기준으로 검토했다면 생략한다.
-->

{% for item in scope %}
- {{ item }}
{% endfor %}
{% endif %}

## 🔎 Findings

<!--
확인된 문제만 finding으로 기록한다. 단순 선호나 근거 없는 가능성은 제외한다.
Line-specific finding은 inline review comment에 두고 여기서 완전히 반복하지 않는다.
본문 finding이 없고 qualifying inline finding만 있으면 `See inline review comments for findings.`를 사용한다.
둘 다 없을 때만 `No findings identified in the reviewed scope.`를 사용한다.
Required Change는 필요한 결과나 제약을 적고, 특정 구현이 필수가 아니면 해결 방법을 과도하게 지정하지 않는다.

Importance:
🔴 Critical — 보안·권한·데이터 손실이나 광범위한 장애처럼 즉시 차단해야 하는 문제
🟠 High — correctness, security 또는 repository contract를 실질적으로 깨뜨려 merge 전에 수정해야 하는 문제
🟡 Medium — 범위가 제한적이지만 실제 결함이나 의미 있는 운영·유지보수 위험을 만드는 문제
🔵 Low — 영향이 작고 기본적으로 non-blocking이지만 실제 개선 가치가 있는 문제
-->

{% if findings %}
{% for finding in findings %}
### {{ finding.importance }} · F{{ loop.index }} · {{ finding.title }}

{% if finding.locations %}
**Location**

{% for location in finding.locations %}
- {{ location }}
{% endfor %}
{% endif %}

{% if finding.evidence %}
**Evidence**

{% for item in finding.evidence %}
- {{ item }}
{% endfor %}
{% endif %}

**Impact:** {{ finding.impact }}

{% if finding.required_changes %}
**Required Change**

{% for change in finding.required_changes %}
- {{ change }}
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

## 🧪 Validation

<!--
직접 확인한 check와 근거만 기록한다.
중요한 미확인 영역은 ⚪ Not Verified로 남긴다.
-->

{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}

{% if remaining_risks %}
## ⚠️ Remaining Risks

{% for risk in remaining_risks %}
- {{ risk }}
{% endfor %}
{% endif %}

{% if author or revision %}
```yaml
{% if author %}
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
{% endif %}
{% if revision %}
revision:
  base: {{ revision.base }}
  head: {{ revision.head }}
{% endif %}
```
{% endif %}
