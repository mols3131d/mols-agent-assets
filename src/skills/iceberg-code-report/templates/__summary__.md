---
title: '{{Title}}'
datetime: 'yyyy-MM-dd HH:mm'
type: 'code-report-summary'
scope: '{{report_target}}'
---

<!--
Code report summary template. 코드와 테스트로 확인한 내용만 작성한다.
-->
## Overview

<!-- 해결하는 문제, 주요 입력·출력, 분석 범위, 핵심 기술을 먼저 요약한다. -->

{{overview}}

## System Map

<!-- 핵심 관계가 본문보다 단순할 때만 Mermaid 또는 ASCII diagram을 사용한다. -->

```mermaid
flowchart LR
    {{entrypoint}} --> {{core_component}}
    {{core_component}} --> {{boundary}}
```

## Core Components

| Component | Responsibility | Input / Output | Dependencies |
| --- | --- | --- | --- |
| [`{{component}}`]({{link}}) | {{responsibility}} | {{input_output}} | {{dependencies}} |
| [`{{additional_component}}`]({{additional_link}}) | {{additional_responsibility}} | {{additional_input_output}} | {{additional_dependencies}} |

## Core Execution Walkthroughs

### {{walkthrough_title}}

1. **Start**: {{start_condition}}
2. **Call flow**: {{call_sequence}}
3. **State**: {{state_access_or_change}}
4. **Result**: {{return_result}}
5. **Failure boundary**: {{failure_boundary}}

## Code Reading Guide

1. [`{{file}}:{{line}}`]({{file_link}}) — {{reading_reason}}
2. [`{{additional_file}}:{{additional_line}}`]({{additional_file_link}}) — {{additional_reading_reason}}

## Understanding Notes

- **Contract**: {{contract}}
- **Boundary**: {{system_boundary}}
- **Inference / Unverified**: {{uncertainty}}
- **Terminology**: {{terminology}}
