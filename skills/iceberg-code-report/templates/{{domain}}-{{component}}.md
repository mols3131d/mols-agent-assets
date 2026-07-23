---
title: '{{domain}}-{{component}}'
description: '{{description}}'
type: 'code-report-component'
domain: '{{domain}}'
---

<!--
Core component report template. 평가나 개선 권고 없이 현재 동작을 설명한다.
-->
- Location: [{{location}}](/{{location_link}})

## Summary

{{summary}}

## Responsibility

**[{{domain}}] {{heading}}**: {{responsibility}}

- Input: {{input}}
- Output: {{output}}
- Direct dependencies: {{dependencies}}

## Execution Flow

1. **Start**: {{start_condition}}
2. **Calls**: {{call_sequence}}
3. **State**: {{state_access_or_change}}
4. **Return**: {{return_result}}

## Boundaries

**Failure boundary**: {{failure_boundary}}

- External system: {{external_system}}
- Transaction / read-write boundary: {{data_boundary}}
- Contract / invariant: {{contract}}

## Evidence

- [{{symbol}}](/{{symbol_link}}): {{verified_fact}}
- [{{test_symbol}}](/{{test_link}}): {{test_contract}}
- Unverified / inference: {{uncertainty}}
