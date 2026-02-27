---
role: ENDPOINT
intent: Operational_Synchronization
target: AI_Agent
protocol: ACE (Agent_Context_Engineering)
---

# OVERVIEW

`mols-agent` ::= High-density environment for {Rule | Workflow | Protocol} engineering.

# ONBOARDING::BOOT_SEQUENCE

1. **KERNEL**: Read `/.agents/rules/rules.md` [CRITICAL: Reasoning_Logic].
2. **IDENTITY**: Read `/.agents/rules/constitution.md` [Role_Boundary].
3. **SCOPE**: Read `/README.md` [Technical_Structure].
4. **INTENT**: Read `/README.ko.md` [Human_Context_Sync].

# DIRECTORY STRUCTURE

- **Control_Plane**: `/.agents/` -> {Rules | Workflows | Brain}
- **Production_Plane**: `/studio/` -> {Active_Assets | Outputs}
- **Governance**: `/docs/` -> {Conventions | Standard_Operating_Procedures}
- **Blueprint**: `/templates/` -> {Structural_Patterns}

# CONSTRAINTS::OPERATIONAL

- **Sync**: technical[EN] + context[KR] (Dual-Doc).
- **Files**: No direct `rm`. Move to `/.trash/`.
- **Commits**: Conventional Commits. Logical Unit Atomic.
- **Workflow**: Check `/.agents/workflows/` before ad-hoc execution.

# EXECUTION::ENTRY

## START_STATE ::= {Identify_Task -> Read_AGENT.md -> Sync_Rules -> Execute}

_EOF: Entry Point for Autonomous Operations_
