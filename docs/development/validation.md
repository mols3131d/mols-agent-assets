---
description: 저장소의 자산·도구·생성물·문서 등 여러 도메인에서 무엇을 어떤 authority와 evidence로 검증할지 정할 때 사용하는 공통 Validation 정책입니다.
---

# Validation

Validation은 **대상이 만족해야 하는 계약을 적절한 authority와 evidence로 확인하는 일**입니다. 하나의 validator가 모든 correctness를 증명한다고 간주하지 않습니다.

검증은 대상과 계약에 맞는 가장 좁은 owner에게 맡깁니다. upstream tool이나 specification이 소유하는 semantics를 repository validator가 다시 구현하지 않습니다.

## Domains

| Domain | Primary validation |
| --- | --- |
| Agent Assets | 작성 framework·official specification·target contract와 필요한 semantic·routing review |
| Rulesync assets | Rulesync CLI가 소유하는 parser·processor·target adapter |
| Generated projections | 작성 원본에서 재생성한 결과와 committed output의 drift |
| Documentation | 적용되는 documentation policy, linter와 metadata·index contract |
| Repository tooling | toolchain, lock state와 configuration contract |
| Repository-owned behavior | deterministic test로 확인할 수 있는 executable behavior |
| External dependencies | upstream lock·source·installer가 소유하는 revision과 materialization contract |

도메인별 validator가 다르더라도 **계약을 소유하는 source를 우선하고 repository는 필요한 orchestration과 local acceptance만 추가합니다.**

## Evidence

검증 결과는 실제로 확인한 범위까지만 주장합니다.

- parser, compiler, validator, deterministic script나 command가 확인한 결과는 해당 계약에 대한 deterministic evidence입니다.
- target-specific compatibility는 해당 target의 contract나 runtime evidence 없이 확대 해석하지 않습니다.
- semantic quality, routing quality와 behavior는 structural validation 통과만으로 증명되지 않습니다.
- model/runtime evaluation은 deterministic validation을 대체하지 않습니다.

검증하지 않은 영역은 통과한 것으로 간주하지 않습니다.

## Automation

검증 automation은 가능한 한 read-only여야 합니다. 생성이나 materialization이 필요한 검증은 source를 보존하면서 결과만 비교할 수 있게 설계합니다.

- PR Gate는 [Testing](testing.md)이 소유하는 repository deterministic test만 실행합니다.
- 비용이 높거나 항상 필요하지 않은 검증은 `Optional Validation`에서 명시적으로 선택해 실행합니다.
- generated projection 갱신처럼 write가 필요한 작업은 local generation path가 소유하고 validation은 drift를 확인합니다.
- formatter, generator, validator와 evaluation을 하나의 거대한 CI gate로 합치지 않습니다.

## Agent Skills

Agent Skill도 하나의 검증으로 모든 계약을 확인하지 않습니다.

| Concern | Owner |
| --- | --- |
| 작성 원본의 syntax·projection | Rulesync 등 실제 source framework |
| 공통 Skill package contract | applicable Agent Skills specification과 official validator |
| target-specific compatibility | 실제 target의 official contract와 필요한 runtime evidence |
| repository-owned deterministic mechanics | [Testing](testing.md) |
| trigger·output·behavior quality | [Evaluation](evaluation.md) |
| semantic·routing·adversarial review | `mols-agent-asset-validator` |

Skill의 공식 source routing은 [Agent Skills Specification](../references/agent-assets/skills/specification.md), Rulesync의 구체적인 validation contract와 entrypoint는 [Rulesync](../references/tooling/rulesync.md)가 소유합니다.

## Boundary

- deterministic test 설계와 PR Gate → [Testing](testing.md)
- model/runtime behavior evidence → [Evaluation](evaluation.md)
- 작성 원본과 upstream/local authority → [작성 원본과 권한](source-authority.md)
