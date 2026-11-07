---
name: prj-workflow-pattern
description: >-
  이 저장소의 catalog/patterns/ 패턴 문서를 신설·개선·리뷰·검증·제공·유지·
  이동·통합·은퇴·삭제할 때 작업별 워크플로를 선택한다. 외부 프로젝트의
  패턴 적용이나 일반 문서·Agent Asset 작성에는 사용하지 않는다.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
metadata:
  dependencies: "mols-documentation, mols-text-optimizer"
---

# Project Pattern Workflow

패턴 문서 작업에서 **요청에 해당하는 파일만** 읽고, 복합 작업이면 필요한 워크플로를 조합한다. 전체 상태·전환 판단에는 [Lifecycle](workflows/lifecycle.md)을 사용한다.

| 작업 | Workflow |
| --- | --- |
| 후보 판정·신설 | [Create](workflows/create.md) |
| 수정·개선·확장 | [Improve](workflows/improve.md) |
| 적합성·품질 리뷰 | [Review](workflows/review.md) |
| 형식·링크·인덱스 검증 | [Validate](workflows/validate.md) |
| 탐색·제공 | [Publish](workflows/publish.md) |
| 근거 갱신·재분류·이동 | [Maintain](workflows/maintain.md) |
| 통합·분리·대체 | [Restructure](workflows/restructure.md) |
| 사용 중단·은퇴 | [Retire](workflows/retire.md) |
| 원본 삭제 | [Delete](workflows/delete.md) |

패턴의 의미·작성 기준은 [Patterns](../../../catalog/patterns/README.md)가 소유한다. `metadata.dependencies`는 참고용이며 자동 설치·로드를 뜻하지 않는다. 필요한 전문 Skill은 해당 워크플로에서 선택한다. 이 Skill은 기존 정책·권한을 재정의하지 않는다.
