---
description: mols-loops를 유지보수할 때 outer adaptive orchestration, RPI loop kernel, progressive context/composition, intensity와 artifact 결정을 찾는 entrypoint입니다.
---

# Mols Loops Maintainer Docs

Runtime behavior의 canonical source는 `src/rulesync/.rulesync/skills/mols-loops/SKILL.md`입니다. `mols-loops`는 outer adaptive orchestrator이고 RPI는 내부 default loop kernel입니다. Loops는 outer Goal/Scope, Run envelope·accounting, cross-capability composition과 phase placement, recursion, handoff와 Finalize를 소유합니다. RPI는 Main Loop의 Research → Plan → Implementation/Work → Review prerequisite와 Review-driven stage transition을 소유하고, task-specific workflow와 capability는 자신의 내부 procedure·ordering·dependency를 계속 소유합니다. 이 디렉토리는 Skill을 변경할 때 보존해야 할 핵심 결정만 기록합니다.

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
