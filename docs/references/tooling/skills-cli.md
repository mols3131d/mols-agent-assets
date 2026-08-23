---
title: skills CLI
description: 외부 Agent Skill dependency에 skills CLI를 사용할 때의 repository integration과 official source routing
---

# skills CLI

외부 Skill dependency의 설치 경로 선택은 [작성 원본과 권한](../../development/source-authority.md)이 소유합니다. Rulesync 경유가 비효율적이라 `skills add`를 선택한 경우 이 문서의 integration boundary를 따릅니다.

## Repository Integration

- `skills` CLI version은 [`mise.toml`](../../../mise.toml)이 고정합니다.
- project external Skill dependency의 선택과 revision은 root [`skills-lock.json`](../../../skills-lock.json)이 소유합니다.
- dependency 추가·갱신은 `skills add`/`skills update`를 사용하고 생성된 lock을 commit합니다.
- repository setup은 lock에서 복원하며 dependency 선택을 다른 config에 다시 선언하지 않습니다.
- 설치된 Skill copy는 generated dependency state이며 repository-owned canonical asset처럼 수정하지 않습니다.
- upstream을 계속 authority로 둘 수 없는 수준의 변경이 필요하면 dependency 설치가 아니라 migration/adaptation으로 다시 판단합니다.

현재 pin된 CLI에서 lock 복원 command는 `skills experimental_install`입니다. Command 이름과 semantics는 upstream에서 바뀔 수 있으므로 current CLI contract를 확인합니다.

## Official Sources

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [CLI usage](https://github.com/vercel-labs/skills#cli)

## Boundary

- 외부 자산의 authority와 installer 선택 → [작성 원본과 권한](../../development/source-authority.md)
- Rulesync source, import, fetch, convert → [Rulesync](rulesync.md)
- tool version과 setup entrypoint → [mise](mise.md)
