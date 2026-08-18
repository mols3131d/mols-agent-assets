# Decisions

## Accepted

### **[Scripts] Markdown generation script**

- DECISION | **Python generator** - Create script for automatic markdown generation.
- REASON | **Automation** - Automates document scaffolding and enforces consistency.
- IMPACT | **Less overhead** - Reduces model overhead by generating standardized structures automatically.

### **[Validation] Markdown frontmatter validation script**

- DECISION | **YAML validator** - Implement validator for frontmatter integrity.
- REASON | **Data integrity** - Prevents missing or malformed metadata fields.
- IMPACT | **Safe commits** - Pre-commit hooks block commits with invalid frontmatter.

### **[Validation] Markdown header validation script**

- DECISION | **Hierarchy validator** - Implement validator for header structure.
- REASON | **Structure standard** - Ensures heading structure matches the design template.
- IMPACT | **Early warning** - Automated checks flag header nesting and structure issues.

### **[Dependencies] Minimize dependencies**

- DECISION | **Strict limitation** - Allow adding external libraries but minimize their use.
- REASON | **Maintainability** - Keeps the workspace lightweight and reduces dependency conflicts.
- IMPACT | **Standard library first** - Favor Python standard libraries or existing dev-dependencies over new external packages.

### **[Dependencies] Optional dependency fallback**

- DECISION | **Fallback delegation** - Optional dependencies (like PyYAML) are not strictly enforced. Execute fallback: Option 1 (ask commander to delegate parsing to LLM) or Option 2 (auto-delegate to LLM).
- REASON | **Robustness** - Ensures script continues execution even if optional libraries are missing.
- IMPACT | **Context-based fallback** - Default is Option 1. Switch to Option 2 automatically if the commander token budget is high or agent runs in autopilot mode.
