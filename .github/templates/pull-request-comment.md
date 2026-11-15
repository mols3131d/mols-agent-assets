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

<!-- 기본은 일반 목록. 독립적인 완료 추적이 필요하고 갱신할 때만 체크박스로 교체합니다. -->
{% for action in next_actions %}
- {{ action }}
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
