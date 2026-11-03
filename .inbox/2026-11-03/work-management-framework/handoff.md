---
description: 외부 재사용 작업 관리 프레임워크 Skill의 독립 구현 PR을 이어받을 때 목표, 범위, 선행 검토, 완료 기준을 확인합니다.
---

# Work Management Skill — Handoff

## Goal

외부 프로젝트의 **여러 작업을 발견·분해·선택·추적하고, 의존 관계·중단·재개·인계를 관리**하는 재사용 가능한 **단일 Agent Skill**을 설계·구현한다. ChatGPT Chat처럼 로컬 CLI가 없는 런타임도 지원 범위에 포함하되, 실제 연결·읽기·쓰기 권한을 확인하고 없는 기능을 실행했다고 표시하지 않는다.

**이 PR의 현재 상태는 설계·인계 자료만 있는 Draft**이다. Skill 작성 원본, 테스트, 스크립트, 동작 평가가 아직 없으며 개발 작업은 후속 수행자가 이 PR에서 계속한다. Spec/Test-driven Skill의 구현은 별도 PR #283의 책임이다.

## Scope and Non-goals

- 담당: 사용자가 요청한 작업 단위의 파악, 필요할 때 분해, 의존 관계·우선순위·ready/blocked 판정, 실제 진행 기록과 근거, 중단·재개·권한 제약 시 인계, 여러 작업 간 조정.
- 담당하지 않음: 스펙 본문·수락 조건·테스트 설계·코드 정합성의 정본 소유, 개발 방법론 강제, 모든 작업에서 새로운 추적 파일 생성, 자기만의 데이터베이스·서비스·전역 스케줄러 구축, 기존 task runner/build task 명령 관리.
- 기존 GitHub Issues/Projects, Beads, 기타 현장 도구를 **가능한 한 그대로 사용**하고, 기존 owner가 없을 때만 최소한의 임시·영속 표현을 허용한다. 최초 실행 시 도구 설치나 외부 쓰기를 강제하지 않는다.
- 여러 프로젝트와 실행 환경에서 독립 실행되어야 하며, 동일 저장소의 다른 Skill/하네스나 PR #283을 숨은 필수 의존성으로 요구하지 않는다.

## Architecture Hypothesis — To Validate

**Work Item**을 추상적 작업 단위로 보고 기존 시스템의 Issue·Task·PR 또는 사용자가 정한 단위에 매핑한다. Skill은 작업 자료를 복제한 새 tracker가 아니라 선택·조정·재개에 필요한 판단과 연결만 제공한다.

| Concern | Owner |
| --- | --- |
| 작업 식별자, 상태, 우선순위, 의존성, assignee, 시간 계획 | 프로젝트가 이미 사용하는 작업 관리 시스템 |
| 작업 선택·분해·진행·인계의 에이전트 동작 | Work Management Skill |
| 연구→계획→실행→리뷰의 작업 내부 반복 방법 | 호출자/프로젝트의 실행 워크플로·에이전트 런타임 |
| 소프트웨어 수락 조건·테스트·구현 증거 | 프로젝트 코드·검증 도구 및 선택적인 Spec/Test-driven Skill |
| API·CLI의 의미와 권한 | 해당 도구와 실행 환경 |

GitHub Issue↔software change는 1:1 관계를 강제하지 않는다. 함께 사용할 때는 작업 ref, 관련 스펙 ref, 검증 링크만 교환하고 각자의 상태를 중복 기록하지 않는 방향을 우선 검토한다.

## First Decisions Before Coding

1. **Value test:** GitHub Issues, Beads 또는 현지 tracker의 기본 기능만으로 해결되지 않는 실제 실패 사례가 있는가? 없다면 더 작은 Skill/가이드 또는 구현 취소가 낫다.
2. **Activation:** 작업 관리 요청과 Spec/Test-driven 구현, 개인 할 일 관리, project task/build command 관리, 내부 RPI 반복 요청을 자연어 intent로 분리한다. 작은 단일 작업에는 불필요하게 개입하지 않는다.
3. **State:** 원본 시스템의 현재 상태가 정본이며, 스냅샷은 읽는 순간부터 stale할 수 있다. 재개 시 최신성·권한을 확인한다. 저장소에 임의로 `tasks.json` 등의 복제 정본을 만들지 않는다.
4. **Available actions:** ChatGPT Chat GitHub Plugin 등 실제 tool이 하위 이슈/의존 관계 생성까지 지원하는지 확인한다. 플랫폼 기능이 있어도 Plugin 액션이 없으면 '지원'으로 표시하지 않는다.
5. **Side-effect safety:** 외부 쓰기 전에 정확한 연결 계정·명의, 객체, 현재 ref, 권한, 사용자 승인 및 중복 생성 가능성을 확인한다. 읽기 전용 상태에서는 제안·인계까지 진행한다.
6. **Design exit:** 최소 책임·선택 기준·상태 계약·근거 수준·실제 eval 계획이 합의된 뒤 Skill source를 신설한다. 자체 scheduler/DB/MCP/CLI는 정당화 전 금지.

## Acceptance for Delivery

- 저장소의 단일 작성 원본 정책에 맞는 재사용 Skill 한 개와 필요한 만큼의 자료만 추가한다. 별도 maintainer 가이드에는 변하지 않는 설계 의도만 둔다.
- 최소 시나리오: (a) 기존 GitHub 이슈 5개에서 차단되지 않은 다음 작업 선택, (b) 큰 작업을 기존 원본 tracker 규칙으로 분해, (c) 중단·새 세션 재개 시 stale 상태를 재확인하고 인계, (d) 연결이 읽기 전용이거나 의존성 API가 없는 ChatGPT에서 가능한 기능만 수행, (e) 단일 스펙 변경 요청에는 과잉 활성화하지 않음.
- 비교 기준: 기존 도구 직접 사용 대비 추가 파일/메타데이터 수, 도구 호출·진입 절차, 잘못된 상태·순서 판정, 세션 재개 성공, 권한·계정 안전성. 실제 실행 근거 없는 '호환성 완료' 주장은 금지한다.
- 검증은 frontmatter/참조 경로 등의 deterministic validation, 책임·activation의 semantic review, 실제 runtime behavior eval을 서로 구분한다. 수행할 수 없는 테스트는 명시한다.
- 이번 handoff-only PR은 개발 완료가 아니다. 작업이 진행되면 PR 설명 및 수락 조건을 실제 구현 근거로 갱신한다.

## Start Here

1. 현재 PR base/head와 적용되는 `CHATBOT.md` → `AGENTS.md` → 저장소 자산 작업 워크플로를 확인한다.
2. [Design Context](design.md)와 공개 upstream 자료를 읽고, 작업 관리 Skill의 독립 책임을 작은 사례로 검증한다.
3. Task Skill 설계를 최적화한 뒤 `mols-agent-asset`의 design/review/validate/eval 방법과 저장소의 문서 생명주기를 따른다.
4. 기존 Spec Skill PR과는 소유권·참조만 조정하며, 그 브랜치의 구현 코드를 이 PR에 복사하지 않는다.
