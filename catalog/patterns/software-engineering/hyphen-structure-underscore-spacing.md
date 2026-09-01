---
description: 파일 이름에서 하이픈은 구조 경계로, 언더바는 한 구조 단위 안의 띄어쓰기로 사용해 의미 단위를 구분할 때 참고하는 naming pattern입니다.
---

# Hyphen Structure, Underscore Spacing

파일 이름에서 **하이픈(`-`)은 구조 경계**, **언더바(`_`)는 한 구조 단위 안의 띄어쓰기**로 사용할 수 있습니다. 이 패턴은 어떤 구조를 선택할지가 아니라, 선택된 구조를 filename 안에서 어떻게 구분할지를 다룹니다.

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

하이픈은 `agent_assets → routing_policy → validation_rules`라는 구조적 분리를 보여주고, 언더바는 각 구조 단위 안의 여러 단어를 하나의 이름으로 묶습니다.

구조 단위의 수와 각 단위 안의 언더바 수는 고정하지 않습니다. 필요한 만큼의 의미 있는 경계와 단어만 사용합니다.

## Boundaries

- 어떤 domain·family·subject를 앞에 둘지는 이 패턴이 정하지 않습니다.
- 읽는 순서를 위한 `01-`, `02-` 같은 numbering은 다루지 않습니다.
- language, framework, tool이 filename 형식을 소유하면 그 convention을 우선합니다.
