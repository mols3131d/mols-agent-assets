# GitHub Surfaces — Consistency Findings

## Inspected

[`.github/templates/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/.github/templates/README.md), [`pull-request.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/.github/templates/pull-request.md), [`.github/workflows/pr-gate.yml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/.github/workflows/pr-gate.yml), [`branch-check.yml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/.github/workflows/branch-check.yml)을 [`docs/development/github.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/github.md) 및 [`ci.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/ci.md)와 비교했다.

## Result

**표본에서 확인된 이슈 없음.** PR template에는 validation status와 `author`·`revision` metadata 구조가 있고, CI workflow는 PR `main` 대상과 non-main push를 분리해 두 정책의 주요 구분과 일치한다.

## Coverage Limits

GitHub Ruleset의 required checks, 실행 성공 여부, 실제 formatter gating 및 모든 template을 검증한 결과가 아니다.
