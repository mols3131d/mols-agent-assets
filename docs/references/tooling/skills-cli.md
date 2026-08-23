---
title: skills CLI
description: 외부 Agent Skill dependency에 skills CLI를 사용할 때의 repository integration과 official source routing
---

# skills CLI

외부 Skill dependency의 설치 경로 선택은 [작성 원본과 권한](../../development/source-authority.md)이 소유합니다. Rulesync 경유가 비효율적이라 `skills add`를 선택한 경우 이 문서의 integration boundary를 따릅니다.

## Repository Integration

- 외부 Skill은 `npx skills add`로 추가합니다.
- project dependency의 선택과 revision은 root [`skills-lock.json`](../../../skills-lock.json)에 기록하고 commit합니다.
- 추가·갱신은 skills CLI가 lock을 갱신하게 하며 같은 선택을 별도 manifest나 task에 다시 선언하지 않습니다.
- 설치된 copy는 dependency state이며 repository-owned canonical asset처럼 수정하지 않습니다.
- upstream을 계속 authority로 둘 수 없는 수준의 변경이 필요하면 dependency 설치가 아니라 migration/adaptation으로 다시 판단합니다.

## Official Sources

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [CLI usage](https://github.com/vercel-labs/skills#cli)

구체적인 command와 lock semantics는 current upstream을 확인합니다.

## Boundary

- 외부 자산의 authority와 installer 선택 → [작성 원본과 권한](../../development/source-authority.md)
- Rulesync source, import, fetch, convert → [Rulesync](rulesync.md)
