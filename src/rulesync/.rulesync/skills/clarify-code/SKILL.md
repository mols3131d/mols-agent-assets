---
name: clarify-code
description: Use this skill to make code easier to understand by improving code-adjacent explanatory text such as docstrings, comments, and module-level explanations without changing executable code. Trigger when caller contracts, rationale, invariants, ordering, side effects, unusual implementation choices, or other non-obvious meaning should be explained inside source files. Do not use to rename symbols, change types or signatures, restructure control or state flow, change representations, or remove indirection; use code-comprehension-refactor for code changes. Do not use for user-facing documentation.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Clarify Code

실행 코드를 바꾸지 않고 **코드 파일 안에서 함께 유지되는 설명**을 개선해 caller와 maintainer의 이해 비용을 줄인다.

주된 surface는 docstring, comment와 module-level explanation이다. 코드 구조 자체가 이해 비용의 원인이면 prose로 덮지 않고 `code-comprehension-refactor`를 사용한다.

## Arguments

```yaml
target: auto
scope: auto
validation: auto
```

| Argument | `auto` 동작 |
| --- | --- |
| `--target <value\|auto>` | 요청, 선택 영역 또는 현재 변경에서 설명이 필요한 code-adjacent surface를 식별한다. |
| `--scope <value,...\|auto>` | target과 실제 caller·maintainer가 설명을 읽는 가까운 surface까지만 포함한다. |
| `--validation <command\|auto\|none>` | docstring, doctest, directive처럼 explanation text가 tool/runtime에 소비될 가능성이 있을 때 필요한 최소 validation을 선택한다. |

명시된 argument를 우선한다. 넓은 정책이나 사용자 문서까지 추측으로 확대하지 않는다.

## Workflow

1. 적용되는 repository/source instructions와 target code, 가까운 caller·maintainer context를 읽는다.
1. 독자가 code만으로 복원하기 어려운 의미와 그 때문에 생기는 추론·탐색·오해 비용을 확인하고 reader를 구분한다: caller contract인지, maintainer rationale·constraint인지 판단한다.
1. 먼저 **prose가 맞는 해법인지** 확인한다. 이름, representation, control/state flow, responsibility 또는 indirection이 실제 원인이면 설명을 추가하지 말고 `code-comprehension-refactor`로 넘긴다.
1. 실행 코드가 이미 적절하지만 caller나 maintainer에게 필요한 durable contract·invariant·constraint·consequence·rationale를 code만으로 안정적으로 복원하기 어렵고 같은 의미가 가까운 surface에 없다면, 사용자가 comment나 docstring을 직접 요청하지 않았어도 설명을 추가하거나 개선하는 것을 기본으로 한다.
1. 반대로 code, name, type이 이미 충분한 정보를 주거나 prose가 읽기·유지 비용만 늘리면 추가하지 않거나 불필요한 설명을 제거한다. 설명의 양 자체를 품질로 보지 않는다.
1. caller가 사용 전에 알아야 하는 비자명한 contract는 docstring에, maintainer가 구현을 수정할 때 알아야 하는 code-local constraint·consequence·rationale는 comment에 둔다. 의미의 실제 scope와 owner에 맞는 위치는 [Documentation](references/documentation.md)을 따른다.
1. 선택한 설명 surface만 수정한다. 실행 statement, identifier, signature, type, control flow와 data representation은 변경하지 않는다.
1. 설명이 runtime, tooling 또는 validation에 소비되는지 확인한다. doctest, reflection-dependent docstring, pragma, linter/type-check directive, magic comment는 일반 prose처럼 수정하지 않는다.
1. 코드와 설명을 다시 읽어 중복, stale claim, 구현을 그대로 번역한 문장을 제거한다. 필요한 의미가 더 안정적인 canonical owner에 있다면 복제하지 않고 최소 projection만 남긴다.
1. 변경한 설명, 보존한 code boundary, 수행한 validation과 남은 uncertainty만 짧게 보고한다.

필요한 설명이 충분해지면 중단한다. durable한 non-obvious meaning이 남아 있는데 comment를 피하기 위해 no-op으로 조기 종료하지 않는다. 반대로 추가 prose가 제거하는 이해 비용보다 읽기·유지 비용이 크면 추가하지 않는다.

## Progressive Disclosure

- docstring, comment 또는 module-level explanation을 추가·수정·제거할지 판단할 때 [Documentation](references/documentation.md)을 읽는다.

## Boundaries

- 실행 코드, identifier, type, signature, representation, control/state flow 또는 abstraction을 clarification 명목으로 변경하지 않는다.
- 코드 자체를 리팩터링해야 이해 비용이 줄어들면 `code-comprehension-refactor`를 사용한다.
- 함수 이름, type annotation, 다음 statement처럼 code가 이미 직접 표현하는 내용을 prose로 반복하지 않는다.
- 넓은 architecture·domain policy를 source comment에 복제하지 않는다. caller나 maintainer에게 필요한 local projection만 남긴다.
- user-facing guide, README, API manual 같은 독립 문서는 이 skill의 scope가 아니다.
- `noqa`, `type: ignore`, coverage pragma, formatter directive, shebang, encoding cookie와 같은 machine-consumed comment를 일반 설명 comment로 취급하지 않는다.
- docstring이 reflection, documentation generation, doctest 또는 framework behavior의 contract라면 observable surface를 보존한다.
- 실행하지 않은 validation을 수행했다고 보고하지 않는다.
