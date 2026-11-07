---
name: prj-workflow-pattern
description: >-
  이 저장소의 catalog/patterns/ 패턴 문서에 대한 후보 판정·신설·개선·리뷰·
  검증·제공·유지·재구성·은퇴·삭제를 상황별 워크플로로 연결한다.
  외부 프로젝트의 패턴 적용, 일반 문서·정책 또는 Agent Asset 자체의
  작성·관리에는 사용하지 않는다.
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

이 저장소의 `catalog/patterns/`에 있는 **재사용 패턴 문서의 라이프사이클**을 라우팅한다. 패턴의 의미·분류·작성·리뷰 기준은 [Patterns](../../../catalog/patterns/README.md), 일반 문서 품질·정본 관리와 Git·검증·권한은 각 저장소 정책이 소유한다.

## Route

현재 repository·ref·대상과 요청 결과를 확인하고 **해당 워크플로 파일만** 읽는다. 복합 작업은 필요한 파일을 조합한다. 상태 간 전환이나 전체 흐름을 판단할 때는 [Lifecycle](workflows/lifecycle.md)을 선택한다.

| 요청 | Workflow |
| --- | --- |
| 새 패턴 후보 판정·신설 | [Create](workflows/create.md) |
| 기존 패턴 수정·개선·확장 | [Improve](workflows/improve.md) |
| 패턴 적합성·내용·품질 리뷰 | [Review](workflows/review.md) |
| 문서 형식·링크·인덱스 검증 | [Validate](workflows/validate.md) |
| 카탈로그 탐색·제공 정리 | [Publish](workflows/publish.md) |
| 근거 갱신·재분류·경로 이동 | [Maintain](workflows/maintain.md) |
| 통합·분리·대체·책임 재구성 | [Restructure](workflows/restructure.md) |
| 사용 중단·은퇴 결정 | [Retire](workflows/retire.md) |
| 원본과 참조의 실제 삭제 | [Delete](workflows/delete.md) |

## Shared Boundary

- `catalog/INDEX.tsv`는 원본에서 생성한 탐색 자료다. 실제 작업 전에 관련 category와 capsule 원본을 확인한다. `.inbox/` 기록도 정본·지침으로 승격하지 않는다.
- `mols-documentation`은 문서 구성·표현, `mols-markdown-maintenance`와 repository-native tooling은 결정적 형식·projection 검증, `mols-loops`는 필요한 반복 개선을 맡는다. Agent Asset 자체를 변경할 때만 별도 자산 워크플로를 적용한다.
- 패턴은 **선택 가능한 설계 제안**이다. 이를 강제 정책·고정 실행 절차로 바꾸지 않는다. 읽기 전용 리뷰는 수정·PR 생성 권한이 아니다.
- 외부 소비자의 사용·권한을 추측하지 않는다. 변경·이동·삭제 같은 쓰기는 요청 범위와 계정·영향을 확인한 뒤 수행하고, 실행하지 못한 검증을 통과로 보고하지 않는다.
