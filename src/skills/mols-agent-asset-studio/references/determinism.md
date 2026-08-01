# Reasoning and Determinism

Use language instructions for judgment and scripts for stable mechanics.

## Scriptification Decision

| Signal | Script suitability |
| --- | ---: |
| Stable input and output schema | High |
| Repeated frequently | High |
| Objective pass or fail | High |
| Failure is costly or sequence is fragile | High |
| Project configuration changes parameters but not logic | Medium |
| Meaning, intent, or trade-off interpretation is central | Low |
| Exceptions vary on every run | Low |
| Maintenance cost exceeds saved execution cost | Low |

Before adding a script, answer:

1. Does the step require semantic reasoning? Keep that part in the agent workflow.
1. Is the mechanical remainder repeated, fragile, or objectively testable?
1. Can it accept parameters rather than encode project assumptions?
1. Is it covered by execution tests and discoverable from `operations.md`?
1. Does it reduce token cost or uncertainty enough to justify maintenance?

Scripts must not hide policy decisions. They should return explicit results and
leave interpretation to the lifecycle owner.
