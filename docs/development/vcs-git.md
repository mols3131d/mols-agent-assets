---
description: repository-local branch policy, branch naming, Git commit convention과 deterministic enforcement boundary를 확인할 때 사용합니다.
---

# VCS / Git

이 문서는 repository-local **VCS와 Git policy**를 소유합니다. 전체 개발 작업의 순서나 GitHub collaboration workflow는 정의하지 않습니다.

## Branch Policy

- `main`은 직접 수정하지 않습니다.
- 변경은 dedicated branch에서 수행합니다.
- 기본 base는 current `main`입니다. 다른 base가 명시적으로 필요한 작업은 해당 target을 따릅니다.
- `main`으로의 integration은 [GitHub](github.md)의 Pull Request와 Merge policy를 따릅니다.

## Branch Naming

기본 branch 이름:

```text
<owner>/<type>/<topic>
```

- `owner`: 작업 주체를 식별하는 짧은 이름
- `type`: 변경 성격을 나타내는 짧은 category. 고정 enum은 두지 않으며 `docs`, `feat`, `fix`, `chore`처럼 의미가 명확한 값을 사용합니다.
- `topic`: 변경 대상을 나타내는 간결한 kebab-case 이름

각 segment는 특별한 이유가 없으면 lowercase와 kebab-case를 사용합니다.

## Commit Messages

직접 작성하는 commit message의 authoring convention은 repository root의 [`.gitmessage`](../../.gitmessage)가 authoritative source입니다.

- [`scripts/validate_commit_msg.py`](../../scripts/validate_commit_msg.py)는 deterministic하게 검사할 수 있는 최소 subset을 검증합니다.
- [`lefthook.yml`](../../lefthook.yml)의 `commit-msg` hook이 validator를 실행합니다.
- Validator가 검사하지 않는 `.gitmessage`의 human convention까지 validator의 contract로 확대 해석하지 않습니다.

## Boundary

- Issues, Pull Requests, PR Reviews, PR Merge, Rulesets와 Actions → [GitHub](github.md)
- 변경 대상의 작성 원본 선택 → [작성 원본과 권한](source-authority.md)
- verification과 merge-blocking evidence → [Testing](testing.md)

이 문서는 일반적인 Git 사용법이나 repository-wide change workflow를 정의하지 않습니다.
