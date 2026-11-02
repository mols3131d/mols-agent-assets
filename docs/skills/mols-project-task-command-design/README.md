---
description: 프로젝트 개발·검증·자동화 명령의 공개 진입점을 설계하는 Skill의 이식성과 책임 경계, 주요 리뷰 사례를 유지보수할 때 사용합니다.
---

# Project Task/Command Design — Maintainer Guide

실제 선택·행동 계약은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-project-task-command-design/SKILL.md)가 소유한다. 이 문서는 재사용 설계의 **보존해야 할 판단과 검토 사례**를 기록하며 실행 지침을 복제하지 않는다.

## Scope and portability

`task`는 프로젝트 runner의 명령이지 개인 To-do, GitHub Issue 또는 에이전트의 계획·작업 분해가 아니다. `mise`, `Make`, `just`, `npm scripts`, 언어별 CLI가 달라도 적용 가능해야 한다. 각 도구의 정확한 명령·지원 버전·OS semantics는 소비하는 프로젝트와 해당 upstream이 소유하며 이 Skill이 고정하지 않는다.

`mols-dev-env-bootstrap-design`은 설치·잠금·업데이트 안전성, `mols-ci-design`은 CI admission/증거 설계, `mols-code-comprehension-refactor`는 일반 코드 이해비용을 소유한다. 이 Skill은 그 정책을 바꾸지 않고, 해당 작업에 **진입하는 명령 인터페이스**의 중복·호환성을 다룬다.

## Durable decisions

- One-liner 자체는 삭제 신호가 아니다. 안정적 팀 호출점과 cwd, locked env, 실패 판정이 있으면 task를 유지한다.
- 명령 진입점 통합과 도메인 구현 파일 통합은 다른 결정이다. 읽기 전용 검사와 쓰기·staging의 경계를 보존한다.
- Native 도구 옵션과 버전을 확인한 뒤에만 자체 wrapper 제거를 제안한다. 기존 CI·hook·IDE·문서 호출자는 계약의 일부다.
- 새로운 추상화·스크립트·참조 파일의 비용이 절감되는 호출 계층보다 크면 추가하지 않는다. 실제 프로젝트 변경은 별도 실행 권한과 검증에 따른다.

## Review cases

| Scenario | Expected decision |
| --- | --- |
| `mise run test`가 단 한 줄이지만 잠금/group을 지정 | 단순 줄 수로 제거하지 않음 |
| `mise run outdated`가 native 조회와 완전히 동일 | 소비자·독립 정책이 없으면 직접 호출 |
| suite별 고정 npm/mise alias 다수 | config/필터 인수로 통합하되 cache·write·원격 비용 보존 |
| `generated sync`와 `validate`를 한 CLI로 통합 | sync의 생성·staging과 검증의 읽기 전용 계약 유지 |
| cwd만 설정하는 Python wrapper | runner native cwd·OS 실행 호환성을 검토 |
| 구버전 runner에 새 Doctor subcommand 사용 제안 | 실제 지원 버전 확인 후 대안 또는 미도입 |
| 할 일 task 정리, agent orchestration, CI gate 자체 설계 | 근접 비적용 사례로 구별 |

각 사례는 **선택 경계와 의사결정 품질을 리뷰하기 위한 정적 시나리오**다. 실제 Skill 자동 선택이나 런타임 수행을 시험한 결과가 아니며, 해당 성능을 입증하려면 별도 routing/behavior eval이 필요하다. 정식 Skill을 관리할 때 소스·파생 route 정합성과 Rulesync 구조 검증도 함께 확인한다.
