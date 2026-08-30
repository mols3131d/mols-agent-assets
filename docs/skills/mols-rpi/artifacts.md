---
description: RPI artifact의 배치, persistence, durable continuation과 lifecycle을 설계하거나 변경할 때 보존해야 할 결정사항을 정리한 maintainer 문서입니다.
---

# RPI Artifacts

이 문서는 RPI의 artifact 정책을 유지보수하기 위한 **design decision**을 기록합니다. Runtime behavior의 canonical source는 `SKILL.md`이며, 이 문서는 runtime instruction이나 deployable reference가 아닙니다.

## Decision

RPI의 artifact 정책은 가능한 한 하나의 `artifacts` control로 수렴합니다.

- `durable_handoff`를 독립적인 public argument로 유지하지 않습니다.
- `artifacts_path` 같은 별도 path argument도 기본 설계로 두지 않습니다.
- `artifacts`는 artifact를 어디에 두고 어떻게 이어갈지에 대한 단일 진입점입니다.
- `<auto>`는 현재 project, workspace 또는 harness가 이미 정의한 working-artifact 방식을 우선 사용합니다.
- 적절한 persistent surface가 없거나 persistence가 허용되지 않으면 inline artifact로 fallback합니다.
- Persistence는 새 저장소, directory, task system 또는 권한을 임의로 만드는 근거가 되지 않습니다.

이 결정의 목적은 artifact placement와 handoff durability를 별도 toggle로 조합하는 대신, **persistent working artifact라면 continuation에 쓸 수 있을 정도의 durability를 기본 품질로 갖게 하는 것**입니다.

## Environment First

Artifact의 실제 destination과 lifecycle은 portable RPI가 새로 표준화하기보다 현재 작업 환경의 established mechanism을 따릅니다.

우선순위는 다음과 같습니다.

1. 사용자나 상위 instruction이 명시한 artifact destination 또는 persistence boundary
1. project, workspace 또는 harness가 이미 정의한 artifact convention
1. 현재 작업을 이미 소유하는 issue, PR, task, plan, working note 또는 동등한 surface
1. 위 방식이 없거나 사용할 수 없을 때 inline artifact

파일은 흔한 persistent surface이지만 유일한 형태는 아닙니다. 반대로 repository가 file-based working artifact를 사용한다면 그 directory, naming, lifecycle과 cleanup policy를 그대로 따릅니다.

Portable RPI는 모든 환경에 통하는 고정 path grammar, artifact registry 또는 storage schema를 만들지 않습니다.

## Persistent Means Resumable

RPI artifact를 persistent surface에 남긴다면, 그 artifact는 예상하는 handoff boundary 뒤에도 다음 실행이 작업을 재개하는 데 쓸 수 있어야 합니다.

여기서 `durable`은 영구 보존이나 canonical documentation을 뜻하지 않습니다. 현재 작업에서 예상하는 context, session, worker, human 또는 machine 전환 뒤에도 필요한 state를 다시 찾을 수 있을 만큼 지속된다는 뜻입니다.

Persistent artifact에는 필요할 때 다음과 같은 resume-critical state를 유지합니다.

- 현재 Goal과 Scope
- 완료한 Work, 현재 Work와 남은 Work
- material decision과 짧은 evidence basis
- validation 결과와 current health
- freshness 판단에 필요한 revision, task state 또는 동등한 anchor
- 반복 비용이 큰 실패한 접근과 관찰된 이유
- blocker와 residual uncertainty
- 다음 시작점 또는 next transition
- 관련 source와 artifact reference

모든 항목을 항상 기록하지 않습니다. 다음 실행의 재탐색 비용이나 판단을 실제로 줄이는 state만 남깁니다.

## Reuse Before Creating

RPI는 이미 Research, Active Scope, Plan, Review 같은 observable artifact를 유지합니다. Persistent continuation이 필요하다고 해서 별도 `handoff.md`를 기본 생성하지 않습니다.

- 기존 Research, Plan, Review 또는 established task surface가 필요한 state를 소유할 수 있으면 그것을 갱신합니다.
- 여러 artifact가 실제로 유리할 때만 역할별로 나눕니다.
- 하나의 compact working artifact가 충분하면 artifact 개수를 늘리지 않습니다.
- 별도 handoff artifact는 기존 owner로는 continuation state를 명확히 복구하기 어려울 때만 고려합니다.

Artifact-rich와 compact form 사이에서 정답을 고정하지 않습니다. **Continuation cost를 충분히 낮추는 가장 작은 형태**를 선택합니다.

## Checkpoint Policy

Persistent artifact를 매 tool call이나 command마다 갱신하지 않습니다. 다음 실행의 판단이나 시작점을 바꾸는 material state가 달라졌을 때만 checkpoint합니다.

대표적인 checkpoint는 다음과 같습니다.

- Research 결과가 Plan의 방향을 바꾼 경우
- Scope나 acceptance condition이 material하게 바뀐 경우
- substantive Review가 Work 상태나 next transition을 바꾼 경우
- blocker, known-good 또는 known-broken health가 바뀐 경우
- handoff boundary가 임박했고 현재 artifact가 stale한 경우

Checkpoint maintenance는 별도 RPI Loop가 아니며 Scope, authority, persistence permission 또는 Loop budget을 넓히지 않습니다.

## Resume Contract

Persistent artifact는 현재 truth가 아니라 **resume evidence**입니다.

다음 실행은 artifact의 내용을 그대로 믿고 이어가지 않습니다. Material한 next action을 바꿀 수 있는 경우 다음을 먼저 확인합니다.

- freshness anchor가 현재 state와 맞는지
- source, repository, task 또는 environment가 artifact 작성 이후 바뀌지 않았는지
- 이전 validation이나 health claim이 여전히 유효한지
- blocker나 residual uncertainty가 해소되거나 새로 생기지 않았는지

Stale state는 갱신하거나 폐기하고, stale한 handoff를 authority처럼 사용하지 않습니다.

## Working State Is Not Canonical Knowledge

Persistent RPI artifact는 기본적으로 working 또는 handoff state입니다. 오래 남는다는 이유만으로 canonical documentation이 되지 않습니다.

작업 과정에서 future decision을 계속 바꾸는 rule, invariant, recovery knowledge 또는 non-obvious rationale이 생기면 해당 project의 documentation policy에 따라 적절한 canonical owner로 승격할 수 있습니다.

반대로 완료된 일반 작업 기록을 durable documentation으로 중복 보존하지 않습니다. 작업 종료 뒤 artifact의 archive, cleanup 또는 retention은 현재 환경의 lifecycle policy를 따릅니다.

## Boundaries

다음은 artifact 정책이 의도적으로 소유하지 않습니다.

- 별도 `durable_handoff` toggle
- 모든 runtime에 공통인 artifact path 문법
- 고정된 `research.md`, `plan.md`, `review.md`, `handoff.md` filename 요구
- artifact registry나 artifact framework
- reasoning transcript, conversation 전체 또는 매 command의 실행 로그 보존
- persistence를 이유로 한 새로운 권한이나 side effect의 암묵적 허용

Persistent surface가 예상 handoff boundary를 실제로 버티지 못한다면 durable하다고 주장하지 않습니다. 이 경우 inline 결과나 현재 가능한 surface를 사용하고 limitation을 명확히 남기는 편이 낫습니다.

## Runtime Reflection

이 결정사항을 `SKILL.md`에 반영할 때는 runtime source가 이 문서에 의존하지 않도록 필요한 behavior contract만 간결하게 옮깁니다.

향후 artifact argument를 정리할 때 보존할 핵심은 다음과 같습니다.

- `artifacts`가 artifact policy의 단일 public control이어야 합니다.
- `<auto>`는 established environment mechanism을 우선합니다.
- Persistent artifact는 기본적으로 resumable하게 관리합니다.
- Persistence가 불가능하거나 허용되지 않으면 inline fallback을 허용합니다.
- Existing artifact를 우선 재사용하고 불필요한 duplicate handoff surface를 만들지 않습니다.
- Resume 시 freshness와 material health를 다시 확인합니다.

정확한 argument representation은 실제 runtime과 사용 사례가 요구하는 최소 surface로 유지하며, 미래 가능성만을 위해 enum이나 schema를 늘리지 않습니다.
