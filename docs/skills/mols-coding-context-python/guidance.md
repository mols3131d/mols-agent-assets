---
description: Python coding agent context의 핵심 목적과 유지 원칙을 정의합니다.
---

# Python Coding Agent Context

## Goal

Python으로 코딩하는 agent가 Python semantics와 runtime 특성에서 반복적으로 만드는 잘못된 판단을 줄인다.

Python 지식이나 best practice를 포괄하지 않고, 실제 code behavior와 caller-visible contract를 왜곡하는 agent anti-pattern을 교정하는 context를 유지한다.

## Principles

- **Agent failure first** — Python에서 중요하다는 이유보다 agent가 반복적으로 만드는 material error를 우선한다.
- **Core ownership / Python delta only** — `mols-coding-context`의 확장이므로 Core가 소유하는 판단을 재정의하거나 중복 소유하지 않는다. Core와 함께 적용했을 때 Python 고유의 semantics 또는 실행 계약으로 인해 추가로 필요한 판단만 소유한다. 단지 Python 코드에도 적용된다는 이유로 범용 지침을 추가하지 않는다. 언어 독립적인 판단의 개선은 Core에서 검토하고, 기존 add-on 지침이 Core에 흡수되면 중복을 제거한다.
- **Deterministic tooling owns deterministic work** — formatter, linter, type checker, schema validator 등 결정적 도구로 충분히 판정·해소할 수 있는 문제는 이 Skill의 책임에서 제외한다. 소비 환경에 해당 도구가 없다는 이유로 규칙 목록이나 수정 절차를 Skill에 복제하지 않는다. 도구의 판정만으로 결정할 수 없는 실제 실행 의미와 계약에 대한 판단만 남긴다. 도구 설정·설치·실행 절차는 소유하지 않는다.
- **Semantics over heuristics** — Pythonic 외형, token, annotation, 통념보다 실제 Python semantics와 runtime behavior를 우선한다.
- **Context earns its cost** — 실제 판단 오류를 줄일 근거가 있는 guidance만 유지한다. 모델이 이미 충분히 아는 문법·일반 Python 지식과 라이브러리 사용법, smell taxonomy를 축적하지 않는다.
