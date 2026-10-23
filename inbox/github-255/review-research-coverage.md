# Research-to-Skill Coverage Review — missing decisions and optional references

- PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255)
- Reviewed revision: `fed5dd61bf50610dbda03bce9a02b2b43cdbe882`
- Scope: **review and planning only**. This report does not approve runtime performance, create deployable references, or modify the canonical Skill.
- Sources: [initial research](research.md), [agentic testing study](research-agentic-testing.md), [oracle/cost deep loop](research-oracle-validation.md), [research handoff](research-loop-review.md), [independent testability review](review-test-independence.md), [Skill source](../../src/rulesync/.rulesync/skills/mols-test-design/SKILL.md), [eval fixtures](../../evals/skills/mols-test-design/cases.json), [maintainer goal](../../docs/skills/mols-test-design/goal.md), [evaluation contract](../../docs/skills/mols-test-design/evaluation.md).

## Summary and review disposition

**Strong core; targeted additions warranted.** Current ~3.2k-char `SKILL.md` already covers protected contracts, independent oracle provenance, meaningful failure cases, minimal observation level, parallel change/test ownership, flakiness and evidence honesty. Portability is good: no prescribed framework, external Skill, testing pyramid, blanket TDD, full suite, or multi-agent choreography.

The missing part is primarily **how to adjudicate weak/invalid tests when the agent actually receives conflicting execution feedback**, not a missing taxonomy of test types. Do not split the current core simply because references are possible. Introduce new detail only if it is truly conditional and changes decisions that the core cannot already support.

## Findings (risk-first, no severity-by-count)

### F1 — High: oracle validity and discriminating power are not an explicit two-sided check

**Research:** [ReqTestAgent](research-oracle-validation.md) distinguished tests that pass an accepted reference from tests that detect faulty variants; [SWE-Mutation and benchmark audit](research-agentic-testing.md) identified weak oracles, false rejection and false confidence.

**Source status:** `Ground the oracle` requires independent provenance, `Discriminate failures` asks which faulty implementation fails; strong foundation. However, it does not explicitly direct the tester to keep **valid/contract-compliant behavior passing** while checking at least one *relevant defect/counterexample* fails, nor handle conflicts between reference and requirements.

**Failure case:** a generated test kills many mutants but also rejects the known accepted customer-visible behavior. Conversely, all tests pass a current implementation that omits a requested deliverable.

**Recommendation:** add a very small core criterion (accepted/valid examples remain valid; relevant incorrect variant is rejected; if no trusted reference exists, declare the oracle uncertainty). Keep detailed techniques conditional.

### F2 — High: after failed execution, determine whether the defect is in product code, test/oracle, or runner/fixture

**Research:** feedback-driven repair and independent oracle validity are separate in [research-agentic-testing.md](research-agentic-testing.md) and [research-oracle-validation.md](research-oracle-validation.md). A successful test run is evidence only for its specific claim.

**Source status:** the regression paragraph covers fail-before/pass-after and `Evidence and Handoff` correctly handles not-run. But **unexpected test failure triage and test correction** are not described as a design decision. An agent could alter product code to satisfy a faulty assertion or repeatedly regenerate tests without establishing fault meaning.

**Recommendation:** core-level conditional principle: when a test fails or contradicts the contract, first classify product defect vs invalid expectation/test vs unstable environment before changing code or claiming success. Deeper examples belong in oracle validation reference.

### F3 — Medium–High: mixed-intent coding requests can underactivate the Skill

**Research & purpose:** The Skill is for test-design judgment useful to a coding agent, but not for every implementation or runner failure. Most current positive routing fixtures explicitly say 'decide tests', 'review oracles', or 'design a test strategy'.

**Source status:** description excludes ordinary code implementation; this is reasonable, but can be misread as **never selecting the Skill during feature implementation** even when the same request materially asks for test strategy, regression oracles or acceptance design.

**Recommendation:** clarify intent, not keywords: *use for a material test-design subtask within implementation; do not trigger merely because code will later be tested*. Add paired positive and negative near-miss fixtures for mixed implementation/test requests; do not take over implementation ownership.

### F4 — Medium: observability/controllability can be blockers to a meaningful test

**Research:** the independent-testability loop covers avoiding private implementation coupling and isolating shared state; the agentic harness material emphasizes inspectable execution feedback. Both presume the protected behavior can actually be observed and the failure condition can be reproduced.

**Source status:** `Choose the observation boundary` and `Check reliability and cost` choose test level and isolate fixtures, but do not explicitly surface missing observation seams, injectible time, a reproducible state, or control of external interactions. Without these, proposing more tests may be ceremonial.

**Recommendation:** when a claim cannot be meaningfully observed or a failure cannot be controlled/reproduced, flag a bounded testability change or missing contract/owner decision. This Skill may **recommend** a seam, stable test interface or controlled fixture; it does not own architectural redesign. No universal mandate for dependency injection or mock-first design.

### F5 — Medium: acceptance completeness and risk-based stopping need clearer treatment

**Research:** [Microsoft's Building-to-the-Test](research-agentic-testing.md) shows passing available tests need not deliver the requested library; research also supports no-new-test and cost-proportional verification.

**Source status:** Skill warns against calling the entire deliverable complete solely because tests pass, but does not explicitly check requested artifacts/public integration surfaces against protected claims. `Protect the contract` mentions failure cost but lacks a clear criterion for deciding whether existing evidence is sufficient to stop.

**Recommendation:** lightly connect requested deliverable/consumer-facing paths to acceptance criteria and remaining gaps. Select higher-risk missing behavior first; stop adding tests when they no longer contribute material defect discrimination or acceptance confidence. Do not invent coverage percentages or force universal checklists.

### F6 — Evaluation blocker: 34 fixtures describe intended behavior but do not demonstrate model improvement

**Evidence:** `evals/skills/mols-test-design/cases.json` has 8 positive activations, 8 negative activations and 18 behavioral fixtures; many prompts already describe their intended defect, and behavior assertions are prose. `docs/skills/mols-test-design/evaluation.md` rightly requires actual A/B results.

**Implication:** structural JSON/route and GitHub PR Gate PASS are not proof that model selection, behavior, cost or reference loading will improve. Simply adding fixtures will not resolve the evidence gap.

**Recommendation:** create harder/less leading held-out cases for (a) a false oracle that passes a faulty implementation, (b) a test that rejects accepted behavior, (c) product-vs-test-vs-runner failure triage, (d) cannot-observe/cannot-reproduce design, (e) mixed implementation + material test design, (f) true no-test change. Compare `mols-coding-context` baseline and new Skill with matching runtime/model/tool/context budgets; grade distinct outcomes and costs. **No performance claim until executed.**

## Reference decision

### Candidate A — recommended first, conditional: `references/oracle-validation.md`

**Load only when:** generated/existing tests have questionable expected values, pass despite suspected defects, disagree with the spec/reference, an unexpected test failure requires triage, or high-risk property/differential/mutation strengthening is considered.

**Distinct useful decisions to own:**

- Provenance of the expected behavior: spec/consumer contract/trusted example/reference vs present implementation; what to do without a known-good reference.
- **Two-sided validity/discrimination:** accept justified normal behavior, reject important known bad behavior; distinguish false rejection from missed defects.
- Failing-test triage: product regression vs invalid oracle/assertion vs runner/fixture/environment; when to revise expectations versus implementation.
- Conditional escalation to property/metamorphic, differential, targeted mutation/fault injection; scrutinize equivalent mutants and execution cost.
- Evidence interpretation, including a missing requested deliverable and unknown oracle.

**Do not include:** a new test runner, framework cookbook, benchmark score table, generic TDD workflow, or replicated research literature.

**SKILL.md route:** near `Ground the oracle` or `Stronger Evidence When It Pays`, e.g. *'If the oracle is disputed, a generated test is suspect, or stronger counterexamples are needed, read `references/oracle-validation.md`.'* The 2-sided invariant remains in SKILL.md because it matters to ordinary tests too.

### Candidate B — conditional, defer until demonstrated: `references/boundaries-and-isolation.md`

**Load only when:** multiple owners/components, consumer/provider compatibility, mutable shared test environments, flaky parallel fixtures, contracts mixed with mocks, or stateful transactional flows materially complicate test design.

**Potential distinct decisions:**

- Test ownership vs observed external behavior; internal refactors that should *not* break neighboring tests.
- Independently runnable local tests paired with real consumer-provider contract evidence and narrowly scoped integration.
- Interaction-order/protocol requirements versus incidental call sequence.
- Shared immutable reference fixtures versus mutable shared state; test data, clock/time, concurrency and cleanup.
- A missing ownership/contract decision that test design should surface but not silently invent.

**Why defer:** Most of this boundary judgment is already in the 3.2k-char core, 8 added behavior cases and [independence review](review-test-independence.md). Transferring a paraphrase into another file would create an extra read without new value. Create B only if a real evaluation, a substantial case with genuinely distinct decisions, or a documented context-loading benefit warrants it.

### Not recommended

- `testing-pyramid.md`, `test-levels.md` as mandatory generic taxonomies: framework-neutral model knowledge is sufficient; no independent runtime decision demonstrated.
- Separate `tdd.md`, `mutation.md`, `property-based-testing.md` merely because papers mention them: overfits to method names, adds unnecessary routing and lookup burden.
- Project-specific fixtures, CLI recipes, Promptfoo adapters, Github Actions snippets inside deployable Skill: violates portability and asset owner boundaries.
- Copying `inbox/github-255/research-*.md` into `references/`: research history and citations are maintainer evidence, not runtime instructions.

## Proposed implementation order for a follow-up

1. Minimal core edits for **F1 (two-sided oracle validity), F2 (failure meaning), F3 (mixed intent)**; F4/F5 only when the same lines can be strengthened without sprawling procedures.
2. Add **one** conditional `references/oracle-validation.md` with behavior-changing examples and explicit trigger in core. Test portability when the whole Skill directory is copied elsewhere.
3. Add a small number of **paired hard/near-miss evals**. Test both the default no-reference path and conditional reference path; do not require reference loading for trivial tasks.
4. Compare behavior against baseline under equivalent model/runtime. If details duplicate the core or are almost always loaded, **merge back into SKILL.md and remove the reference**.
5. Only then decide whether Candidate B has distinct operational value.

## Acceptance for adding a reference

- The Skill remains correct and useful **without loading** the reference for ordinary test design.
- The reference supplies a decision, examples or a non-trivial failure mechanism not already in core; it is not a long-form rephrasing.
- A discoverable **conditional trigger** in core routes to it without forcing unrelated readers to load it.
- The reference is in the portable package; it does not rely on project-local `docs/`, `inbox/`, another Skill or a vendor tool.
- Behavior cases demonstrate at least one meaningful positive difference, and near-miss cases do not activate extra loading.
- Measured context/latency/complexity does not outweigh the benefit.

**Final review disposition:** **Targeted improvement warranted; one optional oracle reference is the first good candidate. Do not bulk-expand the Skill or automatically create both references.** This is a static research-to-source comparison, not a runtime behavior evaluation.
