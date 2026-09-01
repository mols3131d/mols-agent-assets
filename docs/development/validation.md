---
description: 문서 frontmatter·INDEX.tsv, Agent Asset routing, Rulesync 관리 자산의 repository validation 범위와 실행 경계를 확인할 때 사용하는 정책입니다.
---

# Validation

Validation은 이 repository가 유지하는 **네 가지 구조·파생 계약**을 확인합니다. 파일 표현은 [Formatting](formatting.md), repository-owned executable behavior는 [Testing](testing.md), model/runtime behavior evidence는 [Evaluation](evaluation.md)이 소유합니다.

## Targets

| Target | Check |
| --- | --- |
| Documentation frontmatter | 적용 대상 문서의 YAML frontmatter와 필수 metadata |
| Documentation `INDEX.tsv` | 작성 원본에서 계산한 index와 committed output의 drift |
| Agent Asset routing | source에서 생성한 route와 committed output의 drift |
| Rulesync-managed assets | Rulesync CLI를 통한 read-only structural validation |

각 검증은 계약을 소유하는 기존 도구와 source를 재사용합니다. Schema나 projection semantics를 별도 validator에서 다시 구현하지 않습니다.

문서 frontmatter의 적용 범위는 [Frontmatter](../documentation/frontmatter.md), index 정책은 [Document Indexing](../documentation/indexing.md), Rulesync contract는 [Rulesync](../references/tooling/rulesync.md)가 소유합니다.

## Automation

`Optional Validation`에서 `docs_frontmatter`, `docs_indexes`, `asset_routes`, `rulesync_assets`를 필요할 때 각각 선택해 실행합니다. 기본값은 모두 OFF입니다.

Index와 route의 갱신은 local generation path가 소유합니다. Validation은 현재 상태를 read-only로 확인하거나 재생성한 결과와 committed output을 비교합니다.

`npm run rulesync:validate`는 Rulesync-managed assets의 structural validation entrypoint입니다. 통과 결과를 semantic quality, routing quality나 runtime behavior까지 확대 해석하지 않습니다.
