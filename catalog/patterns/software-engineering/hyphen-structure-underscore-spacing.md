---
description: 파일 이름에서 하이픈은 구조 경계로, 언더바는 한 구조 단위 안의 띄어쓰기로 사용해 의미 단위를 구분할 때 참고하는 naming pattern입니다.
---

# Hyphen Structure, Underscore Spacing

파일 이름에서 **하이픈(`-`)은 구조 경계**, **언더바(`_`)는 한 구조 단위 안의 띄어쓰기**로 사용할 수 있습니다. 두 구분자에 다른 역할을 주면 어디가 구조이고 어디가 하나의 이름인지 더 쉽게 읽을 수 있습니다.

이 패턴은 어떤 domain·family·subject를 앞에 둘지 결정하지 않습니다. 선택된 구조를 filename 안에서 **어떤 구분자로 표현할지**만 다룹니다.

## Core

기본 형태는 다음과 같습니다.

```text
<structural_unit>-<structural_unit>-<structural_unit>.<ext>
```

한 구조 단위가 여러 단어라면 그 안의 띄어쓰기를 언더바로 표현합니다.

```text
<domain_name>-<topic_name>-<detail_name>.<ext>
```

예를 들어:

```text
agent_assets-routing_policy-validation_rules.md
```

다음처럼 읽습니다.

```text
agent_assets     → agent assets
routing_policy   → routing policy
validation_rules → validation rules
```

하이픈은 `agent_assets → routing_policy → validation_rules`라는 구조적 분리를 보여주고, 언더바는 각 단위 안의 단어를 하나의 이름으로 묶습니다.

구조 단위의 수와 각 단위 안의 언더바 수는 고정하지 않습니다. 필요한 만큼의 의미 있는 경계와 단어만 사용합니다.

## Structural Units

구조 단위는 domain, subdomain, family, subject, aspect, role처럼 파일을 분류하거나 탐색할 때 의미 있는 경계가 될 수 있습니다.

```text
agent_assets-skill-authoring_guide.md
agent_assets-skill-validation_rules.md
agent_assets-subagent-authoring_guide.md
```

여기서 `agent_assets`, `skill`, `authoring_guide`는 각각 하나의 구조 단위입니다. `agent_assets`와 `authoring_guide` 안의 언더바는 구조를 더 나누지 않고 띄어쓰기 역할만 합니다.

## Composition with Sort-Aware Naming

Filesystem 정렬을 이용한 grouping과 함께 쓰면 하이픈은 grouping hierarchy를 드러내고, 언더바는 각 grouping key 안의 여러 단어를 묶습니다.

```text
agent_assets-routing_policy.md
agent_assets-routing_policy-runtime_checks.md
agent_assets-routing_policy-validation_rules.md
agent_assets-validation_policy.md
```

앞쪽의 구조 단위가 같을수록 기본 이름 정렬에서도 가까이 모이기 쉽습니다. 다만 **무엇을 앞에 둘지와 어떤 정렬 축을 선택할지는 이 패턴의 책임이 아닙니다.**

## Boundaries

- 읽는 순서를 위한 `01-`, `02-` 같은 numbering은 다루지 않습니다.
- 하이픈 개수나 구조 깊이를 고정하지 않습니다.
- 언더바 개수도 제한하지 않습니다.
- 어떤 domain·family·subject를 앞에 둘지는 정하지 않습니다.
- filename만으로 repository architecture 전체를 표현하려 하지 않습니다.
- directory가 이미 충분한 구조를 제공하면 filename에서 같은 구조를 반복하지 않아도 됩니다.
- language, framework, tool이 filename 형식을 소유하면 그 convention을 우선합니다.

이 패턴은 모든 filename을 같은 문법으로 강제하려는 것이 아니라, **하이픈과 언더바를 함께 사용할 때 서로 다른 의미를 일관되게 부여하는 방법**입니다.
