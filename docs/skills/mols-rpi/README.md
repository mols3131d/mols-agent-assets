---
description: mols-rpi를 유지보수할 때 RPI의 핵심 설계, Research, Plan과 artifact 결정 문서를 찾는 entrypoint입니다.
---

# Mols RPI Maintainer Docs

Runtime behavior의 canonical source는 `src/rulesync/.rulesync/skills/mols-rpi/SKILL.md`입니다. 이 디렉토리는 Skill을 변경할 때 보존해야 할 핵심 결정만 기록합니다.

- [RPI](rpi.md) — RPI, adaptive control, recursive resolution의 핵심
- [Research](rpi-research.md) — adaptive recursive RPI에서 Research의 역할
- [Plan](rpi-plan.md) — delta replanning과 child-parent reintegration
- [Artifacts](artifacts.md) — artifact placement, persistence와 continuation 결정
