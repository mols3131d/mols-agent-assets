from typing import Final

KANBAN_DOCUMENT_TEMPLATE: Final[str] = """---
id: "{card_id}"
title: "{title}"
status: "{status}"
priority: "{priority}"
description: "{description}"
assignee: "{assignee}"
tags: {tags}
---

# {card_id}: {title}

## Description (카드 설명)

카드 상세 설명 및 요구사항을 입력하세요.

## Checklist (체크리스트)

- [ ] 할 일 1
"""
