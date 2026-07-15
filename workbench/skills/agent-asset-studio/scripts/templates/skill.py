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

## Routing

1. Read `INDEX.csv` once.
2. Compare the request with each route's `use_when` and `avoid_when`.
3. Select the smallest route set that covers the request.
4. Read only the selected `entrypoint` files.
5. Load additional resources only when a workflow requires them.

Route by semantic intent, not keyword overlap. Do not scan `workflows/`.

## Ambiguity

- Select one route when it fully covers the request.
- Select multiple routes only when the request explicitly spans them.
- Ask one targeted question when routes imply materially different actions.
- State that the skill does not cover the request when no route matches.

## Rules

- Keep global constraints here; keep task procedures in workflow modules.
- Use exact entrypoints from `INDEX.csv`.
- Keep routing depth to one layer.

## Resources

- `INDEX.csv`: semantic route registry.
{resource_notes}

"""
