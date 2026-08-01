# Asset Naming

Use the first available authority:

1. explicit project naming policy
1. neighboring accepted asset convention
1. target runtime convention
1. Studio fallback below

## Studio Fallback

| Responsibility | Pattern | Example |
| --- | --- | --- |
| Single domain action | `<domain>-<verb>` | `github-review` |
| Complex multi-action workflow | `<domain>-<object>` | `asset-lifecycle` |
| Tool-specific operation | `<tool>-<action>` | `gh-address-comments` |
| Validator | `<asset>-validate` | `skill-validate` |
| Review workflow | `<domain>-review` | `security-review` |
| Router or hub | `<domain>-router` or a clear product noun | `docs-router` |

Rules:

- use lowercase letters, numbers, and single hyphens
- keep one or two distinguishing domain tokens near the front
- omit a repeated domain prefix inside an already scoped router
- prefer the shortest name that still distinguishes responsibility
- never rename an accepted asset without explicit authority and reference updates
- treat `studio`, `console`, `hub`, `portal`, and `workspace` as optional product
  nouns, not mandatory suffixes
