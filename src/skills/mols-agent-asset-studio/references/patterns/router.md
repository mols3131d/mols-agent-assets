---
name: router-pattern
description: >
  Establish router asset boundaries, intent navigation, and routing instruction design for progressive disclosure.
  Use when designing router assets or embedding routing instructions into workflows.
  Does not apply to single-file skills or monolithic scripts.
---

# Router Pattern

Connect request intents with downstream assets seamlessly through progressive disclosure and semantic navigation.

## 1. Router Asset Concept

A Router asset maps user requests to specific execution workflows or knowledge assets, protecting context by loading targets on demand.

| Pattern | Common Examples | Focus |
| :--- | :--- | :--- |
| **Path Router** | Directory index (e.g. `INDEX.md, INDEX.csv`) | Resolves assets within a specific folder scope by file path. |
| **Intent Router** | Dedicated router directory or topic index | Resolves assets based on specialized goals or domain topics. |

## 2. Routing Mechanics & Instructions

Guidelines for writing and evaluating inline routing logic within prompts, workflows, or routers:

- **Semantic Over Keyword**: Route by underlying goal and constraints, not literal keyword matching.
- **Description Boundaries**: Put positive scope and exclusions together in each workflow `description`.
- **Minimal Selection**: Select the smallest route set that covers the requested outcome.
- **Ambiguity Resolution**: Ask targeted questions when remaining routes imply materially different actions.

## 3. Creating & Inspecting Routing Methods

When inspecting existing skills or creating new routing logic:

1. **Analyze Domain Scope**: Determine if workflows share a common domain or have unrelated triggers.
2. **Define Boundaries**: Write a `description` containing positive scope and explicit exclusions.
3. **Establish Route Index**: Generate `name,description` entries from workflow frontmatter.
