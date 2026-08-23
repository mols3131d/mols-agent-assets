---
description: 저장소 고유 branch policy, 병렬 작업 격리, branch naming, Git history 안전성과 commit convention을 확인할 때 사용합니다.
---

# VCS / Git

이 문서는 이 repository의 **VCS와 Git policy**를 소유합니다. 전체 개발 작업의 순서나 GitHub collaboration workflow는 정의하지 않습니다.

## Authority

- 저장소 고유 VCS/Git policy → 이 문서
- Git command와 worktree, ref, history semantics → Git 공식 문서
- agent runtime의 workspace, worktree와 ephemeral branch 동작 → 해당 runtime의 공식 문서
- GitHub의 Pull Request, Merge, Ruleset과 server-side enforcement → [GitHub](github.md)
- verification과 merge-blocking evidence → [Testing](testing.md)

Runtime이 편의를 위해 branch나 worktree를 자동으로 만들더라도 이 repository의 변경 격리와 history 안전성 policy가 자동으로 완화되지는 않습니다.

## Working State Safety

Git으로 변경하기 전에 **현재 repository, worktree, branch 또는 ref, base commit과 working tree 상태를 식별**합니다. Agent도 작업 공간이 clean하다고 가정하지 않습니다.

- 이미 존재하는 수정, untracked file과 commit은 이번 작업의 소유라고 확인되기 전까지 보존합니다.
- 환경을 clean하게 만들기 위해 다른 작업을 reset, discard, delete하거나 임의로 stash하지 않습니다.
- `reset --hard`, `switch --discard-changes`, `checkout -f`, `clean`, stash 삭제와 강제 branch reset처럼 작업을 잃을 수 있는 조작은 이번 작업이 해당 상태를 소유하고 있거나 별도 권한이 있을 때만 사용합니다.
- 기존 작업과 안전하게 분리할 수 없으면 덮어쓰지 않고 별도 worktree, clone 또는 runtime sandbox로 격리합니다.

## Parallel Work Isolation

**동시에 파일을 변경하는 독립 작업은 같은 working tree를 공유하지 않습니다.** 각 변경 작업은 독립된 작업 공간과 dedicated branch를 사용합니다.

Git 환경에서는 `git worktree`가 같은 repository history를 공유하면서 working tree와 `HEAD`, index를 분리하는 기본 수단입니다. Runtime이 자체 worktree, ephemeral checkout 또는 sandbox를 제공하면 동등한 격리 수단으로 사용할 수 있습니다.

- Branch 이름만으로 filesystem 변경이 격리되지는 않습니다. 병렬 write 작업은 working tree도 분리합니다.
- 독립 작업은 독립 branch를 사용합니다. 여러 agent나 사람이 같은 branch를 동시에 수정하려면 그 공유가 의도적으로 조정되어 있어야 합니다.
- Runtime이 isolated execution 내부에서 detached `HEAD`나 임시 ref를 사용해도 괜찮지만, repository에 지속시키는 변경은 integration 전에 dedicated branch에 명확히 귀속되어야 합니다.
- Worktree는 Git metadata 전체를 격리하지 않습니다. 일반 `refs/*`와 기본 repository config는 worktree 사이에 공유될 수 있으므로 stash, shared ref와 repository-level config를 task-local scratch state처럼 사용하지 않습니다.
- 같은 branch를 여러 worktree에서 강제로 checkout하여 동시 write하는 방식은 격리로 간주하지 않습니다.

## Branch Policy

- `main`은 직접 수정하지 않습니다.
- 변경은 dedicated branch에서 수행합니다.
- 기본 base는 current `main`입니다. 여기서 current는 단순히 로컬 `main`이라고 가정하지 않고 작업 시작 시점에 확인한 최신 target commit을 의미합니다.
- 최신 remote state를 확인할 수 없으면 확인한 base commit과 freshness 불확실성을 보존합니다. 오래된 로컬 state를 current `main`으로 단정하지 않습니다.
- 다른 base가 명시적으로 필요한 작업이나 stacked change는 해당 target을 따릅니다.
- 서로 독립적으로 review하거나 폐기할 수 있는 변경은 branch도 분리합니다. Agent session, model, RPI phase 같은 실행 세부사항만을 이유로 branch를 추가하지 않습니다.
- `main`으로의 integration은 [GitHub](github.md)의 Pull Request와 Merge policy를 따릅니다.

## Branch Naming

기본 branch 이름:

```text
<owner>/<type>/<topic>
```

- `owner`: 작업 주체를 식별하는 짧은 이름. 작업 ownership을 위한 label이며 permission이나 approval을 뜻하지 않습니다.
- `type`: 변경 성격을 나타내는 짧은 category. 고정 enum은 두지 않으며 `docs`, `feat`, `fix`, `chore`처럼 의미가 명확한 값을 사용합니다.
- `topic`: 변경 대상을 나타내는 간결한 kebab-case 이름

각 segment는 특별한 이유가 없으면 lowercase와 kebab-case를 사용합니다. Branch 이름은 **누가 어떤 종류의 무엇을 바꾸는지**를 빠르게 식별하는 데 필요한 정보만 담고 model 이름, session ID나 작업 단계 같은 일시적 metadata를 넣지 않습니다.

## History Safety

History rewrite는 작업 편의를 위한 기본 동작이 아닙니다.

- `main` history는 rewrite하지 않습니다.
- `amend`, `rebase`와 branch reset은 현재 작업이 독점적으로 소유하는 dedicated branch에서만 수행합니다.
- 다른 actor가 branch를 사용하거나 그 tip을 기준으로 작업했을 가능성이 있으면 fast-forward가 아닌 rewrite를 임의로 수행하지 않습니다.
- 이미 공개된 remote branch를 rewrite해야 한다면 먼저 예상 remote tip을 확인하고 live repository policy가 허용하는 범위에서 guarded update를 사용합니다. Git CLI에서는 blind `--force`보다 expected ref를 보호하는 `--force-with-lease`를 우선합니다.
- Commit 수를 줄이거나 history를 보기 좋게 만들기 위한 이유만으로 shared branch를 rewrite하지 않습니다. 최종 Merge 방식은 [GitHub](github.md)가 소유합니다.

## Commit Messages

직접 작성하는 commit message의 authoring convention은 repository root의 [`.gitmessage`](../../.gitmessage)가 authoritative source입니다. 사람이 작성하든 agent가 작성하든 같은 convention을 적용하며 agent lifecycle이나 model attribution을 위한 별도 commit format을 만들지 않습니다.

- [`scripts/validate_commit_msg.py`](../../scripts/validate_commit_msg.py)는 deterministic하게 검사할 수 있는 최소 subset을 검증합니다.
- [`lefthook.yml`](../../lefthook.yml)의 `commit-msg` hook이 validator를 실행합니다.
- Validator가 검사하지 않는 `.gitmessage`의 human convention까지 validator의 contract로 확대 해석하지 않습니다.

## Upstream References

- [Git worktree](https://git-scm.com/docs/git-worktree) — 여러 working tree, shared ref와 worktree-specific state
- [Git switch](https://git-scm.com/docs/git-switch) — branch 전환, detached `HEAD`와 local change 보존 semantics
- [Git push](https://git-scm.com/docs/git-push) — fast-forward와 `--force-with-lease`
- [OpenAI Codex app](https://openai.com/index/introducing-the-codex-app/) — multi-agent 작업에서 worktree isolation을 사용하는 현재 사례
- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees) — 병렬 agent session과 subagent를 worktree로 격리하는 현재 사례

Vendor-specific branch 생성, cleanup, handoff와 session lifecycle은 빠르게 바뀔 수 있으므로 이 문서에 복제하지 않고 해당 runtime 공식 문서를 따릅니다.

## Boundary

- Issues, Pull Requests, PR Reviews, PR Merge, Rulesets와 Actions → [GitHub](github.md)
- 변경 대상의 작성 원본 선택 → [작성 원본과 권한](source-authority.md)
- verification과 merge-blocking evidence → [Testing](testing.md)

이 문서는 일반적인 Git 사용법이나 repository-wide change workflow를 정의하지 않습니다.
