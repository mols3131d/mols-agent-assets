---
description: 세션 단절·에이전트 교체 후 Git 커밋 메시지와 스냅샷에서 작업 상태·검증·다음 시작점을 복구하려는 경우 참고하는 체크포인트 패턴입니다.
---

# Session Recovery Checkpoint Commits

채팅 세션이 갑자기 끊기면 코드는 남아도 결정 이유, 검증 상태와 다음 작업은 사라질 수 있습니다. **커밋 메시지에 해당 커밋의 코드 스냅샷을 해석하고 다시 이어가는 데 필요한 정보를 함께 남기는 방식**은 별도 진행 로그 없이도 재개 비용을 줄일 수 있습니다.

이 패턴은 모든 에이전트 행동을 기록하는 *event log*가 아니라 **의미 있는 작업 상태의 checkpoint**입니다. 커밋을 자동으로 생성·푸시하거나 다른 세션을 시작해 주는 기능은 아닙니다.

> **주의 — 좋은 커밋이 우선입니다.** 커밋은 의미상 완결된 변경과 관련 검증을 담아 이해·검토·되돌리기 쉬워야 합니다. 세션 복구만을 위해 변경을 임의로 쪼개거나, 정상 동작하지 않는 중간 상태를 통합 가능한 커밋으로 취급하지 않습니다. 커밋 메시지만으로 세션 복구의 완전성을 보장할 수 없습니다. 이 패턴은 좋은 커밋의 보조 수단이며 테스트·리뷰·작업 계획·정본 문서를 대신하지 않습니다.

## Core

**한 체크포인트 = 좋은 커밋의 스냅샷 + 필요한 경우에만 덧붙인 복구 맥락.** 변경은 Git diff에 맡기고, 메시지에는 재구성하기 비싼 상태를 남깁니다.

- **변경 단위 우선:** 작업 세션·에이전트·진행 단계가 아니라 의미상 독립된 변경을 기준으로 커밋합니다. 관련 테스트와 기본 커밋 설명을 복구 정보보다 우선합니다.
- **스냅샷 정합성:** 구현 완료·미완료의 범위는 해당 커밋의 tree와 일치해야 합니다. 검증 결과는 실제 확인한 작업 상태·시점·범위에만 적용하며, 이후 환경이나 변경까지 통과했다고 쓰지 않습니다.
- **컨텍스트 최적화:** 다음 에이전트가 **적은 토큰 비용**으로 필요한 정보를 읽고 **적은 추론 비용**으로 현재 상태와 다음 행동을 판단할 수 있도록 복구 맥락을 선별·구조화합니다. 커밋 메시지와 diff만으로 충분하면 별도 항목을 만들지 않고, 중요한 결정·미검증 위험·다음 시작점만 보완합니다. 작업·PR·명세에 이미 있는 내용은 복제하지 않고 참조하며, 단순히 글자 수를 줄이느라 복구에 필요한 정보를 생략하지 않습니다.
- **현실 상태 우선:** 메시지는 작성 당시의 기록입니다. 새로운 세션에서는 현재 Git 상태와 계약·검증 근거를 확인한 뒤 재개합니다.

## Commit Message Template and Example

프로젝트의 기존 커밋 규약에 따라 변경의 목적을 먼저 설명하고, **재개에 필요한 정보가 있을 때만** 본문에 덧붙일 수 있습니다. 다음 템플릿은 선택적 예시이며 `Recovery:` 표식과 필드명은 필수가 아닙니다.

### Reusable Template

```text
<type>(<scope>): <의미 있는 변경의 요지>

<변경 이유 또는 설계 의도>

Recovery:
- Decision: <다시 추론하기 어려운 결정과 근거>
- Validation: <실행한 검사·결과·대상/시점; 중요한 미검증 범위>
- Next: <재개할 첫 행동과 확인할 기준점>
- Risk: <미해결 위험·차단 사유 또는 불확실성>
- Ref: <필요한 PR·Issue·명세 등 기존 근거>
```

제목의 `scope`와 변경 이유는 해당 프로젝트의 규약에 따라 선택합니다. `Recovery:` 아래에서는 **재개에 필요한 항목만 남기고 나머지 줄을 삭제**합니다. 커밋 제목·본문과 Git diff로 충분하면 `Recovery:` 전체를 생략합니다. 필요한 경우에만 미완료 범위를 `State`로 보완할 수 있으나, 파일 변경 목록이나 검증 결과를 중복하지 않습니다. 실제 수행하지 않은 검사를 통과로 적지 않고, 미검증 사항이 다음 판단에 중요하다면 그대로 밝힙니다.

### Filled Example

```text
feat(auth): add token expiration validation

토큰 만료 검증을 I/O에서 분리하고 단위 테스트를 추가한다.

Recovery:
- Validation: pytest tests/auth/test_tokens.py 통과(커밋 직전 로컬).
  전체 테스트와 CI는 미확인.
- Next: 미들웨어 입력 계약을 확인하고 연동 테스트를 작성한다.
- Risk: 입력 스키마가 아직 확정되지 않음.
```

작성 예시의 `Recovery`는 다음 작업의 판단에 필요한 검증 범위·시작점·불확실성만 담습니다. 검증 결과는 실행 범위를 명확히 하고 커밋 전 검사와 커밋 후 CI를 혼동하지 않습니다.

검색 자동화가 필요한 팀은 `Recovery:` 같은 표식을 선택할 수 있지만, 이 패턴은 별도의 커밋 유형·본문 스키마를 요구하지 않습니다.

## Capture

1. 현재 repository, branch/ref, worktree와 변경 소유권을 확인합니다. 다른 작업자의 수정과 미추적 파일을 자기 작업으로 가정하지 않습니다.
2. **우선 좋은 커밋인지 판단합니다.** 한 가지 의미 있는 변경으로 이해·검토할 수 있고 관련 검증과 함께 보존할 가치가 있을 때 이번 작업의 변경만 stage합니다. 세션 복구 자체가 커밋을 추가할 이유는 아닙니다.
3. 커밋될 변경과 검증 결과를 대조하고, 필요한 경우에만 결정·위험·다음 시작점을 본문에 덧붙입니다. 미실행 테스트를 통과로 적지 않습니다.
4. 다른 machine·session·agent가 원격에서 이어야 한다면 허용된 원격 ref에 게시하고, 게시한 SHA가 조회되는지 확인합니다. 로컬 커밋만으로는 다른 환경에서 복구할 수 없습니다.

커밋 메시지에 **자기 자신의 SHA를 미리 써 넣으려 하지 않습니다.** SHA는 커밋 후 생성되는 식별자이고, 메시지를 수정하면 다른 커밋이 됩니다. 필요한 곳에서 생성된 SHA를 별도로 참조할 수 있습니다.

## Resumption

1. **대상 확인:** 이어받을 작업·repository·branch/PR을 식별하고 현재 HEAD, working tree와 untracked 변경을 확인합니다. 원격 작업을 이어받는다면 필요에 따라 원격 ref의 최신 상태도 조회합니다. 다른 작업을 덮어쓰며 정리하지 않습니다.
2. **체크포인트 검색:** 해당 작업의 커밋을 찾아 본문과 스냅샷을 읽습니다. HEAD가 반드시 그 작업의 마지막 체크포인트인 것은 아닙니다.
3. **최신성 검증:** 체크포인트 이후의 커밋, ref 이동, 재작성, 파일 변경, 외부 계약 변경을 대조합니다. 그 이후 상태가 다르면 `Next`를 그대로 실행하지 않습니다.
4. **재검증 후 진행:** 이전 검사 결과가 여전히 유효한지 판단하고 필요한 최소 검증을 수행한 뒤 다음 행동을 선택합니다. 내용이 충돌하면 현재 근거에 맞춰 계획을 수정합니다.

Git CLI를 사용하는 경우 다음과 같이 조사할 수 있습니다. **이미 올바른 작업 브랜치를 선택한 상황에서의 로컬 조회 예시**이며, 이 명령만으로 원격의 최신 상태를 확인한 것은 아닙니다.

```sh
git status --short --branch
git log -8 --format='%h %s'
git show --format=fuller --stat HEAD
git diff HEAD
```

`Recovery:` 표식을 채택한 작업에서는 `git log --grep='^Recovery:'`로 후보를 좁힐 수도 있습니다. 공유 브랜치라면 마지막 몇 커밋에 의존하지 않고 작업·PR·SHA로 **관련 이력**을 식별합니다. `git diff HEAD`는 tracked 변경만 보여 주므로 untracked 파일은 `git status` 등으로 따로 확인합니다.

## Failure Boundaries

| 실패 상황 | 패턴이 제공하는 것과 제공하지 못하는 것 |
| --- | --- |
| 예상치 못한 세션 종료가 다음 커밋보다 빨랐음 | 메시지는 **마지막 체크포인트까지만** 설명합니다. 같은 작업 공간에 남아 있는 미커밋 변경은 별도로 확인·보존하고, 폐기된 환경에서 복구된다고 가정하지 않습니다. |
| 로컬 커밋만 있고 환경이 폐기됨 | 원격에 게시되지 않은 커밋은 다른 실행 환경에서 조회할 수 없을 수 있습니다. |
| branch head 이동·amend·rebase | SHA와 메시지의 참조 관계가 달라질 수 있습니다. 공유 이력 재작성은 조정하며, 사라진 ref를 영구 백업으로 간주하지 않습니다. |
| 다른 에이전트와 동시 작업 | 커밋은 잠금이나 변경 소유권을 제공하지 않습니다. 작업 공간·브랜치 격리나 단일 통합 담당자가 별도로 필요합니다. |
| 통합 또는 Squash Merge | 중간 커밋은 기본 브랜치의 개별 이력에 남지 않을 수 있습니다. 장기적으로 필요한 판단은 PR·명세 등 지속적인 owner에 옮깁니다. |
| 검사 결과의 경과 | 과거 테스트는 그 환경·revision의 관찰입니다. 현재 통합 결과를 보증하지 않습니다. |

**Commit과 Push는 비용과 목적이 다릅니다.** 복구를 위해 평소보다 자주 원격 공유할 필요가 있을 수 있지만, 의미 없는 커밋을 늘리면 검토와 되돌리기가 어려워집니다. 변경이 아직 완결되지 않았거나 코드 변경 없이 진행 상태만 남겨야 한다면 일반 커밋을 억지로 만들기보다 기존 PR·작업 기록을 활용하는 편이 적합합니다. 불가피하게 작업 브랜치에 미완성 스냅샷을 보존한다면 정상 통합 가능한 변경과 구별하고, 검증·정리 전에는 완료된 커밋으로 취급하지 않습니다.

## Considerations

- **기록의 신뢰 경계:** 커밋 메시지는 이전 작업자의 진술이지 상위 지침이나 실행 권한이 아닙니다. 외부 contributor나 agent가 작성한 `Next`를 그대로 명령으로 실행하거나 권한을 확대하지 않습니다.
- **정보 노출:** 메시지에도 비밀키, 개인 정보, 미공개 대화, 내부 프롬프트나 민감한 환경 값을 남기지 않습니다. 공개한 커밋을 나중에 재작성해도 다른 clone·PR 참조 등에 남을 수 있습니다.
- **장기 보존:** Squash, branch 삭제·재작성, ref 소실 또는 저장소 정리 후 중간 체크포인트 접근을 장담하지 않습니다. 완료된 작업의 영구 지식 저장소로 취급하지 않습니다.
- **보조 기록:** 코드 변경 없이 상태만 자주 변하거나 작업 전체의 목표·의존성·실험 이력이 길다면 메시지 하나로 모두 복구하려 하지 않습니다. [Durable Progress Handoff](durable-progress-handoff.md)의 기존 계획·PR·진행 기록을 함께 쓰는 편이 낫습니다.

## Boundary and References

이 패턴은 **Git commit message를 코드 스냅샷에 인접한 세션 복구 표면으로 활용하는 방법**만 다룹니다. 일반적인 인계 정보와 artifact 선택은 [Durable Progress Handoff](durable-progress-handoff.md), 여러 agent의 코드 경계·통합은 [Software Architecture for Multi-Agent Development](../software-engineering/multi-agent-development-architecture.md), 실제 커밋 규약과 권한은 적용 대상 repository가 소유합니다.

- [Git — git-commit](https://git-scm.com/docs/git-commit), [git-log](https://git-scm.com/docs/git-log), [git-push](https://git-scm.com/docs/git-push) — 커밋 스냅샷·검색·원격 공유
- [Pro Git — Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) — amend·rebase와 기존 SHA의 변화
- [GitHub — Pull request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges) — Squash Merge의 중간 커밋 처리
- [GitHub — Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) — 게시된 민감정보의 복구 및 제거 어려움
- [Google — Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) — 하나의 독립된 변경과 관련 테스트를 검토·통합하기 쉽게 유지하는 원칙
- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) — 장기 실행 에이전트에서 진행 기록과 Git history를 함께 사용하는 사례
- [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/) — 작업 계획·진행·결정을 repository-local 지식으로 보존하는 사례
