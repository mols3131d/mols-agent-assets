---
title: Rulesync
description: 이 저장소에서 Rulesync를 사용할 때 local entrypoint와 current official documentation을 빠르게 찾기 위한 reference
---

# Rulesync

이 문서는 Rulesync 동작을 복제하지 않고 **이 저장소의 사용 지점과 current official source를 연결**합니다. Schema, file format, target adapter와 CLI semantics는 upstream이 authoritative합니다.

Repository-local workspace/source 정책은 [Rulesync Repository Conventions](../common/rulesync.md)가 소유합니다.

## Local Entry Points

| 확인할 것 | Source |
| --- | --- |
| reusable workspace와 canonical assets | [`src/rulesync/`](../../../src/rulesync/) |
| library configuration | [`src/rulesync/rulesync.jsonc`](../../../src/rulesync/rulesync.jsonc) |
| Rulesync 실행 wrapper | [`scripts/run_rulesync.py`](../../../scripts/run_rulesync.py) |
| repository command entrypoints | [`package.json`](../../../package.json) |

현재 값이나 command를 이 문서에 복제하지 않습니다. 작업 시 위 source를 읽습니다.

## Frequent Official References

| 판단 | 공식 source |
| --- | --- |
| Rulesync 문서 탐색 시작 | [Documentation](https://rulesync.dyoshikawa.com/) · [Repository](https://github.com/dyoshikawa/rulesync) |
| `rulesync.jsonc`, target/feature와 configuration field | [Configuration](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/configuration.md) · [Latest config schema](https://github.com/dyoshikawa/rulesync/releases/latest/download/config-schema.json) |
| Rules, Skills, Subagents 등 source/target file shape | [File Formats](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md) |
| `doctor`, `generate`, `install`, `fetch`, `docs` 등 command와 option | [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md) |
| target 이름과 feature support | [Supported Tools](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/supported-tools.md) |
| 특정 target adapter의 상세 동작 | [Tool Documentation](https://github.com/dyoshikawa/rulesync/tree/main/docs/tools) |
| 예상과 다른 동작·자주 묻는 문제 | [FAQ](https://github.com/dyoshikawa/rulesync/blob/main/docs/faq.md) |
| 최근 변경과 compatibility 확인 | [Releases](https://github.com/dyoshikawa/rulesync/releases) |

## Situational References

- 외부 repository/package의 Rule·Skill을 `sources`로 선언하고 설치한다 → [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/declarative-sources.md)
- 실제 write 없이 generation 결과를 확인한다 → [Dry Run](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/dry-run.md)
- input/output root 구성을 바꾼다 → [Separate Input Root](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/separate-input-root.md)
- global configuration을 사용한다 → [Global Mode](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/global-mode.md)
- simulated feature의 의미를 판단한다 → [Simulated Features](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/simulated-features.md)
- Agent가 Rulesync 자체 사용법을 로드해야 한다 → [Official Rulesync Skill](https://github.com/dyoshikawa/rulesync/blob/main/skills/rulesync/SKILL.md)

## Lookup

Rulesync-specific detail을 판단할 때 기억이나 이 문서보다 current official source를 우선합니다. 특히 target adapter, metadata field, generated path, feature support와 CLI option은 작업 시점에 다시 확인합니다.

CLI에서 bundled documentation을 직접 조회할 수도 있습니다.

```bash
npx --yes rulesync@latest docs
npx --yes rulesync@latest docs <document>
npx --yes rulesync@latest docs --search <term>
```

Historical compatibility를 조사할 때만 해당 release/tag의 문서를 고정해서 봅니다.
