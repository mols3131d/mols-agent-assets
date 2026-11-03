---
description: 소규모 프로젝트용 Work Management Skill 구현에 앞서 사용자 지정 작업 경로·Git ref·사람 중심 문서 품질 기준을 전달합니다.
---

# Work Management — Handoff

## Objective and State

개인 토이 프로젝트와 국지적 개발 작업에서 사용자가 **어디에, 어떤 Git ref로** 작업을 기록할지 결정하고, 에이전트가 읽기 쉬운 Markdown 작업 파일로 선택·의존성·진행·재개를 돕는 경량 Skill `mols-work-management`를 구현한다. Beads의 작업 단위·dependency-aware ready 개념은 참고하지만 Beads·Dolt·서버·CLI/MCP는 요구하지 않는다.

**PR #284는 설계 작업이 반영된 Draft이며 Skill은 아직 구현되지 않았다.** 설계의 원본 근거와 예시는 [Design](design.md)에 둔다. `.inbox/` 자체는 Agent Asset의 실행 정본이 아니다.

## Key Decisions

| Concern | Implementation direction |
| --- | --- |
| 사용자 선택 | 작업 디렉터리와 선택적 Git branch/ref를 프로젝트·사용자가 결정 |
| Storage locator | `workspace/repository + task ref(있을 때) + task directory` |
| Code vs. tasks | 코드 ref와 작업 ref는 같거나 달라도 됨. task 전용 branch 허용 |
| 기본 디렉터리 | 없음. `.work/`, `items/` 등을 자동 생성하거나 기본값으로 강제하지 않음 |
| 식별·구분 | 사용자 선택 task root 기준 상대 파일 경로(확장자 제외), 짧고 의미 있는 filename과 H1 제목 |
| 최소 구조 | Markdown 파일별 제목·`status`; 필요할 때 `depends_on`, 우선순위·완료 조건·다음 행동 |
| 상태 | `todo | doing | done | cancelled`; `ready | blocked | unknown`은 조회 결과 |
| 진행·재개 | 마지막 관찰 근거·남은 것·다음 행동만 파일에 기록, 새 세션에서 선택된 ref와 실제 산출물 재확인 |
| Git 역할 | 버전·diff·branch 관리. 별도 task branch를 코드 branch로 자동 merge하거나 lock으로 취급하지 않음 |
| 인간 가독성 | 의미 있는 제목·파일명·상태 구분, 짧은 목적·완료 조건·다음 행동, 불필요한 메타데이터 배제 |

작업 경로·ref를 모르는 경우 임의의 위치나 기본 branch에 기록하지 않는다. 사용자에게 위치를 확인하거나 read-only 제안만 수행한다. 기존 프로젝트가 다른 작업 정본을 소유하면 추가 파일 저장소를 무단 도입하지 않는다. 원격 쓰기 전 실제 계정·명의·ref·권한을 확인하고 다른 연결로 우회하지 않는다.

## Acceptance Criteria

1. 사용자 지정 폴더(프로젝트 루트 포함)에서 작업 파일을 관리하며 `.work/` 같은 기본 경로에 종속되지 않는다.
2. 전용 작업 branch와 코드 branch를 다르게 선택해도 올바른 task ref에서 읽고 쓴다. 지정 branch가 없거나 접근 불가하면 기본 branch로 대체하지 않는다.
3. 의미 있는 파일명·H1 제목·필요한 완료 조건/다음 행동으로 **사람이 탐색기·에디터·diff에서 작업을 알아보고 구분**할 수 있다. 경로가 다른 동명 작업도 모호하지 않다.
4. 파일 이동·개명 시 상대 경로 의존 참조를 확인하고, 누락·순환·취소된 의존성을 성공으로 취급하지 않는다.
5. 5개 작업의 `ready / blocked / unknown`, `doing` 재개와 선택적 우선순위를 일관되게 판단한다.
6. Git과 파일 API의 실제 지원 범위 안에서만 수정하고, 다른 ref의 파일이나 동일 파일의 경쟁 변경을 덮어쓰지 않는다.
7. 단일 버그·스펙·테스트·build task에는 불필요하게 활성화하지 않는다. 필요 이상의 파일·필드·인덱스를 만들지 않는다.
8. 정적 검증, 의미 리뷰, 실제 런타임 평가는 다른 근거로 표시하고 미실행 동작을 성공으로 보고하지 않는다.

## Next Steps

1. `mols-agent-asset`의 설계/검증/평가 방법과 저장소의 작성 원본·문서 라이프사이클에 따라 **단일 `SKILL.md`**를 구현한다: `src/rulesync/.rulesync/skills/mols-work-management/SKILL.md`.
2. 인라인 경로·별도 task branch·동일/상이한 코드 branch·동명 작업·파일 이동·오래된 인계 시나리오를 실제 접근 가능한 환경에서 검토한다.
3. 작업 도구별 한계와 독립 Skill의 사용성을 평가하되, 반복 문제 확인 전에는 DB·스크립트·registry·별도 설정 파일을 추가하지 않는다.
4. 필요한 유지보수 문서와 PR 설명을 갱신하고 검증 여부를 분리한다. Merge는 별도 승인·게이트에 맡긴다.

`mols-spec-stdd`는 이미 별도로 병합된 독립 Skill이며 이 PR에서 구현을 복제하지 않는다.
