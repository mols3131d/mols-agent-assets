---
description: review-changes Skill의 설치·사용 진입점과 유지보수 명세를 찾을 때 사용합니다.
---

# Review Changes

Standalone coding-agent Skill for an evidence-backed review of a specific Git change set.

## Install

Copy [the Skill package](../../../src/rulesync/.rulesync/skills/review-changes/) to the Skill directory expected by your target runtime. The package consists of `SKILL.md` and `templates/review.md`; no other Skill or package is required.

## Invoke

```text
/review-changes Review staged and unstaged changes for behavioral regressions. Save a Markdown report.
```

For an explicit comparison:

```text
/review-changes Review changes from <base-commit> to <head-commit>. Prioritize real bugs and precise source evidence.
```

Reports are Markdown with optional script-free HTML `<details>` and default to `docs/reviews/<topic>.md` when file output is requested. Running tests, altering Git state and applying fixes are not automatic.

Maintenance contract: [spec.md](spec.md).
