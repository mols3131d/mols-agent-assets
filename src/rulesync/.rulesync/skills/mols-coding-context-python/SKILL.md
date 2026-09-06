---
name: mols-coding-context-python
description: >-
  Python-specific engineering judgment overlay for code-facing tasks. Select
  together with mols-coding-context whenever the active work materially depends
  on Python code, Python runtime semantics, or Python-facing tests, especially
  for exception and failure semantics, asyncio or concurrency and cancellation,
  dynamic data boundaries, subprocess or dynamic execution, and recurring
  generated-code risks. Do not select merely because a repository contains
  incidental Python files or tooling, or because Python is mentioned without
  code-facing work. Adds Python-specific judgment only; exact API and version
  behavior remains with current project and runtime authority.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context Python

Python이 현재 code-facing work의 material surface일 때 `mols-coding-context` 위에 **Python-specific semantic/runtime judgment**를 추가한다. Python tutorial, style guide, security checklist 또는 API reference를 복제하지 않는다.

## Contract

- Base의 engineering judgment를 반복하지 않는다. Python에서만 달라지는 failure mode와 runtime semantics만 추가한다.
- 현재 변경과 failure surface에 material한 항목만 적용한다. Python이라는 이유로 async, schema, retry, subprocess 또는 security 구조를 새로 만들지 않는다.
- Python, standard library, dependency와 framework의 exact semantics는 current authoritative source와 project/runtime evidence를 따른다.
- formatter, linter, type checker, SAST와 tests가 안정적으로 판정하는 항목을 prose rule로 다시 구현하지 않는다.

## Exceptions and Failure Semantics

- 실제로 처리할 의도가 있는 concrete exception을 우선한다.
- broad `Exception` catch가 필요하더라도 예상 밖 failure를 success-like fallback으로 조용히 바꾸지 않는다.
- `try` 범위는 intended failure source 주변으로 좁혀 unrelated programming/parsing error가 domain fallback으로 삼켜지지 않게 한다.
- exception translation이 필요하면 원인과 actionable context를 보존한다.
- `None`, `False`, empty collection, sentinel이 failure를 대신할 때 caller가 not-found, empty, failed와 unknown을 구분해야 하는지 확인한다.

## Async and Concurrency

- `async def` 안에 blocking file, network, process 또는 sleep operation을 무심코 섞지 않는다.
- task의 owner와 lifetime을 명확히 하고 unowned fire-and-forget task를 기본값으로 만들지 않는다.
- local Python/runtime contract가 지원하고 문제에 맞으면 structured concurrency를 우선 검토한다.
- cancellation은 control-flow semantics다. Cleanup을 수행하더라도 cancellation을 의미 없이 삼켜 timeout 또는 task-group semantics를 깨뜨리지 않는다.
- timeout은 임의 숫자를 붙이는 ceremony가 아니라 operation boundary와 caller failure policy의 일부로 다룬다.
- concurrency abstraction은 실제 throughput 또는 lifecycle need가 있을 때만 추가한다.

구체적인 blocking-call 목록, cancellation hierarchy와 version-specific API는 Python/runtime docs와 repository tooling이 소유한다.

## Dynamic Data Boundaries

- `dict[str, Any]`, `.get(..., default)`와 permissive coercion이 boundary uncertainty를 숨기는지 확인한다.
- annotation이 있다는 이유만으로 runtime validation이 존재한다고 가정하지 않는다.
- downstream decision을 바꾸는 field의 requiredness, type, variant와 extra-field semantics를 필요한 boundary에서 확인한다.
- dataclass, TypedDict, Pydantic, attrs 또는 다른 representation을 universal preference로 강제하지 않는다. Existing system과 required runtime guarantee를 따른다.
- untagged dynamic shape가 여러 의미를 가질 때는 ambiguity가 실제 오류 위험을 만드는 경우 더 명시적인 representation을 검토한다.

## Subprocess and Dynamic Execution

- shell이 필요하지 않으면 structured argv 또는 더 직접적인 native API를 우선한다.
- model, tool, user 또는 external text를 그대로 shell command로 승격하지 않는다.
- generated text를 `eval` 또는 `exec`로 host process에서 실행하는 것을 convenience path로 사용하지 않는다.
- dynamic execution이 실제 requirement라면 input trust, allowed capability, isolation, output contract와 failure boundary를 먼저 다룬다.

## Generated-Code Review Lens

다음은 rigid taxonomy나 mandatory rewrite 목록이 아니라 Python code review lens다.

- **Narrative comment** — statement를 단계별로 다시 설명하는 comment가 signal보다 noise를 만드는가?
- **Docstring hallucination** — parameter, return, exception, side effect 설명이 실제 implementation과 caller contract에 근거하는가?
- **Boilerplate padding** — real invariant 없이 defensive wrapper, assertion, helper가 늘어났는가?
- **Redundant type prose** — annotation과 같은 정보를 comment/docstring이 반복해 drift surface를 만드는가?
- **Confident fallback** — 처리하지 못한 상태를 `None`, `-1`, `""`, empty collection 같은 정상값처럼 돌려주는가?
- **Over-protective handler** — broad exception handler가 `pass`, bare return 또는 empty fallback으로 failure를 숨기는가?

Smell label을 찾는 것이 목적이 아니다. 특히 confident fallback과 over-protective handler는 **failure/uncertainty suppression** 관점에서 판단한다.

## Python Tooling Ownership

다음 concern은 가능한 한 기존 deterministic owner를 따른다.

| Concern | Default owner |
| --- | --- |
| formatting / syntax / simple static smell | repository formatter / Ruff |
| deterministic security pattern | repository-selected SAST / analyzer |
| type consistency | repository-selected type checker |
| observable behavior | tests / runtime evidence |
| package, API and version exactness | project metadata + current official docs |
| semantic trade-off and failure prevention | this Skill |

특정 Ruff rule set, type checker, validation library 또는 security tool을 universal configuration으로 강제하지 않는다.

## Boundary

이 Skill은 `mols-coding-context` family의 Python overlay다. 다른 Skill family를 prerequisite로 선언하거나 이름으로 route하지 않는다. Python-specific 판단이 필요하지 않은 task에는 이 context를 추가하지 않는다.
