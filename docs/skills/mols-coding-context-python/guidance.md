---
description: Python coding agent context의 핵심 목적과 유지 원칙을 정의합니다.
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
