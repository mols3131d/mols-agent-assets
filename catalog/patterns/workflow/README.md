---
description: Agentic work의 실행 흐름, working artifact, handoff와 lifecycle surface 패턴을 찾을 때 사용하는 directory entrypoint입니다.
---

# Workflow Patterns

이 디렉터리는 agentic development에서 **작업을 수행하고 상태·산출물·handoff를 관리하는 방식**을 다루는 reusable pattern을 보관합니다.

대표적인 범위는 다음과 같습니다.

- research, plan, review와 handoff 같은 작업 흐름
- working / non-canonical artifact surface
- temporary artifact와 durable owner 사이의 lifecycle
- 반복 작업과 collaboration을 지원하는 execution surface

Context loading과 Agent Asset 구조는 [`context-engineering/`](../context-engineering/), durable 기술 문서 구조는 [`documentation/`](../documentation/), 코드·repository 구현 구조는 [`software-engineering/`](../software-engineering/)이 소유합니다.

Pattern은 primary problem이 workflow일 때 이 directory에 둡니다.
