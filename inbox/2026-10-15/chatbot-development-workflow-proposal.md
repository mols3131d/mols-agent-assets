---
description: 로컬 런타임 없이 GitHub Plugin과 서버 측 CI로 개발하는 챗봇의 반복 지시를 줄이기 위한 워크플로우, MVP, 검증 기준을 결정할 때 참고하는 제안서입니다.
---

# Chatbot Development Workflow 제안

> 상태: 제안 / 검토 대상 — 구현 또는 정책 확정이 아닙니다.

## 제안 요약

**기존 `mols-loops`를 새로 구현하지 않고, 챗봇에서 목표 지향적 개발 작업을 이어 주는 얇은 실행 레시피를 추가합니다.** 첫 검증 대상은 `PR to Ready`입니다. 사용자는 목표를 한 번 전달하고, 챗봇은 사용 가능한 GitHub 도구로 변경·리뷰·CI 확인·개선을 반복한 뒤 완료 또는 정확한 인계 상태를 보고합니다.

새 레시피가 소유할 것은 **실행 가능성 확인, GitHub 피드백 연계, 재개 경계**뿐입니다. RPI 단계, 저장소 정책, CI 판정, 리뷰 방법론, 권한은 기존 정본이 계속 소유합니다.

**결정 요청:** 아래의 MVP 범위와 성공 기준에 합의한 후 작은 챗봇 전용 실행 자산으로 시범 구현합니다. 이 문서만으로 실행 지침을 활성화하거나 자동 병합을 허가하지 않습니다.

## 해결할 문제와 전제

로컬 에이전트와 달리 이 제안의 챗봇은 작업 디렉터리, 터미널, 로컬 테스트 실행을 **전제할 수 없습니다**. GitHub Plugin/connector 수준에서 저장소를 읽고 원격 변경을 제안하며, 실행 가능한 검증은 주로 GitHub Actions가 제공합니다. 제품마다 도구의 종류와 쓰기 권한은 다릅니다.

현재 사용 경험의 문제는 단계별 지시를 반복한다는 점입니다.

```text
"PR 검토해" → "개선해" → "CI 확인해" → "실패 고쳐" → "다시 리뷰해"
```

목표는 이 절차를 하나의 장문 프롬프트로 고정하는 것이 아니라, **현재 상태와 관측된 증거를 보고 다음 유효한 행동을 선택**하게 하는 것입니다. 작업이 같은 대화에서 끝나지 않아도 이전 조사를 불필요하게 다시 반복하지 않아야 합니다.

## 기존 기반과 책임

| 영역 | 재사용할 정본 | 이번 제안의 경계 |
| --- | --- | --- |
| 챗봇 진입·라우팅 | [CHATBOT.md](../../CHATBOT.md), [repository route](../../.agents/route/ROUTE.md) | 새로운 정책 진입점이나 전체 자산 복제는 만들지 않음 |
| 실행 반복 | [mols-loops](../../src/rulesync/.rulesync/skills/mols-loops/SKILL.md) | Prepare/RPI/Review/Finalize, Scope와 종료 상태는 그대로 활용 |
| GitHub 대상 탐색 | [github-context](../../src/rulesync/.rulesync/skills/github-context/SKILL.md) | 최신 ref, 적용 지침, 권한과 도구 범위를 실행 전에 확인 |
| 브랜치·PR·승인 | [VCS](../../docs/development/vcs-git.md), [GitHub](../../docs/development/github.md) | 브랜치/PR/merge 정책을 재정의하지 않음 |
| 원격 검증 | [CI](../../docs/development/ci.md), [Branch Check](../../.github/workflows/branch-check.yml), [PR Gate](../../.github/workflows/pr-gate.yml) | CI 결과를 소비하며 테스트 실행이나 성공을 추측하지 않음 |
| 중단·재개 | [Durable Progress Handoff](../../catalog/patterns/workflow/durable-progress-handoff.md), [Artifact Inbox](../../catalog/patterns/workflow/artifact-inbox.md) | 이미 있는 PR/Issue/artifact를 우선 사용 |
| 챗봇 전용 차이 | [Chatbot Asset Surface](../../catalog/patterns/context-engineering/chatbot-asset-directory.md) | 필요한 delta만 향후 실행 자산으로 분리 |

이 저장소의 현재 `Branch Check`는 `main` 이외의 push에, `PR Gate`는 `main` 대상 PR 이벤트에 연결되어 있습니다. 이 두 workflow는 **검증 근거를 생산**하며 자동으로 원본을 수정하거나 LLM 개발 작업을 이어 실행하지 않습니다.

## 제안하는 실행 모델

```text
사용자 목표
  → bootstrap / github-context
  → 현재 작업과 사용 가능한 capability 확인
  → 기존 mols-loops의 Run
      → 필요한 GitHub read/write
      → branch/PR 이벤트에 따른 서버 측 CI
      → check·diff·review evidence 확인
      → 검증된 결함만 수정, 필요한 단계부터 반복
  → COMPLETE / HANDOFF / BLOCKED
```

### 1. 목표 지향적 호출

사용자가 작업 결과를 명확히 요청하면 해당 결과까지 수행하는 것을 기본으로 합니다. 예를 들어 “PR #N을 머지 가능하게 개선해”는 리뷰 한 번이나 수정 한 번으로 끝내지 않고, 목표 범위에서 필요한 수정과 검증까지 포함합니다.

이는 **반복 지시를 생략**하는 의미이지, 명시되지 않은 범위 확장이나 위험한 side effect를 승인하는 의미가 아닙니다. 새로운 연구·구현·리뷰 방법론을 추가하지 않고 `mols-loops`와 task-specific 자산을 조합합니다.

### 2. Capability와 Authority를 분리

시작할 때 대상 저장소/PR/ref와 **현재 실제 사용 가능한** GitHub read, file write, branch/PR mutation, check/log read, rerun 기능을 확인합니다. 지원 여부가 확인되지 않은 조작은 가능하다고 가정하지 않습니다.

- 도구가 허용하고 승인된 조작만 실행합니다.
- tool 성공, commit 생성, 테스트 성공, PR 승인과 merge 가능 상태를 구분합니다.
- 플랫폼이 강제하는 승인, 권한과 Ruleset을 프롬프트로 우회하지 않습니다.
- 자동 merge는 이 MVP의 범위가 아닙니다.

### 3. GitHub를 실행·검증 접점으로 활용

챗봇은 파일 편집이나 PR 갱신과 같은 GitHub 변경을 수행할 수 있지만 로컬 커맨드 실행을 전제하지 않습니다. GitHub Actions가 체크를 제공하면 **해당 commit/ref 및 PR merge candidate에 대응하는 결과**를 읽고 실패를 분류합니다.

- source/edit 문제: 수정할 수 있으면 좁은 범위로 고치고 다시 검증합니다.
- 일시적인 CI 문제: 근거가 있을 때만 적절한 재실행을 검토합니다.
- generator·formatter처럼 실행 환경이 필요한 문제: 저장소의 공식 복구 경로를 확인합니다. 해당 경로를 호출할 capability가 없으면 임의 수작업으로 동일성을 주장하지 않고 `BLOCKED` 또는 `HANDOFF`로 남깁니다.
- 체크가 미실행/진행 중/조회 불가: `PASS`로 보고하지 않습니다.

현재 대화에서 도구 호출을 계속할 수 있을 때만 확인·개선 루프를 진행합니다. **별도 스케줄러 없이 백그라운드 실행, 세션 종료 후 자동 재개, CI 완료 시 자동 기상을 약속하지 않습니다.**

### 4. 최소 상태로 재개

중단 시 새로운 상태 파일을 무조건 만들지 않습니다. 기존 PR/Issue, 작업 문서 또는 인계 surface가 있다면 그곳에 **다음 실행을 위해 다시 계산하기 비싼 정보만** 남깁니다.

- 목표, Active Scope, 완료·남은 작업과 최신 branch/commit/PR 기준점
- 확인한 검증 근거와 아직 확인하지 못한 조건
- 반복하면 안 되는 실패 시도, blocker, 다음 전환점

재개 때에는 기록된 기준점과 GitHub의 **현재** 상태를 비교한 뒤 유효한 판단만 재사용합니다. 전체 대화, tool 로그, canonical 정책을 복제하지 않습니다.

## MVP: PR to Ready

**입력 예:** “PR #N을 머지 가능한 수준으로 개선해.”

**목표:** 현재 PR을 검토 가능한 품질과 검증 근거까지 끌어올리고, 리뷰어가 남은 승인 판단을 할 수 있게 합니다. GitHub의 실제 mergeability 및 required approval까지 챗봇이 보증한다는 의미는 아닙니다.

실행 흐름:

1. 대상 PR의 base/head SHA, diff, 적용되는 저장소 지침, 기존 리뷰·checks를 확인합니다.
2. 변경 의도와 acceptance를 파악하고 구현·검증·리뷰의 실제 gap을 구분합니다.
3. 수정이 필요하고 가능한 경우 승인된 PR head 범위 안에서만 변경합니다.
4. 해당 revision의 CI 및 리뷰 증거를 확인하고, 실질적인 실패만 재작업합니다.
5. 목표 충족 시 검증 범위와 잔여 위험을 요약하고 종료합니다. 확인 불가능한 조건이 남으면 근거와 재개점을 남깁니다.

`COMPLETE`는 **이 Run에 요청된 준비 작업의 완료**만 뜻합니다. 플랫폼의 merge authorization이나 사람의 최종 승인이 아닙니다. `HANDOFF`는 실행/시간/반복 경계에 이르렀지만 이어갈 수 있는 작업이 남은 경우, `BLOCKED`는 필요한 권한·도구·승인·검증 근거 없이는 신뢰할 수 있는 다음 행동이 불가능한 경우를 구분합니다. 종료 semantics 자체는 `mols-loops`가 소유합니다.

## 검증할 가설과 성공 기준

첫 시범에서는 자동화 범위를 넓히기 전에 **동일 과업을 기존의 여러 사용자 지시 방식과 비교**합니다. 정량값은 지금 추측하지 않고 시험에서 기록합니다.

| 가설 | 확인 방법 |
| --- | --- |
| 반복 프롬프트 감소 | 완료 또는 정직한 인계까지 추가로 필요한 사용자 작업 지시 횟수 |
| 작업 품질 유지 | diff·CI·리뷰의 근거 수준과 실제 수정 결과 대조 |
| 실행 가능성 | 로컬 터미널 없이 지원되는 GitHub 도구만으로 완료 가능한 단계 기록 |
| 재개 비용 감소 | 새 세션에서 기준점 검증 후 다음 행동을 식별하는 도구 호출/컨텍스트 비용 |
| 통제 경계 준수 | 미승인 merge·scope 확대·수행하지 않은 검증의 PASS 주장 없음 |

필수 시나리오는 **정상 PR**, **수정 후 CI 실패**, **지원하지 않는 생성 작업**, **세션 중단 후 다른 revision으로 재개**를 포함합니다. CI가 늦거나 도구에서 조회되지 않는 경우도 `HANDOFF/BLOCKED`와 잘못된 성공 주장 여부를 검사합니다. 관측된 결과와 모델의 설명을 분리하고, 가능하면 같은 조건에서 반복해 비교합니다.

## 대안과 채택 이유

| 대안 | 판단 |
| --- | --- |
| 상시 프로젝트 지침에 모든 개발 절차 추가 | 부팅 컨텍스트 비용과 정책 중복 증가. 좁은 routing + 선택적 레시피 우선 |
| 새 RPI 또는 별도의 챗봇 오케스트레이터 작성 | `mols-loops`와 역할 중복. 실행 접점만 보완 |
| GitHub Actions 내부에서 LLM 에이전트 상시 실행 | 별도 모델 실행 비용·권한·운영 부담 발생. 필요해질 때 별도 선택 |
| GitHub CI를 챗봇 전용으로 복제 | 검증 계약 drift 유발. 기존 branch/PR gate 재사용 |

## 구현 순서와 보류 범위

1. **실행 레시피 시범 구현:** 챗봇 전용 자산 위치에서 `PR to Ready`만 작게 시작합니다. 활성화 방식은 현재 runtime의 실제 discovery 지원을 확인해 정합니다.
2. **실제 PR로 검증:** 동일 목표를 수동 다단계 지시와 비교하고, 결과·도구 제약·추가 사용자 개입·미검증 조건을 기록합니다.
3. **반복 사례가 확인될 때만 확장:** Issue to PR, CI Recovery, Review Loop, Resume 등의 별도 호출 단위가 정말 필요한지 결정합니다. 기존 자산과 겹치는 Skill을 무조건 늘리지 않습니다.

보류 사항: 독립 LLM runner, 원격 비동기 agent, vendor 공통 API 추상화 계층, 새로운 상태 데이터베이스, 자동 merge, 새 CI gate. 이런 요소가 없어서 실패하는 실제 사례가 확인되기 전에는 추가하지 않습니다.

## 주요 위험과 완화

- **프롬프트만으로 지속 실행을 기대하는 오류:** 실행 중 도구 호출과 미래 이벤트를 분리하고, 이후 재개는 최신 상태 확인으로 시작합니다.
- **근거 없이 “머지 가능”을 주장하는 오류:** CI evidence, review, GitHub mergeability, 최종 merge 승인을 구분합니다.
- **도구별 capability 차이:** 제품명이 아니라 현재 도구 결과와 권한으로 실행 분기합니다.
- **장황한 절차의 토큰·도구 비용:** 선택적 context loading, 최소 인계 상태, 의미 있는 gap에만 반복 실행합니다.
- **CI를 통제 표면 변경의 독립 검토로 오인:** 기존 GitHub 정책에 따라 사람의 승인과 독립된 근거를 유지합니다.

## 이후 결정

이 제안서의 범위를 확정한 다음, **별도의 구현 PR**에서 `PR to Ready` 실행 자산 한 개와 대표 검증 사례를 만듭니다. 이 PR 자체는 연구·설계 제안이며, 동작하는 자동화나 에이전트 런타임을 제공한다고 주장하지 않습니다.
