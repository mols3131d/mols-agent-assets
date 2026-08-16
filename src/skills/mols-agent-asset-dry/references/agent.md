# Agent DRY

Use this reference for custom agent or subagent profiles defined primarily by natural-language role instructions.

## Preserve

Preserve role or mission, delegation or invocation boundary, tools and permissions, model or host constraints, handoff behavior, expected outputs, and independent ownership or lifecycle.

Similar expertise does not make two agents duplicates when their authority, tools, delegation boundary, or output responsibility differs.

## Repeated Agent Content

- Treat two agent profiles as consolidation candidates only when role, delegation boundary, authority, tools or permissions, outputs, and lifecycle are compatible.
- Remove repeated instructions inside one profile when one statement already governs the same behavior.
- Keep specialized agents when they narrow responsibility, permissions, or expected outputs even if much of the surrounding guidance is shared.
- Use host-native composition or shared context only when the dependency is explicit and does not blur agent authority.

## Shared Policy

Do not move common policy from several agents into a rule merely to reduce text unless that cross-type migration is explicitly requested and the rule would have the same intended activation and authority.

Do not give an agent broader tools or permissions as a side effect of consolidation.

## Handoffs

If two agents cooperate through delegation or handoff, repeated interface expectations may be intentional protocol. Remove them only when one authoritative contract is reliably available to both sides.

## Verify

After changes, confirm each intended task still reaches the correct agent, delegation boundaries remain clear, tools and permissions are unchanged, and handoff or output contracts still hold.
