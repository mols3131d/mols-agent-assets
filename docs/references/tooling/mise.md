---
title: mise
description: 이 저장소의 mise와 uv tool ownership 및 official source routing
---

# mise

Repository tool version authority는 root [`mise.toml`](../../../mise.toml)입니다. Python 자체의 version과 dependency environment는 uv가 소유합니다.

| Owner | Scope |
| --- | --- |
| mise | `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync, skills CLI binary/version과 cross-tool tasks |
| uv | `.python-version`, `pyproject.toml`, `uv.lock`, Python environment와 Python dependencies |

Python을 `mise.toml`에 중복 선언하지 않습니다. Non-Python tool을 Python dependency group에 넣지 않습니다. Rulesync와 skills CLI는 mise의 npm backend로 exact version을 pin하며 repository runner는 `@latest`를 직접 호출하지 않습니다.

## Common entry points

```bash
mise install
mise run setup
mise run check
mise run test
mise run format
```

Promptfoo처럼 Node runtime이 필요한 기존 command는 mise environment에서 실행합니다.

```bash
mise exec -- npm run eval:promptfoo:mols-rpi
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
