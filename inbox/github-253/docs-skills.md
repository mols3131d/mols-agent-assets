# Docs Skills — Consistency Findings

## Inspected

[`docs/skills/artifact-consistency-inspector/customization.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/artifact-consistency-inspector/customization.md)를 [`src/rulesync/.rulesync/skills/artifact-consistency-inspector/SKILL.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/src/rulesync/.rulesync/skills/artifact-consistency-inspector/SKILL.md)와 대조했다. [`docs/skills/mols-loops/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-loops/README.md) 및 [`evaluation.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-loops/evaluation.md)도 관련 Skill 및 `evals/` 실행 진입점과 대조했다.

## Result

**확인된 이슈 없음(표본 범위).** inspector maintainer 문서의 read-only·report invariant는 실제 Skill 본문에 명시돼 있다. mols-loops의 Trigger/Behavior/Smoke 구분 및 `mise` entrypoint는 확인한 [`mise.toml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/mise.toml)과 모순되지 않는다.

## Coverage Limits

그 밖의 `docs/skills/*`와 동일한 이름의 Skill package들을 전수 대조하지 않았다. Runtime/eval을 실행하지 않았다.
