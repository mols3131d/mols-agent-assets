# Update Workflow

기존 dashboard를 현재 근거에 맞게 갱신할 때만 읽는다.

## Source Order

1. 현재 canonical spec, source code, tests와 실행 근거를 확인한다.
2. 기존 YAML을 이전 snapshot의 구조화된 주장으로 읽는다.
3. 기존 Markdown은 렌더 결과로 취급한다. YAML과 충돌하면 현재 근거를 우선한다.

## Update

1. dashboard level과 item identity가 여전히 유효한지 확인한다.
2. snapshot과 current focus를 현재 기준으로 갱신한다.
3. 각 item의 Requirement와 Verification Target을 현재 근거와 다시 대조한다.
4. status, denominator 또는 gap identity가 바뀌면 근거를 확인한 뒤 YAML을 수정한다.
5. risks와 references에서 stale 항목을 제거하거나 갱신한다.
6. Markdown을 다시 렌더링하고 stale content가 남지 않았는지 확인한다.

핵심 표의 수동 Markdown 수정은 재렌더링 시 보존된다고 가정하지 않는다.
