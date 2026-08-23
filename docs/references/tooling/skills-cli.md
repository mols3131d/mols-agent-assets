---
title: skills CLI
description: 외부 Agent Skill dependency에 skills CLI를 사용할 때의 repository integration과 official source routing
---

# skills CLI

외부 Skill dependency의 설치 경로 선택은 [작성 원본과 권한](../../development/source-authority.md)이 소유합니다. Rulesync 경유가 비효율적이라 `skills add`를 선택한 경우 이 문서의 integration boundary를 따릅니다.

## Repository Integration

- 외부 Skill의 선택과 revision은 root [`skills-lock.json`](../../../skills-lock.json)에 기록하고 commit합니다. Lock은 upstream skills CLI 형식을 그대로 유지하며 repository 전용 target field를 추가하지 않습니다.
- skills CLI 버전은 [`mise.toml`](../../../mise.toml)에 고정합니다.
- Repository가 reusable Rulesync 자산에 사용하는 target 목록은 [`src/rulesync/rulesync.jsonc`](../../../src/rulesync/rulesync.jsonc)의 `targets`에서 읽어 Skill install target으로 재사용합니다. 별도 install manifest에 같은 목록을 복제하지 않습니다.
- [`scripts/sync_agent_skills.py`](../../../scripts/sync_agent_skills.py)는 lock의 Skill과 revision을 읽고 Rulesync target ID를 skills CLI agent ID로 변환해 명시적인 `skills add --agent ...`를 실행합니다. 새로운 target에 대응하는 mapping이 없으면 누락시키지 않고 실패합니다.
- Agent와 사람은 project dependency를 materialize하거나 갱신할 때 `mise run skills-sync`를 사용합니다. `mise run setup`, session setup과 VS Code의 `Sync Agent Skills` task도 같은 구현을 사용합니다.
- 자동 동기화에서는 telemetry를 비활성화합니다. 설치된 copy와 symlink는 dependency state이며 repository-owned canonical asset처럼 수정하지 않습니다.
- upstream을 계속 authority로 둘 수 없는 수준의 변경이 필요하면 dependency 설치가 아니라 migration/adaptation으로 다시 판단합니다.

이 wrapper는 **dependency 선택이나 target authority를 다시 정의하지 않습니다**. `skills-lock.json`은 무엇을 어느 revision에서 설치할지 계속 소유하고, `src/rulesync/rulesync.jsonc`은 자신의 target 목록을 계속 소유합니다. Wrapper는 그 목록을 설치 target으로 재사용하면서 두 upstream schema 사이의 target ID 차이와 실행만 소유합니다.

## Official Sources

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [CLI usage](https://github.com/vercel-labs/skills#cli)

구체적인 command와 lock semantics는 current upstream을 확인합니다.

## Boundary

- 외부 자산의 authority와 installer 선택 → [작성 원본과 권한](../../development/source-authority.md)
- Rulesync source, import, fetch, convert → [Rulesync](rulesync.md)
