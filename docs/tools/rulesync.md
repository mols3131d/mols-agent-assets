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

버전 갱신 시 `npm run rulesync:doctor`, `npm run rulesync:preview`, `npm run rulesync:validate`와 관련 projection diff를 확인합니다. structural validation 통과를 runtime 의미의 동등성이나 검토 승인으로 해석하지 않습니다.

## 권장 버전 정책

**Minor**(초기 전환 후보 `43`)를 권장합니다. 현재 `40.x`에서 `43.x`로 옮기는 첫 단계는 Major 전환이므로 config·lock schema와 projection 결과를 별도로 검증해야 합니다. 이후 43.x 내 갱신에도 `doctor`·`preview`·`validate`와 생성 diff를 확인합니다. CLI 범위와 외부 Agent Asset revision 잠금은 독립적으로 관리합니다.

## 상세 경계와 공식 문서

[Rulesync 통합 reference](../development/tooling/rulesync.md)는 workspace·target·source/derived 경계와 공식 문서 탐색을 맡습니다. 이 문서는 프로젝트의 설정·버전 선택과 운영 예외만 설명합니다.

- [Official documentation](https://rulesync.dyoshikawa.com/)
- [Releases](https://github.com/dyoshikawa/rulesync/releases)
