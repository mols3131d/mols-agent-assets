---
title: Rulesync
description: 이 저장소에서 Rulesync를 사용할 때 자주 확인하는 local entrypoint와 current official documentation 링크
---

# Rulesync

이 문서는 Rulesync 동작을 복제하는 local specification이 아니라 **이 저장소의 사용 지점과 current official source를 빠르게 연결하는 reference**입니다. Rulesync schema, file format, target adapter와 CLI semantics는 upstream이 authoritative합니다.

Repository-local workspace/source 정책은 [Rulesync Repository Conventions](../common/rulesync.md)가 소유합니다.

## This Repository

- reusable workspace → [`src/rulesync/`](../../../src/rulesync/)
- canonical assets → [`src/rulesync/.rulesync/`](../../../src/rulesync/.rulesync/)
- library config → [`src/rulesync/rulesync.jsonc`](../../../src/rulesync/rulesync.jsonc)
- runner → [`scripts/run_rulesync.py`](../../../scripts/run_rulesync.py)
- npm entrypoints → [`package.json`](../../../package.json)

현재 library config는 target을 repository identity로 고정하지 않고 `targets: []`로 두며 `rules`, `skills`, `subagents`를 canonical feature로 관리합니다. Repository runner는 `npx --yes rulesync@latest`를 사용합니다.

```bash
npm run rulesync:doctor
npm run rulesync:preview -- --targets <target>
npm run rulesync:validate -- --targets <target>
```

## Frequent Official References

| 확인할 것 | 공식 source |
| --- | --- |
| 문서 전체 entrypoint | [Rulesync Documentation](https://rulesync.dyoshikawa.com/) |
| upstream repository | [dyoshikawa/rulesync](https://github.com/dyoshikawa/rulesync) |
| `rulesync.jsonc`, local config, target/feature selection | [Configuration](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/configuration.md) |
| Rules, Skills, Subagents 등 canonical/target file format | [File Formats](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md) |
| `doctor`, `generate`, `import`, `fetch`, `install`, `docs` 등 CLI | [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md) |
| target 이름과 feature support | [Supported Tools](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/supported-tools.md) |
| target별 상세 동작 | [Tool Documentation Directory](https://github.com/dyoshikawa/rulesync/tree/main/docs/tools) |
| 최신 변경·breaking change | [Releases](https://github.com/dyoshikawa/rulesync/releases) |
| current config schema | [Latest `config-schema.json`](https://github.com/dyoshikawa/rulesync/releases/latest/download/config-schema.json) |
| 동작이 예상과 다를 때 | [FAQ](https://github.com/dyoshikawa/rulesync/blob/main/docs/faq.md) |

## Situational References

- source repository에서 Skills 등을 가져오거나 설치 구조를 확인한다 → [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/declarative-sources.md)
- 실제 write 없이 projection을 확인한다 → [Dry Run](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/dry-run.md)
- input root와 output root를 분리한다 → [Separate Input Root](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/separate-input-root.md)
- global configuration을 다룬다 → [Global Mode](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/global-mode.md)
- simulated command/subagent/skill behavior를 판단한다 → [Simulated Features](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/simulated-features.md)
- Rulesync 자체의 official agent Skill을 참고한다 → [Rulesync `SKILL.md`](https://github.com/dyoshikawa/rulesync/blob/main/skills/rulesync/SKILL.md)

## Lookup Rule

기억이나 이 문서의 요약보다 current official source를 우선합니다. 특히 target adapter, metadata field, generated path, feature support와 CLI option은 변경 가능성이 있으므로 작업 시점에 다시 확인합니다.

설치된 Rulesync가 있으면 bundled documentation도 사용할 수 있습니다.

```bash
npx --yes rulesync@latest docs
npx --yes rulesync@latest docs guide/configuration
npx --yes rulesync@latest docs --search <term>
```

Historical compatibility를 조사할 때만 해당 release/tag의 문서를 고정해서 보고, 평상시 authoring과 validation은 current upstream을 기준으로 합니다.
