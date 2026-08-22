# Docs Frontmatter Audit

Current `main` 기준으로 repository documentation의 frontmatter 상태를 전수조사하고, 서로 충돌 없이 병렬 처리할 수 있는 작업 단위로 분리한다.

- Baseline: `e3c85134f435d10284d88eba513c0ffba2fdb021`
- Field contract: root `frontmatter.json`
- Documentation scope: `docs/**/*.md`
- Config exclusion: `docs/**/baseline/**`
- Required document field: `description`
- Optional document field: `title`

## Scope Contract

Frontmatter 캠페인은 **문서 역할**을 먼저 판정한 뒤 field contract를 적용한다.

1. 일반 repository documentation은 이번 캠페인 대상이다.
1. `AGENTS.md`, `SKILL.md`, subagent, agent file 등 **Agent Asset 자체는 문서 frontmatter를 일괄 강제하지 않는다.** Frontmatter가 없어야 한다는 뜻이 아니며, 해당 자산의 표준·framework·vendor·repository 관행이 metadata contract를 소유한다.
1. `__*__` 같은 **systemic asset**도 일반 문서 frontmatter 강제 대상에서 제외하고 해당 systemic contract를 따른다.
1. `README.md`처럼 directory의 entrypoint 역할을 하는 문서는 frontmatter가 **README 파일 자체가 아니라 그 directory의 metadata**를 설명해야 한다. 최소한 directory의 책임, 범위 또는 언제 이 entrypoint를 사용하는지가 드러나야 한다.
1. `docs/references/agent-assets/**`와 `docs/skills/**`의 maintainer docs는 Agent Asset을 설명하는 **documentation**이지 Agent Asset 자체가 아니므로 이번 문서 캠페인 대상이다.
1. `frontmatter.json`의 path inclusion만으로 문서 역할을 판정하지 않는다. Role-based exception과 entrypoint semantics는 별도 policy/validation concern으로 유지한다.

## Result

PR #120의 pattern domain restructuring을 반영한 최신 inventory다.

| Sector | Scope | Files | `description` OK | Missing required `description` |
| --- | --- | ---: | ---: | ---: |
| A | Core / project docs | 12 | 5 | 7 |
| B | Reusable knowledge root + Agent Asset references | 10 | 9 | 1 |
| C | Reusable patterns | 19 | 6 | 13 |
| D | Tooling references | 4 | 4 | 0 |
| E | Skill maintainer docs | 7 | 2 | 5 |
| **Total** | | **52** | **26** | **26** |

현재 in-scope documentation 52개 중 26개가 required `description`을 가지고 있고 26개가 보완 대상이다.

`title`은 현재 contract상 optional이다. 기존 값은 보존하되 없는 title을 이번 required remediation에서 일괄 추가하지 않는다. `title`을 모든 일반 문서에 강제하려면 별도 정책 결정과 field contract 변경이 선행되어야 한다.

## Entrypoint README Audit

현재 in-scope `README.md` entrypoint는 14개다.

| README | Required `description` | Directory metadata semantics |
| --- | --- | --- |
| `docs/README.md` | ✅ | ✅ |
| `docs/development/README.md` | ✅ | ✅ |
| `docs/document/README.md` | ✅ | ✅ |
| `docs/references/README.md` | ✅ | ✅ |
| `docs/references/agent-assets/README.md` | ✅ | ✅ |
| `docs/references/patterns/README.md` | ✅ | ✅ |
| `docs/references/patterns/context-engineering/README.md` | ✅ | ✅ |
| `docs/references/patterns/documentation/README.md` | ✅ | ✅ |
| `docs/references/patterns/workflow/README.md` | ✅ | ✅ |
| `docs/references/patterns/software-engineering/README.md` | ✅ | ✅ |
| `docs/skills/mols-markdown-dashboard/README.md` | 🔴 | TODO |
| `docs/skills/mols-markdown-maintenance/README.md` | 🔴 | TODO |
| `docs/skills/mols-markdown/README.md` | ✅ | ✅ |
| `docs/skills/mols-mermaid/README.md` | ✅ | ✅ |

12개 README는 field 존재와 directory metadata semantics를 모두 충족한다. 누락 2개는 단순 파일 설명이 아니라 해당 maintainer directory의 책임·범위·selection context를 설명하도록 작성한다.

## Status Legend

- ✅ required `description` 충족
- 🔴 required `description` 누락 — MUST fix
- README의 ✅는 field 존재뿐 아니라 directory metadata semantics까지 확인한 경우에만 사용한다.

## Sector A — Core / Project Docs

독립 작업 범위: `docs/README.md`, `docs/consumption.md`, `docs/development/**`, `docs/document/**`

- ✅ `docs/README.md`
- ✅ `docs/consumption.md`
- ✅ `docs/development/README.md`
- 🔴 `docs/development/authority-routing.md`
- 🔴 `docs/development/change-workflow.md`
- 🔴 `docs/development/testing.md`
- ✅ `docs/document/README.md`
- 🔴 `docs/document/asset-capsules.md`
- 🔴 `docs/document/dry.md`
- ✅ `docs/document/frontmatter.md`
- 🔴 `docs/document/knowledge-lifecycle.md`
- 🔴 `docs/document/ownership.md`

### TODO A

- [ ] 7개 🔴 문서에 실제 책임을 설명하는 `description`을 작성한다.
- [ ] 기존 frontmatter가 있는 문서는 field와 body 의미가 일치하는지 검토한다.
- [ ] README는 directory metadata semantics를 보존한다.
- [ ] optional `title` normalization은 required remediation과 분리한다.

## Sector B — Reusable Knowledge / Agent Asset References

독립 작업 범위: `docs/references/README.md`, `docs/references/agent-assets/**`

- ✅ `docs/references/README.md`
- ✅ `docs/references/agent-assets/README.md`
- ✅ `docs/references/agent-assets/common/chatbot-compatibility.md`
- ✅ `docs/references/agent-assets/common/design-principles.md`
- ✅ `docs/references/agent-assets/common/instruction-authoring.md`
- ✅ `docs/references/agent-assets/common/naming.md`
- ✅ `docs/references/agent-assets/skills/agent-assets-skills-baseline-directive-template.md`
- ✅ `docs/references/agent-assets/skills/agent-assets-skills-template-driven-markdown.md`
- ✅ `docs/references/agent-assets/skills/skill-authoring-conventions.md`
- 🔴 `docs/references/agent-assets/skills/specification.md`

### TODO B

- [ ] `specification.md`에 required `description`을 작성한다.
- [ ] 기존 description이 reusable knowledge의 실제 책임과 일치하는지 검토한다.
- [ ] 두 README의 directory metadata semantics를 보존한다.
- [ ] optional `title` normalization은 required remediation과 분리한다.

## Sector C — Reusable Patterns

독립 작업 범위: `docs/references/patterns/**`

### Entrypoints / already compliant

- ✅ `docs/references/patterns/README.md`
- ✅ `docs/references/patterns/context-engineering/README.md`
- ✅ `docs/references/patterns/documentation/README.md`
- ✅ `docs/references/patterns/workflow/README.md`
- ✅ `docs/references/patterns/software-engineering/README.md`
- ✅ `docs/references/patterns/software-engineering/filesystem-legible-structure.md`

### Missing required `description`

- 🔴 `docs/references/patterns/context-engineering/argument-driven-assets.md`
- 🔴 `docs/references/patterns/context-engineering/asset-configuration-surface.md`
- 🔴 `docs/references/patterns/context-engineering/chatbot-asset-directory.md`
- 🔴 `docs/references/patterns/context-engineering/chatbot-repository-entrypoint.md`
- 🔴 `docs/references/patterns/context-engineering/directory-context-capsule.md`
- 🔴 `docs/references/patterns/context-engineering/layered-context-instructions.md`
- 🔴 `docs/references/patterns/context-engineering/progressive-context-routing.md`
- 🔴 `docs/references/patterns/context-engineering/routing-index-assets.md`
- 🔴 `docs/references/patterns/context-engineering/skill-source-workspace.md`
- 🔴 `docs/references/patterns/context-engineering/template-schema-driven-assets.md`
- 🔴 `docs/references/patterns/documentation/baseline-document.md`
- 🔴 `docs/references/patterns/documentation/nonstandard-directory-guide.md`
- 🔴 `docs/references/patterns/workflow/artifact-inbox.md`

### TODO C

- [ ] 13개 🔴 pattern 문서에 required `description`을 작성한다.
- [ ] Root/category README의 directory metadata semantics를 보존한다.
- [ ] 개별 Pattern description은 구현 세부보다 **무엇을 해결하는 pattern인지 / 언제 참고하는지**를 중심으로 작성한다.
- [ ] Pattern body의 범위보다 description을 넓히지 않는다.
- [ ] 4개 domain은 서로 exclusive write scope로 취급해 필요하면 병렬 sub-lane으로 더 나눌 수 있다.
- [ ] optional `title` normalization은 required remediation과 분리한다.

## Sector D — Tooling References

독립 작업 범위: `docs/references/tooling/**`

- ✅ `docs/references/tooling/front-matter-cms.md`
- ✅ `docs/references/tooling/mise.md`
- ✅ `docs/references/tooling/promptfoo.md`
- ✅ `docs/references/tooling/rulesync.md`

### TODO D

- [ ] Required field 관점에서는 변경하지 않는다.
- [ ] 기존 `title`과 `description`이 현재 문서 책임과 일치하는지만 검토한다.
- [ ] 의미 수정이 필요하지 않으면 no-op으로 종료한다.

## Sector E — Skill Maintainer Docs

독립 작업 범위: `docs/skills/**`, 단 `**/baseline/**` 제외

- 🔴 `docs/skills/artifact-consistency-inspector/customization.md`
- 🔴 `docs/skills/mols-markdown-dashboard/ARCHITECTURE.md`
- 🔴 `docs/skills/mols-markdown-dashboard/MAINTENANCE.md`
- 🔴 `docs/skills/mols-markdown-dashboard/README.md`
- 🔴 `docs/skills/mols-markdown-maintenance/README.md`
- ✅ `docs/skills/mols-markdown/README.md`
- ✅ `docs/skills/mols-mermaid/README.md`

### TODO E

- [ ] 5개 🔴 문서에 required `description`을 작성한다.
- [ ] 두 missing README description은 해당 maintainer directory의 metadata를 담는다.
- [ ] 비-README description은 해당 maintainer document의 실제 책임을 정확히 나타낸다.
- [ ] 기존 두 README의 directory metadata semantics를 보존한다.
- [ ] optional `title` normalization은 required remediation과 분리한다.

## Explicit Exclusions

### Configuration exclusion

`frontmatter.json`이 `**/baseline/**`을 명시적으로 제외하므로 다음 파일은 이번 completion 대상이 아니다.

- `docs/skills/clarify-code/baseline/decisions.md`
- `docs/skills/mols-agent-asset-validator/baseline/DIRECTIVE.md`
- `docs/skills/mols-markdown-dashboard/baseline/DIRECTIVE.md`

### Role-based exclusion

다음 종류는 일반 documentation frontmatter를 일괄 강제하지 않는다.

- `AGENTS.md` 같은 agent guidance asset
- `SKILL.md`
- Rulesync/vendor subagent 및 agent asset
- 해당 자산 표준이 metadata를 소유하는 기타 Agent Asset
- `__*__` 같은 systemic asset

이 exclusion은 **frontmatter 금지 규칙이 아니다.** 각 asset의 자체 표준·framework·vendor·repository 관행이 frontmatter 또는 metadata를 요구하면 그것을 따른다.

Root `README.md`, `inbox/**`, `route/**`, `src/**`, `tests/**` 등도 현재 documentation completion scope가 아니며, 특히 `src/**`의 Agent Asset을 docs schema로 검증하지 않는다.

## Parallel Work Contract

각 sector는 path ownership이 겹치지 않으므로 독립 branch/PR에서 병렬 처리할 수 있다.

| Lane | Exclusive write scope | Required fixes | Dependency |
| --- | --- | ---: | --- |
| A | core + `docs/development/**` + `docs/document/**` | 7 | none |
| B | `docs/references/README.md` + `docs/references/agent-assets/**` | 1 | none |
| C | `docs/references/patterns/**` | 13 | none |
| D | `docs/references/tooling/**` | 0 | verification only |
| E | `docs/skills/**` excluding baseline | 5 | none |

Sector C는 필요하면 `context-engineering`(10), `documentation`(2), `workflow`(1), `software-engineering`(0)로 다시 분리할 수 있다. 이 sub-lane들은 서로 write scope가 겹치지 않는다.

Rules:

1. 각 lane은 작업 시작 시 최신 `main`을 다시 조회하고 자기 write scope만 수정한다.
1. 대상이 일반 documentation인지 Agent/systemic asset인지 역할을 먼저 판정한다.
1. Description은 filename만 보고 생성하지 않고 해당 문서 body와 local README가 정의하는 책임을 읽고 작성한다.
1. README description은 파일 설명이 아니라 directory metadata를 작성한다.
1. 기존 frontmatter field는 의미상 잘못되지 않은 한 보존한다.
1. Required remediation에서 body 의미를 바꾸지 않는다. Frontmatter가 body와 충돌하면 별도 finding으로 보고한다.
1. `title`은 optional이다. 기존 값은 보존하되 없는 title을 일괄 추가하지 않는다.
1. `**/baseline/**`, Agent Asset, systemic asset은 일반 docs remediation으로 끌어들이지 않는다.
1. 각 lane은 변경 파일에 대해 frontmatter 파싱과 required `description` 존재를 검증하고 Markdown 검사를 수행한다.
1. Lane 간 shared file을 만들지 않는다. 공통 정책·validator 변경이 필요하면 integration review로 넘긴다.

## Validation

Repository의 `mols-markdown-maintenance` frontmatter validator를 사용할 수 있다. 일반 documentation의 최소 deterministic acceptance는 각 in-scope 파일이 YAML frontmatter로 parse되고 `description` key를 가지는 것이다.

```bash
uv run src/rulesync/.rulesync/skills/mols-markdown-maintenance/scripts/validate_frontmatter.py <sector-files...> --required description
```

단, validator에 모든 Markdown을 무차별 전달하지 않는다. 먼저 role-based scope를 적용한다.

Deterministic key presence만으로 metadata 품질이 증명되지는 않는다. 각 sector review에서 다음 semantic acceptance를 함께 확인한다.

- 일반 문서: description이 실제 문서 책임·사용 시점·boundary와 일치한다.
- README entrypoint: description이 directory의 책임·범위·selection context를 나타낸다.
- Agent/systemic asset: 일반 docs contract가 아니라 해당 asset contract를 따른다.

## Integration TODO

- [ ] A, B, C, E required remediation을 병렬 완료한다.
- [ ] D를 verification-only로 확인한다.
- [ ] 모든 sector 결과를 통합한 최신 `main`에서 directory tree 기반 inventory를 다시 생성한다.
- [ ] role-based exclusion을 먼저 적용한 뒤 일반 documentation의 required `description`을 검증한다.
- [ ] README entrypoint metadata semantics를 별도로 검토한다.
- [ ] 현재 baseline 기준 목표 상태 `52/52 description compliant`를 확인한다. 작업 중 문서가 추가·삭제되면 고정 숫자보다 최신 inventory를 우선한다.
- [ ] Agent Asset과 systemic asset이 일반 docs validator에 잘못 포함되지 않는지 확인한다.
- [ ] role-based scope와 README semantics를 durable policy/validator에 어떻게 반영할지 integration 단계에서 결정한다.
- [ ] optional `title` normalization은 별도 정책으로 결정한다.
- [ ] final Markdown/frontmatter validation과 PR Gate를 통과시킨다.

## Done

이번 artifact는 **조사와 병렬 실행 계획**만 고정한다. 실제 frontmatter 수정은 sector별 후속 작업에서 수행한다.
