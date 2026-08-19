# Skill 레퍼런스

이 디렉터리는 Skill 관련 레퍼런스의 **탐색 경로만** 소유한다. 규격이나 세부 제약을 이 인덱스에서 다시 정의하지 않는다.

## 먼저 볼 문서

1. [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)
   — Tier 1 `agentskills.io` 형식과 Tier 2 공식 target/harness 링크 모음.
1. [Personal Skill Standard](agent-assets-skills-standard-personal.md)
   — 이 저장소에서 추가한 Skill 전용 관행.
1. [Agent Skill Design Guide](agent-skills-guide.md)
   — Skill을 설계·작성·검증하는 통합 흐름.
1. [Skill Package and Target Boundaries](agent-assets-skills-target-profiles.md)
   — `src/rulesync/.rulesync/skills/<name>/SKILL.md` package shape, single-file 관행, supporting resource와 target-specific boundary.

## 주제별 레퍼런스

`agent-skills-io/`는 Tier 1 생태계의 특정 주제를 다룬다.

- [Skill Creation Best Practices](agent-skills-io/agent-skills-io-best-practices.md)
- [Optimizing Skill Descriptions](agent-skills-io/agent-skills-io-optimizing-descriptions.md)
- [Using Scripts in Skills](agent-skills-io/agent-skills-io-scripts.md)
- [Adding Skills Support to Clients](agent-skills-io/agent-skills-io-adding-support.md)

## 저장소 전용 보조 레퍼런스

- [Baseline Directive Template](agent-assets-skills-baseline-directive-template.md)
  — 특정 Skill에 durable intent와 decision을 별도로 보존할 가치가 있을 때 `docs/skills/<skill-name>/baseline/`에서 사용할 수 있는 **선택적** maintainer template.
- [Template-Driven Markdown](agent-assets-skills-template-driven-markdown.md)
  — 저장소 template 기반 Markdown 생성에 관한 Skill 레퍼런스. Agent Skills 표준의 일부가 아니다.

새 레퍼런스는 기존 소유자로 연결할 수 없고 독립 책임이 있을 때만 추가한다.
