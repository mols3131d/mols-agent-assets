---
title: Node.js and npm
description: Node.js·npm의 LTS 버전 선택, mise 관리 npm CLI와 평가 실행의 호환성·잠금 예외를 확인할 때 사용합니다.
---

# Node.js and npm

Node.js는 npm CLI와 평가 runner의 실행환경입니다. Node와 관리형 npm CLI의 버전은 [`mise.toml`](../../mise.toml)과 [`mise.lock`](../../mise.lock), repository 명령은 [`package.json`](../../package.json)이 소유합니다.

## 기본 설정과 예외

[mise 버전 선택지](README.md#mise-버전-선택지) 중 Node의 공식 LTS alias를 우선하는 방안을 제안합니다. 현재 exact pin은 유지하며 실제 전환 전 호환성을 검증합니다. npm은 Node가 제공하는 것을 사용하며 별도 전역 npm 최신화를 기본 절차로 두지 않습니다.

- Node는 검토한 LTS 라인의 exact pin을 사용합니다. `setup`과 현재 `update`는 LTS 라인을 재선택하지 않습니다. 새 Active LTS가 나와도 지원 중인 기존 라인을 즉시 폐기하지 않고 npm CLI·평가 runner의 호환성을 검증한 뒤 전환합니다.
- Biome·Rulesync·skills CLI는 mise의 npm backend가 관리합니다. 프로젝트에 별도 `npm install`로 같은 CLI를 중복 관리하지 않습니다.
- bootstrap의 npm 실행은 잠근 Node와 설치 package identity·경로를 검증합니다. Windows `.cmd` shim과 호스트 PATH의 동명 CLI로 묵시적으로 대체하지 않습니다.
- [Promptfoo](promptfoo.md)는 별도의 runner pin과 최소 Node 요구조건을 갖습니다. mise의 npm CLI lock이나 `package.json`만으로 Promptfoo 전이 의존성까지 잠겼다고 주장하지 않습니다.

## 버전 정책: LTS

**추천: LTS** (mise의 `node = "lts"`). mise가 제공하는 native alias를 사용해 lock 갱신 시 지원 중인 LTS 버전을 선택합니다. 새로운 LTS Major로 전환될 수 있으므로 npm CLI 3종과 Promptfoo의 실행 호환성을 확인한 뒤 lock diff를 승인합니다.

Node Major를 자동으로 전환하지 않으려면 `node = "24"`처럼 **Minor 추적**을 대신 선택할 수 있습니다. 이 표현은 24.x 범위만 제한하며 LTS 상태를 강제하지 않습니다. mise의 LTS alias와 SemVer prefix를 임의 교집합으로 결합하는 별도 정책 엔진은 만들지 않습니다.

현재는 `mise.toml`에 exact pin을 사용하며 bootstrap도 이를 요구합니다. 추천 정책은 추후 구현·검증한 후 활성화합니다.

버전 갱신 시 관리형 npm CLI 3종과 평가 runner의 실행을 확인합니다. pin 변경 없이 단순히 `npx ...@latest`를 기존 task의 대체 경로로 쓰지 않습니다.

## Official Sources

- [Node.js releases](https://nodejs.org/en/about/previous-releases)
- [npm documentation](https://docs.npmjs.com/)
- [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
