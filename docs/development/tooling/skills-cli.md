---
title: skills CLI
description: 외부 Skill을 dependency로 사용할 때 upstream skills CLI, root skills-lock.json, 저장소 native installer adapter의 책임과 설치 부작용을 구분할 때 사용합니다.
---

# skills CLI

[skills CLI](https://github.com/vercel-labs/skills)는 외부 Agent Skill을 찾고 설치하며 dependency를 관리하는 upstream 도구입니다. 그러나 **이 저장소의 `mise run skills-sync`는 skills CLI 자체의 동기화 명령이 아닙니다.** 잠긴 의존성 정보를 읽어 source-native installer에 설치를 위임하는 별도 wrapper입니다.

어떤 Skill을 외부 dependency로 유지할지, Rulesync와 skills CLI 중 어떤 intake 경로를 선택할지는 [작성 원본과 권한](../source-authority.md)이 결정합니다. 도구 버전과 HOME 설치 승인 등 프로젝트 운영 예외는 [skills CLI 운영 안내](../../tools/skills-cli.md)가 소유합니다.

## 통합 구성

| 구성요소 | 소유하는 정보·동작 |
| --- | --- |
| Root [`skills-lock.json`](../../../skills-lock.json) | 사용할 외부 Skill의 source와 고정 `ref`. Upstream lock 형식을 유지하며 로컬 전용 target 필드를 추가하지 않음 |
| [`mise.toml`](../../../mise.toml) | 사용할 skills CLI 버전과 `skills-sync` 실행 진입점 |
| [`scripts/agent_assets/skills_sync.py`](../../../scripts/agent_assets/skills_sync.py) | Lock을 읽어 설치 계획을 만들고, 알려진 source의 native installer에 전달하는 제한된 adapter |
| 외부 source의 installer | 해당 source가 지원하는 vendor·payload·resource·설치 방식 |

이 구분에서 **CLI 버전 갱신**, **외부 Skill revision 갱신**, **현재 설치본 동기화**는 서로 다른 작업입니다. `skills-sync`는 최신 revision resolver가 아니고 `skills-lock.json`을 수정하지 않습니다. 반대로 lock 파일이 존재한다고 설치본이 그 내용과 일치하는 것도 아닙니다.

현재 adapter와 지원 source 목록은 `skills_sync.py`의 `NATIVE_ADAPTERS`가 소유합니다. 특정 vendor가 실제로 지원되는지, 추가 resource가 어디에 설치되는지는 그 source의 installer 문서를 우선합니다. Generic `skills add --agent ...`가 native installer와 같은 payload를 설치한다고 가정하지 않습니다.

## Dependency를 사용할 때

1. **설치 경로 선택:** 원본 구조를 Rulesync로 충실히 보존할 수 있는지, source-native installer가 필요한지 [작성 원본과 권한](../source-authority.md)에 따라 결정합니다.
1. **Lock 갱신:** 신규 dependency 도입이나 upstream revision 채택은 별도의 의도적 변경으로 처리합니다. Skills CLI의 현재 명령·lock semantics는 [공식 Commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)를 확인하고, 설치·lock diff와 실제 실행 부작용을 검토합니다.
1. **Adapter 확인:** `skills-sync` 경로를 사용할 dependency라면 현재 wrapper가 source와 Skill을 지원하는지 확인합니다. 모르는 source는 조용히 일반 설치로 fallback하지 않고 실패합니다.
1. **설치 상태 동기화:** 승인 후 `mise run skills-sync`를 사용합니다. Wrapper의 `--dry-run`은 source·revision·installer 계획만 출력하며 native installer가 실제로 쓸 모든 파일을 미리 검증하지는 않습니다.

Lock에서 제거된 dependency의 사용자 수준 설치본은 자동 삭제되지 않습니다. 제거는 해당 upstream의 uninstall 절차와 사용자 승인에 따릅니다. Copy·symlink·source cache·HOME의 vendor별 설치본은 **외부 의존성 상태**이지 이 저장소가 편집하는 작성 원본이 아닙니다.

### 재현성과 부작용

`skills-sync`는 lock의 `ref`를 checkout하고 외부 installer를 실행합니다. 현재 wrapper는 lock의 `computedHash`를 다시 계산·검증하지 않으므로 **ref가 고정됐다는 사실만으로 파일 내용의 무결성 검증이나 완전한 재현성을 주장하지 않습니다.** Upstream ref의 변경 가능성과 installer 부작용을 따로 고려해야 합니다.

실행 중에는 source cache와 사용자 수준 vendor 설치가 변경될 수 있습니다. 따라서 core `mise run setup`·`mise run update`에서 자동 실행하지 않고, 명시적 승인 후 호출합니다. `skills-sync`를 skills CLI의 `experimental_install` 또는 `experimental_sync`와 같은 명령으로 취급하지 않습니다. CLI와 원본 installer의 지원 범위는 각각 현재 공식 문서에서 확인합니다.

## 공식 문서와 연결

- [skills CLI Repository](https://github.com/vercel-labs/skills) — 설치 방식과 지원 범위의 진입점
- [skills CLI Commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) — `add`·`use`·`check`·`update`·`experimental_install` 등 CLI 동작
- [Rulesync 통합 안내](rulesync.md) — Rulesync dependency 및 작성 원본 intake 경로
- [프로젝트 skills CLI 운영 안내](../../tools/skills-cli.md) — 버전·설치 승인·운영 예외
