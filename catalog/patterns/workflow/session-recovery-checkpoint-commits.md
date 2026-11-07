---
description: 세션 단절·에이전트 교체 후 Git 커밋 메시지와 스냅샷에서 작업 상태·검증·다음 시작점을 복구하려는 경우 참고하는 체크포인트 패턴입니다.
---

# Session Recovery Checkpoint Commits

채팅 세션이 갑자기 끊기면 코드는 남아도 결정 이유, 검증 상태와 다음 작업은 사라질 수 있습니다. **커밋 메시지에 해당 커밋의 코드 스냅샷을 해석하고 다시 이어가는 데 필요한 정보를 함께 남기는 방식**은 별도 진행 로그 없이도 재개 비용을 줄일 수 있습니다.

이 패턴은 모든 에이전트 행동을 기록하는 *event log*가 아니라 **의미 있는 작업 상태의 checkpoint**입니다. 커밋을 자동으로 생성·푸시하거나 다른 세션을 시작해 주는 기능은 아닙니다.

> **주의 — 좋은 커밋이 우선입니다.** 커밋은 의미상 완결된 변경과 관련 검증을 담아 이해·검토·되돌리기 쉬워야 합니다. 세션 복구만을 위해 변경을 임의로 쪼개거나, 정상 동작하지 않는 중간 상태를 통합 가능한 커밋으로 취급하지 않습니다. 커밋 메시지만으로 세션 복구의 완전성을 보장할 수 없습니다. 이 패턴은 좋은 커밋의 보조 수단이며 테스트·리뷰·작업 계획·정본 문서를 대신하지 않습니다.

## Core

**좋은 커밋을 남기는 과정에서 자연스럽게 작업 재개에 필요한 단서도 보존합니다.** 코드 변경은 diff에서 확인하고, 메시지는 변경 이유와 쉽게 재구성할 수 없는 판단을 설명합니다.

- **변경 단위 우선:** 세션·에이전트·작업 단계가 아니라 독립적으로 이해·검토할 수 있는 변경을 기준으로 커밋합니다. 복구를 위해 별도의 커밋을 만들지 않습니다.
- **이유 중심의 본문:** 제목은 무엇이 달라졌는지, 본문은 왜 그렇게 했는지 설명합니다. 중요한 설계 결정, 제약, 검증 한계나 후속 작업이 있을 때만 자연스러운 문장으로 덧붙입니다.
- **컨텍스트 최적화:** 다음 사람이 **적은 토큰 비용**으로 읽고 **적은 추론 비용**으로 맥락을 재구성할 수 있도록 중복된 변경 목록과 형식적 상태 보고를 피합니다. PR·명세 등의 내용을 복제하지 않고 참조하되, 필요한 판단 근거를 과도하게 압축하지 않습니다.
- **상태와 근거의 경계:** 커밋 메시지는 작성 당시의 기록입니다. 검사 결과를 적을 때는 실제 확인한 범위만 설명하고, 재개할 때는 현재 Git 상태·계약·검증 근거를 다시 확인합니다.

## Sample Commit Messages

커밋 제목·본문·footer의 형식은 각 프로젝트의 규약을 따릅니다. 아래 템플릿은 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)를 **참고한 작성 예시**일 뿐이며, 이 패턴은 Conventional Commits의 채택·준수를 전제하거나 요구하지 않습니다. 다른 형식의 커밋 메시지에도 동일한 복구 맥락을 담을 수 있습니다.

### Sample Template

```text
<type>[optional scope][!]: <description>

[optional body]

[optional continuation context: only what the body does not cover]

[optional footer(s)]
```

- **제목·본문:** 프로젝트의 기존 형식으로 변경 내용과 이유를 전달합니다. 위 예시의 `type`·`scope`·`!` 표기는 Conventional Commits에서 빌린 것이며 패턴의 필수 요소가 아닙니다.
- **Continuation context:** 검증 범위·남은 작업·다음 확인 지점 등 **기존 본문에서 알 수 없는 복구 필수 정보만** 보완합니다. 짧으면 본문에 합치고, 중복되거나 불필요하면 문단 자체를 생략합니다.
- **Footer:** 프로젝트에서 사용하는 경우에만 작성합니다. 위 예시의 footer 배치 역시 강제하지 않습니다.

커밋의 변경 이유가 자명하면 본문 없이 제목만 남겨도 됩니다. 복구 문단이 커밋 품질을 대신하거나, 별도의 `Recovery:` 표식·고정 스키마를 요구하지 않습니다.

### Examples

제목만으로 충분한 변경:

```text
fix(auth): reject expired access tokens
```

변경 이유 외에 재개에 필요한 검증·후속 정보를 남길 가치가 있는 변경:

```text
refactor(auth): extract token expiry validation

Keep expiry rules separate from HTTP middleware so unit tests
can exercise the policy without request setup. Preserve existing
middleware behavior.

Token unit tests pass, but middleware integration is not yet
verified. Confirm the request schema before integration tests.
```

두 번째 예시는 본문에 없는 **검증 범위와 다음 확인 지점**만 추가합니다. 예시의 제목 형식을 따르는 것보다 기존 메시지와 중복 없이 맥락을 전달하는 것이 중요합니다.

## Capture

1. 현재 repository, branch/ref, worktree와 변경 소유권을 확인합니다. 다른 작업자의 수정과 미추적 파일을 자기 작업으로 가정하지 않습니다.
2. **우선 좋은 커밋인지 판단합니다.** 한 가지 의미 있는 변경으로 이해·검토할 수 있고 관련 검증과 함께 보존할 가치가 있을 때 이번 작업의 변경만 stage합니다. 세션 복구 자체가 커밋을 추가할 이유는 아닙니다.
3. 커밋될 변경과 검증 결과를 대조합니다. 제목만으로 의도가 충분하지 않다면 본문에 이유와 중요한 결정·제약을 설명합니다. 후속 작업이나 검증 한계는 다음 판단에 중요할 때만 덧붙이며 미실행 테스트를 통과로 적지 않습니다.
4. 다른 machine·session·agent가 원격에서 이어야 한다면 허용된 원격 ref에 게시하고, 게시한 SHA가 조회되는지 확인합니다. 로컬 커밋만으로는 다른 환경에서 복구할 수 없습니다.

커밋 메시지에 **자기 자신의 SHA를 미리 써 넣으려 하지 않습니다.** SHA는 커밋 후 생성되는 식별자이고, 메시지를 수정하면 다른 커밋이 됩니다. 필요한 곳에서 생성된 SHA를 별도로 참조할 수 있습니다.

## Resumption

1. **대상 확인:** 이어받을 작업·repository·branch/PR을 식별하고 현재 HEAD, working tree와 untracked 변경을 확인합니다. 원격 작업을 이어받는다면 필요에 따라 원격 ref의 최신 상태도 조회합니다. 다른 작업을 덮어쓰며 정리하지 않습니다.
2. **체크포인트 검색:** 해당 작업의 커밋을 찾아 본문과 스냅샷을 읽습니다. HEAD가 반드시 그 작업의 마지막 체크포인트인 것은 아닙니다.
3. **최신성 검증:** 해당 커밋 이후의 변경, ref 이동·재작성과 외부 계약 변화를 대조합니다. 메시지에 적힌 후속 계획은 현재 작업 상태와 맞는지 확인한 뒤 참고합니다.
4. **재검증 후 진행:** 이전 검사 결과가 여전히 유효한지 판단하고 필요한 최소 검증을 수행한 뒤 다음 행동을 선택합니다. 내용이 충돌하면 현재 근거에 맞춰 계획을 수정합니다.

Git CLI를 사용하는 경우 다음과 같이 조사할 수 있습니다. **이미 올바른 작업 브랜치를 선택한 상황에서의 로컬 조회 예시**이며, 이 명령만으로 원격의 최신 상태를 확인한 것은 아닙니다.

```sh
git status --short --branch
git log -8 --format='%h %s'
git show --format=fuller --stat HEAD
git diff HEAD
```

공유 브랜치라면 최근 커밋 몇 개만 보지 않고 작업·PR·SHA와 연결된 **관련 이력**을 찾습니다. `git diff HEAD`는 tracked 변경만 보여 주므로 untracked 파일은 `git status` 등으로 따로 확인합니다.

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

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) — 샘플 메시지 형식을 참고한 자료(채택·준수 필수 아님)
- [Git — git-commit](https://git-scm.com/docs/git-commit), [git-log](https://git-scm.com/docs/git-log), [git-push](https://git-scm.com/docs/git-push) — 커밋 스냅샷·검색·원격 공유
- [Pro Git — Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) — amend·rebase와 기존 SHA의 변화
- [GitHub — Pull request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges) — Squash Merge의 중간 커밋 처리
- [GitHub — Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) — 게시된 민감정보의 복구 및 제거 어려움
- [Google — Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) — 하나의 독립된 변경과 관련 테스트를 검토·통합하기 쉽게 유지하는 원칙
- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) — 장기 실행 에이전트에서 진행 기록과 Git history를 함께 사용하는 사례
- [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/) — 작업 계획·진행·결정을 repository-local 지식으로 보존하는 사례
