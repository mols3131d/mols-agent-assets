---
name: routing-skill-visualizations
description: >
  USE WHEN: referencing Mermaid diagrams for agent skill loading hierarchies and architectures.
  EXCLUDES: routing code implementation, folder validation, or CSV index maintenance.
---

# Skill & Router Architecture Visualizations

## Goal

Provide Mermaid diagrams visualizing the progressive loading hierarchies of agent skills, ranging from simple single-file skills to multi-tiered routing architectures.

## 1. Single-File Skill Pattern (`SKILL.md` only)

Simple, self-contained skill where all instructions, procedures, and validation steps reside in a single root file.

```mermaid
graph TD
    User([User Request]) --> Router[SKILL.md<br/>Root Entry & Execution]
```

## 2. Skill with Shared References Pattern (`SKILL.md` -> `references/`)

A skill that delegates passive knowledge, specifications, or rules to external reference files loaded on demand.

```mermaid
graph TD
    User([User Request]) --> Router[SKILL.md<br/>Root Execution]
    Router -->|On-demand load| Ref[references/*.md<br/>Passive Knowledge / Specs]
```

## 3. Composite Routing Skill Pattern (`SKILL.md` -> `workflows/INDEX.csv` -> `references/`)

A dedicated routing skill where `SKILL.md` acts as a pure router, evaluating incoming intent via `workflows/INDEX.csv`, dispatching to a specific workflow module in `workflows/`, and loading passive references only when needed.

```mermaid
graph TD
    User([User Request]) --> Router["SKILL.md<br/>Skill Router"]
    Router -->|1. Parse Index| Index["workflows/INDEX.csv<br/>Route Registry"]
    Index -->|2. Dispatch Route ID| Workflow["workflows/action.md<br/>Workflow Module"]
    Workflow -->|3. On-demand load| Ref["references/*.md<br/>Shared References"]
```

## 4. Multi-Tiered Routing with Progressive Help Pattern (`SKILL.md` -> `workflows/INDEX.csv` -> `workflows/--help.md` -> `references/`)

A routing skill supporting optional command flag workflows (`--help`, `--config--help`, etc.) for progressive disclosure, where flag workflows load detailed reference schemas and architectural guides when explicitly requested.

```mermaid
graph TD
    User([User Request / Flag]) --> Router["SKILL.md<br/>Skill Router"]
    Router -->|1. Parse Flag / Index| Index["workflows/INDEX.csv<br/>Route Registry"]
    Index -->|2a. Dispatch Action Route| Workflow["workflows/action.md<br/>Action Module"]
    Index -->|2b. Dispatch Flag Route| FlagHelp["workflows/--help.md / --config--help.md<br/>Progressive Disclosure Help Module"]
    Workflow -->|3a. Load Task Ref| Ref["references/task-spec.md<br/>Task Reference"]
    FlagHelp -->|3b. Load Detailed Schema Ref| SchemaRef["references/progressive-help-pattern.md<br/>Detailed Schema & Architecture Ref"]
```
