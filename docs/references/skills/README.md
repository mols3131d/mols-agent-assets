# Skill References

이 directory는 Skill 관련 reference의 **navigation만** 소유한다. 규격이나 세부 constraint를 이 index에서 다시 정의하지 않는다.

## Start Here

1. [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)
   — Tier 1 `agentskills.io` format과 Tier 2 공식 target/harness link registry.
1. [Personal Skill Standard](agent-assets-skills-standard-personal.md)
   — 이 저장소에서 추가한 Skill-specific convention.
1. [Agent Skill Design Guide](agent-skills-guide.md)
   — Skill을 설계·작성·검증하는 통합 흐름.
1. [Skill Package and Target Boundaries](agent-assets-skills-target-profiles.md)
   — `.agentsmesh/skills/<name>/SKILL.md` package shape, single-file 관행, supporting resource와 target-specific boundary.

## Focused References

`agent-skills-io/`는 Tier 1 ecosystem의 특정 주제를 다룬다.

- [Skill Creation Best Practices](agent-skills-io/agent-skills-io-best-practices.md)
- [Optimizing Skill Descriptions](agent-skills-io/agent-skills-io-optimizing-descriptions.md)
- [Using Scripts in Skills](agent-skills-io/agent-skills-io-scripts.md)
- [Adding Skills Support to Clients](agent-skills-io/agent-skills-io-adding-support.md)

## Repository-Local Supporting References

- [Baseline Directive Template](agent-assets-skills-baseline-directive-template.md)
  — 특정 Skill에 durable intent와 decision을 별도로 보존할 가치가 있을 때 `docs/skills/<skill-name>/baseline/`에서 사용할 수 있는 **선택적** maintainer template.
- [Template-Driven Markdown](agent-assets-skills-template-driven-markdown.md)
  — repository template 기반 Markdown 생성에 관한 Skill reference. Agent Skills 표준의 일부가 아니다.

새 reference는 기존 owner로 연결할 수 없고 독립 responsibility가 있을 때만 추가한다.
