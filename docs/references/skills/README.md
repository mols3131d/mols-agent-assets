# Skill 레퍼런스

이 디렉터리는 Skill 관련 reference의 탐색 경로만 소유합니다. Rulesync canonical schema나 target mapping을 여기서 다시 정의하지 않습니다.

## 먼저 볼 문서

1. [Rulesync Repository Conventions](../common/standards/rulesync-repository-conventions.md)
   — 이 저장소에서 Rulesync canonical source와 derived target surface를 구분하는 기준.
1. [Skill Authoring Conventions](skill-authoring-conventions.md)
   — single-file 기본, package responsibility, maintainer docs와 naming 같은 repository-local 관행.
1. [Agent Skill Design Guide](agent-skills-guide.md)
   — Skill을 설계·작성·검증하는 통합 흐름.
1. [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)
   — Agent Skills open standard와 공식 target/harness 링크 모음. Rulesync `agentsskills` projection을 검토할 때 사용.

## 주제별 레퍼런스

`agent-skills-io/`는 외부 Agent Skills 생태계의 특정 주제를 다룹니다.

- [Skill Creation Best Practices](agent-skills-io/agent-skills-io-best-practices.md)
- [Optimizing Skill Descriptions](agent-skills-io/agent-skills-io-optimizing-descriptions.md)
- [Using Scripts in Skills](agent-skills-io/agent-skills-io-scripts.md)
- [Adding Skills Support to Clients](agent-skills-io/agent-skills-io-adding-support.md)

## 저장소 전용 보조 레퍼런스

- [Baseline Directive Template](agent-assets-skills-baseline-directive-template.md)
  — 특정 Skill의 durable intent와 decision을 별도로 보존할 가치가 있을 때 사용하는 선택적 maintainer template.
- [Template-Driven Markdown](agent-assets-skills-template-driven-markdown.md)
  — repository template 기반 Markdown 생성 reference. Rulesync나 Agent Skills standard의 일부가 아닙니다.

새 reference는 기존 authoritative owner로 연결할 수 없고 독립 책임이 있을 때만 추가합니다.
