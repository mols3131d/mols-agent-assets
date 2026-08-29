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
| `--scope <value,...\|auto>` | 설명을 수정할 mutation scope를 target과 필요한 source surface로 제한한다. Explanation의 사실성을 확인하는 evidence read도 적용되는 user/repository scope와 authority 안에서 가장 좁게 수행하며, 읽은 surface에 write authority가 생기지는 않는다. |
| `--validation <command\|auto\|none>` | docstring, doctest, directive처럼 explanation text가 tool/runtime에 소비될 가능성이 있을 때 필요한 최소 validation을 선택한다. |

명시된 argument를 우선한다. 넓은 정책이나 사용자 문서까지 추측으로 확대하지 않는다.

## Default Explanation Signals

실행 코드가 이미 적절하고 아래 의미가 code만으로 안정적으로 드러나지 않으면 explanation 후보로 본다.

| Signal | Default surface |
| --- | --- |
| hidden caller contract 또는 non-obvious call semantics | docstring |
| maintainer가 보존해야 하는 invariant 또는 local constraint | code-local comment |
| ordering 또는 failure consequence | code-local comment |
| external system·protocol constraint | code-local comment |
| 현재 constraint 때문에 잘못되는 durable rejected alternative | code-local comment |
| 개별 symbol보다 file 전체에 안정적으로 적용되는 local convention | module-level explanation |

사용자가 comment나 docstring을 직접 요청하지 않았어도 같은 기준을 적용한다. Signal 수나 comment 수 자체를 품질 지표로 사용하지 않는다.

## Workflow

1. 적용되는 repository/source instructions와 target code, 가까운 caller·maintainer context를 읽는다.
1. 독자가 code만으로 복원하기 어려운 의미와 그 때문에 생기는 추론·탐색·오해 비용을 확인하고 reader를 구분한다: caller contract인지, maintainer constraint·consequence·rationale인지 판단한다.
1. 먼저 **prose가 맞는 해법인지** 확인한다. 이름, representation, control/state flow, responsibility 또는 indirection이 실제 원인이면 설명을 추가하지 말고 `code-comprehension-refactor`로 넘긴다.
1. **Evidence before Explanation.** Candidate meaning을 source prose로 고정하기 전에 target behavior, caller, test, canonical contract/spec, current config·schema·protocol 등 필요한 가장 좁은 current evidence로 확인한다. Evidence read도 적용되는 explicit scope와 authority를 넘지 않는다. 필요한 evidence가 그 밖에 있다면 조용히 범위를 넓히지 말고 uncertainty나 필요한 handoff를 남긴다. Git history나 old discussion은 후보 이유를 찾는 supporting context일 수 있지만 current invariant의 단독 근거로 사용하지 않는다.
1. Current evidence가 지지하는 의미만 설명한다. 현재 constraint·consequence는 확인되지만 historical reason은 확인되지 않으면 확인 가능한 현재 의미만 남긴다. Evidence source가 서로 충돌하면 하나를 편의상 선택해 explanation으로 굳히지 않는다. Material rationale를 확정할 수 없으면 그럴듯한 이유를 invent하지 않고 unsupported explanation을 추가하지 않는다.
1. 같은 semantic이 적절한 owner에 이미 충분히 있는지 확인한다. 그래도 caller나 maintainer가 해당 지점에서 알아야 하는 local projection이 필요하거나 explanation이 없다면 가장 작은 설명을 추가·개선한다. 반대로 code, name, type이 이미 충분하거나 prose가 읽기·유지 비용만 늘리면 추가하지 않거나 불필요한 설명을 제거한다.
1. caller가 사용 전에 알아야 하는 contract는 docstring에, maintainer가 구현을 수정할 때 알아야 하는 code-local meaning은 comment에 둔다. 위치·scope·owner가 단순하지 않으면 [Documentation](references/documentation.md)을 따른다.
1. 선택한 설명 surface만 수정한다. 실행 statement, identifier, signature, type, control flow와 data representation은 변경하지 않는다.
1. 설명이 runtime, tooling 또는 validation에 소비되는지 확인한다. doctest, reflection-dependent docstring, pragma, linter/type-check directive, magic comment는 일반 prose처럼 수정하지 않는다.
1. 코드와 설명을 다시 읽어 unsupported claim, 중복, stale claim과 구현을 그대로 번역한 문장을 제거한다. 변경한 설명, 보존한 code boundary, 수행한 validation과 남은 uncertainty만 짧게 보고한다.

Evidence-backed durable meaning이 남아 있는데 comment를 피하기 위해 no-op으로 조기 종료하지 않는다. 반대로 semantic claim을 뒷받침할 evidence가 없거나 충돌이 해소되지 않았거나 필요한 evidence가 허용된 scope 밖에 있거나 추가 prose가 제거하는 이해 비용보다 읽기·유지 비용이 크면 설명을 invent하지 않고 중단할 수 있다.

## Progressive Disclosure

다음 판단이 실제로 필요할 때만 [Documentation](references/documentation.md)을 읽는다.

- explanation의 placement, scope 또는 semantic owner가 불명확함
- evidence source가 충돌하거나 historical/indirect evidence의 의미를 구분해야 함
- canonical policy/contract의 local projection을 판단해야 함
- rejected alternative, history 또는 stale explanation이 얽힘
- module-level explanation이 적절한지 판단해야 함
- machine/runtime/tool-consumed text를 수정할 가능성이 있음

## Boundaries

- 실행 코드, identifier, type, signature, representation, control/state flow 또는 abstraction을 clarification 명목으로 변경하지 않는다.
- 코드 자체를 리팩터링해야 이해 비용이 줄어들면 `code-comprehension-refactor`를 사용한다.
- 함수 이름, type annotation, 다음 statement처럼 code가 이미 직접 표현하는 내용을 prose로 반복하지 않는다.
- unusual code shape, naming, history 또는 관례만 보고 확인되지 않은 rationale를 만들어내지 않는다.
- 넓은 architecture·domain policy를 source comment에 복제하지 않는다. caller나 maintainer에게 필요한 local projection만 남긴다.
- evidence 확인을 위한 read도 적용되는 explicit scope와 authority를 넘지 않으며, 읽은 surface를 수정할 권한이 생기지 않는다.
- user-facing guide, README, API manual 같은 독립 문서는 이 skill의 scope가 아니다.
- `noqa`, `type: ignore`, coverage pragma, formatter directive, shebang, encoding cookie와 같은 machine-consumed comment를 일반 설명 comment로 취급하지 않는다.
- docstring이 reflection, documentation generation, doctest 또는 framework behavior의 contract라면 observable surface를 보존한다.
- 실행하지 않은 validation을 수행했다고 보고하지 않는다.
