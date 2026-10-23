# Docs References — Consistency Findings

## Inspected

[`docs/references/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/README.md), [`tooling/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/README.md), [`tooling/rulesync.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/rulesync.md), [`tooling/skills-cli.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/skills-cli.md), [`tooling/promptfoo.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/tooling/promptfoo.md)와 실행 경로 [`package.json`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/package.json), [`mise.toml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/mise.toml)의 관련 명령을 비교했다.

## Result

**기존 표본에서 이슈가 없었으나, 확장된 제목 검토에서 다음 두 건을 추가 확인하고 수정했다.** 예를 들어 문서의 `npm run rulesync:validate`와 `mise run skills-sync` 진입점은 확인한 package/mise 선언과 대응한다.

## Findings DOC-005–006 · Resolved · Low

- **DOC-005:** [Agent Asset design principles](../../docs/references/agent-assets/common/design-principles.md)의 `## 판단 순서`가 영어 H2 정책과 불일치했다. `## Decision Order`로 변경했다.
- **DOC-006:** [GitHub sensitive data removal runbook](../../docs/references/tooling/github-sensitive-data-removal-runbook.md)의 한국어 H1–H3 제목 44개가 같은 정책과 불일치했다. 해당 제목만 영어로 바꾸고 명령·본문·코드 블록은 유지했다. 기존 로컬 heading fragment 링크는 발견되지 않았으나 외부 deep link 영향은 확인하지 못했다.

## Coverage Limits

외부 Rulesync, skills CLI 및 Promptfoo 최신 버전의 upstream 사실관계는 검증하지 않았다. 해당 링크가 지금도 유효한지 판단하지 않았다.
