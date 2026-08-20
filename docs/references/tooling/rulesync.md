---
title: Rulesync
description: 이 저장소의 Rulesync integration boundary와 current official documentation을 빠르게 찾기 위한 reference
---

# Rulesync

이 문서는 **이 저장소의 Rulesync integration boundary와 official source routing**을 함께 소유합니다. Schema, file format, feature, target namespace, target adapter와 CLI semantics는 current upstream Rulesync가 authoritative합니다.

## Repository Integration

### Workspaces

| Workspace | 책임 |
| --- | --- |
| root `.rulesync/` + `rulesync.jsonc` | 실제 필요가 있을 때만 사용하는 repository-local Rulesync assets/configuration |
| `src/rulesync/.rulesync/` + `src/rulesync/rulesync.jsonc` | 재사용 asset library의 canonical authoring source |

두 workspace는 독립적입니다. Repository-specific asset을 reusable library에 넣지 않고, library를 root에 mirror하거나 자동 활성화하지 않습니다.

### Canonical and Derived

```text
src/rulesync/.rulesync/
  author / edit / review / evaluate
            ↓ Rulesync
runtime usage surface
  consume / run
```

- `src/rulesync/.rulesync/`가 reusable asset의 authority입니다.
- Repository verification은 `tests/`, `evals/`가 소유합니다.
- Generated vendor projection과 Rulesync lock state는 reusable source가 아닙니다.
- `route/`는 library metadata에서 파생되는 cross-runtime discovery surface이며 canonical body를 대체하지 않습니다. 세부 contract는 [`route/README.md`](../../../route/README.md)가 소유합니다.

### Target and Schema

이 저장소는 supported vendor/target matrix를 정의하지 않습니다. Target은 구체적인 projection 또는 검증 operation에서만 선택합니다. 개별 asset의 유효한 target-specific metadata는 현재 projection 대상이 아니라는 이유만으로 제거하지 않습니다.

Repository-local superset schema나 manual projection semantics는 만들지 않습니다. Custom semantic은 **current Rulesync로 required behavior를 표현할 수 없다는 것이 확인된 경우에만** 후보가 됩니다.

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

## Boundary

- runtime semantics → target contract
- Skill authoring → [Skill Authoring Conventions](../skills/skill-authoring-conventions.md)
- filesystem naming → [Naming](../common/naming.md)
- verification → [Testing](../../testing.md)
