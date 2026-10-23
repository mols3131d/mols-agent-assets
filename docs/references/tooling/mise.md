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

## Shared and local environment

공통 실행 환경은 [`mise.toml`](../../../mise.toml)의 `[env]`가 소유하며 Python에 UTF-8을 적용합니다. Git 설정은 전체 mise 프로세스에 강제하지 않습니다. Rulesync의 외부 dependency 임시 clone에서 LF가 필요한 경우에만 `mise run rulesync-install`이 기존 Git 환경 설정을 보존하면서 `core.autocrlf=false`를 추가합니다. 저장소의 [`.gitattributes`](../../../.gitattributes)만으로는 외부 clone의 LF를 보장하지 못합니다.

PC별 설치 경로만 Git에서 제외된 `mise.local.toml`에 둡니다. 예를 들어 Windows에서 Git Bash를 PATH에 추가해야 한다면 다음처럼 설정합니다.

```toml
[env]
_.path = ["C:/Program Files/Git/bin"]
```

기존 로컬 파일의 `PYTHONUTF8` 중복과 이전 LF 보정용 `GIT_CONFIG_*` 값은 제거합니다. PC 또는 상위 프로세스의 인증용 Git 설정은 보존해야 합니다. Git 전역 설정은 변경하지 않습니다. Rulesync의 로컬 설정 정리는 [Rulesync](rulesync.md#repository-local-installation)를 따릅니다.

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
