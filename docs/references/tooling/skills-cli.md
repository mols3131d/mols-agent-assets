---
title: skills CLI
description: 외부 Agent Skill dependency의 lock, source-native 설치와 repository integration 경계
---

# skills CLI

외부 Skill dependency의 설치 경로 선택은 [작성 원본과 권한](../../development/source-authority.md)이 소유합니다. Rulesync 경유가 비효율적이라 skills CLI를 선택한 경우에도 vendor별 semantics를 일반화하지 않습니다.

## Repository Integration

- 외부 Skill의 선택과 revision은 root [`skills-lock.json`](../../../skills-lock.json)에 기록하고 commit합니다. Lock은 upstream skills CLI 형식을 그대로 유지하며 repository 전용 target field를 추가하지 않습니다.
- skills CLI 버전은 [`mise.toml`](../../../mise.toml)에 고정하며 dependency를 추가하거나 lock 상태를 의도적으로 변경할 때 사용합니다.
- [`scripts/sync_agent_skills.py`](../../../scripts/sync_agent_skills.py)는 lock의 source와 revision을 **읽기만** 합니다. 설치 상태를 맞추는 과정에서 `skills-lock.json`을 다시 쓰지 않습니다.
- `skills-sync`는 latest revision resolver가 아닙니다. Upstream의 더 새로운 revision을 채택하려면 dependency update로 lock을 먼저 의도적으로 갱신한 뒤 sync합니다.
- 한 source가 vendor별로 서로 다른 payload나 추가 runtime 자산을 제공하면 generic `skills add --agent ...`로 같은 payload를 여러 target에 강제하지 않습니다. 해당 source의 native installer가 더 충실한 경우 adapter는 그 installer에 vendor 감지와 설치를 위임합니다.
- 현재 `epoko77-ai/im-not-ai`의 `humanize-korean` dependency는 고정된 lock ref를 user cache에 checkout한 뒤 upstream `install.sh`를 실행합니다. Claude Code, Codex CLI, Gemini CLI의 payload와 지원 범위는 upstream installer가 결정합니다. GitHub Copilot처럼 upstream이 지원 대상으로 선언하지 않은 vendor에는 임의로 설치하지 않습니다.
- `skills-sync`는 dependency source cache와 upstream installer가 정의한 user-level vendor 설치 상태를 변경할 수 있습니다. 이는 외부 Skill을 실제 runtime에서 사용할 수 있게 만드는 의도된 side effect이며, repository의 authored source를 변경하는 작업은 아닙니다.
- Lock에서 dependency가 제거됐다는 이유만으로 user-level 설치를 자동 삭제하지 않습니다. 제거는 해당 source의 native uninstall 절차를 명시적으로 사용합니다.
- Agent와 사람은 dependency를 materialize하거나 lock된 revision으로 다시 맞출 때 `mise run skills-sync`를 사용합니다. `mise run setup`, session setup과 VS Code의 `Sync Agent Skills` task도 같은 구현을 사용합니다.
- 새로운 dependency에 native adapter가 없으면 추측해서 설치하지 않고 실패합니다. 이 경우 [작성 원본과 권한](../../development/source-authority.md)에 따라 generic skills CLI 설치가 충분한지, source-native installer가 필요한지 먼저 결정합니다.
- 설치된 copy, symlink, source cache는 dependency state이며 repository-owned canonical asset처럼 수정하지 않습니다.

이 구조에서 `skills-lock.json`은 **무엇을 어느 revision에서 사용할지**, source-native installer는 **그 source가 vendor별로 어떻게 설치되는지**, repository wrapper는 **둘을 연결하고 자동화하는 좁은 adapter**만 소유합니다. Reusable Rulesync 자산의 distribution target은 이 dependency 설치 정책의 authority가 아닙니다.

## Official Sources

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [CLI usage](https://github.com/vercel-labs/skills#cli)

구체적인 command와 lock semantics는 current upstream을 확인합니다. Dependency별 native 설치 방식은 해당 upstream source의 현재 설치 문서를 우선합니다.

## Boundary

- 외부 자산의 authority와 installer 선택 → [작성 원본과 권한](../../development/source-authority.md)
- Rulesync source, import, fetch, convert → [Rulesync](rulesync.md)
