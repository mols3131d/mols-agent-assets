# Skill DRY

Use this reference only for Agent Skills or equivalent repeatable workflows loaded on demand.

## Preserve

Preserve the skill's user purpose, trigger or description, discovery metadata, workflow behavior, tools or permissions, outputs, package boundary, dependencies, and release lifecycle.

Two skills are not duplicates merely because they share procedures or domain knowledge. Different triggers, permissions, outputs, dependencies, or independent release ownership are meaningful boundaries.

## DRY Inside One Skill

- Keep only content needed by every invocation in `SKILL.md`.
- Move conditional detail to a focused resource and give it an explicit load condition.
- Remove repeated guidance between `SKILL.md`, workflows, and references once one canonical location is clear.
- Do not create a resource that is always loaded only to shorten `SKILL.md`.
- Keep one responsibility owner; supporting resources refine that responsibility rather than becoming hidden sibling skills.

## DRY Across Skills

Treat two skills as consolidation candidates only when their user purpose, activation boundary, authority, permissions, outputs, dependencies, and lifecycle are compatible.

If they should remain independently invocable, keep them separate. Prefer explicit routing or composition only when the project and runtime support that relationship and it does not create a hidden cross-package dependency.

Do not extract shared text into an external common file merely to make independent skill capsules physically DRY. Do not retire a discoverable skill entrypoint unless its invocation responsibility is itself redundant and retirement is authorized.

## Verify

After changes, confirm intended requests still select the correct skill, conditional resources still load only when needed, discovery metadata remains valid, and no responsibility, permission, dependency, or output contract was lost.
