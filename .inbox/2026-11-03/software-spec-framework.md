---
description: 외부 소프트웨어 프로젝트용 단일 Skill Spec Framework의 초기 요구사항, 기본 8단계 워크플로와 리뷰 복귀 설계 및 구현 전 미결정 사항을 정리합니다.
---

# Software Spec Framework — Design Preparation

## Objective

외부 프로젝트에서 재사용할 **소프트웨어 개발 전용 Spec-driven Development Framework**를 설계한다. 첫 번째 목표는 CLI 의존 없이 ChatGPT Chat 수준의 도구로도 명세 기반 작업을 진행할 수 있게 하는 것이다. 패키지의 배포·관리 단위는 **하나의 Agent Skill**이며, 필요하면 같은 패키지 안에 문서·템플릿·스크립트·검증 코드를 둔다.

이 문서는 작업 중인 설계 근거이며 실행 정본이 아니다. 장기 보존할 설계 의도와 유지보수 경계는 [Maintainer Guide](../../docs/skills/mols-software-spec/README.md)에 분리했다. 이번 작업은 **문서·PR 준비까지만** 포함하며 Skill·CLI·스크립트를 구현하거나 설치하지 않는다.

## Agreed Design Direction

| 구분 | 방향 |
| --- | --- |
| 제품 범위 | 소프트웨어 변경의 명세·테스트·코드 구현 및 리뷰 기반 반복 |
| 배포 단위 | 단일 Skill 패키지: `SKILL.md`, 필요시 `references/`, `assets/`, `scripts/` |
| Artifact definitions | 종류·의미·형식·검증 기준을 정의하고 순서는 모름 |
| Workflow definitions | 단계·순서·전환·재진입·선택적 단계/재사용을 소유 |
| Runtime | 실제 가용 도구·권한·원본 상태를 확인해 실행하고 없는 기능은 꾸미지 않음 |
| Script | 결정적인 초기화·검사·상태 처리; CLI 설치를 필수로 하지 않음 |
| 완료 판정 | 실증된 결과로만 통과; 실패 시 원인에 맞는 단계로 복귀 또는 차단·인계 |

### Default Eight-Step Workflow

```text
1. Proposal (제안서)
2. Research (조사 보고서)
3. Plan (계획서)
4. Specification (스펙)
5. Test Design (테스트 설계)
6. Test Implementation (테스트 구현)
7. Code Implementation (코드 구현)
8. Review (검토)
```

1~5는 문서 산출물을 중심으로 한다. 6과 7은 실제 테스트·제품 코드이며, 별도 문서 파일이 반드시 필요한 것은 아니다. Review는 단계이자 결과 판정으로, 리뷰 기록이 별도 문서 종류인지까지 지금 확정하지 않는다. 단계와 산출물은 1:1 관계를 강제하지 않는다.

기본 순서에서 테스트를 먼저 구현하므로 **코드 구현 전 테스트 실패는 예상 가능한 중간 상태**다. 단계별 가벼운 확인은 허용하지만 마지막 Review를 생략하거나 통과한 것으로 간주해서는 안 된다. 워크플로를 바꾸더라도 Artifact 정의는 재사용되어야 한다.

### Review-Driven Rework

| 발견한 결함 | 우선 검토할 복귀 단계 |
| --- | --- |
| 잘못된 목표·범위 | Proposal |
| 근거 부족·기술 가정 오류 | Research |
| 실행 전략·의존 관계 오류 | Plan |
| 요구사항·수락 조건 오류 | Specification |
| 누락된 테스트 시나리오 | Test Design |
| 오류 있는 테스트 코드 | Test Implementation |
| 제품 구현 결함 | Code Implementation |

Review는 finding, 근거, 원인 후보, 영향받은 산출물과 복귀 제안을 남긴다. **Workflow가 유효한 복귀 단계와 재실행 범위를 결정**한다. 이전 단계부터 필요하다면 순서대로 다시 진행하되, 영향이 없는 산출물은 재사용한다. 복귀 이후에는 다시 Review로 수렴해야 한다. 원인을 특정하지 못하거나 실행 권한이 없으면 임의로 성공·완료 처리하지 않는다.

예시: 동시성 요구 누락 → Specification 수정 → 영향을 받는 Test Design / Test Implementation / Code Implementation만 재검증·수정 → Review. 테스트 assertion 자체가 잘못된 경우에는 Test Implementation부터 수정하고 제품 코드를 불필요하게 변경하지 않는다.

## Questions to Resolve Before Implementation

1. **Source and distribution:** 작성 원본을 Rulesync 표준 Skill 패키지 또는 벤더 네이티브 어느 쪽으로 관리할지, scripts/assets가 목표 런타임에 온전히 전달되는지 실증한다. `mols-software-spec`은 작업명이다.
2. **Artifact contract:** 문서별 최소 필드, 스키마·템플릿, 변경 ID, 파일 경로, 업데이트/중복/충돌 규칙을 정한다. 코드 산출물에는 경로·commit·테스트 참조 등 무엇을 기록할지 정한다.
3. **Workflow and state:** step 상태, 선행 조건, 순서 변경, 조건부 생략, 여러 finding의 복귀 대상 충돌, 중간 상태 저장 및 세션 재개 규칙을 정한다.
4. **Review semantics:** finding의 심각도·근거, 영향도 추적, 무효화·재검증, 완료·재작업·차단·인계의 기계 판독 형태를 정한다. 검토만으로 테스트 성공을 선언하지 않는다.
5. **Spec lifecycle:** 여러 변경에서의 장기 스펙 정본, 변경 명세와 코드 사이 추적, 동시 변경, 완료 후 정리·아카이브의 안전한 동작을 정한다.
6. **Runtime parity:** ChatGPT Chat의 원격 저장소 연결과 분석/스크립트 환경 간 경계를 확인하고, native/adapted/partial/blocked 판단과 실제 실행 증거를 정의한다.
7. **Termination:** review → rework 반복의 수렴·중단·인계 기준과 프로젝트 하네스·기존 개발 워크플로와의 충돌 해결을 정한다.

## Proposed Implementation Slices

1. Artifact 계약과 기본 Workflow 계약을 최소 예제로 정의하고, Review 복귀·영향 추적을 종이에 먼저 검증한다.
2. 단일 `SKILL.md`와 필요한 참조·템플릿만 작성한다. 기본 시나리오의 positive / negative / near-miss 활성화·절차를 평가한다.
3. 반복적이고 결정적인 연산만 `scripts/`로 구현하고 단위 테스트한다. 별도 CLI·서비스·여러 Skill은 실제 수요가 확인될 때만 도입한다.
4. 실제 외부 샘플 프로젝트에서 ChatGPT Chat 및 실행 가능한 코딩 에이전트의 동일 명세 처리, 리뷰 복귀, 새 세션 재개, 근거 기반 완료를 비교·검증한다.

## Acceptance for the Next Work

다음 구현 PR의 최소 수락 시나리오는 **제안서에서 시작해 Review까지 한 번 진행하고, Specification 결함을 발견해 해당 단계로 되돌아가 영향받은 테스트·구현을 다시 확인하는 흐름**이다. 필요한 검증기가 없는 Chat 환경에서는 수행 가능한 부분만 보고해야 한다. 테스트 실행이 없는데 통과했다고 표시하거나 실제 파일을 갱신하지 않았는데 완료했다고 표시하면 실패로 본다.

이번 문서 PR에서는 범위·책임·미결정 사항을 정확히 구분하고, 향후 구현 작업을 위한 근거를 남기는 것으로 충분하다.
