---
title: Lefthook
description: Lefthook의 Git hook 설정, 별도 설치와 공유 hooksPath 보호, 자동 포맷·stage 예외를 확인할 때 사용합니다.
---

# Lefthook

Lefthook은 로컬 Git hook의 명령 실행을 관리합니다. hook 구성은 [`lefthook.yml`](../../lefthook.yml), 도구 버전은 [`mise.toml`](../../mise.toml)과 [`mise.lock`](../../mise.lock)이 소유합니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 native hook 기능과 최신 안정 버전을 우선 검토하고, 실제 실행은 검증한 exact pin을 사용합니다. 새로운 호환성 제약을 임의로 만들지 않으며 갱신할 때 기존 hook 명령을 확인합니다.

- `no_tty: true`로 비대화형 실행을 사용합니다. 실행할 Python group과 `--locked`는 각 hook 명령에 명시돼 있습니다.
- pre-commit은 staged 입력에 대한 generated artifact 동기화를 실행합니다. formatter를 자동 실행하거나 일반 파일을 자동 stage하는 경로로 사용하지 않습니다.
- commit-msg는 저장소 commit message validator, pre-push는 deterministic tests를 실행합니다. 구체적인 명령은 설정 파일을 따릅니다.
- **hook 설치는 선택 사항**입니다. core bootstrap은 `lefthook install`을 실행하지 않습니다. 설치 전에 공유 `core.hooksPath`와 기존 hook을 확인하고 별도 승인을 받습니다.

hook이 설치됐거나 통과했다는 사실로 remote write와 PR의 검증을 대신하지 않습니다. [CI](../development/ci.md)의 admission 경계와 [VCS / Git](../development/vcs-git.md)의 사용자 작업 보호를 유지합니다.

## 권장 버전 정책

**Minor**(mise 요청 `2`)를 권장합니다. 최초 범위 전환과 이후 lock 갱신 시 `lefthook validate`, hook 명령·staged 파일 처리 동작을 확인합니다. 도구 버전 갱신은 Git hook을 설치하거나 사용자 `core.hooksPath`를 변경할 권한이 아닙니다.

## Official Sources

- [Configuration](https://lefthook.dev/configuration/)
- [Install command](https://lefthook.dev/usage/commands/install/)
