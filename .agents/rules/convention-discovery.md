---
trigger: model_decision
description: Logic-dense protocol for automated convention discovery.
---

# Convention Discovery Protocol (CDP)

## 1. Discovery Syntax

- `[SCAN]` -> `list_dir(CONTEXT_ROOT)` -> Extract `Nodes` | `Casing_Style`
- `[MAP]` -> `Target_Intent` -> `Match(Nodes)` -> `Identify(Active_Path)`
- `[RECURSE]` -> `Match_Fail` -> `Search(Logical_Containers)` -> `Identify(Nested_Path)`
- `[ANALYZE]` -> `Project_Metadata` -> `Determine(Native_Norms)`

## 2. Decision Logic

- **Precedence**: `History` > `Existing_Structure` > `Hardcoded_Hint`
- **Integrity**: `Exists(Path)` -> `Lock(Path)` | `NEVER` create redundant root entries.
- **Selection**: `Conflict` -> `ArgMax(Activity_Timestamp | Item_Density)`
- **Styling**: `Apply(Casing_Style)` to all `New_Assets`

## 3. Failsafe

- `Structure_Null` -> `grep_search(CONTEXT_ROOT, Keywords(Intent))` -> `Infer_Pattern`
