---
name: guide-technical-docs-repo
description: Explain a technical system from provided documentation and source code. Use for repository onboarding, architecture orientation, execution-flow tracing, document-to-code comparison, or preparation for a code change.
---

# Technical Docs & Repository Guide

## Goal

Create a concise understanding guide from supplied technical documents or source code.

Focus on:

- system or feature purpose
- core components and their relationships
- one representative execution flow
- files or sections to read first
- material differences between documentation and implementation

## Rules

- Follow the scope requested by the user.
- For a broad request, target an engineer new to the project and cover the primary runtime path.
- Use documentation for stated design and source code for current implementation.
- Support important claims with the narrowest available file, symbol, line, page, or section.
- Write `확인 불가` when the available sources do not support a conclusion.
- Do not invent architecture, dependencies, data flow, or runtime behavior.
- Do not claim execution or test results unless the commands were actually run and inspected.
- Ignore generated, vendored, and unrelated files unless they affect the requested scope.
- Do not expand into code review, security audit, refactoring, or implementation unless requested.
- Do not list every file or restate entire documents.

## Procedure

### 1. Inspect the minimum useful sources

Start with:

- overview, architecture, API, and operations documents
- README and dependency manifest
- application or package entrypoint
- core domain or orchestration module
- configuration loading
- tests covering the target behavior

### 2. Explain the core structure

For each necessary component, state:

- responsibility
- input and output
- connection to other components
- supporting source

Do not treat the directory tree itself as architecture.

### 3. Trace the main flow

Trace one representative path:

1. trigger
1. entrypoint
1. core processing
1. state read or write
1. external call or side effect
1. result and failure handling

Skip helper details that do not change understanding.

### 4. Compare documentation and code

When both are available, include only differences that affect behavior, integration, operation, or future changes.

Use these statuses:

- `일치`
- `차이`
- `확인 불가`

State the practical impact of each difference.

### 5. Recommend a reading order

Select three to seven files or document sections. For each item, state what the reader should learn from it.

## Output

Use only the sections relevant to the request.

```markdown
# 이해 가이드

## 한눈에 보기
<시스템 또는 기능을 3~5문장으로 설명>

## 핵심 구조
| 구성 요소 | 책임 | 근거 |
|---|---|---|

## 주요 실행 흐름
1. <진입>
2. <핵심 처리>
3. <상태 또는 외부 연동>
4. <결과와 실패 처리>

## 먼저 읽을 곳
1. `<파일 또는 문서>` — <읽는 목적>

## 문서와 구현 차이
| 항목 | 상태 | 차이와 영향 | 근거 |
|---|---|---|---|

## 확인 불가
- <현재 자료로 확인할 수 없는 내용>
```

Omit sections that do not apply.
