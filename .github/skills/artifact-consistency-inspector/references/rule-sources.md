# Rule Sources

`rule_sources`는 expected state를 결정할 때 사용할 source의 **순서형 목록**입니다. Repository마다 authority 구조가 다르므로 source type에 대한 universal precedence를 정의하지 않습니다.

## Accepted forms

```yaml
rule_sources: auto
```

```yaml
rule_sources:
  - "docs/engineering/api-policy.md"
  - "config/eslint.config.js"
  - auto
  - "baseline:release-2026.07"
```

목록 item은 다음 중 하나일 수 있습니다.

- repository-relative artifact locator
- repository file URL 또는 heading·symbol locator
- user-provided rule text
- named policy, specification, configuration, or revision
- bounded selector whose result can be reported as actual locators
- `auto`

## Ordered semantics

- 목록 앞 item이 뒤 item보다 우선합니다.
- 사용자가 지정한 순서는 source type에 대한 일반 규칙보다 우선합니다.
- 같은 item이 여러 source로 해석되면 가장 구체적인 locator로 정규화합니다.
- `auto`는 최대 한 번 사용하며 위치에서 확장됩니다.
- 중복 source는 첫 번째 위치를 유지하고 병합합니다.

## Auto expansion

`auto`는 target relation에 직접 적용될 가능성이 있는 실제 source를 탐색합니다. 특정 filename이나 directory를 전제하지 않습니다.

Candidate discovery signals:

- target artifact가 직접 참조하는 policy, specification, schema, or configuration
- repository entry point, contribution guide, ownership metadata, index, manifest, or build graph
- active ADR, RFC, design decision, or requirement linked to the target
- lint, formatter, compiler, schema, test, deployment, or workflow configuration wired to the target
- source code or validation artifact가 authority로 인용하는 document or contract
- stable repeated pattern relevant to the target, only as inferred convention

Candidate ordering is repository-specific. The model establishes order from evidence such as:

- explicit scope and applicability
- mandatory or normative statement
- active versus superseded status
- target specificity
- revision alignment
- enforcement or registration wiring
- repository cross-reference and ownership evidence

These are evaluation dimensions, not a fixed source-type hierarchy.

## Conflict handling

- If two sources have a user-defined order, follow that order and record the lower source as counterevidence when relevant.
- If auto-discovered sources conflict and authority is distinguishable, use the better-supported source and record the basis.
- If authority is not distinguishable, keep them at the same unresolved tier.
- If both are authoritative for the same scope and revision, the conflict itself may be a verified `contradiction`.
- Never choose by filename convention, directory depth, recency alone, or model preference.

## Convention handling

Repeated patterns may be included as a resolved source with authority `inferred-convention`, but:

- verify the pattern across a bounded representative set
- check documented exceptions and generators
- do not call deviation a verified violation without mandatory authority
- use `unresolved` when the pattern is strong but not established as a rule
- omit weak or incidental patterns

## Report representation

Coverage records the final expansion and authority basis:

```yaml
resolved_rule_sources:
  - order: 1
    source: "docs/engineering/api-policy.md#request-validation"
    authority: "explicit mandatory policy"
    basis: "applies to all public v2 endpoints and is referenced by the API governance index"
  - order: 2
    source: "api/openapi.yaml"
    authority: "active contract"
    basis: "registered as the generated client source"
  - order: 3
    source: "observed handler naming pattern"
    authority: "inferred convention"
    basis: "consistent in 18 directly related handlers; no mandatory policy found"
```

The report body uses a compact Markdown list instead of literal YAML. Record resolved ordering and authority conflicts in Coverage. Do not add a default `Rule source` metadata row to every finding; include the relevant locator naturally in References when it is material to the observed difference.
