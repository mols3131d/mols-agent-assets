---
title: Prompt Canonical Superset
description: 여러 invocation surface에 투영할 Prompt의 repository-local canonical superset 기준
---

# Prompt Canonical Superset

여러 agent/chatbot invocation surface에 같은 Prompt를 배포할 때의 권장 Superset은 **Markdown body와 declarative front matter를 가진 `<name>.prompt.md` source**다.

Prompt의 본질인 task intent와 input/output contract는 Markdown에 유지하고, 실행 surface가 지원하는 selector와 execution hint는 front matter에 보존한다.

```text
<name>.prompt.md
├─ task intent / workflow
├─ arguments and constraints
├─ output contract
└─ target-scoped execution metadata
        ↓
   target invocation surfaces
```

## Superset Owns

- invocation의 목적과 완료 조건
- arguments, defaults와 input semantics
- task-local constraint와 workflow
- output semantics
- agent/model/tool 선택이 Prompt 의미의 일부일 때 그 의도
- target별 execution capability 차이

현재 repository validator가 다루는 `.prompt.md` front matter surface는 `name`, `description`, `argument-hint`, `agent`, `model`, `tools`다. 모든 field를 항상 채우는 schema로 사용하지 않고 실제 의미가 있을 때만 둔다.

## Projection

Projection은 canonical Prompt의 task contract를 target의 native invocation 방식으로 옮긴다.

```text
Prompt Superset
├─ VS Code / Copilot prompt file
├─ chatbot reusable prompt
└─ other target-native invocation
```

Target에 agent/model/tools 같은 selector가 없으면 그 차이를 숨기지 않는다. 해당 selector가 단순 실행 최적화인지, Prompt 성공에 필요한 behavioral requirement인지 구분한 뒤 omit, adapt 또는 unsupported로 처리한다.

문구를 문자 단위로 보존하는 것보다 task intent, arguments, constraints와 output contract를 보존하는 것이 우선이다.

## Source Placement

이 저장소의 canonical reusable Prompt source는 `src/prompts/<name>.prompt.md`에 둔다. Target이 같은 source를 직접 사용할 수 있으면 별도 projection을 만들지 않는다.

Prompt는 일회성 user request 자체와 구분한다. 반복 가능한 invocation source로 관리할 가치가 있을 때만 repository asset으로 둔다.

## Boundary

- 이 문서는 Prompt 유형의 **최적 canonical Superset**을 소유한다.
- Prompt를 persistent Rule이나 독립 Agent로 확장하지 않는다.
- target-specific selector를 모든 target의 공통 capability라고 가정하지 않는다.
- vendor schema가 바뀌면 target-native projection contract를 갱신하되 Prompt의 task authority를 임의로 이동하지 않는다.
