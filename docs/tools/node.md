---
title: Node.js and npm
description: Node.js·npm의 LTS 버전 선택, mise 관리 npm CLI와 평가 실행의 호환성·잠금 예외를 확인할 때 사용합니다.
---

# Node.js and npm

Node.js는 npm CLI와 평가 runner의 실행환경입니다. Node와 관리형 npm CLI의 버전은 [`mise.toml`](../../mise.toml)과 [`mise.lock`](../../mise.lock), repository 명령은 [`package.json`](../../package.json)이 소유합니다.

## 기본 설정과 예외

[SemVer 선택지](README.md#semver-버전-선택지)를 기본으로 하고, Node가 공식적으로 제공하는 LTS는 필요할 때 추가하는 지원 수명 조건으로 봅니다. 현재 프로젝트는 지원 중인 LTS Major의 검증된 버전을 사용하지만, 최신 LTS Major로의 자동 전환까지 허용하는 것은 아닙니다. npm은 Node가 제공하는 것을 사용하며 별도 전역 npm 최신화를 기본 절차로 두지 않습니다.

- Node는 검토한 LTS 라인의 exact pin을 사용합니다. `setup`과 현재 `update`는 LTS 라인을 재선택하지 않습니다. 새 Active LTS가 나와도 지원 중인 기존 라인을 즉시 폐기하지 않고 npm CLI·평가 runner의 호환성을 검증한 뒤 전환합니다.
- Biome·Rulesync·skills CLI는 mise의 npm backend가 관리합니다. 프로젝트에 별도 `npm install`로 같은 CLI를 중복 관리하지 않습니다.
- bootstrap의 npm 실행은 잠근 Node와 설치 package identity·경로를 검증합니다. Windows `.cmd` shim과 호스트 PATH의 동명 CLI로 묵시적으로 대체하지 않습니다.
- [Promptfoo](promptfoo.md)는 별도의 runner pin과 최소 Node 요구조건을 갖습니다. mise의 npm CLI lock이나 `package.json`만으로 Promptfoo 전이 의존성까지 잠겼다고 주장하지 않습니다.

## 선택적 LTS 필터

LTS는 SemVer의 Exact·Patch·Minor·전체 Major 선택을 대체하지 않습니다. 공식 지원 수명과 결합할 때 다음 중 하나를 명시적으로 택합니다.

- **미적용:** SemVer 허용 범위만 사용합니다. 단, 유지보수·보안 지원 상태를 별도로 확인합니다.
- **LTS Major 유지(기본 제안):** 예를 들어 `node = "24"`로 24.x 범위 안에서 갱신합니다. 공식 LTS 지원 종료 전에 새 Major 전환을 검토하며, 24.x가 끝까지 LTS라는 의미는 아닙니다.
- **최신 LTS 추적(선택 사항):** mise의 `node = "lts"`는 lock 갱신 시 다른 Major를 선택할 수 있습니다. Node·npm CLI·Promptfoo 호환성을 검증할 수 있는 운영에서만 사용합니다. `lts/krypton`처럼 특정 LTS 라인을 지정하는 native alias도 사용할 수 있습니다.

Node.js는 26까지 짝수 Major 중심의 LTS 정책이었으나, **27부터 연간 릴리스로 전환하며 각 Major가 LTS 단계로 들어갈 예정**입니다. 따라서 짝수 Major라는 규칙만으로 LTS를 판정하지 않습니다. [공식 지원 일정](https://nodejs.org/en/about/previous-releases)과 [mise Node 버전 요청](https://mise.jdx.dev/lang/node.html)을 확인합니다.

현재 `mise.toml`은 exact pin이며 이 항목들은 **추후 선택 가능한 방식**입니다. 범위·alias 선언만 바꾸지 말고 bootstrap의 exact pin 제약과 `mise.lock` 갱신 경로를 함께 변경해야 합니다.

버전 갱신 시 관리형 npm CLI 3종과 평가 runner의 실행을 확인합니다. pin 변경 없이 단순히 `npx ...@latest`를 기존 task의 대체 경로로 쓰지 않습니다.

## Official Sources

- [Node.js releases](https://nodejs.org/en/about/previous-releases)
- [npm documentation](https://docs.npmjs.com/)
- [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
