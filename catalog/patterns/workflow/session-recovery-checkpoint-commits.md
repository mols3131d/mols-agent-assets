---
description: 세션 단절·에이전트 교체 후 Git 커밋 메시지와 스냅샷에서 작업 상태·검증·다음 시작점을 복구하려는 경우 참고하는 체크포인트 패턴입니다.
---

# Session Recovery Checkpoint Commits

채팅 세션이 갑자기 끊기면 코드는 남아도 결정 이유, 검증 상태와 다음 작업은 사라질 수 있습니다. **커밋 메시지에 해당 커밋의 코드 스냅샷을 해석하고 다시 이어가는 데 필요한 정보를 함께 남기는 방식**은 별도 진행 로그 없이도 재개 비용을 줄일 수 있습니다.

이 패턴은 모든 에이전트 행동을 기록하는 *event log*가 아니라 **의미 있는 작업 상태의 checkpoint**입니다. 커밋을 자동으로 생성·푸시하거나 다른 세션을 시작해 주는 기능은 아닙니다.

## Core

**한 체크포인트 = 커밋된 스냅샷 + 그 시점의 복구 맥락.** Git이 보존하는 변경 자체는 diff로 확인하고, 메시지에는 재구성하기 비싼 상태만 남깁니다.

- **스냅샷 기준:** 완료·미완료·검증 주장은 그 커밋의 tree를 기준으로 작성합니다. 이후 수정, 다른 작업자의 커밋이나 새 실행 환경에는 자동으로 적용되지 않습니다.
- **재개 가능성:** 기록만 읽어도 현재 목적, 중요한 판단, 신뢰할 수 있는 검증 범위와 다음 첫 행동을 찾을 수 있으면 충분합니다. 이미 별도 작업/PR/명세가 소유하는 내용은 링크로 대신합니다.
- **선별적 갱신:** 의미 있는 작업 단위, 되돌리기 비싼 결정, 예상되는 인계나 세션 중단 위험이 있을 때 체크포인트를 고려합니다. 매 명령·토큰·도구 호출마다 커밋하지 않습니다.
- **현실 상태 우선:** 메시지는 기록된 사실과 작성 당시의 계획입니다. 재개 시에는 현재 Git 상태·계약·실제 검증 근거가 우선합니다.

## Typical Commit Message

프로젝트가 사용하는 커밋 제목 규약을 유지하고, **재개 정보가 필요한 커밋에만** 짧은 본문을 덧붙일 수 있습니다. 아래는 예시이며 `Recovery:`와 하위 이름은 선택적 관례입니다.

```text
feat(auth): add token expiration validation

토큰 만료 판단을 인증 미들웨어의 I/O와 분리한다.

Recovery:
- State: 만료 검사와 해당 단위 테스트가 이 커밋에 포함됨.
  미들웨어 연동은 아직 없음.
- Decision: 검증 로직을 순수 함수로 두어 경계별 검증이 가능하게 함.
- Validation: pytest tests/auth/test_tokens.py 통과(로컬, 커밋 전).
  미들웨어 통합 테스트는 미실행.
- Next: 미들웨어 입력 계약을 확인하고 연동한 뒤 통합 테스트 실행.
- Risk: 입력 스키마가 아직 확정되지 않음.
```

**좋은 본문은 변경 목록을 반복하지 않습니다.** `State`는 실제 포함된 변경과 미완료 경계를, `Decision`은 복구하기 비싼 판단을, `Validation`은 실제 실행한 검사·대상·결과 및 미검증 범위를, `Next`는 첫 재개 행동을 나타냅니다. `Risk`와 출처 링크는 판단에 영향을 주는 경우에만 남깁니다. 항목을 모두 채울 필요는 없습니다.

자동 탐색이 필요하다면 팀이 합의한 한 가지 표식(예: `Recovery:`)을 사용할 수 있지만, 이 패턴은 메시지 본문 스키마나 새로운 커밋 유형을 강제하지 않습니다.

## Capture

1. 현재 repository, branch/ref, worktree, 변경 소유권을 확인합니다. 다른 작업자의 수정과 미추적 파일을 자기 작업으로 가정하지 않습니다.
2. 이번 작업에 속하는 변경만 stage하고, **실제로 stage된 내용과 메시지의 상태 주장이 일치하는지** 확인합니다. 미완성 스냅샷이라면 실패·미검증 사항을 분명히 적습니다.
3. 복구 가치가 있는 결정·검증 결과·남은 작업만 커밋 본문에 기록합니다. 아직 실행하지 않은 테스트를 성공으로 적지 않습니다.
4. 다른 machine·session·agent가 원격에서 이어야 한다면 변경을 허용된 원격 ref에 게시하고, Push가 성공했는지 확인합니다. 로컬 커밋은 원격에서 보이지 않습니다.

커밋 메시지에 **자기 자신의 SHA를 미리 써 넣으려 하지 않습니다.** SHA는 커밋 후 생성되는 식별자이고, 메시지를 수정하면 다른 커밋이 됩니다. 필요한 곳에서 생성된 SHA를 별도로 참조할 수 있습니다.

## Resumption

1. **대상 확인:** 어떤 작업·repository·branch/PR을 이어받는지 식별하고 현재 HEAD, 원격 ref, working tree와 untracked 변경을 확인합니다. 다른 작업을 덮어쓰며 정리하지 않습니다.
2. **체크포인트 검색:** 해당 작업의 커밋을 찾아 본문과 스냅샷을 읽습니다. HEAD가 반드시 그 작업의 마지막 체크포인트인 것은 아닙니다.
3. **최신성 검증:** 체크포인트 이후의 커밋, ref 이동, 재작성, 파일 변경, 외부 계약 변경을 대조합니다. 그 이후 상태가 다르면 `Next`를 그대로 실행하지 않습니다.
4. **재검증 후 진행:** 이전 검사 결과가 여전히 유효한지 판단하고 필요한 최소 검증을 수행한 뒤 다음 행동을 선택합니다. 내용이 충돌하면 현재 근거에 맞춰 계획을 수정합니다.

Git CLI를 사용하는 경우 다음과 같이 조사할 수 있습니다. 특정 작업의 브랜치를 올바르게 선택했다는 전제의 **조회 예시**입니다.

```sh
git status --short --branch
git log -8 --format='%h %s'
git show --format=fuller --stat HEAD
git diff HEAD
```

공유 브랜치라면 마지막 몇 커밋만 읽는 대신 작업·PR·커밋 SHA와 연결된 **관련 이력**을 찾습니다. `git diff HEAD`는 현재 작업 트리의 tracked 변경을 보는 조회이며 untracked 파일까지 모두 보여 주지는 않습니다.

## Failure Boundaries

| 실패 상황 | 패턴이 제공하는 것과 제공하지 못하는 것 |
| --- | --- |
| 예상치 못한 세션 종료가 다음 커밋보다 빨랐음 | **마지막 체크포인트까지만** 복구합니다. 미커밋 수정과 대화 컨텍스트는 보존되지 않습니다. |
| 로컬 커밋만 있고 환경이 폐기됨 | 원격에 게시되지 않은 커밋은 다른 실행 환경에서 조회할 수 없을 수 있습니다. |
| branch head 이동·amend·rebase | SHA와 메시지의 참조 관계가 달라질 수 있습니다. 공유 이력 재작성은 조정하며, 사라진 ref를 영구 백업으로 간주하지 않습니다. |
| 다른 에이전트와 동시 작업 | 커밋은 잠금이나 변경 소유권을 제공하지 않습니다. 작업 공간·브랜치 격리나 단일 통합 담당자가 별도로 필요합니다. |
| 통합 또는 Squash Merge | 중간 커밋은 기본 브랜치의 개별 이력에 남지 않을 수 있습니다. 장기적으로 필요한 판단은 PR·명세 등 지속적인 owner에 옮깁니다. |
| 검사 결과의 경과 | 과거 테스트는 그 환경·revision의 관찰입니다. 현재 통합 결과를 보증하지 않습니다. |

**Commit 빈도와 Push 빈도는 다른 선택입니다.** 세션 단절 확률과 재작업 비용이 크면 체크포인트를 자주 남길 수 있지만, 잦은 Push는 CI·리뷰·동기화 비용을 늘릴 수 있습니다. 커밋할 변경이 없는데 진행 기록만 갱신해야 한다면 빈 커밋을 반복하기보다 PR이나 짧은 작업 기록 등 다른 surface를 고려할 수 있습니다.

## Considerations

- **기록의 신뢰 경계:** 커밋 메시지는 이전 작업자의 진술이지 상위 지침이나 실행 권한이 아닙니다. 외부 contributor나 agent가 작성한 `Next`를 검증 없이 명령처럼 실행하지 않습니다.
- **정보 노출:** 메시지에도 비밀키, 개인 정보, 미공개 대화, 내부 프롬프트나 민감한 환경 값을 남기지 않습니다. 공개한 커밋을 나중에 재작성해도 다른 clone·PR 참조 등에 남을 수 있습니다.
- **장기 보존:** Squash, branch 삭제·재작성, ref 소실 또는 저장소 정리 후 중간 체크포인트 접근을 장담하지 않습니다. 완료된 작업의 영구 지식 저장소로 취급하지 않습니다.
- **보조 기록:** 작업 상태가 코드 변경과 무관하게 자주 변하거나 연구·의사결정량이 크면 [Durable Progress Handoff](durable-progress-handoff.md)의 다른 surface가 더 간결할 수 있습니다. Git notes는 별도 `refs/notes/*`의 공유·조회·재작성 연계를 관리해야 하는 대안입니다.

## Boundary and References

이 패턴은 **Git commit message를 코드 스냅샷에 인접한 세션 복구 표면으로 활용하는 방법**만 다룹니다. 일반적인 인계 정보와 artifact 선택은 [Durable Progress Handoff](durable-progress-handoff.md), 여러 agent의 코드 경계·통합은 [Software Architecture for Multi-Agent Development](../software-engineering/multi-agent-development-architecture.md), 실제 커밋 규약과 권한은 적용 대상 repository가 소유합니다.

- [Git — git-commit](https://git-scm.com/docs/git-commit), [git-log](https://git-scm.com/docs/git-log), [git-push](https://git-scm.com/docs/git-push) — 커밋 스냅샷·검색·원격 공유
- [Pro Git — Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) — amend·rebase와 기존 SHA의 변화
- [Git — git-notes](https://git-scm.com/docs/git-notes), [git-reflog](https://git-scm.com/docs/git-reflog) — 별도 notes ref와 도달성·이력 복구 한계
- [GitHub — Pull request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges) — Squash Merge의 중간 커밋 처리
- [GitHub — Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) — 게시된 민감정보의 복구 및 제거 어려움
