---
title: mise
description: 이 저장소에서 tool version·task entrypoint를 어디에 고정할지, mise와 uv의 ownership을 어떻게 나눌지 확인하거나 setup·check·test·format 명령을 찾을 때 사용합니다.
---

# mise

Repository tool version authority는 root [`mise.toml`](../../../mise.toml)입니다. Python 자체의 version과 dependency environment는 uv가 소유합니다.

| Owner | Scope |
| --- | --- |
| mise | `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync, skills CLI의 binary/version과 cross-tool tasks |
| uv | `.python-version`, `pyproject.toml`, `uv.lock`, Python environment와 Python dependencies |

Python을 `mise.toml`에 중복 선언하지 않습니다. Non-Python tool을 Python dependency group에 넣지 않습니다. npm backend로 관리하는 CLI는 `mise.toml`에서 exact version을 pin하며 repository task는 `@latest`를 직접 호출하지 않습니다.

## Current bootstrap boundary

현재 `mise run setup`은 Python 의존성 동기화, Rulesync 설치·생성, 외부 Skill 동기화와 Git Hook 설치를 순서대로 수행합니다. 개발 중 사용할 **허용 버전 범위 내 최신 업데이트**를 전담하는 별도 task는 아직 없습니다. 현재 `mise.toml`의 도구 버전은 exact pin이며, 업데이트 정책과 실제 설치·적용 동작을 혼동하지 않습니다.

`mise` 자체나 system package manager, Git·Bash와 같은 host prerequisite는 repository-local Python dependency와 구분합니다. 기존 `setup`은 user-level Skill installer도 실행하므로 초기 설치는 실행 전에 side effect 범위를 확인해야 합니다.

## Common entry points

```bash
mise install
mise run setup
mise run skills-sync
mise run check
mise run test
mise run format
```

외부 Skill dependency의 lock과 source-native 동기화 경계는 [skills CLI](skills-cli.md)를 따릅니다.

Promptfoo처럼 Node runtime이 필요한 기존 command는 mise environment에서 실행합니다.

```bash
mise exec -- npm run eval:promptfoo:mols-loops
```

## Official sources

- [mise configuration](https://mise.jdx.dev/configuration.html)
- [mise tools and backends](https://mise.jdx.dev/dev-tools/backends/)
- [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
- [mise tasks](https://mise.jdx.dev/tasks/)
- [mise CI](https://mise.jdx.dev/continuous-integration.html)
- [uv Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [uv projects](https://docs.astral.sh/uv/concepts/projects/)
- [rumdl installation](https://github.com/rvben/rumdl#installation)
- [Lefthook with mise](https://lefthook.dev/installation/mise/)
- [Lefthook install](https://lefthook.dev/usage/commands/install/)
- [Biome configuration](https://biomejs.dev/reference/configuration/)
- [Biome CLI](https://biomejs.dev/reference/cli/)
- [Rulesync](rulesync.md)
- [skills CLI](skills-cli.md)

Version-dependent behavior는 `mise.toml`의 pin과 current official source를 함께 확인합니다.
