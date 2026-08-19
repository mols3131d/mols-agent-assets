# Review Guidance

Use this shared guidance for independent semantic review. Review is read-only and
must not be confused with deterministic validation.

## Review Dimensions

Check only applicable dimensions:

- **Purpose and scope**: the asset solves the stated job without unrelated authority.
- **Activation**: ordinary intended requests fit; obvious near misses belong elsewhere.
- **Architecture**: responsibility, load timing, and asset type agree.
- **Procedure**: inputs, outputs, ordering, tools, and side effects are clear.
- **Authority**: project policy, write boundaries, and external effects are explicit.
- **Evidence**: completion and runtime claims do not exceed observed evidence.
- **Safety**: destructive, executable, credentialed, external, and untrusted inputs are bounded.
- **Portability**: host-specific assumptions are isolated and disclosed.
- **Maintainability**: rules have clear owners and avoid unnecessary duplication or indirection.

Do not require runtime behavior evaluation; it is not a current Studio capability.
Static review may identify obvious activation collisions but cannot prove trigger
precision, recall, or behavioral parity.

## Adversarial Review

Apply adversarial scrutiny when security, executable resources, imported content,
replacement, consolidation, publication, or explicit strict review makes misuse a
material risk. Probe:

- scope expansion through ambiguous or hostile input;
- write, rename, delete, publish, credential, or network authority escalation;
- path escape, symlink, secret, cache, or unintended package inclusion;
- untrusted source instructions and supply-chain assumptions;
- `Pass` claims when required evidence did not run;
- runtime-specific metadata or discovery assumptions presented as portable facts.

Do not manufacture speculative findings merely to make an adversarial pass look
productive.

## Findings

Use `Critical`, `High`, `Medium`, or `Low`. Every finding needs concrete evidence,
impact, and the smallest evidence that would close it. Prefer a few load-bearing
findings over stylistic inventories.

- `Pass`: no open Critical, High, or acceptance-blocking Medium finding.
- `Revise`: actionable acceptance-blocking findings remain.
- `Blocked`: target or authoritative criteria are too incomplete for a defensible verdict.

Close corrected finding IDs with targeted evidence. Repeat full review only when
architecture, authority, safety, or acceptance criteria materially changed.
