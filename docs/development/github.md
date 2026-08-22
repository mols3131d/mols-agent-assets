---
description: GitHub Issues, Pull Requests, PR Reviews, merges, Rulesets와 Actions의 repository-local policy와 authority boundary를 확인할 때 사용합니다.
---

# GitHub

이 문서는 이 repository의 **GitHub-specific collaboration policy**를 소유합니다. GitHub의 일반 사용법이나 하나의 end-to-end development workflow는 정의하지 않습니다.

## Authority

- repository-specific intent와 policy → 이 문서
- 현재 GitHub enforcement → live repository settings와 Rulesets
- GitHub platform semantics → GitHub 공식 문서
- verification과 evaluation evidence의 의미 → [Testing](testing.md), [Evaluation](evaluation.md)

문서의 policy와 live GitHub configuration이 다르면 둘을 임의로 합리화하지 않고 drift로 취급합니다.

## Issues

Issue는 idea, feedback, task, bug처럼 **논의하거나 추적할 work item**을 표현하는 GitHub object입니다.

- 모든 change에 Issue를 선행 조건으로 요구하지 않습니다.
- Issue와 Pull Request는 서로 다른 object입니다.
- PR에서 Issue를 link할 수 있지만, link는 traceability를 제공할 뿐 Issue를 PR lifecycle의 필수 단계로 만들지 않습니다.

## Pull Requests

Pull Request는 head branch의 변경을 base branch에 통합하도록 **제안하고 논의하는 GitHub object**입니다.

- `main` 대상 변경은 [VCS / Git](vcs-git.md)의 dedicated branch policy를 따르고 PR로 제안합니다.
- PR 생성은 review approval이나 merge readiness를 의미하지 않습니다.
- PR 안에 conversation, reviews, checks가 함께 보이더라도 각각의 책임은 구분합니다.

## PR Reviews

PR Review는 PR의 변경에 대한 **검토 판단과 feedback을 기록하는 GitHub review surface**입니다.

- `Comment`, `Approve`, `Request changes`는 review를 제출할 때 기록하는 decision입니다.
- Automated check나 test success는 PR Review가 아니며, Review도 deterministic verification을 대체하지 않습니다.
- Required review 수, stale approval 처리, blocking review 같은 enforcement는 live Rulesets가 소유합니다.
- Review 방법론이나 품질 기준 자체는 이 문서가 재정의하지 않습니다.

## PR Merge

PR Merge는 PR의 변경을 base branch에 **실제로 통합하는 finalizing operation**입니다.

- PR 존재, approval, check success와 Merge는 서로 다른 상태와 operation입니다.
- Merge는 target branch에 적용되는 required reviews, required checks와 기타 GitHub admission rule을 만족한 뒤 수행합니다.
- 이 repository의 `main` PR은 **squash merge**를 사용합니다. Live repository settings가 이 policy를 enforce해야 합니다.

## Rulesets

Rulesets는 branch와 PR에 대한 GitHub-side admission/enforcement를 소유합니다. PR requirement, required reviews, required status checks, linear history 같은 조건은 live Rulesets에서 enforce합니다.

구체적인 현재 설정값은 이 문서에 복제하지 않습니다. 현재 enforcement를 판단할 때는 live GitHub configuration을 확인합니다.

## GitHub Actions

GitHub Actions는 automation과 checks를 실행하는 mechanism입니다. `PR Gate`의 verification 의미와 merge-blocking evidence는 [Testing](testing.md)이 소유하고, stochastic model/runtime evaluation evidence는 [Evaluation](evaluation.md)이 소유합니다.

## Upstream Authority

- [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
- [About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
- [Giving reviews](https://docs.github.com/en/pull-requests/concepts/giving-reviews)
- [Merge and close pull requests](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests)
- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

## Boundary

- branch policy, naming과 commit convention → [VCS / Git](vcs-git.md)
- 작성 원본과 local authority resolution → [작성 원본과 권한](source-authority.md)
- repository correctness verification과 PR Gate → [Testing](testing.md)
- behavioral evaluation과 evidence interpretation → [Evaluation](evaluation.md)
