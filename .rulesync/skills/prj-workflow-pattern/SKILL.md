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
compatibility: >-
  For mols-agent-assets; uses mols-documentation for document quality and may
  use mols-text-optimizer only for generic wording-only fallback.
---

# Project Pattern Workflow

패턴 문서 작업에서 **요청에 맞는 워크플로만** 읽는다. 여러 작업이 필요하면 해당 파일을 조합한다.

| Workflow | 선택 기준 |
| --- | --- |
| [Lifecycle](workflows/lifecycle.md) | 후보→정본→제공→유지→은퇴·제거의 **전체 상태와 전환**을 판단할 때. 개별 작업 절차가 아닌 라이프사이클 개요. |
| [Create](workflows/create.md) | 새 아이디어가 독립적인 재사용 패턴인지, 기존 패턴과 중복되는지 판단하고 **분류·신설**할 때. 기존 문서 수정은 Improve. |
| [Improve](workflows/improve.md) | 기존 문서의 **핵심 설명·적용 조건·구성·예시·표현**을 수정하거나 확장할 때. 패턴 간 소유권 변경은 Restructure. |
| [Review](workflows/review.md) | 패턴 **적합성·독립성·선택 유연성·근거·가독성**을 평가하고 결함을 도출할 때. 검토만 요청되면 읽기 전용. |
| [Validate](workflows/validate.md) | Markdown·frontmatter·링크와 **생성 인덱스의 정합성**을 검사할 때. 내용의 적절성 판단은 Review. |
| [Publish](workflows/publish.md) | `description`·category 안내·링크를 정리해 **카탈로그에서 발견·선택**하기 쉽게 할 때. 외부 프로젝트 설치·채택은 제외. |
| [Maintain](workflows/maintain.md) | **근거·참조의 유효성**을 갱신하거나 분류·이름·경로를 옮기고 기존 링크를 정리할 때. 본문 개선은 Improve와 조합. |
| [Restructure](workflows/restructure.md) | 여러 패턴의 **책임 중복·통합·분리·대체**를 판단하고 지식을 이관할 때. 단순 위치 변경은 Maintain. |
| [Retire](workflows/retire.md) | 패턴을 **더 이상 권장하지 않을지** 판단하고 사용 범위·대안을 안내할 때. 원본 삭제는 별도 작업. |
| [Delete](workflows/delete.md) | **실제 원본 제거**가 요청됐을 때 영향·권한·참조·지식 이관을 처리하고 삭제할 때. 은퇴 판단만 필요하면 Retire. |

패턴의 의미·작성 기준은 [Patterns](../../../catalog/patterns/README.md)가 소유한다. `compatibility`는 관련 Skill을 설명하지만 자동 설치·로드를 뜻하지 않는다. 실제 선택 여부는 해당 워크플로에서 판단한다. 이 Skill은 기존 정책·권한을 재정의하지 않는다.
