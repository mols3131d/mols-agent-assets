from typing import Final

RULE_TEMPLATE: Final[str] = """---
name: {rule_name}
description: {description}
{optional_frontmatter}---

# Rule: {rule_title}

## Overview

- 목적: 이 규칙이 규제하거나 강제하려는 행동 방침을 1-2문장으로 기술한다.

## Rationale

- 이 규칙이 왜 제정되었는지 배경과 당위성을 설명한다.

## Enforcement

- 에이전트가 어떤 상황에서 이 규칙을 준수해야 하는지 구체적인 조건을 기술한다.
- 예외 상황이 있다면 명확히 기술한다.

## Violation Cases

- 이 규칙을 위반하는 잘못된 예시를 기술한다.

## Compliance Cases

- 이 규칙을 잘 지켜 수정한 올바른 예시를 기술한다.
"""
