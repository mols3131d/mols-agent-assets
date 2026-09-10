---
description: Python coding agent context의 목적과 유지 원칙, 반복적인 agent anti-pattern을 다루는 pattern을 정의합니다.
---

# Python Coding Agent Context

## Goal

Python으로 코딩하는 agent가 Python semantics와 runtime 특성에서 반복적으로 만드는 잘못된 판단을 줄인다.

Python 지식이나 best practice를 포괄하지 않고, 실제 code behavior와 caller-visible contract를 왜곡하는 agent anti-pattern을 교정하는 context를 유지한다.

## Principles

- **Agent failure first** — Python에서 중요하다는 이유보다 agent가 반복적으로 만드는 material error를 우선한다.
- **Python delta only** — generic engineering judgment나 deterministic tooling이 더 잘 소유하는 문제를 중복하지 않는다.
- **Semantics and evidence** — Pythonic, defensive, typed, async 같은 외형이나 통념보다 실제 semantics, project contract와 runtime evidence를 우선한다.
- **No speculative robustness** — 불확실성만으로 validation, fallback, concurrency, wrapper 또는 compatibility machinery를 추가하게 만들지 않는다.
- **Context earns its cost** — 반복적인 agent failure를 줄이는 guidance만 유지하고 syntax, library, smell taxonomy를 축적하지 않는다.

## Patterns

- **Narrow failure boundary** — broad exception handling과 success-like fallback으로 unrelated failure를 숨기는 패턴을 막는다.
- **Resist defensive padding** — contract 없이 type check, coercion, default, validation과 fallback을 연쇄적으로 추가하는 패턴을 막는다.
- **Own async lifetime** — async/concurrency를 반사적으로 도입하거나 task lifetime, cancellation과 failure propagation을 흐리는 패턴을 막는다.
- **Judge execution by provenance** — 실행 경계를 단순 token heuristic으로 판단하거나 출처가 불명확한 입력을 실행 대상으로 취급하는 패턴을 막는다.
- **Measure before optimizing** — Python 성능 통념만으로 async, thread, process, native path, memoization 등의 mechanism을 선택하는 패턴을 막는다.
