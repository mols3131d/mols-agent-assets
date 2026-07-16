---
name: mols-agent-assets
description: USE WHEN the user wants to create, compile, or manage agent assets in the mols-agent-assets repository. INCLUDES building .human.md sources into optimized .md binaries. EXCLUDES general coding tasks outside of agent asset management.
---

# mols-agent-assets

## Overview

A routing skill designed to manage the workspace and compilation pipeline for agent assets within the `mols-agent-assets` repository.

## Goal

Enforce the human-agent asset pipeline (compiling `.human.md` to `.md`), maintain repository structure, and route tasks to specialized asset-management workflows.

## When to Use

Use this skill when requested to create a new asset, build/compile an existing `.human.md` into an `.md` file, or manage asset synchronization in this repository.

## Instructions

- Adhere strictly to the human-agent asset pipeline: never modify `.md` binaries manually if a `.human.md` source exists.
- Follow the routing algorithm below to select the appropriate workflow for the user's request.

## Routing

1. Read `workflows/INDEX.csv` once.
2. Identify the requested outcome, operation, object, and constraints.
3. Eliminate routes matching `excludes`.
4. Select the minimum route set matching `use_when`.
5. Resolve material ambiguity with one targeted question.
6. Resolve selected IDs from the index directory and load only those files.
7. Load referenced resources only when a selected workflow requires them.
8. Run each selected workflow's validation before completion.

Route by semantic intent, not keyword overlap. Do not scan `workflows/` to discover routes.

## Ambiguity

- Select one route when it fully covers the request.
- Select multiple routes only when the request explicitly spans them.
- Ask one targeted question when remaining routes imply materially different actions.
- If no route matches, state that the skill does not cover the request.
