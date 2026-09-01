---
description: 파일 이름의 prefix·subject·postfix를 구성해 기본 filesystem 정렬에서도 관련 파일이 서로 가까이 모이도록 설계할 때 참고하는 naming pattern입니다.
---

# Filesystem Sort-Aware Naming

파일 이름을 단순한 식별자가 아니라 **filesystem의 기본 이름 정렬에서 관련 파일을 가까이 모으는 탐색 단서**로 사용할 수 있습니다.

핵심은 읽는 순서를 강제하는 것이 아니라, 함께 찾을 가능성이 높은 파일들이 이름 정렬에서도 자연스럽게 군집되도록 이름의 구조를 설계하는 것입니다.

## Core

기본 형태는 다음처럼 볼 수 있습니다.

```text
<prefix...>-<subject>-<postfix...>.<ext>
```

`prefix`와 `postfix`는 각각 하나로 제한되지 않습니다. 여러 단계가 필요하면 다음처럼 이어질 수 있습니다.

```text
<prefix-1>-<prefix-2>-<subject>-<postfix-1>-<postfix-2>.<ext>
```

의미 구조로 보면 다음과 같은 형태가 될 수 있습니다.

```text
<domain>-<subdomain>-<family>-<subject>-<aspect>-<variant>.<ext>
```

각 단계는 왼쪽에서 오른쪽으로 더 구체적인 의미를 더합니다. 단계 수를 늘리는 것 자체가 목적은 아니며, 실제 grouping과 탐색에 의미가 있는 요소만 사용합니다.

## Prefix

Prefix는 관련 파일을 **넓은 범위에서 먼저 모으는 정렬 키**로 사용할 수 있습니다. Domain, subdomain, family처럼 파일을 함께 찾을 가능성이 높은 상위 맥락을 앞쪽에 둡니다.

```text
agent-assets-routing.md
agent-assets-validation.md
agent-assets-workflow.md

documentation-indexing.md
documentation-readme.md
documentation-writing.md
```

Prefix가 여러 단계라면 큰 범위에서 작은 범위로 좁혀갈 수 있습니다.

```text
agent-assets-skill-authoring.md
agent-assets-skill-validation.md
agent-assets-subagent-authoring.md
```

여기서 `agent-assets`가 넓은 domain을, `skill`과 `subagent`가 그 아래의 더 좁은 grouping을 만듭니다.

## Subject and Postfix

Subject는 파일이 직접 다루는 이름이나 주제를 나타냅니다. Postfix는 그 subject 아래의 aspect, role, variant처럼 더 구체적인 구분을 뒤에 이어 붙입니다.

```text
agent-assets-routing.md
agent-assets-routing-generation.md
agent-assets-routing-policy.md
agent-assets-routing-validation.md
```

이때 `agent-assets-routing` 전체가 다시 하나의 작은 prefix처럼 작동합니다.

Postfix도 하나로 제한되지 않습니다.

```text
agent-assets-routing-validation.md
agent-assets-routing-validation-runtime.md
agent-assets-routing-validation-schema.md
```

여기서 `validation`은 `routing`에 대해서는 postfix지만, `runtime`과 `schema`를 묶을 때는 `agent-assets-routing-validation`이라는 더 구체적인 grouping key의 일부가 됩니다.

즉 prefix와 postfix는 고정된 한 단계의 문법 요소라기보다 **파일 이름을 왼쪽에서 오른쪽으로 확장하면서 계층적인 정렬 군집을 만드는 위치적 역할**로 볼 수 있습니다.

## Choosing the Sort Axis

어떤 의미를 앞쪽에 두느냐에 따라 filesystem 정렬에서 형성되는 군집이 달라집니다.

대상을 먼저 두면 관련 작업이 대상별로 모일 수 있습니다.

```text
routes-generate.py
routes-validate.py

rulesync-doctor.py
rulesync-preview.py
rulesync-validate.py

skills-install.py
skills-sync.py
```

작업을 먼저 두면 같은 파일들도 작업 이름을 중심으로 정렬됩니다.

```text
doctor-rulesync.py
generate-routes.py
install-skills.py
preview-rulesync.py
sync-skills.py
validate-routes.py
validate-rulesync.py
```

둘 다 이해 가능한 이름일 수 있습니다. **같은 directory에서 어떤 파일들을 함께 찾는 경우가 더 많은지**를 기준으로 앞쪽 grouping key를 선택합니다.

## Directory Context

Directory가 이미 충분한 맥락을 제공한다면 filename에서 같은 정보를 반복하지 않아도 됩니다.

```text
agent-assets/
├─ routing.md
├─ routing-policy.md
└─ validation.md
```

다음처럼 directory가 이미 제공하는 맥락을 filename마다 반복하면 이름만 길어질 수 있습니다.

```text
agent-assets/
├─ agent-assets-routing.md
└─ agent-assets-validation.md
```

반대로 하나의 directory 안에서 여러 domain이나 family가 섞여 있고 이를 함께 유지할 이유가 있다면 prefix가 유용한 grouping surface가 될 수 있습니다.

반복 prefix가 길어지고 관련 파일군이 독립적인 탐색 영역처럼 커지면 filename의 반복을 계속 늘리기보다 directory grouping과 비교해 봅니다.

## Boundaries

이 패턴은 **읽는 순서를 표현하는 numbering을 다루지 않습니다.**

```text
01-introduction.md
02-design.md
03-testing.md
```

이런 이름은 순서를 filesystem에 표현하려는 별도의 문제입니다. 여기서 다루는 목적은 순서가 아니라 **의미적으로 가까운 파일을 이름 정렬에서도 가깝게 만드는 것**입니다.

또한 다음을 목표로 하지 않습니다.

- 모든 파일에 prefix나 postfix를 강제하지 않습니다.
- filename만으로 repository의 전체 architecture를 표현하려 하지 않습니다.
- directory가 더 자연스러운 grouping boundary인데도 긴 prefix chain을 유지하지 않습니다.
- language, framework, tool이 요구하는 naming convention을 덮어쓰지 않습니다.
- locale, case sensitivity, natural sort 등 모든 filesystem·UI의 정렬 방식이 동일하다고 가정하지 않습니다. 주로 사용하는 이름 정렬에서 grouping cue가 유지되는 정도면 충분합니다.

Separator는 `-`, `_`, `.`, 기타 ecosystem convention 중 자연스러운 것을 사용합니다. 이 패턴의 본질은 특정 구분자가 아니라 **이름의 왼쪽에서 오른쪽으로 grouping axis를 구성하는 것**입니다.

## Short Form

> **파일 이름을 filesystem 정렬의 grouping key로 활용할 수 있습니다. Prefix는 domain·subdomain·family처럼 상위 범위를 모으고, subject 뒤의 postfix는 그 subject를 다시 작은 prefix처럼 확장해 하위 군집을 만듭니다. Prefix와 postfix는 각각 여러 단계가 될 수 있으며, 읽는 순서를 위한 numbering은 이 패턴에서 다루지 않습니다.**
