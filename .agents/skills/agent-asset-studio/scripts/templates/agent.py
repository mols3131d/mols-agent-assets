from typing import Final

AGENT_TEMPLATE: Final[str] = """---
name: {agent_name}
description: {description}
version: "1.0.0"
model: "TODO: e.g., gemini-2.5-flash"
system-prompt: "TODO: e.g., prompts/system.md"
allowed-tools: "TODO: e.g., search_web, read_file"
{optional_frontmatter}---

# Agent Persona: {agent_title}

## Profile

- 역할: 이 에이전트가 수행할 주요 역할을 정의한다.
- 목표: 에이전트가 궁극적으로 달성해야 하는 목표를 1-2문장으로 설명한다.

## System Prompt Guidelines

- 에이전트의 행동 지침, 말투, 의사결정 시 고려해야 할
  페르소나 관련 핵심 지침을 기술한다.

## Capabilities

- 에이전트가 활용할 수 있는 핵심 스킬(Skills) 및 도구(Tools)의
  목록이나 동작 메커니즘을 기술한다.

## Interaction Workflow

- 사용자가 요청을 전달했을 때 에이전트가 단계를 밟아 처리하는 워크플로우를 기술한다.
"""
