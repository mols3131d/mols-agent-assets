---
title: Rulesync
description: Rulesync의 repository-local·재사용 workspace, 작성 원본과 생성 결과, target 범위 및 공식 CLI·schema 문서의 참조 경로를 확인할 때 사용합니다.
---

# Rulesync

Rulesync는 공통 작성 원본을 target별 Agent Asset 형식으로 투영하고 외부 Rulesync dependency를 설치하는 도구입니다. 이 문서는 **저장소 통합 구조와 공식 문서의 탐색 경로**를 다룹니다. Schema·CLI 옵션·adapter의 실제 동작은 [Rulesync 공식 문서](https://rulesync.dyoshikawa.com/)가 소유하고, 이 저장소의 버전·설치 승인·인증 예외는 [프로젝트 Rulesync 운영 안내](../../tools/rulesync.md)가 소유합니다.

## Workspace와 작성 원본

| 구분 | 작성·설정 위치 | 역할 |
| --- | --- | --- |
| 저장소 자체 사용 | [`.rulesync/`](../../../.rulesync/), [`rulesync.jsonc`](../../../rulesync.jsonc) | 이 저장소 전용 자산 및 외부 dependency의 소비 설정 |
| 재사용 자산 | [`src/rulesync/.rulesync/`](../../../src/rulesync/.rulesync/), [`src/rulesync/rulesync.jsonc`](../../../src/rulesync/rulesync.jsonc) | 여러 프로젝트에 제공할 Rulesync 작성 원본과 별도 projection 설정 |

두 workspace는 독립적입니다. `src/`에 관리되는 자산이 이 저장소에 자동 설치·활성화되는 것은 아니며, root에 재사용 원본의 복제본을 만들지도 않습니다. 재사용 vendor-native 원본은 `src/<vendor>/`에서 별도로 관리합니다. 원본 형식과 위치를 고르는 정책은 [작성 원본과 권한](../source-authority.md)을 따릅니다.

- **작성 원본:** 각 workspace의 `.rulesync/`. 사람이 수정·리뷰하는 대상입니다.
- **파생 결과:** Rulesync가 생성한 vendor별 파일. 원본을 대신하거나 독립적인 작성 원본이 되지 않습니다.
- **의존성 상태:** root [`rulesync.lock`](../../../rulesync.lock). 외부 revision의 잠금 기준이지 실제 설치·적용 여부의 증거는 아닙니다.
- **탐색 결과:** [`route/`](../../../route/). 자산의 본문을 대체하지 않으며 생성·관리 계약은 [Route 안내](../../../route/README.md)를 따릅니다.

## 작업에 맞는 경로

| 하려는 일 | 확인할 곳 |
| --- | --- |
| 이 저장소에서 외부 Rulesync dependency 사용·재설치 | root `rulesync.jsonc`와 `rulesync.lock`, [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/declarative-sources.md) |
| 재사용 Rule·Skill·Subagent·Command 작성 또는 수정 | `src/rulesync/.rulesync/`와 [File Formats](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md) |
| 원격 target-native 자산을 Rulesync 작성 원본으로 가져오기 | `fetch` |
| 현재 workspace에 존재하는 target-native 자산 가져오기 | `import` |
| 작성 원본을 채택하지 않는 일회성 target 간 변환 | `convert` |
| Rulesync 대신 외부 Skill installer로 dependency 사용 | [skills CLI 통합 안내](skills-cli.md) |

`fetch`·`import`·`convert`의 옵션과 지원 범위는 [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md)에서 확인합니다. 가져온 결과는 자동으로 canonical이 되지 않습니다. 필요한 동작, supporting resources, license·provenance, 대상별 지원을 검토한 뒤 채택합니다. 설치할지 작성 원본으로 흡수할지는 [작성 원본과 권한](../source-authority.md)의 결정입니다.

### Root dependency 설치의 경계

Root dependency는 `rulesync.jsonc`에 선언되며 GitHub transport를 사용합니다. Core `mise run setup`에서 설치하지 않습니다. 별도 승인과 설치 대상 확인 후 `rulesync install --frozen`을 사용하고, 필요한 GitHub token은 **설치 프로세스에만** 전달합니다. `GITHUB_TOKEN`·`GH_TOKEN`이나 개인별 `rulesync.local.jsonc`를 저장소에 기록하지 않습니다. 상세한 재현·승인·인증 지침은 [프로젝트 운영 안내](../../tools/rulesync.md)를 따릅니다.

`rulesync.lock`의 revision과 설치 상태, Rulesync 자체 CLI 버전은 서로 다른 상태입니다. Lock·transport·schema의 수정만을 이유로 외부 asset revision을 갱신하지 않습니다.

## Target과 검증

재사용 library의 [`rulesync.jsonc`](../../../src/rulesync/rulesync.jsonc)가 repository에서 유지할 target·feature의 **상한**을 선언합니다. 그러나 실제 적용 대상은 개별 Rule·Skill·Subagent·Command가 선언하는 `targets`를 기준으로 확인합니다.

- 이 저장소의 재사용 자산은 의미 있게 지원하는 target을 명시적으로 나열합니다. Workspace 설정이나 wildcard만으로 개별 자산의 호환성을 가정하지 않습니다.
- 개별 target의 원본 표현력, metadata, feature mode와 생성 경로는 Rulesync 및 해당 runtime의 현재 공식 계약을 따릅니다. 지원하지 않는 동작을 임의의 로컬 schema로 보충하지 않습니다.
- `agentsskills`는 필요한 내부 소비자가 있는 Skill에서만 쓰는 projection target이며, 재사용 library의 vendor 지원 범위에 넣지 않습니다. 전체 Agent Skills 생태계의 지원 선언으로 해석하지 않습니다.

재사용 자산의 결정론적 검증은 [`scripts/agent_assets/rulesync_validate.py`](../../../scripts/agent_assets/rulesync_validate.py)가 수행합니다. 이 스크립트는 `src/rulesync`에서 Rulesync `doctor --strict`와 `generate --dry-run`을 실행하고 warning도 실패로 취급합니다. 이 확인은 **설정과 선언된 projection의 구조적 검증**이며 runtime 동작·의미적 동등성·지원하지 않는 target까지 검증했다는 뜻이 아닙니다. 실행 진입점은 [`mise.toml`](../../../mise.toml)을 확인합니다.

## 공식 문서 찾기

| 확인 사항 | 공식 자료 |
| --- | --- |
| Configuration·schema | [Configuration](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/configuration.md), [config schema](https://github.com/dyoshikawa/rulesync/releases/latest/download/config-schema.json) |
| Command·option·lock 처리 | [CLI Commands](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/cli-commands.md) |
| Target별 feature·mode·file shape | [Supported Tools](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/supported-tools.md), [File Formats](https://github.com/dyoshikawa/rulesync/blob/main/docs/reference/file-formats.md) |
| Target adapter의 예외 | [Tool Documentation](https://github.com/dyoshikawa/rulesync/tree/main/docs/tools) |
| 변경·호환성 확인 | [Releases](https://github.com/dyoshikawa/rulesync/releases) |

프로젝트에 설치된 버전의 상세 계약을 확인하려면 `rulesync docs`, `rulesync docs <document>`, `rulesync docs --search <term>`을 사용할 수 있습니다. 최신 동작은 공식 문서, 과거 동작은 해당 버전의 문서와 릴리스에서 확인합니다.

문서 작성 규칙이나 검증 전반은 각각 [Skill 작성 규약](../agent-assets/skills/skill-authoring-conventions.md), [Testing](../testing.md)을 따릅니다.
