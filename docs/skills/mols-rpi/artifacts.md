---
description: RPI artifact의 배치, persistence, durable continuation과 lifecycle을 설계하거나 변경할 때 보존해야 할 결정사항을 정리한 maintainer 문서입니다.
---

# RPI Artifacts

RPI Skill의 artifact 동작을 설계할 때 참고할 결정사항만 정리합니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Decisions

- Public control은 가능하면 `artifacts` 하나로 둡니다.
- Structured syntax를 요구하지 않고, 같은 의도의 자연어 지시도 `artifacts` override로 해석합니다.
- `durable_handoff`, `artifacts_path`를 별도 argument로 두지 않습니다.
- `<auto>`는 사용자·project·workspace·harness가 이미 정한 artifact 방식을 우선합니다.
- 적절한 persistent surface가 없거나 persistence가 허용되지 않으면 inline으로 fallback합니다.
- 새 path, registry, storage schema나 권한을 RPI가 임의로 만들지 않습니다.

## Persistent Artifacts

Persistent RPI artifact는 별도 toggle 없이 **resume 가능한 working state**로 관리합니다.

필요한 경우 다음 상태만 남깁니다.

- Goal과 Scope
- 완료·현재·남은 Work
- material decision과 validation 상태
- blocker와 residual uncertainty
- freshness를 확인할 기준점
- 다음 시작점과 필요한 reference

모든 항목을 항상 기록하지 않고, 다음 실행의 재탐색 비용을 줄이는 최소 상태만 유지합니다.

## Placement

기존 surface를 새 artifact보다 우선합니다.

1. 사용자나 상위 instruction이 지정한 destination
1. project/workspace/harness의 artifact convention
1. 기존 PR, Issue, task, plan, Research, Review 같은 working surface
1. 사용할 persistent surface가 없으면 inline

고정 filename이나 `handoff.md`를 기본 생성하지 않습니다.

## Checkpoint and Resume

- Material state가 바뀔 때만 persistent artifact를 갱신합니다.
- Artifact 갱신은 별도 RPI Loop로 계산하지 않습니다.
- Resume할 때 artifact를 current truth로 가정하지 않고 freshness와 필요한 health를 다시 확인합니다.
- Stale state는 갱신하거나 폐기합니다.

## Boundary

Persistent artifact는 working/handoff state이지 canonical knowledge가 아닙니다. 장기적으로 유효한 rule, invariant, rationale은 해당 환경의 canonical owner로 승격하고, 작업 artifact의 retention·archive·cleanup은 그 환경의 lifecycle policy를 따릅니다.
