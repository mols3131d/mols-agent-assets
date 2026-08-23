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
| `src/rulesync/.rulesync/` + `src/rulesync/rulesync.jsonc` | 재사용 Rulesync asset library의 canonical authoring source |

두 workspace는 독립적입니다. Repository-specific asset을 reusable library에 넣지 않고, library를 root에 mirror하거나 자동 활성화하지 않습니다.

### Canonical and Derived

```text
src/rulesync/.rulesync/
  author / edit / review / evaluate
            ↓ Rulesync
runtime usage surface
  consume / run
```

- `src/rulesync/.rulesync/`가 Rulesync-managed reusable asset의 authority입니다.
- Repository verification은 `tests/`, `evals/`가 소유합니다.
- Generated vendor projection과 Rulesync lock state는 reusable source가 아닙니다.
- `route/`는 library metadata에서 파생되는 cross-runtime discovery surface이며 canonical body를 대체하지 않습니다. 세부 contract는 [`route/README.md`](../../../route/README.md)가 소유합니다.

### External Sources, Fetch, Import, and Convert

Rulesync가 외부 자산을 다루는 경로는 **원본 형식과 목적**에 따라 구분합니다.

| 목적 | Rulesync 경로 | Authority |
| --- | --- | --- |
| 외부 Rulesync-compatible Rule·Skill을 dependency로 사용 | declarative `sources` / `add` / `install` | upstream source |
| remote repository의 target-native 자산을 Rulesync 작성 원본으로 흡수 | `fetch <source> --target <target>` | 검토 후 채택한 `.rulesync/` source |
| 이미 작업 공간에 있는 target-native 자산을 Rulesync 작성 원본으로 흡수 | `import --targets <target>` | 검토 후 채택한 `.rulesync/` source |
| Canonical source 없이 target 형식끼리 일회성 변환 | `convert --from <target> --to <target>` | 변환의 실제 source |

`fetch --target`과 `import`는 source 위치가 다릅니다. `fetch --target`은 remote repository의 파일을 지정한 target 형식으로 해석해 Rulesync source로 가져오고, `import`는 현재 작업 공간에 이미 존재하는 target configuration을 읽습니다. External revision이 중요하면 fetch 시 ref를 고정하고 provenance를 보존합니다.

Fetch/import가 성공했다는 사실만으로 원본과 완전한 semantic parity를 보장하지 않습니다. Target/feature별 지원 범위와 supporting resource 보존 여부를 확인하고 결과를 검토합니다. 표현할 수 없는 동작을 local shadow schema나 임의 wrapper로 보완해 Rulesync-compatible인 것처럼 만들지 않습니다.

Rulesync의 `fetch`는 현재 upstream에서 development 상태로 명시되어 있으므로 사용 시 현재 release의 contract를 다시 확인합니다. 외부 자산을 dependency로 사용할지 작성 원본으로 흡수할지에 대한 정책은 [작성 원본과 권한](../../development/source-authority.md)이 소유합니다.

### Target and Schema

`src/rulesync/rulesync.jsonc`는 이 library가 적극적으로 유지하는 **vendor support ceiling**을 선언합니다. 현재 target 이름과 feature 목록은 config가 authority이며 이 문서에 복제하지 않습니다.

실제 target applicability는 가능한 한 **개별 asset이 소유**합니다.

- Rule, Skill, Subagent는 `targets`를 명시하고 그 asset이 실제로 의미 있게 projection될 수 있는 target만 선언합니다.
- upstream Rulesync나 target runtime이 해당 asset type 또는 필요한 semantics를 지원하지 않으면 그 target을 선언하지 않습니다.
- 이 repository의 reusable asset에서는 생략 또는 `targets: ["*"]`에 의존하지 않습니다. Broad portability도 현재 유지 대상들을 명시적으로 열거합니다.
- workspace target에 포함되어 있다는 이유만으로 모든 asset이 그 target을 지원한다고 간주하지 않습니다.
- `agentsskills`는 vendor support ceiling에 포함하지 않습니다. Root self-consumer나 ChatGPT compatibility처럼 **실제 내부 consumer가 필요한 Skill에만** internal projection target으로 사용할 수 있습니다. 이는 Agent Skills 생태계 전체를 지원한다는 약속이 아닙니다.

Per-asset targeting은 다른 configuration layer를 대체하지 않습니다. Rulesync의 per-target feature configuration, target-specific metadata section, local config, CLI override와 upstream adapter semantics는 각각 필요한 책임을 계속 소유합니다. 현재 projection 대상이 아니라는 이유만으로 유효한 target-specific metadata를 삭제하지 않습니다. 더 구체적인 설정이 필요한 경우 해당 공식 Rulesync contract를 사용하고 local shadow schema를 만들지 않습니다.

Repository-local superset schema나 manual projection semantics는 만들지 않습니다. Vendor-native authored source의 선택과 배치는 [작성 원본과 권한](../../development/source-authority.md)을 따릅니다.

## Local Entry Points

| 확인할 것 | Source |
| --- | --- |
| reusable Rulesync workspace와 canonical assets | [`src/rulesync/`](../../../src/rulesync/) |
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
| `doctor`, `generate`, `fetch`, `import`, `convert`, `install`, `docs` 등 command와 option | [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md) |
| target 이름과 feature support | [Supported Tools](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/supported-tools.md) |
| 특정 target adapter의 상세 동작 | [Tool Documentation](https://github.com/dyoshikawa/rulesync/tree/main/docs/tools) |
| 예상과 다른 동작·자주 묻는 문제 | [FAQ](https://github.com/dyoshikawa/rulesync/blob/main/docs/faq.md) |
| 최근 변경과 compatibility 확인 | [Releases](https://github.com/dyoshikawa/rulesync/releases) |

## Situational References

- 외부 Rulesync-compatible Rule·Skill을 dependency로 선언하고 설치한다 → [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/declarative-sources.md)
- remote repository의 target-native 자산을 Rulesync source로 가져온다 → [CLI Commands: Fetch](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md#fetch-command)
- 이미 존재하는 target-native configuration을 `.rulesync/`로 가져오거나 target 간 직접 변환한다 → [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md)
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

- authored source placement와 target authority → [작성 원본과 권한](../../development/source-authority.md)
- runtime semantics → target contract
- Skill authoring → [Skill Authoring Conventions](../agent-assets/skills/skill-authoring-conventions.md)
- filesystem naming → [Naming](../agent-assets/common/naming.md)
- verification → [Testing](../../development/testing.md)
