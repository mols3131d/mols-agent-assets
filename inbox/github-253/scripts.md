# Scripts — Consistency Findings

## Inspected

[`scripts/agent_assets/routes_distribution_generate.py`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/scripts/agent_assets/routes_distribution_generate.py), [`scripts/generated_artifacts_sync.py`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/scripts/generated_artifacts_sync.py), [`scripts/docs_indexes_generate.py`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/scripts/docs_indexes_generate.py)의 선언·검색 결과를 [`docs/development/validation.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/validation.md), [`route/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/README.md), [`mise.toml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/mise.toml)과 비교했다.

## Result

**확인된 이슈 없음(정적 표본).** 문서에 적힌 route generator 경로가 존재하고 `mise run generated-sync`의 선언도 확인된다.

## Coverage Limits

실제 generator를 실행하지 않았고 index/route 출력 바이트를 재생성해 비교하지 않았다. 그 동작·실행 가능성은 이 문서에서 검증됐다고 주장하지 않는다.
