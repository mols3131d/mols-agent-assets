---
name: mols-coding-context-python
description: >-
  Python add-on for mols-coding-context. Select together with mols-coding-context
  when the active work materially depends on Python code, Python runtime
  semantics, or Python-facing tests, especially for exception and failure
  semantics, asyncio or concurrency and cancellation, dynamic data boundaries,
  subprocess or dynamic execution, and recurring generated-code risks. Do not
  select merely because a repository contains incidental Python files or tooling,
  or because Python is mentioned without code-facing work. Adds Python-specific
  judgment only; exact API and version behavior remains with current project and
  runtime authority.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context Python

`mols-coding-context`에 **Python-specific judgment만 추가하는 add-on**이다. Core를 대체하거나 generic coding guidance를 반복하지 않는다.

## Add-on Contract

- Python code, Python runtime semantics 또는 Python-facing tests가 현재 task에 material할 때만 적용한다.
- Python이라는 이유만으로 async, schema, retry, subprocess 또는 security structure를 새로 만들지 않는다.
- Exact Python, standard-library, dependency와 framework behavior는 current authoritative source와 project/runtime evidence를 따른다.
- Formatter, linter, type checker, SAST와 tests가 안정적으로 판정하는 항목은 해당 deterministic owner에 맡긴다.

## Exceptions and Failure Semantics

- 실제로 처리할 concrete exception과 caller-visible failure contract를 식별한다.
- Broad catch가 예상 밖 failure를 success-like fallback으로 조용히 바꾸지 않게 한다.
- `try` scope는 intended failure source 주변으로 좁혀 unrelated programming/parsing error를 domain fallback으로 삼키지 않는다.
- Exception translation은 필요한 cause와 actionable context를 보존한다.
- `None`, `False`, empty collection과 sentinel이 not-found, empty, failed와 unknown을 혼합하면 caller semantics를 확인한다.

## Async and Concurrency

현재 code가 async/concurrent일 때만 적용한다.

- Event loop 안에 blocking I/O, process 또는 sleep operation을 무심코 섞지 않는다.
- Task owner와 lifetime을 명확히 하고 unowned fire-and-forget task를 기본값으로 만들지 않는다.
- Cancellation을 ordinary error처럼 삼켜 timeout 또는 task-group semantics를 깨뜨리지 않는다.
- Structured concurrency와 timeout은 current runtime과 actual lifecycle/failure policy에 맞을 때만 사용한다.

## Dynamic Data Boundaries

현재 boundary가 dynamic, externally shaped 또는 runtime-validated일 때만 적용한다.

- `dict[str, Any]`, `.get(..., default)`와 permissive coercion이 requiredness 또는 uncertainty를 숨기는지 본다.
- Annotation만으로 runtime validation이 생긴다고 가정하지 않는다.
- Downstream decision을 바꾸는 field의 requiredness, type, variant, coercion과 extra-field semantics를 필요한 boundary에서 확인한다.
- Dataclass, TypedDict, Pydantic, attrs 등 특정 representation을 universal default로 강제하지 않는다.

## Subprocess and Dynamic Execution

현재 code가 process, shell 또는 generated execution boundary를 다룰 때만 적용한다.

- Shell이 필요하지 않으면 structured argv 또는 더 직접적인 native API를 우선한다.
- Model, tool, user 또는 external text를 그대로 shell command나 host-language execution으로 승격하지 않는다.
- Dynamic execution이 requirement면 trust boundary, allowed capability, isolation, input/output contract와 failure semantics를 먼저 확인한다.
- `shell=True`, `eval`, `exec` token 자체를 unconditional defect로 취급하지 않는다.

## Generated-Code Review Lens

다음은 mandatory checklist가 아니라 review lens다.

- Narrative comment
- Docstring hallucination
- Boilerplate padding
- Redundant type prose
- Confident fallback
- Over-protective handler

Label을 찾는 것보다 contract fidelity, failure visibility와 context noise를 우선한다.

## Boundary

이 Skill은 Python add-on이다. `mols-coding-context` 없이 standalone coding core로 사용하지 않으며, 다른 Skill family를 prerequisite로 선언하거나 이름으로 route하지 않는다.
