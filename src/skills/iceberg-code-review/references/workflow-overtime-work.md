---
name: iceberg-code-review-overtime-work
description: Create a review handoff and marked summary when a review pass is paused for explicit continuation.
---

# Overtime Work

## Procedure

1. Create or replace `<review_dir>/__overtime__.md` with:
   - review target and selected engines;
   - links or filenames for completed details;
   - coverage still unreviewed, organized by engine or review area;
   - a short reason each area remains, if known; and
   - the exact next coverage to start with.
2. Create and validate `__summary__.md` using the normal summary workflow. Immediately after its frontmatter, add this callout before every other report content:

   ```md
   > [!IMPORTANT]
   > Review paused. See [remaining review coverage](__overtime__.md) before continuing.
   ```

3. End the response by offering continuation only on the commander's explicit request.

## Explicit Continuation

When the commander explicitly asks to continue, read `__overtime__.md` first. Resume from its next coverage without duplicating completed details. Replace `__overtime__.md` and update and validate `__summary__.md` if the review pauses again. When the requested review coverage is complete, remove the overtime callout, update the summary, and validate it.

---
