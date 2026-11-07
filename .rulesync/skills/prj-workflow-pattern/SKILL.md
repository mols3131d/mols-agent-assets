---
name: prj-workflow-pattern
description: >-
  이 저장소의 catalog/patterns/에서 재사용 패턴 문서를 발굴·신설·개선·리뷰·검증·
  유지·재분류·통합·이동·은퇴·삭제할 때 작업별 절차와 정본·검증 도구를 연결한다.
  외부 프로젝트에서 패턴을 적용하거나 일반 문서·정책·Agent Asset 자체를
  작성·관리하는 작업에는 사용하지 않는다.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Project Pattern Workflow

이 저장소의 `catalog/patterns/`에 있는 **재사용 패턴 문서의 라이프사이클**을 라우팅한다. 패턴의 의미·분류·작성·리뷰 기준은 [Patterns](../../../catalog/patterns/README.md), 문서 품질·정본 관리는 `docs/documentation/`, Git·검증·권한은 저장소 정책이 소유한다. 이 Skill은 이를 복제하거나 패턴을 강제 지침으로 만들지 않는다.

## Route

1. 현재 repository·ref·대상과 요청 결과를 확인한다. **후보 판정 / 신설 / 개선·확장 / 리뷰·검증 / 유지·이동·통합 / 은퇴·삭제** 중 요청된 상황만 선택한다. 읽기 전용 리뷰를 임의로 수정·삭제 작업으로 확대하지 않는다.
2. [Catalog Index](../../../catalog/INDEX.tsv)에서 후보를 좁히고 해당 category README·기존 capsule과 관련 인용·참조를 읽는다. 패턴의 *primary problem*, 현재 소유자, 겹치는 패턴과 영향을 받는 소비 경로를 확인한다. 인덱스는 생성된 탐색 자료이며 정본이 아니다.
3. 상황에 필요한 전문 Skill만 조합한다. 패턴 본문의 정보 구조와 표현은 `mols-documentation`, Markdown·frontmatter·인덱스의 결정적 검사는 `mols-markdown-maintenance`와 저장소 native tooling, 복잡한 반복 개선은 `mols-loops`가 맡는다. Agent Asset 자체의 변경이 함께 필요할 때만 해당 자산 관리 워크플로를 별도로 적용한다.

## Lifecycle

| 상황 | 판단과 작업 |
| --- | --- |
| **후보·신설** | 여러 맥락에서 참고·변형할 가치가 있는 문제 해결 방식인지 확인한다. 일회성 기록은 `.inbox/`, 강제 정책은 해당 owner, Agent Asset 실행 계약은 그 원본에 둔다. 기존 capsule로 충분하면 신설하지 않는다. 고유 책임이 있다면 primary problem에 맞는 category 하나를 택한다. |
| **작성·개선·확장** | 문제, 적용 조건과 부적합 조건, core, 선택적 구현, 유의미한 한계·대안을 필요한 만큼 설명한다. 기존 capsule은 사실·의도·호환 관계를 보존하면서 오래된 주장과 중복을 정리한다. 새 파일보다 기존 owner의 수정·연결을 우선한다. |
| **리뷰·검증** | [Patterns의 Review](../../../catalog/patterns/README.md#review)로 독립성·분류·소유권·권고와 불변조건의 구분·선택 유연성·근거의 지속 가치를 확인한다. 문서·링크·인덱스 검증과 실제 적용 사례의 효과 검토는 구분한다. 요청이 리뷰뿐이면 findings와 판단만 남긴다. |
| **유지·재분류·이동** | 사용 맥락, 근거·외부 링크의 최신성, 중복 패턴과 탐색성을 재평가한다. 분류·이름·경로가 책임을 가리지 않는지 확인하고 변경이 유의미할 때만 이동한다. 알려진 내부 참조, README, 관련 문서와 인덱스 생성 결과의 영향을 처리한다. |
| **통합·분리·대체** | 반복된 core와 책임 경계를 비교해 단일 owner로 통합할지, 독립 문제가 있으면 나눌지 판단한다. 관련 capsule·링크·예제를 필요한 범위에서 이관하고, 중복된 정본을 남기지 않는다. 실질적 필요 없이 alias·호환 파일을 만들지 않는다. |
| **은퇴·삭제** | 내용이 더 이상 유효하지 않거나 다른 owner로 대체됐는지, 사용·참조가 남아 있는지 확인한다. 필요한 지식과 알려진 연결은 먼저 이관하고, 승인된 범위에서 원본·관련 참조·파생 항목을 정리한다. 단지 오래됐다는 이유로 삭제하거나 형식상 archive·tombstone을 만들지 않는다. |

단순한 패턴은 category의 단일 Markdown 파일로 유지하고, 독립적인 resource·책임이 생길 때만 bundle로 확장한다. 특정 section·template·reference 수나 일률적인 lifecycle 순서를 강제하지 않는다. 외부 표준은 내용의 근거가 되는 경우에만 연결하고, 중복·노후·판단 가치가 낮은 자료는 남기지 않는다.

## Close

1. 영향을 받은 정본 capsule과 category 탐색·내부 링크를 확인한다. `description`은 패턴 선택에 유용해야 하며, 작업 기록 `.inbox/`를 정본으로 승격했다고 간주하지 않는다.
2. 패턴 원본을 생성·수정·이동·삭제했다면 저장소의 `mise run generated sync`로 `catalog/INDEX.tsv`를 갱신하고 `mise run generated validate`로 drift를 확인한다. **생성 인덱스는 직접 편집하지 않는다.** 필요한 형식·링크·문서 검사를 적용하고 실행할 수 없는 검증은 미검증으로 구분한다.
3. 완료된 변경, 연결·호환 영향, 확인한 근거, 남은 불확실성을 기존 작업·PR에 남긴다. 필요한 정본 갱신을 마친 뒤 전용 branch·PR로 인계하며, 배포·외부 적용·Merge 성공을 파일 작성만으로 단정하지 않는다.

## Boundary

- 이 Skill은 **패턴 문서의 유지관리 워크플로**만 소유한다. 다른 프로젝트가 패턴을 실제로 적용하거나 프로젝트 정책으로 채택하는 결정을 대신하지 않는다.
- 문서의 제안은 선택 가능한 패턴이다. 이를 필수 규칙·고정 실행 절차·평가 통과 기준으로 바꾸지 않는다.
- 외부 소비자의 사용 현황과 GitHub 권한을 추측하지 않는다. 경로 이동·삭제에 필요한 영향이나 승인을 확인할 수 없으면 범위를 축소하거나 차단·인계한다.
