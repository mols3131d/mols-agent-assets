---
name: mols-project-task-command-design
description: >-
  Design, review, or refactor a project's shared developer command interface:
  build, test, check, generate, or release commands exposed through task runners,
  package scripts, build targets, and CLIs. Use to decide which commands to
  keep, expose, parameterize, combine, split, or remove while preserving callers
  and execution semantics. Not for personal to-do tasks, agent job orchestration,
  CI admission policies, dependency upgrades alone, or single-command usage help.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Project Task/Command Design

프로젝트가 **개발자·에이전트·자동화에 제공하는 명령 인터페이스**를 설계하고 개선한다. 여기서 `task`는 빌드/명령 실행기의 항목이며, 개인 할 일이나 에이전트 작업 분해를 뜻하지 않는다. 언어, 저장소 구조, 실행기와 특정 도구의 존재를 가정하지 않는다.

## 핵심 판단

- **명령의 가치와 길이는 별개다.** 한 줄이라도 팀이 기억하는 진입점, 발견 가능성, 호출 API 안정성, 공통 환경·실패 판정을 제공하면 유효하다. 여러 줄이어도 중복 호출만 반복하면 통합 후보가 된다.
- **작은 공개 인터페이스와 단순한 구현 계층을 구별한다.** 사용자에게 안정된 이름이 필요하면 내부 구현은 native CLI로 대체하더라도 명령은 남길 수 있다. 실행기 설정, 언어 CLI, 프로젝트 전용 로직 사이에 의미 없는 중계를 추가하지 않는다.
- **네이티브 메커니즘을 우선 검토한다.** 인수 전달, 설정 선택, 작업 디렉터리, 의존 작업, lock·cache·diagnostics를 기존 도구가 지원하는지 확인한다. 다만 native 직접 호출이 항상 사용성·호환성에 더 좋은 것은 아니다.
- **동작과 영향 범위를 섞지 않는다.** 조회·검증과 생성·설치·배포는 수정 권한과 실패 의미가 다르다. 하나의 CLI로 묶더라도 명시적 하위 명령과 안전한 기본값을 사용하고 읽기 전용 명령에서 쓰기를 유발하지 않는다.
- **계약은 대상 프로젝트가 소유한다.** 기존 정책·실행기·문서·소비자를 확인한 뒤 판단한다. CI 게이트 정책, 환경 설치·업데이트 정책, 일반 제품 코드 리팩터링을 이 Skill이 새로 정의하지 않는다.

## 적용 방법

1. **목표와 사용자를 확인한다.** 명령을 줄이는 것이 목표인지, 로컬·CI 실행 일관성, 온보딩, ergonomics, 이식성, 실행 안전성이 목표인지 구분한다. 요청 범위 밖의 전체 빌드 체계를 재설계하지 않는다.
2. **실제 호출 그래프를 확인한다.** 해당 범위의 실행기 설정·CLI 엔트리포인트와 CI, Git hook, IDE, 문서, 자동화, 직접 호출자를 찾는다. 팀이 의존하는 공개 명령과 교체 가능한 내부 중계를 구분한다. 자료가 없으면 관찰된 부분과 추정을 분리한다.
3. **대안을 비교한다.** `유지 / 네이티브 직접 호출 / 인수·서브커맨드로 통합 / 의미에 따라 분리 / 제거` 중 가장 단순한 유효 구조를 선택한다. 각 대안의 사용성, 변경 비용, 중복 계층, 소비자 호환성을 함께 평가한다. 이름만 다른 작업인지, 별도 실패·권한·캐시 경계를 갖는 작업인지 확인한다.
4. **실행 계약을 보존한다.** 작업 디렉터리, PATH·env, 버전·의존성, 인수와 기본값, exit status, 로그·출력, shell·OS, 네트워크·비용, 파일·Git index·호스트 변경을 **영향받는 항목에 한해** 비교한다. 다른 환경에서 확인되지 않은 동작을 보편적이라고 가정하지 않는다.
5. **의도된 범위만 적용·검증한다.** 설계 요청이면 결정과 근거를, 수정 요청이면 기존 권한·개발 절차 아래 최소 변경과 호출자 이관을 제공한다. 검증은 설정·링크·호출 경로부터 변경된 의미에 필요한 테스트와 실제 실행까지 맞춘다. 수행하지 못한 검증은 명시한다.

## 결과와 경계

결론을 먼저 제시한다. 주요 명령의 **유지·통합·제거 이유**, 새 호출 방식, 영향받는 소비자와 의미 있는 호환성·부작용 위험, 수행한 검증과 남은 불확실성을 작업 크기에 맞춰 전달한다. 명령 사용법만 묻는 요청, 단일 버전 갱신, 일반 CI admission 설계 또는 개인 일정/task 관리만을 위해 이 Skill을 선택하지 않는다.
