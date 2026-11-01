---
title: Node.js and npm
description: Node.js·npm의 LTS 버전 선택, mise 관리 npm CLI와 평가 실행의 호환성·잠금 예외를 확인할 때 사용합니다.
---

# Node.js and npm

Node.js는 npm CLI와 평가 runner의 실행환경입니다. Node와 관리형 npm CLI의 버전은 [`mise.toml`](../../mise.toml)과 [`mise.lock`](../../mise.lock), repository 명령은 [`package.json`](../../package.json)이 소유합니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)의 최신 안정 선호에서 **공식 지원 중인 LTS 라인**을 우선합니다. 최신 Current나 새 major로 자동 승격하지 않고 consumer의 Node 요구조건과 실제 task를 확인합니다. npm은 Node가 제공하는 것을 사용하며 별도 전역 npm 최신화를 기본 절차로 두지 않습니다.

- Node는 검토한 LTS 라인의 exact pin을 사용합니다. `setup`과 현재 `update`는 LTS 라인을 재선택하지 않습니다. 새 Active LTS가 나와도 지원 중인 기존 라인을 즉시 폐기하지 않고 npm CLI·평가 runner의 호환성을 검증한 뒤 전환합니다.
- Biome·Rulesync·skills CLI는 mise의 npm backend가 관리합니다. 프로젝트에 별도 `npm install`로 같은 CLI를 중복 관리하지 않습니다.
- bootstrap의 npm 실행은 잠근 Node와 설치 package identity·경로를 검증합니다. Windows `.cmd` shim과 호스트 PATH의 동명 CLI로 묵시적으로 대체하지 않습니다.
- [Promptfoo](promptfoo.md)는 별도의 runner pin과 최소 Node 요구조건을 갖습니다. mise의 npm CLI lock이나 `package.json`만으로 Promptfoo 전이 의존성까지 잠겼다고 주장하지 않습니다.

버전 갱신 시 관리형 npm CLI 3종과 평가 runner의 실행을 확인합니다. pin 변경 없이 단순히 `npx ...@latest`를 기존 task의 대체 경로로 쓰지 않습니다.

## Official Sources

- [Node.js releases](https://nodejs.org/en/about/previous-releases)
- [npm documentation](https://docs.npmjs.com/)
- [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
