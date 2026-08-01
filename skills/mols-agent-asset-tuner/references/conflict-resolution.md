# Conflict Resolution

Apply precedence within the approved task:

1. explicit current user decision
1. accepted project specification and policy
1. tested project contract
1. project architecture and decisions
1. current implementation and configuration
1. source asset behavior
1. external vendor guidance
1. inference

Rules:

- Code shows current behavior; it does not alone define desired behavior.
- Source behavior may be retained only when it does not conflict with higher
  project authority.
- When user intent and accepted project specification conflict, expose the
  conflict rather than silently choosing.
- Runtime-specific source metadata is adapted or isolated, not copied as a
  portability claim.
- Resolve terminology to project language while retaining provenance mappings.
