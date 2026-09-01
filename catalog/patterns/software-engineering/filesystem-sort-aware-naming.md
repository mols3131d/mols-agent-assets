---
description: 파일 이름의 prefix·subject·postfix를 정렬 키로 구성해 기본 filesystem 정렬에서도 관련 파일이 가까이 모이게 할 때 참고하는 naming pattern입니다.
---

# Filesystem Sort-Aware Naming

파일 이름을 **filesystem 정렬의 grouping key**로 활용해 함께 찾는 파일이 목록에서도 가까이 나타나게 할 수 있습니다.

이 패턴은 읽는 순서를 정하지 않습니다. 어떤 의미를 이름의 앞쪽에 둘지 선택해 **의미적으로 가까운 파일의 정렬 위치를 가깝게 만드는 것**에 초점을 둡니다.

## Core

기본 형태는 다음과 같습니다.

```text
<prefix...>-<subject>-<postfix...>.<ext>
```

`prefix`와 `postfix`는 각각 하나로 제한되지 않습니다.

```text
<prefix-1>-<prefix-2>-<subject>-<postfix-1>-<postfix-2>.<ext>
```

의미 구조는 다음처럼 큰 범위에서 작은 범위로 이어질 수 있습니다.

```text
<domain>-<subdomain>-<family>-<subject>-<aspect>-<variant>.<ext>
```

- **Prefix**는 domain·subdomain·family처럼 관련 파일을 넓은 범위에서 먼저 모으는 정렬 키입니다.
- **Subject**는 파일이 직접 다루는 이름이나 주제입니다.
- **Postfix**는 subject 아래의 aspect·role·variant처럼 더 구체적인 구분입니다.

Postfix는 고정된 끝 장식이 아닙니다. 이름이 확장되면 그 전체가 다시 더 좁은 grouping key로 작동할 수 있습니다.

```text
agent-assets-routing.md
agent-assets-routing-validation.md
agent-assets-routing-validation-runtime.md
agent-assets-routing-validation-schema.md
```

여기서 `validation`은 `routing`에 대해서는 postfix지만, 다음 단계에서는 `agent-assets-routing-validation`이라는 더 구체적인 grouping key의 일부가 됩니다.

단계 수를 늘리는 것 자체가 목적은 아닙니다. 실제 탐색과 grouping에 의미가 있는 요소만 사용합니다.

## Choosing the Sort Axis

이름의 앞쪽에 무엇을 두느냐에 따라 같은 파일도 다른 방식으로 모입니다.

대상을 먼저 두면 대상별 작업이 모입니다.

```text
routes-generate.py
routes-validate.py

rulesync-doctor.py
rulesync-preview.py
rulesync-validate.py

skills-install.py
skills-sync.py
```

작업을 먼저 두면 작업별 대상이 모입니다.

```text
doctor-rulesync.py
generate-routes.py
install-skills.py
preview-rulesync.py
sync-skills.py
validate-routes.py
validate-rulesync.py
```

둘 다 자연스러울 수 있습니다. **같은 directory에서 어떤 파일을 함께 찾는 경우가 더 많은지**를 기준으로 주된 정렬 축을 선택합니다.

## Directory Boundary

Directory가 이미 충분한 grouping 맥락을 제공하면 filename에서 같은 정보를 반복하지 않아도 됩니다.

```text
agent-assets/
├─ routing.md
├─ routing-policy.md
└─ validation.md
```

반대로 한 directory에 여러 domain이나 family를 함께 두어야 한다면 prefix가 유용한 grouping surface가 될 수 있습니다.

반복 prefix가 길어지고 관련 파일군이 독립적인 탐색 영역처럼 커지면 filename을 계속 늘리기보다 directory grouping과 비교합니다.

## Boundaries

- 읽는 순서를 위한 `01-`, `02-` 같은 numbering은 다루지 않습니다.
- 모든 파일에 prefix나 postfix를 강제하지 않습니다.
- filename만으로 repository architecture 전체를 표현하려 하지 않습니다.
- directory가 더 자연스러운 grouping boundary라면 긴 prefix chain을 유지하지 않습니다.
- language, framework, tool이 naming convention을 소유하면 그 convention을 우선합니다.
- locale, case sensitivity, natural sort 등 모든 filesystem·UI의 정렬 방식이 같다고 가정하지 않습니다. 주로 사용하는 이름 정렬에서 grouping cue가 유지되면 충분합니다.

Separator 자체는 이 패턴의 핵심이 아닙니다. `-`, `_`, `.`, 기타 ecosystem convention 중 자연스러운 표현을 사용할 수 있으며, 이 패턴은 **이름의 왼쪽에서 오른쪽으로 어떤 grouping axis를 구성할지**를 다룹니다.
