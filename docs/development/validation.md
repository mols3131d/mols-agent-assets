---
description: 문서 frontmatter·INDEX.tsv, Agent Asset routing, Rulesync 관리 자산의 repository validation 범위와 실행 경계를 확인할 때 사용하는 정책입니다.
---

# Validation

Validation은 이 repository가 유지하는 **네 가지 구조·파생 계약**을 확인합니다. 파일 표현은 [Formatting](formatting.md), repository-owned executable behavior는 [Testing](testing.md), model/runtime behavior evidence는 [Evaluation](evaluation.md)이 소유합니다. 어떤 validation이 merge를 차단하고 언제 실행되는지는 [Continuous Integration](ci.md)이 소유합니다.

## Targets

| Target | Check |
| --- | --- |
| Documentation frontmatter | 적용 대상 문서의 YAML frontmatter와 필수 metadata |
| Documentation `INDEX.tsv` | 작성 원본에서 계산한 index와 committed output의 drift |
| Agent Asset routing | source에서 생성한 route와 committed output의 drift |
| Rulesync-managed assets | Rulesync CLI를 통한 read-only structural validation |

각 검증은 계약을 소유하는 기존 도구와 source를 재사용합니다. Schema나 projection semantics를 별도 validator에서 다시 구현하지 않습니다.

문서 frontmatter의 적용 범위는 [Frontmatter](../documentation/frontmatter.md), index 정책은 [Document Indexing](../documentation/indexing.md), Rulesync contract는 [Rulesync](../references/tooling/rulesync.md)가 소유합니다.

## Projection Validation

Index와 route의 갱신은 canonical source와 공식 generator가 소유합니다. Local authoring에서는 필요하면 `mise run generated-sync`로 committed projection을 동기화합니다.

Validation은 projection을 새로운 source처럼 수정하지 않습니다. CI에서는 runner의 ephemeral working tree에서 공식 generator를 실행한 뒤 committed output과 비교할 수 있으며, 차이가 있으면 drift로 판정합니다. 이 generation은 검증 수단이며 repository write-back을 뜻하지 않습니다.

Generator 자체의 parsing, ordering, failure behavior 같은 executable semantics는 [Testing](testing.md)이 검증합니다.

## Rulesync

`npm run rulesync:validate`는 Rulesync-managed assets의 structural validation entrypoint입니다. 통과 결과를 semantic quality, routing quality나 runtime behavior까지 확대 해석하지 않습니다.

Validation target을 PR Gate, manual 또는 다른 execution surface에 배치하는 admission 결정은 [Continuous Integration](ci.md)을 따릅니다.
