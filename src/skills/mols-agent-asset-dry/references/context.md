# Context DRY

Use this reference when a DRY move changes references, inheritance, composition, imports, or the context loaded by an asset consumer.

## Optimize Loaded Context, Not File Count

A smaller file tree is not automatically more DRY for an LLM. Prefer a shared source only when consumers can reach it without loading materially more irrelevant context or weakening activation boundaries.

Physical repetition can be correct when removing it would require unrelated context, unsupported indirection, or a hidden dependency. Keep source authority explicit when repetition remains.

## Reference Topology

- Prefer host-native, explicit references or composition over ad hoc include conventions.
- Keep dependency paths shallow and directional.
- Do not create circular references or inheritance cycles.
- Do not move conditional detail into an always-loaded common asset.
- Do not make independent packages depend on a sibling file merely to save a few repeated lines.
- Reuse an existing shared source only when its responsibility and load boundary already fit the consumers.

## Context Tradeoff

Before centralizing content, compare the before-and-after load behavior for representative consumers. A DRY move is a regression when it removes physical repetition but increases irrelevant always-loaded context, obscures ownership, or adds more indirection than the repeated content justified.

Prefer the simpler local repetition when the abstraction has no clear loading or ownership benefit.

## Verify

After changing references or composition, confirm every dependency resolves, no cycle was introduced, conditional content still loads conditionally, and representative consumers receive the intended context without unrelated additions.
