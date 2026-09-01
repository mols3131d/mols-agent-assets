---
description: 파일 이름에서 하이픈은 구조 경계로, 언더바는 한 구조 단위 안의 띄어쓰기로 사용해 의미 단위를 구분할 때 참고하는 naming pattern입니다.
---

# Hyphen Structure, Underscore Spacing

파일 이름의 구분자마다 역할을 나누면 **어디가 구조 경계이고 어디가 하나의 이름인지** 더 쉽게 읽을 수 있습니다.

이 패턴에서는 하이픈(`-`)을 서로 다른 구조 단위를 나누는 데 사용하고, 언더바(`_`)를 하나의 구조 단위 안에서 사람이 읽을 때의 띄어쓰기처럼 사용합니다.

## Core

기본 형태는 다음처럼 볼 수 있습니다.

```text
<structural_unit>-<structural_unit>-<structural_unit>.<ext>
```

각 구조 단위가 여러 단어로 이루어지면 그 안의 띄어쓰기를 언더바로 표현합니다.

```text
<domain_name>-<topic_name>-<detail_name>.<ext>
```

예를 들어 다음 파일 이름은 세 개의 구조 단위로 읽을 수 있습니다.

```text
agent_assets-routing_policy-validation_rules.md
```

```text
agent_assets     → agent assets
routing_policy   → routing policy
validation_rules → validation rules
```

하이픈은 `agent_assets → routing_policy → validation_rules`라는 구조적 분리를 보여주고, 언더바는 각 단위 안의 단어들이 하나의 이름을 이룬다는 것을 보여줍니다.

## Structural Units

구조 단위는 domain, subdomain, family, subject, aspect, role처럼 파일을 분류하거나 탐색할 때 의미 있는 경계가 될 수 있습니다.

```text
<domain>-<subdomain>-<subject>-<aspect>.<ext>
```

각 단위가 한 단어일 수도 있고 여러 단어일 수도 있습니다.

```text
agent_assets-skill-authoring_guide.md
agent_assets-skill-validation_rules.md
agent_assets-subagent-authoring_guide.md
```

여기서 `agent_assets`, `skill`, `authoring_guide`는 각각 하나의 구조 단위입니다. `agent_assets`와 `authoring_guide` 내부의 언더바는 구조를 더 나누지 않고 한 이름 안의 띄어쓰기 역할만 합니다.

구조 단위의 개수를 고정하지 않습니다. 실제 파일 이름에 필요한 만큼의 의미 있는 경계만 사용합니다.

## Reading the Filename

구분자를 기준으로 파일 이름을 두 단계로 읽을 수 있습니다.

먼저 하이픈을 따라 큰 구조를 읽습니다.

```text
agent_assets - routing_policy - validation_rules
```

그다음 각 구조 단위 안의 언더바를 띄어쓰기처럼 읽습니다.

```text
agent assets
routing policy
validation rules
```

따라서 하이픈과 언더바를 같은 종류의 단어 구분자로 섞어 쓰는 것보다 파일 이름의 의미 구조를 더 명시적으로 표현할 수 있습니다.

## Composition with Sort-Aware Naming

Filesystem 정렬을 이용해 관련 파일을 모으는 naming과 함께 사용하면 하이픈으로 grouping structure를 드러내면서 각 grouping key의 여러 단어를 언더바로 묶을 수 있습니다.

```text
agent_assets-routing_policy.md
agent_assets-routing_policy-runtime_checks.md
agent_assets-routing_policy-validation_rules.md
agent_assets-validation_policy.md
```

이름 앞쪽의 구조 단위가 같을수록 기본 정렬에서도 가까이 모이기 쉽고, 각 구조 단위 안의 여러 단어는 언더바 덕분에 하나의 의미 단위로 읽힙니다.

이 패턴 자체는 **어떤 구조 단위를 앞에 둘지, 무엇을 주된 정렬 축으로 삼을지 정하지 않습니다.** 여기서는 선택된 구조를 파일 이름 안에서 어떤 구분자로 표현할지만 다룹니다.

## Boundaries

이 패턴은 **구분자의 의미를 나누는 방법**에 초점을 둡니다.

- 읽는 순서를 위한 `01-`, `02-` 같은 numbering은 다루지 않습니다.
- 하이픈 개수나 구조 깊이를 고정하지 않습니다.
- 언더바 개수도 제한하지 않습니다. 하나의 구조 단위가 여러 단어라면 필요한 만큼 사용할 수 있습니다.
- 어떤 domain·family·subject를 앞에 둘지와 같은 grouping axis 선택은 이 패턴이 소유하지 않습니다.
- filename만으로 repository architecture 전체를 표현하려 하지 않습니다.
- directory가 이미 충분한 구조를 제공하면 filename에 같은 구조를 반복하지 않아도 됩니다.
- language, framework, tool이 filename 형식을 강하게 소유하면 그 convention을 우선합니다.

이 패턴은 모든 파일 이름을 반드시 같은 형식으로 만들기 위한 문법이 아니라, **하이픈과 언더바를 함께 사용할 때 각각의 역할을 일관되게 부여하는 방법**입니다.

## Short Form

> **하이픈은 파일 이름의 구조 경계를 나누고, 언더바는 하나의 구조 단위 안에서 띄어쓰기처럼 사용합니다. 구조 단위는 여러 개일 수 있고 각 단위 안의 언더바도 여러 개일 수 있습니다. 이를 통해 파일 이름에서 grouping structure와 multi-word name을 서로 다른 시각적 신호로 구분할 수 있습니다.**
