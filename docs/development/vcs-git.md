---
description: 저장소 고유 branch 정책, 병렬 작업 격리, branch naming, Git history 안전성과 commit convention을 확인할 때 사용합니다.
---

# VCS / Git

이 문서는 이 repository의 **VCS와 Git 정책**을 소유합니다. 전체 개발 작업의 순서나 GitHub 협업 workflow는 정의하지 않습니다.

## Authority

- 저장소 고유 VCS/Git 정책 → 이 문서
- Git 명령과 worktree, ref, history의 동작 의미 → Git 공식 문서
- agent runtime의 작업 공간, worktree와 ephemeral branch 동작 → 해당 runtime의 공식 문서
- GitHub의 Pull Request, Merge, Ruleset과 서버 측 강제 규칙 → [GitHub](github.md)
- verification과 merge-blocking evidence → [Testing](testing.md)

Runtime이 편의를 위해 branch나 worktree를 자동으로 만들더라도 이 repository의 변경 격리와 history 안전성 정책이 자동으로 완화되지는 않습니다.

## Working State Safety

Git으로 변경하기 전에 **현재 repository, worktree, branch 또는 ref, base commit과 working tree 상태를 식별**합니다. Agent도 작업 공간이 `clean` 상태라고 가정하지 않습니다.

- 작업 공간에 여러 Git root가 있으면 각 repository의 ref, base commit, working state와 변경 ownership을 따로 확인합니다. 한 repository에서 확인한 상태를 다른 repository에 일반화하지 않습니다.
- 이미 존재하는 수정, untracked file과 commit은 이번 작업의 소유라고 확인되기 전까지 보존합니다.
- 환경을 `clean` 상태로 만들기 위해 다른 작업을 reset하거나 버리거나 삭제하거나 임의로 stash하지 않습니다.
- `reset --hard`, `switch --discard-changes`, `checkout -f`, `clean`, stash 삭제와 강제 branch reset처럼 작업을 잃을 수 있는 조작은 이번 작업이 해당 상태를 소유하고 있거나 별도 권한이 있을 때만 사용합니다.
- 기존 작업과 안전하게 분리할 수 없으면 덮어쓰지 않고 별도 worktree, clone 또는 runtime sandbox로 격리합니다.

## Parallel Work Isolation

**동시에 파일을 변경하는 독립 작업은 같은 working tree를 공유하지 않습니다.** 각 변경 작업은 독립된 작업 공간과 dedicated branch를 사용합니다.

Git 환경에서는 `git worktree`가 같은 repository history를 공유하면서 working tree와 `HEAD`, index를 분리하는 기본 수단입니다. Runtime이 자체 worktree, ephemeral checkout 또는 sandbox를 제공하면 동등한 격리 수단으로 사용할 수 있습니다.

- Branch 이름만으로 파일 변경이 격리되지는 않습니다. 병렬 변경 작업은 working tree도 분리합니다.
- 독립 작업은 독립 branch를 사용합니다. 여러 agent나 사람이 같은 branch를 동시에 수정하려면 그 공유가 의도적으로 조정되어 있어야 합니다.
- Runtime이 격리된 실행 내부에서 detached `HEAD`나 임시 ref를 사용해도 괜찮지만, repository에 지속시키는 변경은 integration 전에 dedicated branch에 명확히 귀속되어야 합니다.
- Worktree는 Git metadata 전체를 격리하지 않습니다. 일반 `refs/*`와 기본 repository config는 worktree 사이에 공유될 수 있으므로 stash, shared ref와 repository-level config를 작업별 임시 상태처럼 사용하지 않습니다.
- 같은 branch를 여러 worktree에서 강제로 checkout하여 동시에 변경하는 방식은 격리로 간주하지 않습니다.

## Branch Policy

- `main`은 직접 수정하지 않습니다.
- 변경은 dedicated branch에서 수행합니다.
- 기본 target branch는 `main`입니다. 실제 작업 base는 작업 시작 시 확인한 **base ref와 commit**으로 식별합니다.
- 최신 target에서 시작해야 하는 작업은 remote target의 최신성을 확인합니다. 확인할 수 없으면 확인한 base commit과 최신성 불확실성을 보존하고 오래된 로컬 state를 최신이라고 단정하지 않습니다.
- PR head, feature branch, prepared snapshot이나 특정 commit처럼 다른 base가 명시되거나 runtime이 작업 기준을 이미 확정한 경우에는 그 base를 보존합니다. 최신 `main`으로 임의 이동하지 않습니다.
- 다른 base가 필요한 stacked change도 해당 target을 따릅니다.
- 서로 독립적으로 검토하거나 폐기할 수 있는 변경은 branch도 분리합니다. Agent session, model, RPI 단계 같은 실행 세부사항만을 이유로 branch를 추가하지 않습니다.
- `main`으로의 integration은 [GitHub](github.md)의 Pull Request와 Merge 정책을 따릅니다.

## Branch Naming

직접 생성하고 이름을 제어할 수 있는 branch의 기본 이름:

```text
<owner>/<type>/<topic>
```

- `owner`: 작업 주체를 식별하는 짧은 이름. 작업 주체를 나타내는 표식이며 permission이나 approval을 뜻하지 않습니다.
- `type`: 변경 성격을 나타내는 짧은 category. 고정 enum은 두지 않으며 `docs`, `feat`, `fix`, `chore`처럼 의미가 명확한 값을 사용합니다.
- `topic`: 변경 대상을 나타내는 간결한 kebab-case 이름

각 segment는 특별한 이유가 없으면 lowercase와 kebab-case를 사용합니다. Branch 이름은 **누가 어떤 종류의 무엇을 바꾸는지**를 빠르게 식별하는 데 필요한 정보만 담고 model 이름, session ID나 작업 단계 같은 일시적 metadata를 넣지 않습니다.

Runtime이나 hosting platform이 branch를 생성하고 naming을 소유하면 해당 native naming을 허용합니다. Convention을 맞추기 위해 runtime lifecycle이나 추적성을 깨는 rename을 요구하지 않으며, 대신 작업과 실제 branch/ref의 대응을 식별할 수 있어야 합니다.

## History Safety

History 재작성은 작업 편의를 위한 기본 동작이 아닙니다.

- `main` history는 재작성하지 않습니다.
- `amend`, `rebase`와 branch reset은 현재 작업이 독점적으로 소유하는 dedicated branch에서만 수행합니다.
- 다른 작업 주체가 branch를 사용하거나 그 tip을 기준으로 작업했을 가능성이 있으면 fast-forward가 아닌 재작성을 임의로 수행하지 않습니다.
- 이미 공개된 remote branch를 재작성해야 한다면 먼저 예상 remote tip을 확인하고 실제 repository 정책이 허용하는 범위에서 원격 ref의 기대값을 검증하는 방식으로 갱신합니다. Git CLI에서는 무조건적인 `--force`보다 `--force-with-lease`를 우선합니다.
- Commit 수를 줄이거나 history를 보기 좋게 만들기 위한 이유만으로 공유 branch를 재작성하지 않습니다. 최종 Merge 방식은 [GitHub](github.md)가 소유합니다.

## Commit Messages

직접 작성하는 commit message의 authoring convention은 repository root의 [`.gitmessage`](../../.gitmessage)가 authoritative source입니다. 사람이 작성하든 agent가 작성하든 같은 convention을 적용하며 agent 실행 과정이나 model 표기를 위한 별도 commit format을 만들지 않습니다.

- [`scripts/validate_commit_msg.py`](../../scripts/validate_commit_msg.py)는 deterministic하게 검사할 수 있는 최소 subset을 검증합니다.
- [`lefthook.yml`](../../lefthook.yml)의 `commit-msg` hook이 validator를 실행합니다.
- Validator가 검사하지 않는 `.gitmessage`의 human convention까지 validator의 contract로 확대 해석하지 않습니다.

## Upstream References

- [Git worktree](https://git-scm.com/docs/git-worktree) — 여러 working tree, shared ref와 worktree-specific state
- [Git switch](https://git-scm.com/docs/git-switch) — branch 전환, detached `HEAD`와 local change 보존 semantics
- [Git push](https://git-scm.com/docs/git-push) — fast-forward와 `--force-with-lease`
- [OpenAI Codex](https://openai.com/codex/) — multi-agent 작업의 worktree와 cloud environment 사례
- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees) — 병렬 session과 subagent의 worktree 격리, base 선택 사례
- [Cursor worktrees](https://cursor.com/docs/configuration/worktrees) — 병렬 agent와 model candidate를 worktree로 격리하는 사례
- [GitHub Copilot cloud agent risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations) — runtime이 생성하는 전용 branch와 write boundary 사례

Vendor별 branch 생성, cleanup, handoff와 session lifecycle은 빠르게 바뀔 수 있으므로 이 문서에 복제하지 않고 해당 runtime 공식 문서를 따릅니다.

## Boundary

- Issues, Pull Requests, PR Reviews, PR Merge, Rulesets와 Actions → [GitHub](github.md)
- 변경 대상의 작성 원본 선택 → [작성 원본과 권한](source-authority.md)
- verification과 merge-blocking evidence → [Testing](testing.md)

이 문서는 일반적인 Git 사용법이나 repository-wide change workflow를 정의하지 않습니다.
