---
name: mols-text-optimizer
description: >-
  Optimize provided or clearly identified text for lower wording or token cost while
  preserving material meaning, behavior, exact technical content, and the existing
  structure. Use only as a generic fallback when no more specific applicable Skill,
  instruction, document or domain guidance, framework contract, or procedure applies to
  the target or task. Trigger on requests to shorten, compress, or deduplicate wording
  without losing meaning. Do not use when a more specific owner applies, even if this Skill
  is named explicitly. Also do not use for generic response brevity, summarization,
  translation, style or humanization, Markdown or document restructuring, caveman-style
  speech, or latent prompt/context compression.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Text Optimizer

Reduce wording cost, not substance.

## Optimize

Apply the smallest safe local wording changes first:

1. remove non-semantic repetition or filler;
2. collapse local wording that states the same material meaning twice;
3. reduce unnecessary term variation without replacing canonical user or domain terms;
4. use shorter wording only when its meaning range and behavioral effect remain equivalent;
5. stop when no clearly safe reduction remains.

Do not force every step. If there is no safe reduction, return the original wording.
Semantic stability is a constraint on reduction, not a separate expansion objective.

## Preserve

Treat the following as compression-resistant:

- roles and effects: actor, action, target, input/output, side effect, and failure behavior;
- logic and control: condition, exception, fallback, order, dependency, scope, and
  causal/logical relation;
- strength and uncertainty: negation, prohibition, modality, permission, quantifier,
  uncertainty, and comparison;
- exact facts and tokens: numbers, thresholds, units, dates, names, identifiers, paths,
  commands, APIs, fields, code tokens, exact error strings, citations, and attribution;
- agent behavior: activation, permission, safety boundaries, required gates, and stop
  conditions.

For agent-facing text, repetition can be behavior-bearing. Do not remove a repeated guard
or instruction merely because it is lexically duplicate.

## Protect Structure

This Skill does not optimize document or output structure. Preserve existing:

- section and heading hierarchy;
- sentence and paragraph boundaries and order;
- list, table, callout, and numbering representation;
- code fences, delimiters, and indentation;
- JSON, YAML, XML, schema-like structure, and exact format contracts.

Even when the full artifact must be returned, do not broadly rephrase content outside the
actual optimization candidates.

## Check and Stop

After the edit, perform one bounded check over the changed spans and only the surrounding
context needed to judge them:

- Did any material information disappear?
- Did actor, action, target, condition, exception, scope, order, or relation change?
- Did negation, modality, permission, quantifier, or uncertainty change?
- Did any exact technical token, identifier, quantity, threshold, or unit change?
- Could agent-facing activation, permission, safety, or behavior change?
- Did the edit violate protected structure?

If any answer is uncertain, revert that change or keep the original text. Do not add another
optimization pass when the remaining changes are stylistic, ambiguous, or too small to
justify additional review cost.

## Boundary

This Skill owns generic wording-cost reduction only. It does not own target-specific
text-authoring rules, generic response brevity, information-reducing summarization,
translation, grammar-only correction, humanization, tone or persona, Markdown/document
restructuring, caveman-style speech, latent context compression, or tokenizer algorithms.
