# Subagent Orientation Pattern Plan

Based on `subagent-orientation-pattern-research.md`.

## Goal

Make the pattern conceptually precise and reusable while keeping it small enough to act as a pattern capsule rather than a framework guide.

## Planned changes

1. Reframe the document around two independent design dimensions:
   - responsibility orientation: `Role-oriented ↔ Capability-oriented`
   - execution context: `Shared ↔ Isolated`
1. Keep Role-oriented and Capability-oriented as emphasis, not types.
1. Move context isolation out of the Capability-oriented definition and present it as a frequent fit and design reason.
1. Keep `Handoff as Context Boundary`, but tighten it to minimum-sufficient context transfer.
1. Replace `Skill vs Subagent` framing with an execution-boundary choice:
   - inline/shared Skill execution
   - isolated/forked Skill where the runtime supports it
   - capability-oriented Subagent when a delegated context/tool/permission/specialist boundary is useful
1. Keep GitHub Copilot `context: fork` only as a current implementation example and link to upstream authority instead of owning its semantics.
1. Remove duplicated explanation and implementation-detail prose that does not help a reader apply the pattern.

## Acceptance

- The pattern can be understood without vendor knowledge.
- Neither axis is presented as a taxonomy.
- Context isolation is important but not made synonymous with Capability-oriented design.
- Skills and Subagents are composable, not falsely exclusive.
- Vendor-specific behavior is example/reference only.
- One Markdown capsule remains sufficient; no schema, bundle, or additional pattern hierarchy is introduced.
