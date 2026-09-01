---
description: 문서 frontmatter·INDEX.tsv, Agent Asset routing, Rulesync 관리 자산의 repository validation 범위와 실행 경계를 확인할 때 사용하는 정책입니다.
---

# Validation

이 repository의 Validation은 **검증할 가치가 있는 네 가지 파생·구조 계약**만 다룹니다. 테스트, formatting, behavioral evaluation이나 일반적인 toolchain 상태까지 Validation의 범위로 확장하지 않습니다.

## Targets

| Target | Validation |
| --- | --- |
| Documentation frontmatter | 일반 문서가 repository frontmatter contract를 만족하는지 확인 |
| Documentation `INDEX.tsv` | 작성 원본에서 재생성한 index와 committed output의 drift 확인 |
| Agent Asset routing | distribution·repository route를 재생성하고 committed output과 비교 |
| Rulesync-managed assets | Rulesync CLI의 parser·processor·target adapter를 통한 read-only structural validation |

각 검증은 **계약을 소유하는 기존 도구를 재사용**합니다. 같은 schema나 projection semantics를 repository validator에서 다시 구현하지 않습니다.

## Documentation Frontmatter

일반 문서의 적용 범위와 metadata contract는 [Frontmatter](../documentation/frontmatter.md)가 소유합니다. Validation은 해당 범위의 Markdown이 YAML frontmatter로 parse되고 필요한 `description`을 가지는지 `mols-markdown-maintenance`의 `validate_frontmatter.py`로 확인합니다.

Agent Asset, systemic asset과 maintainer baseline처럼 일반 문서 frontmatter 규칙의 적용 대상이 아닌 파일에는 이 검증을 강제하지 않습니다.

## Documentation Index

`docs/**/INDEX.tsv`는 작성 원본에서 다시 만들 수 있는 projection입니다. `scripts/generate_docs_indexes.py --check`로 현재 source에서 계산한 결과와 committed index가 같은지 확인합니다.

Index의 생성 방식과 scope는 [Document Indexing](../documentation/indexing.md)이 소유합니다. Validation은 generated output을 직접 수정하지 않습니다.

## Agent Asset Routing

이 repository가 제공하는 자산의 `route/*.jsonl`과 이 repository가 사용하는 자산의 `.agents/route/*.jsonl`은 각 source에서 재생성한 뒤 committed output과 비교합니다.

Route의 source와 generation contract는 해당 generator가 소유합니다. Validation은 route 내용을 별도 schema로 재정의하지 않습니다.

## Rulesync-Managed Assets

Reusable Rulesync Agent Asset은 `npm run rulesync:validate`로 검증합니다. `scripts/agent-assets/validate_rulesync.py`는 Rulesync의 schema나 projection semantics를 재구현하지 않고 read-only pass를 orchestration합니다.

1. `doctor --strict` — configuration validation
2. `generate --dry-run` — configured projection validation
3. `generate --dry-run --targets "*"` — asset-declared target projection validation

Rulesync JSON output의 warning도 validation failure로 취급합니다. 이 검증은 semantic quality, routing quality 또는 runtime behavior까지 검증했다는 뜻이 아닙니다.

## Automation

네 검증은 필요할 때 `Optional Validation`에서 각각 선택해 실행합니다. 기본값은 모두 OFF입니다.

Write가 필요한 index·route 갱신은 local generation path가 소유합니다. Validation은 read-only 검사 또는 재생성 후 drift comparison만 수행합니다.

## Boundary

- deterministic test 설계와 PR Gate → [Testing](testing.md)
- model/runtime behavior evidence → [Evaluation](evaluation.md)
- documentation frontmatter contract → [Frontmatter](../documentation/frontmatter.md)
- index generation policy → [Document Indexing](../documentation/indexing.md)
- Rulesync source·projection contract → [Rulesync](../references/tooling/rulesync.md)
