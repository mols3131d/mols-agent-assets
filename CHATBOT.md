# `CHATBOT.md`

이 파일은 이 repository를 작업하는 chatbot의 **compatibility entrypoint**입니다. Chat runtime에서 가능한 한 local agent harness와 같은 repository context discovery가 작동하도록 연결합니다.

## Bootstrap

1. 먼저 root [`AGENTS.md`](AGENTS.md)를 읽고 현재 작업에 적용되는 repository instruction을 따릅니다.
1. [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)를 읽고 아래 routing table의 trigger를 참고해 현재 작업에 필요한 Agent Asset만 선택합니다. 아래 표는 route contract를 대체하지 않습니다.
1. 구체적인 GitHub target(repository, path, ref, Pull Request, Issue, check, workflow, release 등)을 대상으로 작업하거나 GitHub Plugin, connector 또는 tool로 target-dependent action을 수행한다면 `github-context`를 필수로 선택합니다. 이름 있는 target의 ID/ref만 더 식별해야 하는 경우도 concrete target으로 봅니다.
1. `github-context`가 필요한 경우 downstream target read/review/change/tool action보다 먼저 로드하고, 현재 repository/ref/object, 적용되는 repository instruction과 필요한 live GitHub state를 확인합니다. Root instruction·route를 읽거나 `github-context`를 로드·수행하는 데 필요한 좁은 GitHub read는 context discovery 자체이므로 gate 완료 전에도 수행할 수 있지만, 그 결과에 의존하는 downstream 판단이나 action은 gate 완료 후에만 수행합니다.
1. 아직 concrete repository 또는 GitHub object가 하나도 특정되지 않은 broad discovery는 `github-context`보다 먼저 수행할 수 있습니다. Discovery가 concrete target을 식별하면 이후 downstream target-dependent action 전에 `github-context` loading을 완료합니다.
1. 작업 대상 경로가 정해지면 `github-context`가 관련 ref의 repository root부터 해당 경로까지 적용되는 instruction과 task-relevant Agent Asset을 확인하도록 합니다. Route는 [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)의 가장 좁은 유효 route를 사용하며, `github-context`를 포함한 필요한 Asset을 좁은 family 하나로 모두 노출할 수 없을 때만 `all`을 사용합니다. 선택한 route 안에서도 task-relevant Skill만 로드합니다.
1. 작업 범위, target repository, ref/object 또는 대상 경로가 실질적으로 바뀌면 적용되는 instruction, GitHub context와 route selection을 다시 평가합니다.

## Git / GitHub 문서 라우팅

여러 trigger가 동시에 맞으면 필요한 문서를 함께 읽습니다. 일반적인 Git/GitHub 개념 설명만 요청하고 이 repository의 policy나 state가 판단에 필요하지 않으면 repository-local 문서를 강제로 로드하지 않습니다. 표는 **언제 어디로 갈지**만 연결하며 각 문서의 정책을 복제하지 않습니다.

| Trigger | Load | 역할 |
| --- | --- | --- |
| working tree, worktree, branch, ref, base, commit, amend, rebase, reset, cherry-pick, stash, push, force update, Git history, branch naming | [`docs/development/vcs-git.md`](docs/development/vcs-git.md) | repository의 VCS/Git 상태·history·branch 안전성 |
| commit message를 작성하거나 검토 | [`docs/development/vcs-git.md`](docs/development/vcs-git.md), [`.gitmessage`](.gitmessage) | commit authoring convention과 그 소유 관계 |
| Issue, Pull Request, PR Review, PR comment, Merge, Ruleset, GitHub Actions, coding agent, automation, GitHub permission·collaboration | [`docs/development/github.md`](docs/development/github.md) | repository의 GitHub 협업·권한·surface 정책 |
| CI, PR Gate, GitHub Actions workflow orchestration, required check, trigger, blocking·deferred evidence, projection gate, branch push와 PR CI | [`docs/development/ci.md`](docs/development/ci.md) | `main` admission과 CI evidence orchestration |
| Issue/PR/Review/comment 본문을 작성·재작성·형식 검토 | [`docs/development/github.md`](docs/development/github.md), [`.github/templates/README.md`](.github/templates/README.md), 아래 surface template | cross-surface 작성 의미와 실제 rendering structure |
| format, formatter, `format-changed`, Ruff·rumdl·Biome을 통한 repository file 정규화 | [`docs/development/formatting.md`](docs/development/formatting.md) | formatting write path와 automation boundary |
| 문서 frontmatter, `INDEX.tsv`, Agent Asset routing, Rulesync-managed asset validation | [`docs/development/validation.md`](docs/development/validation.md) | repository-owned validation 범위와 실행 경계 |
| test, pytest, deterministic test, repository-owned executable behavior | [`docs/development/testing.md`](docs/development/testing.md) | deterministic test evidence의 의미와 범위 |
| Agent Asset behavior, model/runtime evidence, behavioral regression·evaluation | [`docs/development/evaluation.md`](docs/development/evaluation.md) | test와 behavioral eval의 경계와 evidence 해석 |

GitHub text를 작성·재작성·형식 검토할 때는 실제 surface에 맞는 template만 추가로 읽습니다.

| Surface | Template |
| --- | --- |
| Issue | [`.github/templates/issue.md`](.github/templates/issue.md) |
| Pull Request description | [`.github/templates/pull-request.md`](.github/templates/pull-request.md) |
| PR Review | [`.github/templates/pull-request-review.md`](.github/templates/pull-request-review.md) |
| PR conversation comment | [`.github/templates/pull-request-comment.md`](.github/templates/pull-request-comment.md) |
| PR inline review comment | [`.github/templates/pull-request-inline-comment.md`](.github/templates/pull-request-inline-comment.md) |

## Agent Asset 라우팅

이 표는 repository 작업에서 자주 교차 적용되는 Asset의 **selection trigger**만 명시합니다. 실제 source와 전체 후보는 [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)에서 선택합니다.

| Trigger | Select | Boundary |
| --- | --- | --- |
| 구체적인 GitHub repository/path/ref/PR/Issue/check/workflow/release를 읽기·검토·변경하거나 GitHub Plugin·connector·tool로 해당 target에 action을 수행, 또는 이미 확정된 GitHub target의 follow-up | `github-context` | downstream target-dependent action 전에 live repository/ref/object와 적용 context를 확인합니다. 이름 있는 target의 ID/ref resolution도 concrete로 봅니다. 아직 concrete repository/object가 없는 broad discovery와 generic Git/GitHub 설명에는 선택하지 않습니다. |
| CI architecture, PR Gate, merge gate, blocking·deferred evidence, impact routing, projection gate 또는 maintenance automation을 설계·검토·재설계 | `mols-ci-design` | CI의 admission evidence system을 설계·handoff하며 workflow 구현은 명시적으로 요청된 경우에만 수행합니다. |
| `CHATBOT.md` compatibility, chat runtime first-hop, repository entry/router를 생성·수정·복구하거나 그 compatibility를 검토 | `mols-chatbot-bootstrap` | bootstrap과 routing 연결을 다루며 repository policy를 새로 소유하지 않습니다. |
| Skill, Rule, scoped instruction, agent/subagent 또는 agent behavior를 구성하는 bounded asset을 작성·수정·단순화·리팩터링·리뷰·검증·평가 | `mols-agent-asset` | authoring, review, validation, evaluation의 task-specific contract를 소유하며 실제 evidence보다 강한 결론을 만들지 않습니다. |
| Agent Asset을 찾기·선택·로드·설치·동기화·이관 | `mols-agent-asset-find` | 기존 Asset의 discovery와 적용이 주 작업일 때 선택합니다. |
| 사용자가 RPI, 개선 루프, 재귀 루프, 심층 루프를 요구하거나 복합 작업에 반복 Research → Plan → Implementation → Review 및 점진적 context/capability orchestration이 필요 | `mols-loops` + task-specific Asset | Loops가 작업 domain Asset의 authority나 내부 procedure를 대체하지 않습니다. |

`CHATBOT.md`는 repository policy, Agent Asset behavior 또는 routing semantics를 재정의하지 않습니다. 연결된 canonical source와 [`.agents/route/ROUTE.md`](.agents/route/ROUTE.md)가 항상 authoritative합니다.
