# `CHATBOT.md`

이 파일은 이 repository를 작업하는 chatbot의 **compatibility entrypoint**입니다. Chat runtime에서 가능한 한 local agent harness와 같은 repository context discovery가 작동하도록 연결하는 최소한의 bootstrap만 소유합니다.

1. 먼저 root [`AGENTS.md`](AGENTS.md)를 읽고 현재 작업에 적용되는 repository instruction을 따릅니다.
1. 구체적인 GitHub repository나 object(repository, path, ref, Pull Request, Issue, check, workflow, release 등)를 대상으로 읽기·변경·tool action을 수행하는 task라면, 기억이나 이전 대화만 믿지 말고 현재 repository와 관련 ref/object를 live state에서 먼저 식별합니다.
1. 작업 대상 경로가 정해지면 관련 ref의 repository root부터 해당 경로까지 존재하는 `AGENTS.md`를 확인하고, 더 좁은 scope의 instruction이 있으면 함께 적용합니다.
1. 이어서 [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)를 읽고 현재 작업에 필요한 Agent Asset만 선택해 로드합니다. 구체적인 GitHub task에서는 `github-context`와 task-specific Asset을 모두 발견할 수 있는 route를 선택하고, 좁은 family route가 둘을 함께 노출하지 않으면 `all`을 사용합니다. GitHub task가 아니면 `ROUTE.md`의 일반 family selection을 따릅니다.
1. 구체적인 GitHub task에서는 downstream read, review, mutation이나 finalizing action이 그 context에 의존하기 전에 `github-context`가 현재 repository/ref/object, 적용되는 repository instruction과 task에 필요한 live GitHub state를 확인하도록 합니다. 세부 loading 범위와 stop condition은 해당 Skill이 소유합니다.
1. 작업 범위, target repository, ref/object 또는 대상 경로가 실질적으로 바뀌면 적용되는 instruction, GitHub context와 route selection을 다시 평가합니다.

`CHATBOT.md`는 repository policy, Agent Asset behavior, routing semantics 또는 각 문서의 내용을 복제하거나 재정의하지 않습니다. 연결된 canonical source가 항상 authoritative합니다.
