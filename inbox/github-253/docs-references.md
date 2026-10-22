# Docs References — Consistency Findings

## Inspected

[`docs/references/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/README.md), [`tooling/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/README.md), [`tooling/rulesync.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/rulesync.md), [`tooling/skills-cli.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/skills-cli.md), [`tooling/promptfoo.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/promptfoo.md)와 실행 경로 [`package.json`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/package.json), [`mise.toml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/mise.toml)의 관련 명령을 비교했다.

## Result

**확인된 이슈 없음(표본 범위).** 예를 들어 문서의 `npm run rulesync:validate`와 `mise run skills-sync` 진입점은 확인한 package/mise 선언과 대응한다.

## Coverage Limits

외부 Rulesync, skills CLI 및 Promptfoo 최신 버전의 upstream 사실관계는 검증하지 않았다. 해당 링크가 지금도 유효한지 판단하지 않았다.
