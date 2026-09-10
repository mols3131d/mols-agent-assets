---
description: Python coding agent context의 목적, 유지 원칙과 핵심 anti-pattern을 정의합니다.
---

# Python Coding Agent Context

## Goal

Python으로 코딩하는 agent가 Python semantics와 runtime 특성에서 반복적으로 만드는 잘못된 판단을 줄인다.

Python 지식이나 best practice를 포괄하지 않고, 실제 code behavior와 caller-visible contract를 왜곡하는 agent anti-pattern을 교정하는 context를 유지한다.

## Principles

- **Agent failure first** — Python에서 중요하다는 이유보다 agent가 반복적으로 만드는 material error를 우선한다.
- **Python delta only** — generic engineering judgment나 deterministic tooling이 더 잘 소유하는 문제를 중복하지 않는다.
- **Semantics over heuristics** — Pythonic 외형, token, annotation, 통념보다 실제 Python semantics와 runtime behavior를 우선한다.
- **Context earns its cost** — 반복적인 material failure를 줄이는 guidance만 유지하고 syntax, library, smell taxonomy를 축적하지 않는다.

## Patterns

- **Narrow exception boundary** — broad exception handling으로 unrelated failure를 흡수하는 패턴을 막는다.
- **Annotation is not validation** — type annotation을 runtime guarantee로 오인하거나 annotation만으로 validation machinery를 추가하는 패턴을 막는다.
- **Own async lifecycle** — async/concurrency를 반사적으로 도입하거나 task lifetime, cancellation, failure propagation을 흐리는 패턴을 막는다.
- **Judge dynamic execution semantically** — `shell=True`, `eval`, `exec` 같은 token 자체로 결함을 판정하거나 execution semantics를 무시하는 패턴을 막는다.
- **Reject Python performance folklore** — Python 통념만으로 async, thread, process, native path, memoization 같은 mechanism을 선택하는 패턴을 막는다.
