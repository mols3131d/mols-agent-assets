# Src — Consistency Findings

## Inspected

[`src/rulesync/.rulesync/skills/artifact-consistency-inspector/SKILL.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/src/rulesync/.rulesync/skills/artifact-consistency-inspector/SKILL.md), [`mols-loops/SKILL.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/src/rulesync/.rulesync/skills/mols-loops/SKILL.md), [`github-context/SKILL.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/src/rulesync/.rulesync/skills/github-context/SKILL.md), [`mols-documentation/SKILL.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/src/rulesync/.rulesync/skills/mols-documentation/SKILL.md)의 일부 metadata/역할을 제공용 [`route/skills.jsonl`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/skills.jsonl) 및 maintainer 문서와 비교했다.

## Result

**이 표본에서 확인된 정합성 이슈 없음.** 특히 `artifact-consistency-inspector`의 read-only 실행 제한은 maintainer 문서에도 명시돼 있다. `route/`는 배포 discovery이며 source body를 소유하지 않는다는 관계도 일치한다.

## Coverage Limits

기타 Skill, Rule, Subagent의 전체 원문/metadata를 전수 비교하지 않았다. Rulesync-generated projection이나 실제 runtime capability/eval을 확인하지 않았다.
