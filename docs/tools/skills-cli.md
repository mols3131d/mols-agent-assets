---
title: skills CLI
description: skills CLI의 최신 안정 버전 선택과 외부 Skill revision 고정, native installer·HOME 설치 예외를 확인할 때 사용합니다.
---

# skills CLI

skills CLI는 외부 Agent Skill dependency를 선택·설치하는 도구입니다. CLI 버전은 [`mise.toml`](../../mise.toml), 사용할 source·revision은 [`skills-lock.json`](../../skills-lock.json)이 소유합니다. 두 버전은 서로 다른 갱신 대상입니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 최신 안정 CLI를 우선 검토하고, 채택한 버전은 exact pin으로 재현합니다. CLI가 최신이어도 외부 Skill을 매번 최신 revision으로 바꾸지는 않습니다.

- 잠긴 revision의 설치 상태를 맞출 때는 `mise run skills-sync`를 사용합니다. 이 경로는 lock을 읽으며 최신 revision resolver나 lock 갱신 명령이 아닙니다.
- source가 vendor별 payload나 runtime 자산을 따로 제공하면 generic installer로 같은 파일을 모든 vendor에 강제하지 않습니다. source-native installer가 소유하는 지원 범위와 설치 방식에 위임합니다.
- **HOME 설치는 별도 승인 대상**이며 core `setup`/`update`에 포함되지 않습니다. source cache와 사용자 수준 설치에 쓰기가 발생할 수 있고 lock에서 제거됐다고 설치본을 자동 삭제하지 않습니다.
- 설치된 copy·symlink·cache는 외부 dependency 상태입니다. 이 저장소가 작성 권한을 가진 source처럼 수정하지 않습니다.

CLI 갱신과 dependency 갱신을 구분해 diff를 검토하고, 필요한 vendor의 payload·지원 resource와 native installer 호환성을 확인합니다. 세부 설치 경계는 [skills CLI 통합 reference](../development/tooling/skills-cli.md), 원본·installer 선택은 [작성 원본과 권한](../development/source-authority.md)을 따릅니다.

## 권장 버전 정책

**Minor**(mise 요청 `1`)를 권장합니다. CLI만 갱신하며 `skills-lock.json`의 외부 Skill source·revision은 자동 승격하지 않습니다. 최초 전환과 이후 갱신에서 source-native installer의 옵션·payload와 HOME 쓰기 경계를 확인합니다.

## Official Sources

- [Repository and CLI usage](https://github.com/vercel-labs/skills)
