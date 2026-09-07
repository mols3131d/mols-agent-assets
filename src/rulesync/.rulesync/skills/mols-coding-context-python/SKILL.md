---
name: mols-coding-context-python
description: >-
  Python-specific add-on for code-facing tasks materially dependent on Python code
  semantics, runtime behavior, or Python-facing tests. Select only together with
  mols-coding-context. Adds Python-specific judgment for exceptions, async and
  cancellation, runtime validation boundaries, subprocess or dynamic execution,
  and Python performance decisions. Do not select for incidental Python files,
  tooling or mentions, or prose-only edits where Python semantics are irrelevant.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Coding Context Python

`mols-coding-context`에 **Python-specific judgment만 추가하는 add-on**이다. Core의 generic coding guidance를 반복하지 않는다.

## Add-on Contract

- Python code semantics, Python runtime behavior 또는 Python-facing tests가 현재 task에 material할 때만 적용한다.
- Python이라는 이유만으로 async, schema, retry, subprocess, concurrency 또는 security structure를 새로 만들지 않는다.
- Exact Python, standard-library, dependency와 framework behavior는 current authoritative source와 project/runtime evidence를 따른다.
- 해당 construct가 실제 change surface에 없으면 관련 section은 행동을 만들지 않는다.

## Exceptions

- 실제로 처리할 concrete exception과 caller-visible failure contract를 식별하고 `try` scope를 intended failure source 주변으로 좁힌다.
- Broad catch가 unrelated programming, parsing 또는 invariant failure를 success-like fallback으로 삼키지 않게 한다.
- Exception translation은 필요한 cause와 actionable context를 보존한다. Catch가 recovery, translation 또는 required cleanup을 하지 않으면 필요성부터 다시 본다.

## Async and Concurrency

현재 code가 async/concurrent일 때만 적용한다.

- Event loop 안에 blocking I/O, process 또는 sleep operation을 무심코 섞지 않는다.
- Task owner와 lifetime을 명확히 하고 unowned fire-and-forget task를 기본값으로 만들지 않는다.
- Cancellation을 ordinary error처럼 삼켜 timeout, task-group 또는 caller cancellation semantics를 깨뜨리지 않는다.
- Structured concurrency, timeout, thread/process offload는 current runtime과 actual lifecycle/failure policy에 맞을 때만 사용한다.

## Runtime Data Boundaries

현재 boundary가 dynamic, externally shaped 또는 runtime-validated일 때만 적용한다.

- Type annotation은 runtime validation이 아니다. Downstream decision을 바꾸는 requiredness, coercion, variant와 extra-field behavior는 실제 runtime boundary가 무엇을 보장하는지 확인한다.
- Dataclass, TypedDict, Pydantic, attrs 또는 다른 representation을 universal default로 강제하지 않는다. Existing project boundary가 충분하면 새 validation layer를 만들지 않는다.

## Subprocess and Dynamic Execution

현재 code가 process, shell 또는 generated execution boundary를 다룰 때만 적용한다.

- Shell semantics가 필요하지 않으면 structured argv 또는 더 직접적인 native API를 우선한다.
- Model, tool, user 또는 external text를 그대로 shell command, `eval` 또는 `exec` input으로 승격하지 않는다. Dynamic execution이 requirement면 trust boundary, allowed capability, isolation과 failure contract를 확인한다.
- `shell=True`, `eval`, `exec` token 자체를 unconditional defect로 취급하지 않는다. 실제 input provenance와 execution contract가 판단을 소유한다.

## Python Optimization Delta

Python performance work일 때만 core의 evidence-driven optimization에 다음 delta를 추가한다.

- Syntax나 일반적인 Python folklore만으로 bottleneck을 단정하지 않는다. Target interpreter/build와 representative workload에서 profile 또는 benchmark evidence를 우선한다.
- `async`, threads, processes, native/vectorized path, memoization 또는 data-structure 교체를 “Python은 느리다”는 이유만으로 도입하지 않는다. CPU/I/O 비중, allocation/data movement, serialization/interop와 lifecycle cost 중 실제 dominant cost를 확인한다.
- Optimization이 implementation complexity, memory, startup, cancellation, serialization 또는 portability trade-off를 만들면 measured gain과 함께 판단한다.

## Boundary

이 Skill은 Python add-on이다. `mols-coding-context` 없이 standalone coding core로 사용하지 않으며, 다른 Skill family를 prerequisite로 선언하거나 이름으로 route하지 않는다. Generic failure, security, optimization workflow와 language-independent engineering guidance는 core가 소유한다.
