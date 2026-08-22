---
description: Agent Asset, instruction, routing, discovery, scoped context와 context harness 설계 패턴을 찾을 때 사용하는 directory entrypoint입니다.
---

# Context Engineering Patterns

이 디렉터리는 agentic development에서 **context를 발견·선택·로드·구성·변형하는 문제**를 다루는 reusable pattern을 보관합니다.

대표적인 범위는 다음과 같습니다.

- Agent Asset과 context surface의 배치·구성
- instruction과 scoped context
- routing, discovery, index와 progressive loading
- reusable core와 configuration/argument surface
- repository/runtime 사이의 context harness와 compatibility layer

개발 문서 자체의 구조와 유지보수는 [`documentation/`](../documentation/), working artifact와 실행 흐름은 [`workflow/`](../workflow/), 코드·repository 구현 구조는 [`software-engineering/`](../software-engineering/)이 소유합니다.

Pattern은 primary problem이 context engineering일 때 이 directory에 둡니다.
