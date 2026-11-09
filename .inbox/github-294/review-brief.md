# PR #294 — 자동 생성 워크플로 리뷰 브리프

## 판단 요약

[PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294)는 ChatGPT·API 등 로컬 Git hook을 실행하지 않는 변경 경로를 보완하기 위해 **작업 브랜치에 원본이 push되면 기존 generator를 GitHub Actions에서 실행하고, 생성 파일만 추가 커밋**하도록 제안한다. 별도 GitHub App, PAT, secret은 사용하지 않는다.

**현 단계: Draft / 사람 검토 대기.** 기존 `PR Gate`의 read-only admission은 유지하지만, **자동 커밋 후 required PR Gate가 재실행되지 않는 제약** 때문에 이 변경만으로 완전 무인 병합 준비까지 달성되지는 않는다. 이를 알면서 머지할지, 트리거 설계를 수정할지 먼저 판단한다.

## 변경·소유권 경계

| 책임 | 정본/대상 | 이 PR의 행동 |
| --- | --- | --- |
| 실행 시점·쓰기 권한 | [generated-sync.yml](../../.github/workflows/generated-sync.yml) | `push`(main 제외, 원본 경로 필터), `workflow_dispatch`; `contents: write` |
| 생성 동작 | [generated_artifacts.py](../../scripts/generated_artifacts.py) | 기존 `sync` 호출; 생성 의미를 workflow에서 재구현하지 않음 |
| 생성 검증 | 기존 `validate --all` | runner에서 파일 변경 후 정합성 검사 |
| 병합 허용 근거 | [pr-gate.yml](../../.github/workflows/pr-gate.yml) · [CI 정책](../../docs/development/ci.md) | 기존 read-only `PR Gate` 유지 |
| 저장소 갱신 | 작업 브랜치 | `docs/**/INDEX.tsv`, `catalog/INDEX.tsv`, `route/*.jsonl`, `.agents/route/*.jsonl`만 stage·커밋 |
| 최종 통합 | [GitHub 정책](../../docs/development/github.md) · [VCS 정책](../../docs/development/vcs-git.md) | `main` 직접 push/자동 merge 하지 않음 |

`.inbox/`는 인계 근거이고 정본 규칙이 아니다. 실제 동작과 권한은 workflow·generator·Ruleset이 소유한다.

## 설계상 핵심 위험 및 결정

### P0 운영 결정 (2026-11-09)

추가 App/PAT/새 workflow 없이 **원본 브랜치에 먼저 push → 생성 파일 bot commit 완료 확인 → PR 새로 생성**하는 순서를 기본으로 한다. `pull_request: opened`는 정상적으로 required `PR Gate`를 실행할 수 있다. 열린 PR에 후속 source push가 들어오는 경우는 여전히 기본 토큰의 자동 재트리거 한계가 있으므로, [handoff.md](handoff.md)의 사람 계정 후속 push로 최신 후보를 재검증한다. 이는 **운영상 부분 해결**이며 완전 무인 해결은 아니다.

워크플로에는 생성 파일 커밋 직후 이 제한을 알리는 notice를 추가했다. Notice를 실제 검사 실행·승인으로 오해하지 않는다. 사람의 workflow 독립 리뷰 및 E2E 테스트 전에는 Draft를 유지한다.

### High — 생성 후 required PR Gate 공백

기본 `GITHUB_TOKEN`으로 `git push`한 커밋은 새 `push` workflow run을 일반적으로 유발하지 않는다. 따라서 기존 PR의 원본 변경으로 생성 파일을 갱신한 **봇 커밋의 head SHA에 필요한 `PR Gate`가 없을 수 있다**. 이전 SHA의 성공은 최신 SHA에 대한 합격 근거가 아니다. 또한 기존 `PR Gate`는 `pull_request` 전용이므로 현재 구성의 `workflow_dispatch`를 눌러 대체할 수 없다.

- **의사결정 필요:** (A) 생성·커밋은 자동, 이후 사람의 독립적인 push/정상 PR 이벤트로 최신 커밋 재검증을 수행하는 제한적 자동화로 승인하거나, (B) 자동 재검증까지 요구하면 workflow/인증 설계를 별도 변경한다.
- **병합 조건:** latest head/merge candidate에 required `PR Gate` 성공이 표시되는 실제 evidence를 확인하고, 위 제한을 수용했는지 기록한다.
- 근거: [GitHub workflow recursion](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [Required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

### High — 쓰기 가능한 Actions 통제 표면

`contents: write`는 워크플로 한정이며 생성 결과가 바뀐 경우에만 commit/push를 수행한다. 그래도 workflow가 권한을 가진 실행 표면인 이상 **변경된 workflow 자신의 테스트나 자체 점검만으로 독립 승인으로 간주하지 않는다**. 사람이 diff와 토큰 범위, 원본 이벤트 조건, 커밋 대상 경로를 확인해야 한다. Secrets·Ruleset bypass·추가 계정은 요구하지 않는다.

### Medium — 변경 감지·경합

`paths`는 현재 알려진 원본 경로를 대상으로 한다. 신규 source 위치를 도입하면 workflow 필터도 갱신해야 한다. 새 source가 누락되더라도 PR Gate의 생성 드리프트 검증은 유지한다. Push 이후 작업 브랜치가 다른 커밋으로 전진하면 봇 push가 non-fast-forward로 실패할 수 있다. 자동 강제 push나 덮어쓰기로 복구하지 않는다.

### Resolved (F2) — 수동 실행 및 브랜치 ref 한정

`workflow_dispatch`가 태그 ref를 허용하던 결함(F2)은 job 조건 `startsWith(github.ref, 'refs/heads/') && github.ref != 'refs/heads/main'`과 push ref `HEAD:refs/heads/${GITHUB_REF_NAME}`을 명시하여 정적 수정 완료됐다. `main` 및 `refs/tags/*`에서는 실행이 차단되며 오직 작업 브랜치에서만 동기화가 동작한다.

## 확인된 근거와 미검증 범위

- **확인됨:** `main` 보호 Ruleset에 `PR Gate` required check와 squash-merge 제약이 존재함; 기존 `Branch Check`와 `PR Gate`는 read-only.
- **확인됨:** F2 수정 커밋 후 최신 PR head `728399d299e209c019a13c7b2f807827070ec2a1` 시점 `Branch Check` 및 `PR Gate`가 성공. 이는 **해당 revision의 정적/저장소 검증 통과** 근거이며, 신규 write workflow 자체의 실제 E2E 동작 성공은 아님.
- **미검증 (사람 승인 대기):** 원본 push → generator 실행 → 차이 발생 시 봇 커밋, 무변경 no-op, `GITHUB_TOKEN` 실제 write 권한, 봇 커밋 직후 required check 상태의 실제 E2E. 사람의 사전 명시적 승인이 있을 때까지 의도적으로 미실행 상태로 인계한다.
- **미검증:** 실제 원격 환경에서의 충돌/경합 시 실패 처리와 `workflow_dispatch` 수동 운영.

## 독립 리뷰 체크

1. 해당 PR의 최신 diff와 `revision.base`/`revision.head`를 확인한다. 이후 추가된 인계 파일은 작업 근거이지 새로운 실행 권한은 아니다.
1. `contents: write`가 필요한 단계, `main` 차단, generated-only staging, no-diff 분기를 확인한다.
1. source 필터가 generator dependency와 맞는지, 출력 파일만 변경될 때 재실행하지 않는지 확인한다.
1. Required `PR Gate`가 봇 커밋 이후 다시 실행되지 않는 제한을 수용할지 결정한다. 수용하지 않으면 Draft를 유지하고 설계를 수정한다.
1. [handoff.md](handoff.md)의 재현 시나리오와 복구 기준으로 post-merge 검증 계획을 확정한다.
