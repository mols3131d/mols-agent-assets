# `CHATBOT.md`

이 repository를 작업하는 chatbot은 먼저 root [`AGENTS.md`](AGENTS.md)를 읽고 현재 작업에 적용되는 repository instruction을 따릅니다. 이어서 [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)를 읽고 task-relevant Agent Asset만 선택해 로드합니다.

이 파일은 native repository instruction과 Agent Asset discovery가 충분하지 않은 chat runtime을 위한 최소 compatibility bootstrap입니다. Repository policy, Agent Asset behavior와 routing semantics를 복제하거나 소유하지 않습니다.
