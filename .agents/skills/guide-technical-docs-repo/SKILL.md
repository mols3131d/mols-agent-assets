---
name: guide-technical-docs-repo
description: Explain a technical system from provided documentation and source code. Use for repository onboarding, architecture orientation, execution-flow tracing, document-to-code comparison, or preparation for a code change. Do not use when the primary task is code review, security audit, refactoring, implementation, or unrelated factual lookup.
---

# Technical Docs & Repository Guide

Build a concise understanding guide from the supplied documentation and source code.

## Contract

- Follow the user's scope. For broad requests, orient an engineer new to the project around the primary runtime path.
- Use documentation for stated design and source code for current implementation.
- Support important claims with the narrowest available file, symbol, line, page, or section.
- Write `확인 불가` when the available evidence cannot support a conclusion.
- Do not invent architecture, dependencies, data flow, runtime behavior, execution, or test results.
- Ignore generated, vendored, and unrelated material unless it changes the requested scope.
- Do not expand into code review, security audit, refactoring, or implementation unless requested.

## Procedure

### 1. Inspect the minimum useful sources

Start with the sources most likely to establish the requested behavior:

- overview or architecture documentation;
- README and dependency manifest;
- application or package entrypoint;
- core domain or orchestration code;
- configuration loading;
- tests covering the target behavior.

Stop expanding once the important claims are supported.

### 2. Explain the core structure

For each necessary component, state its responsibility, inputs and outputs, connection to other components, and supporting source.

Do not treat the directory tree itself as architecture.

### 3. Trace one representative flow

Trace only the steps needed to understand the main path:

1. trigger and entrypoint;
1. core processing;
1. state read/write or external side effect;
1. result and failure handling.

Skip helpers that do not change the mental model.

### 4. Compare docs and code when both matter

Include only differences that affect behavior, integration, operation, or future changes.
Use `일치`, `차이`, or `확인 불가`, and state the practical impact of each material difference.

### 5. Recommend a reading order

Choose three to seven files or sections. State what the reader should learn from each.

## Output

Use only sections that help answer the request. A broad guide may use:

```markdown
# 이해 가이드

## 한눈에 보기
<핵심 목적과 구조>

## 핵심 구조
| 구성 요소 | 책임 | 근거 |
| --- | --- | --- |

## 주요 실행 흐름
1. <진입>
1. <핵심 처리>
1. <상태 또는 외부 연동>
1. <결과와 실패 처리>

## 먼저 읽을 곳
1. `<파일 또는 문서>` — <읽는 목적>

## 문서와 구현 차이
| 항목 | 상태 | 차이와 영향 | 근거 |
| --- | --- | --- | --- |

## 확인 불가
- <현재 자료로 확인할 수 없는 내용>
```

Omit sections that do not apply.
