<!-- 결론과 현재 상태를 첫 문장에서 전달합니다.
status는 판단에 필요할 때만 사용하고, 없는 상태를 만들지 않습니다.
실제 후속 행동과 근거가 없으면 선택 섹션을 생략합니다.
새 H3 제목은 긴 섹션의 탐색성을 개선할 때만 추가합니다. -->

{% if status %}
**{{ status }}**

{% endif %}
{{ message }}

{% if next_actions %}
## Next Actions

<!-- Next Actions는 실제로 완료를 추적할 후속 작업만 넣습니다.
단순한 제안이나 안내는 본문 메시지에 적습니다. -->
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

<!-- Agent가 작성한 최종 Comment에는 author를 본문 끝의 fenced yaml로 기록합니다. -->
{% if author %}
```yaml
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
```
{% endif %}
