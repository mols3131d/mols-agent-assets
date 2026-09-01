---
description: 파일 이름의 prefix·subject·postfix를 정렬 키로 구성해 기본 filesystem 정렬에서도 관련 파일이 가까이 모이게 할 때 참고하는 naming pattern입니다.
---

# Filesystem Sort-Aware Naming

파일 이름을 **filesystem 정렬의 grouping key**로 활용해 함께 찾는 파일이 목록에서도 가까이 나타나게 할 수 있습니다. 이 패턴은 읽는 순서가 아니라 **어떤 의미를 이름 앞쪽에 두어 관련 파일을 모을지**를 다룹니다.

## Core

기본 형태는 다음과 같습니다.

```text
<prefix...>-<subject>-<postfix...>.<ext>
```

- **Prefix**는 domain·subdomain·family처럼 관련 파일을 넓은 범위에서 먼저 모읍니다.
- **Subject**는 파일이 직접 다루는 이름이나 주제입니다.
- **Postfix**는 subject 아래의 aspect·role·variant처럼 더 구체적인 구분입니다.

Prefix와 postfix는 각각 여러 단계가 될 수 있습니다.

```text
<domain>-<subdomain>-<family>-<subject>-<aspect>-<variant>.<ext>
```

Postfix로 확장된 이름은 다시 더 좁은 grouping key로 작동할 수 있습니다.

```text
agent-assets-routing.md
agent-assets-routing-validation.md
agent-assets-routing-validation-runtime.md
agent-assets-routing-validation-schema.md
```

여기서 `validation`은 `routing`의 postfix이면서, 다음 단계에서는 `agent-assets-routing-validation`이라는 더 구체적인 grouping key의 일부가 됩니다.

## Choosing the Sort Axis

같은 directory에서 **함께 찾는 경우가 많은 기준을 이름 앞쪽에 둡니다.** 무엇을 앞에 두느냐에 따라 정렬 군집이 달라집니다.

대상을 먼저 두면 대상별로 모입니다.

```text
routes-generate.py
routes-validate.py
skills-install.py
skills-validate.py
```

작업을 먼저 두면 작업별로 모입니다.

```text
generate-routes.py
install-skills.py
validate-routes.py
validate-skills.py
```

Directory가 이미 grouping 맥락을 충분히 제공하면 filename에서 같은 맥락을 반복하지 않습니다. 반복되는 prefix가 길어지고 파일군 자체가 독립적인 탐색 영역이 되면 directory grouping을 고려합니다.

## Boundaries

- 읽는 순서를 위한 `01-`, `02-` 같은 numbering은 다루지 않습니다.
- 모든 파일에 prefix나 postfix를 강제하지 않습니다.
- language, framework, tool이 naming convention을 소유하면 그 convention을 우선합니다.
