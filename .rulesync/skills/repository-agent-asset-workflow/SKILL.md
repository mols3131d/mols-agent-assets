---
name: repository-agent-asset-workflow
description: >-
  Route repository-local Agent Asset creation, improvement, review, evaluation,
  distribution, retirement, and documentation to the appropriate workflows.
  Connect this repository's harness, policies, and existing specialist Skills;
  do not replace their methods or apply to external consumer projects.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Repository Agent Asset Workflow

이 저장소에서 Agent Asset을 관리할 때 **상황별 작업 절차를 선택·연결하는 라우터**다. 설계·검증·문서 작성의 전문 지식을 다시 정의하지 않고 실제 소유자를 호출한다. 다른 저장소가 이 library를 소비하는 업무에는 적용하지 않는다.

## Route

1. 현재 ref·대상·요청 결과에서 **신설·이식 / 개선·튜닝 / 리뷰·검증·평가 / 제공·설치 / 은퇴·삭제 / 문서·인계** 중 필요한 상황을 정한다. 여러 상황이 함께 있으면 선택한 절차만 조합한다.
2. `docs/development/agent-assets/common/agent-asset-management.md`에서 필요한 작업 절차와 상태·완료·유지보수 문서 기준을 선택한다. 저장소 원본·권한·검증·문서 정책은 `AGENTS.md`와 연결된 로컬 정본이 소유한다.
3. 선택한 절차가 연결하는 기존 전문 Skill, 실제 source, 하네스 및 정책을 **필요할 때만** 읽는다. 저장소에서 사용하는 Skill의 native discovery를 우선하며 불가능할 때 `.agents/route/ROUTE.md`의 lock-backed route를 따른다. `src/` 소스와 외부 제공용 `route/`를 설치·사용 상태로 오인하지 않는다.
4. 적용되는 `AGENTS.md`·Rule과 개별 전문 Skill의 방법론을 유지한다. `mols-agent-asset`은 자산 설계·개선·검증·평가, `mols-documentation`은 문서 내용, `mols-loops`는 필요한 경우에만 반복 제어를 맡는다. 찾지 못한 필수 자산을 불러온 것처럼 주장하지 않는다.

## Closure

**작성 원본을 바꾼 작업**은 문서 영향 판정 없이 완료로 처리하지 않는다. 영향을 받는 정본·유지보수·사용자 문서를 확인해 `갱신 / 기존 문서로 충분 / 해당 없음` 중 결론을 정한다. 필요한 문서는 해당 owner의 정책을 따라 수정하며 `.inbox/` 작업 기록으로 정본 갱신을 대체하지 않는다.

기존 구조·생성물 검증과 실제 행동 평가를 구분하고, 미검증·권한 부족·부작용 위험은 통합 문서의 완료·인계 경계로 처리한다. 이 라우터는 설치·원격 변경·merge 권한을 새로 부여하지 않는다.
