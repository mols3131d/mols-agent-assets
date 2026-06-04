from typing import Final

SKILL_TEMPLATE: Final[str] = """---
name: {skill_name}
description: {description}
{optional_frontmatter}---

# {skill_title}

## Overview

- 목표: 이 스킬이 에이전트에게 제공하는 능력을 1-2문장으로 설명한다.

## Triggers

- 이 스킬을 적용해야 하는 조건 및 상황을 기술한다.

## Exclusions

- 이 스킬을 사용하지 말아야 하는 예외 조건 및 상황을 기술한다.

## Workflow

- 이 스킬이 수행하는 기본 절차를 기술한다.

## Resources

{resource_notes}

---

## Rules

- <규칙 1>
- <규칙 2>
...

## Constraints

- <제약 1>
- <주의 2>
...

"""

ROUTING_SKILL_TEMPLATE: Final[str] = """---
name: {skill_name}
description: {description}
{optional_frontmatter}---

# {skill_title}

## Overview

- 목표: 이 스킬이 에이전트에게 제공하는 능력을 1-2문장으로 설명한다.

## Triggers

- 이 스킬을 적용해야 하는 조건 및 상황을 기술한다.

## Exclusions

- 이 스킬을 사용하지 말아야 하는 예외 조건 및 상황을 기술한다.

## Routing Sub Skills

1. Read `sub-skills/INDEX.csv`.
2. Pick one sub-skill by `trigger` and `exclusion`.
3. Read only the selected sub-skill file.

## Resources

{resource_notes}

## Rules

- <규칙 1>
- <규칙 2>
...

## Constraints

- <제약 1>
- <주의 2>
...

"""
