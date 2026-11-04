---
title: Rulesync
description: 이 프로젝트의 Rulesync 설정·버전 선택, 자산 revision과 projection·설치의 예외를 확인할 때 사용합니다.
---

# Rulesync

Rulesync는 선택한 작성 원본에서 벤더별 Agent Asset을 생성하고 외부 Rulesync dependency를 관리합니다. root [`rulesync.jsonc`](../../rulesync.jsonc)와 [`rulesync.lock`](../../rulesync.lock)은 이 저장소의 자체 사용, [`src/rulesync/rulesync.jsonc`](../../src/rulesync/rulesync.jsonc)는 재사용 라이브러리의 별도 workspace를 설정합니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 공식 schema·target adapter를 사용하고 최신 안정 릴리스를 우선 검토합니다. CLI는 [`mise.toml`](../../mise.toml)의 exact pin으로 실행하며 갱신 시 config·lock schema와 생성 결과의 호환성을 검증합니다.

- 저장소 전용 schema나 수동 projection을 만들지 않습니다. `targets`·feature와 source 위치는 각 workspace와 asset의 native 선언을 따릅니다.
- CLI 버전과 외부 자산 revision은 별개입니다. 잠긴 dependency 재현에는 `rulesync install --frozen`을 사용하며 단순 설치·transport 정리를 이유로 upstream revision을 갱신하지 않습니다.
- **dependency 설치와 projection은 core bootstrap에서 제외**합니다. source와 출력 대상을 확인하고 별도 승인 후 설치·preview·생성을 수행합니다.
- root dependency는 GitHub transport를 사용합니다. 필요한 인증은 설치 프로세스에만 전달하고 token을 config·로그에 남기지 않습니다. Git 전역 설정과 로컬 override를 임의로 바꾸지 않습니다.
- 문서 조회도 기존 설치본의 `rulesync docs`를 우선합니다. 프로젝트 실행을 `npx rulesync@latest`로 대체하지 않습니다.

버전 갱신 시 `mise run rulesync-doctor`, `mise run rulesync-preview`, `mise run rulesync-validate`와 관련 projection diff를 확인합니다. structural validation 통과를 runtime 의미의 동등성이나 검토 승인으로 해석하지 않습니다.

## 설치와 lock 이전

Root dependency 설치는 공식 `rulesync install --frozen`을 사용합니다. GitHub transport의 인증은 Git credential helper 대신 설치 프로세스의 `GITHUB_TOKEN` 또는 `GH_TOKEN`으로 전달합니다. 기존 환경은 실행 후 복원하고, Git clone·줄바꿈 보정 wrapper로 대체하지 않습니다. PC별 PATH 경계는 [mise](mise.md#shared-and-local-environment)를 따릅니다.

Transport나 lock schema를 이전할 때 config와 lock의 source 표기를 맞추되 `install --update`로 dependency revision을 갱신하지 않습니다. 공식 CLI의 plain `rulesync install`로 기존 locked ref의 entry를 이전하고, integrity가 바뀌면 같은 revision의 전체 파일 목록·바이트가 일치하는지 확인합니다. 이후 새 설치와 재실행에서 `install --frozen` 성공과 lock 불변을 검증합니다. Git에서 제외된 `rulesync.local.jsonc`에 이전 transport·URL만 중복한 override가 있으면 해당 항목만 검토하고 다른 로컬 설정은 보존합니다.

## 자산별 target 정책

- Library [`src/rulesync/rulesync.jsonc`](../../src/rulesync/rulesync.jsonc)는 유지하는 vendor support ceiling입니다. 실제 지원 여부는 개별 자산이 소유하며 workspace target만으로 모든 자산의 지원을 추정하지 않습니다.
- 재사용 Rule·Skill·Subagent·Command는 실제로 의미 있게 projection할 수 있는 `targets`를 명시합니다. 생략이나 `targets: ["*"]`에 의존하지 않으며 source framework·runtime이 필요한 자산 유형과 의미를 지원하는 target만 선언합니다.
- `agentsskills`는 vendor support ceiling에 포함하지 않습니다. Root self-consumer·ChatGPT compatibility처럼 실제 내부 consumer가 필요한 Skill에만 internal projection target으로 사용하며, Agent Skills 생태계 전체의 지원을 뜻하지 않습니다.

## 권장 버전 정책

**Minor**(현재 범위 전환 후보 `43`)를 권장합니다. 실제 CLI 버전은 [`mise.toml`](../../mise.toml)의 exact pin을 따르며, 범위 추적은 bootstrap 호환성 검증 후 별도로 도입합니다. 향후 Major 전환에서는 config·lock schema와 projection 결과를 검증하고, 같은 Major 내 갱신에도 `doctor`·`preview`·`validate`와 생성 diff를 확인합니다. CLI 범위와 외부 Agent Asset revision 잠금은 독립적으로 관리합니다.

## 상세 경계와 공식 문서

[Rulesync 참조 안내](../development/tooling/rulesync.md)는 저장소에서 사용하는 공식 Skill과 upstream 문서로 안내합니다. 이 문서는 프로젝트의 설정·버전 선택과 운영 예외만 설명합니다.

- [Official documentation](https://rulesync.dyoshikawa.com/)
- [Releases](https://github.com/dyoshikawa/rulesync/releases)
