---
description: 이 프로젝트에서 사용하는 도구의 기본 설정·버전 선택 원칙, 도구별 예외와 실제 설정 파일을 찾을 때 사용합니다.
---

# Tools

이 디렉터리는 **이 프로젝트에서 도구를 어떻게 사용하고, 어떤 설정과 버전을 선택하는지**를 정리합니다. 도구 자체의 기능과 기본값은 공식 문서가 소유하고, 여기서는 프로젝트의 선택과 그 이유를 다룹니다. 개발환경 격리와 설치 승인은 [Development Environment](../development/development-environment.md)를 따릅니다.

## 공통 원칙

- **기본 설정 우선:** 공식 기본값과 native 설정·명령을 먼저 사용합니다. 기본값을 그대로 옮겨 적거나 wrapper에서 중복 강제하지 않습니다. 프로젝트 요구 때문에 다른 값이 필요할 때만 설정과 이유를 남깁니다.
- **버전 선택:** SemVer 기반 허용 범위를 도구별로 선택하고, 명시적 갱신 시 그 범위의 적절한 안정 릴리스를 검토합니다. 보안 권고·지원 종료는 우선 대응하며, formatter 출력·생성물·평가 재현성 등 호환성 제약을 고려합니다. Prerelease는 별도 근거 없이 채택하지 않습니다.
- **선택과 실행 분리:** 최신 버전을 선호해도 매 실행에서 `latest`를 해석하거나 설치를 자동 갱신하지 않습니다. 검토·채택한 버전은 manifest와 lock에 고정하고, `setup`은 이를 재현합니다. **Exact pin은 재현성 장치이지 영구 동결 정책이 아닙니다.**
- **설정의 정본 유지:** 실행 가능한 설정·버전·잠금 값은 각 native 파일이 소유합니다. 문서는 값 전체를 복제하지 않고 기본값과 다른 선택, 갱신 시 확인할 항목, 운영 경계를 설명합니다.

## mise 버전 선택지

실제 버전 선택은 mise의 native 요청을 사용하며, lock 갱신과 설치는 분리합니다.

| 선택지 | mise 요청 예시 | 허용 범위 |
| --- | --- | --- |
| Exact | `2.5.6` | 지정한 버전 |
| Patch | `2.5` | 2.5.x |
| Minor | `2` | 2.x |
| Latest | `latest` | backend가 선택하는 최신 버전; Major 전환 가능 |
| LTS | `node = "lts"` | Node.js가 제공하는 LTS alias; Major 전환 가능 |

LTS는 **지원되는 도구에 한해 사용하는 별도의 native 요청 방식**입니다. mise의 버전 prefix와 `lts` alias를 임의로 결합하는 정책 엔진은 만들지 않습니다. `0.x` 도구의 Minor 변경, formatter 출력, 생성물과 평가 조건에는 특히 주의합니다.

### 도구별 권장 정책

아래는 **추후 버전 범위 전환 시 적용할 제안**입니다. 현재 실행 설정은 `mise.toml` 및 lockfile이 정본입니다.

| 대상 | 권장 | 요청/경계 | 갱신 시 핵심 확인 |
| --- | --- | --- | --- |
| Node.js | LTS | `lts` | 새 LTS Major와 npm CLI·평가 runner 호환성 |
| uv | Patch | `0.13` | `0.x` 인터페이스·bootstrap·보안 수정 |
| rumdl | Patch | `0.3` | Markdown format·lint diff |
| Lefthook | Minor | `2` | hook 명령과 설치 영향 |
| Biome | Minor | `2` | schema·formatter diff |
| Rulesync | Minor | `43` | config·lock·projection 호환성 |
| skills CLI | Minor | `1` | 외부 Skill revision 유지·installer 호환성 |

별도 관리자: Python 인터프리터는 uv의 3.13 계열 Patch, Ruff는 0.x Patch(현재 선언에 상한 없음), pytest는 9.x Minor(현재 선언에 상한 없음)를 권장합니다. Promptfoo는 평가 비교를 위한 **Exact**, Front Matter CMS 확장은 편집기 관리의 **Latest**로 구분합니다. [uv·Python](uv.md), [Promptfoo](promptfoo.md), [Front Matter CMS](front-matter-cms.md)의 정본을 따릅니다.

**전환 조건:** 현재 7개 CLI는 Exact pin이고 [bootstrap 실행기](../../scripts/development_bootstrap.py)도 Exact만 받습니다. 이 문서는 선택 기준을 정리할 뿐, `mise.toml`, 잠금, 스크립트 또는 바이너리를 갱신하지 않습니다. 범위 정책을 실제 적용하려면 bootstrap의 잠금 버전 검증과 플랫폼별 실행을 먼저 수정·검증해야 합니다.

## 설정과 잠금

| 대상 | 정본 | 현재 예외와 경계 |
| --- | --- | --- |
| 개발 CLI와 공통 task | [`mise.toml`](../../mise.toml), [`mise.lock`](../../mise.lock) | CLI 7종은 검토한 exact pin을 사용합니다. 현재 `update`는 CLI 버전을 자동 갱신하지 않습니다. |
| Python과 프로젝트 패키지 | [`.python-version`](../../.python-version), [`pyproject.toml`](../../pyproject.toml), [`uv.lock`](../../uv.lock) | Python 선택과 패키지 관리는 uv가 맡고 프로젝트 `.venv`로 격리합니다. `update`는 선언 범위 안의 Python 의존성만 갱신합니다. |
| 코드·문서 포맷과 lint | [`pyproject.toml`](../../pyproject.toml), [`.rumdl.toml`](../../.rumdl.toml), [`biome.json`](../../biome.json) | 도구 기본값보다 저장소의 출력 규칙이 우선합니다. 규칙·버전을 바꿀 때는 기존 파일의 diff를 확인합니다. |
| 외부 Agent Asset | [`rulesync.jsonc`](../../rulesync.jsonc), [`rulesync.lock`](../../rulesync.lock), [`skills-lock.json`](../../skills-lock.json) | CLI 최신화와 자산 revision 갱신은 별개입니다. 일반 bootstrap에서 외부 자산과 HOME 설치를 갱신하지 않습니다. |
| 선택적 연동 | [`lefthook.yml`](../../lefthook.yml), [`frontmatter.json`](../../frontmatter.json) | Git hook 설치와 에디터 연동은 core bootstrap의 성공 조건이 아닙니다. |

## 버전 갱신 방법

1. **후보 확인:** upstream release note·보안 권고·지원 수명과 이 저장소의 사용처를 확인합니다. 특히 formatter 출력, Rulesync projection, Node 실행 호환성, 평가 모델·데이터의 비교 조건을 구분합니다.
1. **Lock 갱신:** 현재 Exact pin은 `mise.toml`에서 버전을 먼저 바꿔야 합니다. 추후 range·alias를 활성화하면 `mise lock --bump`로 허용된 후보를 잠급니다. Lock 갱신이 `mise.toml`의 정책 변경이나 Python·외부 Agent Asset 갱신을 의미하지는 않습니다.
1. **확인 후 통합:** 플랫폼별 잠금·체크섬과 필요한 npm dependency sidecar를 검토하고, 승인된 격리 환경에서 `mise install --locked`, `mise run check`, `mise run test` 및 영향 범위 검증을 수행합니다. 포맷·생성 결과 diff를 검토한 다음 PR Gate로 통합합니다. 설치 승인은 [개발환경 정책](../development/development-environment.md)이 소유합니다.

`mise run update`는 현재 **Python 의존성만** 갱신합니다. CLI·Node major·formatter·Rulesync 버전은 별도 명시적 변경이며, 검사 없이 자동으로 최신화하지 않습니다. [mise 운영 안내](mise.md#cli-version-updates)에 실행 경계를 두고, 실제 버전값은 정본 파일만 봅니다.

## Index

- 환경을 준비·복구한다면 [mise](mise.md)와 [uv·Python](uv.md)을 먼저 확인합니다. npm CLI의 runtime·LTS 선택은 [Node.js](node.md)가 다룹니다.
- format·lint 출력을 바꾼다면 [rumdl](rumdl.md), [Biome](biome.md), Python 도구는 [uv·Python](uv.md#python-개발-도구)을 확인합니다.
- 외부 자산을 설치·생성한다면 [Rulesync](rulesync.md)와 [skills CLI](skills-cli.md)를 구분합니다. hook 설치는 [Lefthook](lefthook.md), 문서 편집 연동은 [Front Matter CMS](front-matter-cms.md)의 별도 범위입니다.
- model/runtime 평가를 실행한다면 [Promptfoo](promptfoo.md)의 pin·데이터·모델 조건을 먼저 확인합니다.

Git·GitHub CLI·Shell은 호스트가 관리하는 호환 가능한 설치본을 사용하며 이 프로젝트의 bootstrap이 전역 설치·설정을 바꾸지 않습니다. 협업·권한 정책은 [VCS / Git](../development/vcs-git.md)과 [GitHub](../development/github.md)가 맡습니다. 재사용할 외부 명세·공식 문서 탐색은 [Tooling References](../development/tooling/README.md)에 둡니다.
