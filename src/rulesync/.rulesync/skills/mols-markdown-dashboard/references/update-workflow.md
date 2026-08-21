# Update Workflow

기존 dashboard를 현재 근거에 맞게 갱신할 때만 읽는다.

## Source Order

1. host repository의 documented authority model에 따라 현재 canonical spec 또는 contract, source code, tests와 실행 근거를 확인한다.
1. 기존 YAML을 이전 snapshot의 구조화된 주장으로 읽는다.
1. 기존 Markdown은 렌더 결과로 취급한다. YAML과 충돌하면 현재 근거를 우선한다.

Plan, change, task, design 같은 work artifact는 host policy가 authoritative로 정의하지 않는 한 current contract source로 자동 승격하지 않는다.

## Update

1. dashboard level과 item identity가 여전히 유효한지 확인한다.
1. snapshot과 current focus를 현재 기준으로 갱신한다.
1. 각 item의 Requirement와 Verification Target을 현재 근거와 다시 대조한다.
1. status, denominator 또는 gap identity가 바뀌면 근거를 확인한 뒤 YAML을 수정한다.
1. risks와 references에서 stale 항목을 제거하거나 갱신한다.
1. Markdown을 다시 렌더링하고 stale content가 남지 않았는지 확인한다.

Renderer-managed Markdown의 직접 수정은 다음 render에서 보존된다고 가정하지 않는다. 추가 visual이나 custom section을 dashboard projection 안에 유지해야 하면 selected template이 소유하게 하고, 별도 artifact로 충분하면 dashboard에서는 reference만 둔다.
