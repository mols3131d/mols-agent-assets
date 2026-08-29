<!--
첫 문장에서 comment의 목적과 현재 결론을 바로 전달한다.
`status`는 workflow 상태를 명확히 전달할 때만 사용한다.
- `🔴 Blocked` — 다음 작업을 진행할 수 없음
- `🟡 Waiting` — 외부 결과나 의존성을 기다리는 중
- `🟢 Unblocked` — 명시한 다음 작업을 막는 알려진 blocker가 없음
Next Actions는 실제 후속 행동이 있을 때만 남기고, Evidence는 판단 근거가 필요할 때만 보충한다.
-->

{% if status %}
**{{ status }}**

{% endif %}
{{ message }}

{% if next_actions %}
## Next Actions

{% for action in next_actions %}
- [ ] {{ action }}
{% endfor %}
{% endif %}

{% if evidence %}
## Evidence

{% for item in evidence %}
- {{ item }}
{% endfor %}
{% endif %}

{% if author %}
```yaml
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
```
{% endif %}
