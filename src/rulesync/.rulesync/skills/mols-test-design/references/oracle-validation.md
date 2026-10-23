# Oracle Validation

Use this reference **only** when a generated or existing test has a disputed expectation, an unexpected failure needs diagnosis, or a high-risk claim warrants a stronger counterexample. The ordinary test selection and evidence boundaries stay in `SKILL.md`.

## Establish the expected behavior

1. Identify the *claim* the test purports to check and the consumer-observable outcome. Compare with authoritative requirements, explicit acceptance examples, compatible public contracts or independently established properties.
2. Distinguish **known-good evidence** from the **system under test**. Passing the current code does not show that the expectation is correct; a trusted reference is not assumed to exist for new behavior.
3. If the source of truth is absent or conflicts with an existing assertion, describe competing interpretations and the decision owner. Do not silently canonize the current result, a model's guess or a test's snapshot.
4. Check **both sides**, when comparable evidence exists:
   - A contract-compliant example/reference must pass. A test that rejects it may have an overstrict or incorrect oracle.
   - A relevant faulty counterexample must fail *for the intended reason*. A test that passes it has insufficient discrimination.
   - Neither side alone proves the whole requested feature exists, is exported or is connected to consumers.

### Example: a wrong reference value

A product contract rounds only the **final** amount, but current code rounds each intermediate amount. A test copied from the implementation will pass an incorrect calculation. Derive expected values from the contract; choose an input where intermediate and final rounding differ. If an otherwise accepted example fails the proposed assertion, investigate the assertion before changing the product.

### Example: test pass while the deliverable is absent

UI rendering assertions may pass for a demo while the request required a usable library. Add or identify the missing consumer-facing package import/export or delivery check rather than treating the demo's test pass as complete acceptance.

## Diagnose unexpected failure before editing

| Observation | Investigate | Appropriate response |
| --- | --- | --- |
| Behavior contradicts a clear, independent contract in reproducible conditions | Product defect, regression or missing integration | Preserve a minimal reproducer; repair through the owning implementation workflow, then check the expected regression and relevant existing contracts |
| A known-valid behavior fails only an assertion or snapshot | Invalid/stale expectation, fixture, too-strict implementation detail | Correct the test against the authoritative contract; do not distort production behavior to match a bad oracle |
| Result depends on clock, test order, shared state, external service or setup | Fixture/runner/environment nondeterminism; possibly a real concurrency defect | Control time and state or isolate the execution; determine whether the unstable behavior is part of the product contract before assigning blame |
| Neither valid reference nor authoritative acceptance rule is available | Undecidable oracle | Record the competing claims and unresolved owner decision; do not label either code or test as correct |

Avoid automatically rewriting a failing test until it passes, silently increasing retries, or modifying product code to satisfy an unsupported assertion. When feasible, verify reproduction **before** repair and meaningful pass **after**, with unaffected contracts still valid. Do not infer execution results from reading code.

## Escalate evidence only for a concrete gap

- **Boundary/property/metamorphic:** A meaningful invariant or relation is independently justified and a few examples may miss violating inputs. Challenge the property with a valid case and an intentionally bad one before relying on generated inputs.
- **Differential/reference:** An accepted prior implementation, protocol specification or independently verified model exists. Examine intended version differences before treating every mismatch as a defect.
- **Targeted mutation/fault injection:** A material failure mode could survive current tests and the runner/environment can support a small focused experiment. Use realistic variants; avoid interpreting equivalent mutants or raw mutation score as proof of oracle correctness.
- **Contract/integration:** A local mock masks behavior observable only across a real API, database, message or permission boundary. Test the narrowest meaningful boundary; keep independently executable local tests where possible.

If the evidence gained does not change a consequential test/design decision, **stop escalating**. Report which good/bad cases were actually run, which were only designed, and any unresolved contract or environment limits. Never equate a thought experiment with a passing test.
