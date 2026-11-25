---
description: mols-loops를 유지보수할 때 outer adaptive orchestration, RPI loop kernel, progressive context/composition, intensity와 artifact 결정을 찾는 entrypoint입니다.
---

# Mols Loops Maintainer Docs

Runtime behavior의 canonical source는 `src/rulesync/.rulesync/skills/mols-loops/SKILL.md`입니다. `mols-loops`는 outer adaptive orchestrator이고 RPI는 내부 default loop kernel입니다. Loops는 outer Goal/Scope, Run envelope·accounting, cross-capability composition과 phase placement, recursion, handoff와 Finalize를 소유합니다. RPI는 Main Loop의 Research → Plan → Implementation/Work → Review prerequisite와 Review-driven stage transition을 소유하고, task-specific workflow와 capability는 자신의 내부 procedure·ordering·dependency를 계속 소유합니다. 이 디렉토리는 Skill을 변경할 때 보존해야 할 핵심 결정만 기록합니다.

## Design Direction

다음 설계는 하나의 세션에서 하나의 작업 목표를 직접 수행하는 에이전트를 위한 범용 적응형 작업 루프에 집중한다. 주요 소비 환경은 챗봇이며, 특정 제품을 적용 전제로 삼지 않는다. 필요한 맥락과 전문 지침을 점진적으로 확보하고, 유효한 근거와 계획에 따라 실행하며, 실질적인 개선과 검증을 거쳐 목표에 수렴시키는 것이 목적이다.

멀티에이전트 오케스트레이션, 위임된 에이전트의 라이프사이클 관리, 세션 간 실행 제어 및 개발 하네스는 이 설계의 책임에 포함하지 않는다. 단일 세션에서의 문제 분해, 도구 사용 및 전문 작업 절차와의 조합은 유지할 수 있다. 자연어 Skill 자체가 런타임의 반복 실행이나 독립 검증을 강제할 수 있다고 가정하지 않는다.

현재 실행 계약은 정본 Skill에 남아 있다. 설계 방향을 실제 동작으로 전환할 때 관련 유지보수 문서, routing 및 평가 계약을 함께 정합화한다.

## Public Rename Boundary

`mols-loops`는 기존 public Skill identity `mols-rpi`의 rename이며 compatibility alias를 유지하지 않습니다. Exact Skill name이나 repository command 이름을 참조하는 consumer는 `mols-loops`로 이관해야 합니다. 같은 trigger의 `mols-rpi` wrapper를 남기면 routing owner가 다시 모호해지므로, 호환성이 필요하면 별도의 제한된 migration contract와 eval을 먼저 정의합니다.

`RPI`, `RPI Main Loop`, `rpi.md`와 `rpi-*.md`는 deprecated public identity가 아니라 Loops 내부 default kernel과 그 유지보수 용어입니다. Public rename을 이유로 이 내부 method terminology를 기계적으로 치환하지 않습니다.

- [RPI](rpi.md) — Prepare → Main RPI → Finalize 외피, prerequisite contract, perspective control과 Loops outer control의 접점
- [Research](rpi-research.md) — evidence prerequisite, adaptive multi-perspective search와 Review-driven reopening
- [Plan](rpi-plan.md) — Research prerequisite, Work coverage와 delta replanning
- [Work](rpi-work.md) — polymorphic one-or-many Work와 RPI stage/domain action의 구분
- [Review](rpi-review.md) — multi-perspective validation, challenge reconciliation과 executable next-transition dispatch
- [Intensity](rpi-intensity.md) — light·standard·deep adaptive effort bias
- [Artifacts](artifacts.md) — outer Run의 artifact placement, persistence와 continuation 결정
- [Description](description.md) — Trigger·routing 필수/보조 signal과 1,024자 portability boundary
- [Evaluation](evaluation.md) — Trigger/Behavior suite, progressive context/composition coverage, Promptfoo projection, grader와 runtime evidence 경계

Progressive context loading과 adaptive composition의 canonical mechanics는 `SKILL.md`가 소유합니다. Maintainer 문서는 해당 behavior를 다른 owner로 복제하지 않고, RPI kernel·artifact·evaluation처럼 별도 유지보수 판단이 필요한 경계만 설명합니다.
