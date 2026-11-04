---
description: PR #284의 통합 Change 모델과 검증 인계 범위입니다.
---

# STDD — Handoff

## Scope

`mols-stdd`의 단위는 작업과 명세를 하나로 묶는 **Change**다. 상태·의존·재개를 `work.md`에 두고, 필요한 명세 delta·코드·테스트·Review를 같은 ID에 연결한다. 완결된 요구사항은 최신 도메인 정본에 반영한 뒤 변경을 종료한다.

## Implemented Surfaces

- `SKILL.md`: 단일 Change 구조·상태·완료 gate.
- `references/bootstrap.md`: 선택한 root/ref에서 최초 Change를 안전하게 시작하는 절차.
- `references/default-workflow.md`: Prepare → RPI → Finalize의 통합 실행.
- `docs/skills/mols-stdd/README.md`: 설계와 유지보수 의도.
- `evals/skills/mols-stdd/cases.json`: 변경·명세·의존·재개·다중 ref 및 인접 Skill의 평가 사례.
- `route/skills.jsonl`: 변경된 activation 설명 반영. 이전 `mols-spec-stdd` 자산은 PR에서 정리.

## Verify

| 관점 | 완료 근거 |
| --- | --- |
| 단일 상태 | 명세 작업에도 하나의 `work.md`만 진행 정본으로 사용 |
| 의존·재개 | 누락·순환은 unknown, 취소·미완료 선행은 blocked, 재개는 근거 재조회 |
| 명세 | delta가 필요한 경우에만 생성하고 검증 후 최신 도메인 정본에 반영 |
| 완료 | 테스트·구현·Review·필수 명세 반영 후 한 Change를 `done`으로 처리 |
| 위치·권한 | 사용자 지정 디렉터리·ref 지원, 부분 실패나 다른 계정으로의 우회 금지 |
| 단순 작업 | 문서·workflow 단계·명세 파일 강제 없음 |

정적 CI와 실제 모델의 routing·behavior evaluation은 별도다. 다중 ref에서의 실제 파일 쓰기·정본 반영은 사용 환경에서 검증해야 한다. Merge는 별도 승인과 저장소 정책에 따른다.
