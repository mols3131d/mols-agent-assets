---
description: 개발·기술 문서, baseline, directory guide와 durable documentation 구조 패턴을 찾을 때 사용하는 directory entrypoint입니다.
---

# Documentation Patterns

이 디렉터리는 agentic development에서 사람이 읽고 agent도 활용할 수 있는 **개발·기술 documentation의 구조와 유지보수 문제**를 다루는 reusable pattern을 보관합니다.

대표적인 범위는 다음과 같습니다.

- durable technical/development documentation 구조
- baseline과 recovery document
- directory와 repository-local surface를 설명하는 entry document
- 문서가 context와 운영 지식을 전달하는 방식

Agent/harness의 context loading mechanics는 [`context-engineering/`](../context-engineering/), working artifact와 실행 흐름은 [`workflow/`](../workflow/), 코드·repository 구현 구조는 [`software-engineering/`](../software-engineering/)이 소유합니다.

Pattern은 primary problem이 documentation일 때 이 directory에 둡니다.
