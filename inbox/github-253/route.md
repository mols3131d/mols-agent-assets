# Route — Consistency Findings

## Inspected

[`route/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/README.md), [`route/ROUTE.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/ROUTE.md), [`routes.jsonl`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/routes.jsonl), [`skills.jsonl`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/skills.jsonl), [`subagents.jsonl`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/subagents.jsonl), [`scripts/agent_assets/routes_distribution_generate.py`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/scripts/agent_assets/routes_distribution_generate.py)를 비교했다.

## Result

**표본에서 확인된 이슈 없음.** `ROUTE.md`는 route index를 로드하도록 연결하며 generator는 해당 metadata를 canonical `src/` 자산에서 생성하는 구조다. `route/`와 `.agents/route/`의 목적을 구분하는 [root README](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/README.md)도 확인했다.

## Coverage Limits

모든 JSONL 레코드의 이름·설명과 canonical frontmatter 전수 일치, generator 재생성 결과의 bit-for-bit 일치는 미검증이다.
