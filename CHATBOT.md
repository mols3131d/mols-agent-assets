# `CHATBOT.md`

이 파일은 이 repository를 작업하는 chatbot의 **compatibility entrypoint**입니다. Chat runtime에서 가능한 한 local agent harness와 같은 repository context discovery가 작동하도록 연결하는 최소한의 bootstrap만 소유합니다.

1. 먼저 root [`AGENTS.md`](AGENTS.md)를 읽고 현재 작업에 적용되는 repository instruction을 따릅니다.
1. 작업 대상 경로가 정해지면 root부터 해당 경로까지 존재하는 `AGENTS.md`를 확인하고, 더 좁은 scope의 instruction이 있으면 함께 적용합니다.
1. 이어서 [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)를 읽고 그 routing contract에 따라 현재 작업에 필요한 Agent Asset만 선택해 로드합니다.
1. 작업 범위나 대상 경로가 실질적으로 바뀌면 적용되는 instruction과 route selection을 다시 평가합니다.

`CHATBOT.md`는 repository policy, Agent Asset behavior, routing semantics 또는 각 문서의 내용을 복제하거나 재정의하지 않습니다. 연결된 canonical source가 항상 authoritative합니다.
