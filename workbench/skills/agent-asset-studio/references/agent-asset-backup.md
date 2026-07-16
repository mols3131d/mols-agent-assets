# Agent Asset Backup Protocol

## Goal

Preserve the original state of an existing Markdown asset before modification to allow for clean rollbacks and diff comparisons.

## When to Use

Use this protocol whenever a workflow or rule requires modifying an existing Markdown asset in the workspace.

## Instructions

- Before making any edits to an existing Markdown asset, save a copy of the source as `<filename>.original.md`.
