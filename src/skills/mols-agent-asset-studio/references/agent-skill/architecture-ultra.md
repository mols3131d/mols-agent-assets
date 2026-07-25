---
name: architecture-ultra
description: >
  USE WHEN: structuring complex agent skill assets by segregating routing, workflows, and CLI commands out of references.
  EXCLUDES: basic single-file or standard shared-reference skill structures.
---

# Agent Skill Architecture Ultra

> [!NOTE]
> Prior knowledge: [`architecture.md`](architecture.md)

Advanced directory partitioning strategy to prevent asset clutter in `references/`. Keep passive knowledge, guidelines, and principles inside `references/`, while offloading structural and operational assets into specialized directories.

## Directory Ultra Breakdown

| Path | Required | Description |
| :--- | :---: | :--- |
| `references/` | ✅ | Passive knowledge, design specifications, and core principles. |
| `workflows/` | ❌ | Actionable procedural guidelines and task execution modules. |
| `router/` | ❌ | Dedicated routing logic and decision matrix assets. |
| `command/` | ❌ | Command-line interface flag handlers (e.g. `--help.md`, `--init.md`, `--config.md`, `--route.md`). |

## Patterns

### 1. Direct Flow

```mermaid
graph LR
    User([Request]) --> Entry[SKILL.md]
    Entry --> RootRouter[Root Router]
    RootRouter --> Action[Workflows]
    Action --> Knowledge[References]
```

### 2. Cascading Flow

```mermaid
graph LR
    User([Request]) --> Entry[SKILL.md]
    Entry --> RootRouter[Root Router]
    RootRouter --> Router1[Router 1]
    Router1 --> Action[Workflows]
    Action --> Router2[Router 2]
    Router2 --> Knowledge[References]
```
