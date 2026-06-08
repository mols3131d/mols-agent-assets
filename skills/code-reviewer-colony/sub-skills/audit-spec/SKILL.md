---
name: audit-spec
description: Audits code changes against specifications, requirements documents, PRDs, and user stories.
---

# Specification Compliance Auditor Skill

Procedural guidelines for auditing whether code changes satisfy requested specifications, designs, or requirements.

## Goal

Ensure all features, rules, behaviors, and edge cases described in the product/technical specifications are fully and correctly implemented without missing requirements or unintended deviations.

## Review Steps

1. **Locate and Read Specifications**:
   - Identify the source of requirements: design documents, PRDs, specs, issues, or ticket descriptions.
   - Read and list all explicit and implicit requirements.

2. **Map Requirements to Code Changes**:
   - Trace each requirement to specific files and line ranges in the pull request.
   - For every rule or behavior in the spec, verify if the corresponding logic is present in the diff.

3. **Verify Compliance and Completeness**:
   - Confirm that all functional requirements are implemented.
   - Confirm that all non-functional requirements (e.g. constraints, performance, limits) are respected.
   - Check if edge cases or error handling scenarios described in the spec are implemented.

4. **Detect Discrepancies and Gap Analysis**:
   - Identify any requested requirements that were omitted or only partially implemented.
   - Spot any implemented features or changes that deviate from the specification or add undocumented complexity (feature creep).

5. **Generate Specification Compliance Report**:
   - Summarize findings in a checklist or tabular format containing:
     - Requirement / Specification Feature
     - Implementation Status (Fully Implemented / Partially Implemented / Missing)
     - Code References (relative paths to relevant code files/lines)
     - Notes / Discrepancies details

## Example Compliance Table

| Requirement / Spec Item | Status | Code Reference | Notes |
| :--- | :--- | :--- | :--- |
| Req 1: User authentication via JWT | Fully Implemented | [auth.py](../../../code-reviewer-colony/scripts/analyze_diff.py) (example) | Matches spec section 2.1 |
| Req 2: Rate limit of 60 req/min | Partially Implemented | [middleware.go](../../../code-reviewer-colony/sub-skills/INDEX.csv) | Logic is present but limit is hardcoded to 100 |
| Req 3: Soft delete for user accounts | Missing | N/A | No code implements this behavior in the diff |
