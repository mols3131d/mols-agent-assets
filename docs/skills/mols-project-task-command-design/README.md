---
description: 서로 다른 기술 스택에서 프로젝트의 공유 명령 인터페이스를 설계하는 Skill의 이식성, 책임 경계와 리뷰 사례를 유지보수할 때 사용합니다.
---

# Project Task/Command Design — Maintainer Guide

실행·선택 계약은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-project-task-command-design/SKILL.md)가 소유한다. 이 문서는 다른 프로젝트와 런타임으로 옮겨도 보존해야 하는 설계 의도와 평가 경계만 기록한다.

## 범용성 기준

- **소비 프로젝트 우선:** 저장소·언어·모노레포 여부·운영체제·CI 서비스·task runner를 미리 지정하지 않는다. 환경에 이미 존재하는 source와 native 기능을 검토한다.
- **도메인 분리:** 공개 프로젝트 명령의 이름·인수·중복 호출·진입점은 이 Skill이 설계한다. 설치와 의존성 갱신의 안전 정책, CI admission 기준, 제품 코드 구조는 각각 실제 프로젝트의 다른 owner에 남긴다.
- **명령 유지 가치:** wrapper 제거만을 최적화로 오해하지 않는다. 안정된 이름, 발견 가능성, 온보딩, 빠른 로컬 피드백, 도구 교체 시 호출자 안정성도 task의 유효한 계약이다.
- **하나의 표면, 여러 구현:** CLI 서브커맨드 통합은 내부 코드를 한 파일로 합치라는 뜻이 아니다. 읽기 전용·쓰기·배포·비용 경계를 구현에서도 보존한다.
- **근거 한정:** 소스 확인과 정적 시나리오 리뷰를 다른 플랫폼·실제 CLI 실행·모델 Skill activation의 검증으로 확대하지 않는다.

## 교차 프로젝트 검토 사례

| 소비 환경 | 요청 | 합리적인 판단 |
| --- | --- | --- |
| Make 기반 C 프로젝트 | `make test`는 한 줄의 `ctest` 호출 | 팀의 공식 검증 계약이면 유지, 단 길이로 판단하지 않음 |
| Node 다중 패키지 workspace | 거의 동일한 package scripts가 필터만 다름 | workspace filter·인수 전달을 활용하되 패키지별 작업 차이는 보존 |
| Gradle 기반 Java 프로젝트 | CI용 `check` wrapper와 Gradle task 중복 | Gradle native lifecycle·캐시·daemon·출력 및 CI 호출자 차이를 검토 |
| Python CLI 서비스 | `generate`와 `verify`가 같은 스크립트의 플래그를 공유 | subcommand 통합을 검토하되 검증은 읽기 전용·생성만 write |
| 여러 OS를 지원하는 CLI | POSIX shell wrapper를 제거하고 native runner 사용 | PowerShell·Windows 인수·환경·작업 디렉터리 동등성 확인 전 단정 금지 |
| Bazel 모노레포 | 수백 개 세부 target을 한 상위 명령으로 묶으려 함 | 탐색 편의성과 cache·증분·target 범위를 함께 고려해 선택 |
| 임의의 프로젝트 | `ci` alias가 checkout·secret·배포도 실행 | 검증과 변경·원격 부작용을 별도 명령으로 분리 |
| 도구가 없는 프로젝트 | 명령 설계를 요청했으나 manifest 미제공 | 설치/전환을 강제하지 않고 필요한 source와 가정 명시 |

**근접 비적용:** 개인 할 일 정렬, 에이전트 작업 스케줄링, 단일 라이브러리 버전 문의, CI gate의 승인 정책만 변경하는 요청, 기존 명령 사용법 질문. `task`라는 문자열이 포함됐다는 사실만으로 선택하지 않는다.

## 검토 방법

대상 프로젝트의 **목표 → 명령·소비자 그래프 → 가능한 최소 변경 → 호출 계약 → 검증 범위**를 각 사례에 대입해, 특정 도구가 없어도 유효한 판단을 제시할 수 있는지 검토한다. 모든 사례를 자동으로 실행하지 않으며, 이 표는 정적 기대 행동이지 통과한 runtime benchmark가 아니다. Routing 성능은 실제 모델·호스트에서 별도로 평가해야 한다.
