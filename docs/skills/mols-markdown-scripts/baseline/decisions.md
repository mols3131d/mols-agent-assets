# Decisions

## Accepted

### **[Scripts] Markdown generation script**

- DECISION | **Python generator** - Create script for automatic Markdown generation.
- REASON | **Automation** - Automates document scaffolding and enforces consistency.
- IMPACT | **Less overhead** - Reduces model overhead by generating standardized structures automatically.

### **[Validation] Markdown frontmatter validation script**

- DECISION | **YAML validator** - Implement validator for frontmatter integrity.
- REASON | **Data integrity** - Prevents missing or malformed metadata fields.
- IMPACT | **Composable failure** - Validation returns failure for invalid frontmatter so a host project can wire it into CI, pre-commit, or another gate without changing validator semantics.

### **[Validation] Markdown header validation script**

- DECISION | **Hierarchy validator** - Implement validator for header structure.
- REASON | **Structure standard** - Ensures heading structure matches the selected document contract.
- IMPACT | **Early warning** - Automated checks flag invalid heading nesting and structure issues.

### **[Dependencies] Minimize dependencies**

- DECISION | **Strict limitation** - Allow adding external libraries but minimize their use.
- REASON | **Maintainability** - Keeps the asset lightweight and reduces dependency conflicts.
- IMPACT | **Standard library first** - Favor Python standard libraries or existing dependencies over new external packages.

### **[Dependencies] Fail explicitly when required tooling is unavailable**

- DECISION | **Deterministic dependency boundary** - Required parser or validation dependencies are checked explicitly. Missing requirements produce a deterministic failure instead of delegating parser or validator semantics to an LLM.
- REASON | **Behavior stability** - A fallback that changes execution from deterministic code to model judgment changes the validation contract and can silently produce different results.
- IMPACT | **Portable failure mode** - The asset behaves the same after being moved to another host: install the declared requirement or report the dependency failure.
