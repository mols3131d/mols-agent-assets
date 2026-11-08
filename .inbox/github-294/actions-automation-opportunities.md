# PR #294 — GitHub Actions 자동화 최종 선별안

> **결론:** 추가 Actions 도입은 보류한다. 먼저 PR #294의 생성 파일 자동 커밋과 최신 커밋 검증의 연계를 안전하게 마무리한다. 현재 자료에는 새 워크플로를 여러 개 만들 만큼 확실한 운영 이득이 없다.

- 대상: [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294), `mols3131d/mols-agent-assets`.
- 2026-11-09 기준 검토. 이 문서는 **제안/인계용 비정본**이다. 구현을 승인하거나 완료한 기록이 아니다.
- 정본: [CI 정책](../../docs/development/ci.md), [GitHub 정책](../../docs/development/github.md), [PR #294 리뷰](review-brief.md), [운영 인계](handoff.md).
- 기존 자동화: `.github/workflows/branch-check.yml`(push 검사), `.github/workflows/pr-gate.yml`(main 대상 PR required check), `lefthook.yml`(로컬 생성·커밋 검증), `mise.toml`(명령 진입점), PR #294의 `generated-sync.yml`(생성·커밋 제안).

## 지금 남길 일: 1개

### P0 — 생성 파일 자동 커밋 이후 최신 PR Gate의 공백 처리

**실제 문제:** PR #294의 `generated-sync.yml`은 원본 push에 반응해 `generated sync` 후 `github-actions[bot]`이 기본 `GITHUB_TOKEN`으로 커밋한다. 그러나 그 커밋은 정상적인 `push`/`pull_request` CI를 자동 트리거하지 않는다. 생성 전 체크가 최신 head의 `PR Gate`를 대체하지 못하면 병합 가능 상태가 중단된다.

**권장 — 작은 운영 경계로 시작**

1. **지금 구현 범위는 생성·커밋까지만** 유지한다. 새로운 App/PAT/secret/서버, Ruleset 수정, 자동 merge는 도입하지 않는다.
2. #294를 병합하려면 먼저 원본 변경이 실제 생성 파일 차이를 만드는 브랜치에서 E2E 검증한다. 최신 PR head/merge candidate의 `PR Gate`와 `Branch Check`가 어떻게 표시되는지 관찰한다.
3. 봇 커밋 뒤 required check가 누락되면 **사람 계정의 정상적인 후속 브랜치 push** 등 GitHub가 인정하는 `push`/`pull_request` 이벤트로 최신 후보를 재검증한다. 결과가 확인되기 전 Merge하지 않는다. 이 절차는 **수동 보완**이지 완전 무인 자동화라고 부르지 않는다.
4. 사람의 마지막 push가 과도하게 자주 필요해진다는 근거가 생길 때만 별도 PR에서 완전 자동 설계를 다시 검토한다. 사용자가 원치 않는 GitHub App을 필수 전제로 두지 않는다.

**금지/주의:** `workflow_dispatch`로 required `PR Gate`를 돌리는 것만으로 해결했다고 주장하지 않는다. GitHub Actions의 `workflow_dispatch` 체크는 PR required check로 인정되지 않을 수 있다. 필요한 체크를 Ruleset에서 제거하거나, 체크 성공을 위조하거나, `main`에 직접 push하지 않는다.

**완료 증거:** 원본 수정 → 생성된 `INDEX.tsv`/`route/*.jsonl`의 예상 변경만 bot commit → no-op에서 불필요한 commit 없음 → 최신 PR 후보의 required Gate 성공 확인. 통합 테스트는 아직 미실행이다.

## 유일한 조건부 후보 — 현재는 구현하지 않음

**영향 기반 생성(`generated sync`의 변경 범위 선택):** 현재 `sync`는 전체 projection을 다시 만든다. 특히 `repository-routes`는 잠긴 외부 Skill 원본을 가져와 단순 문서 변경에도 네트워크를 사용할 수 있다. **실제 소요 시간 증가·네트워크 실패 반복이 확인될 때만** 최적화한다.

- 구현한다면 [`generated_artifacts_sync.py`](../../scripts/generated_artifacts_sync.py)의 기존 source-to-projection mapping을 재사용한다. 새 라우터/매니페스트를 만들지 않는다.
- runner의 staged 변경이 없는 상태에서 `sync --staged`를 그대로 실행하면 대상이 누락될 수 있으므로 피한다. branch diff 기준 영향 계산, 계산 실패 시 전체 검사 fallback이 필요하다.
- 측정 근거가 없으므로 현재는 **전체 생성 방식 유지**가 더 단순한 선택이다.

## 드롭한 항목과 이유

| 후보 | 결정 | 비용/효용 판단 |
| --- | --- | --- |
| Commit message 검사 추가 | **드롭** | 로컬 hook이 이미 있고, GitHub PR은 squash merge 정책. API 커밋 위반이 실제 문제로 확인되지 않아 모든 PR에 체크를 넣을 근거 부족 |
| 변경 파일 formatter CI | **드롭** | Ruff·rumdl·Biome 설치·실행 비용과 스타일성 false positive. `format-changed`가 이미 존재하며 현재 merge-critical 위반 근거 부족 |
| 정기 전체 drift health check | **드롭** | 원본이 PR로 변경되며 현재 PR Gate가 drift를 검증함. 외부 fetch 실패·알림 노이즈·재실행 비용이 커질 수 있음 |
| Skill/lock dependency dry-run 별도 Actions | **드롭** | 기존 `PR Gate`의 Rulesync 검사 및 `mise doctor`와 중복 가능. 신규 실패 근거 없이 범위 확장 불필요 |
| 자동 Promptfoo 모델 평가 | **드롭** | 모델/런타임 설정·원격 데이터 전송·유료 API·긴 실행 시간. deterministic 검증을 대체하지 못함 |
| 자동 formatter write-back, 자동 PR/Issue/merge | **드롭** | 의도하지 않은 변경·실행 루프·권한 확대·리뷰 우회의 위험이 편익보다 큼 |
| 별도 GitHub App·PAT·외부 서버 | **현재 드롭** | 사용자의 Actions-only 선호, 인증 정보 관리·권한 관리 비용. 완전 자동화가 명확히 필요해질 때만 별도 평가 |

## 다음 작업자 인계

1. 같은 계정 `mols3131d`에서 PR #294의 실제 최신 head/base, required checks, 다른 수정 여부를 조회한다.
2. [기존 인계](handoff.md)의 no-op/source-change/E2E 시나리오를 **별도 안전한 작업 브랜치**에서 수행하고 로그·커밋 SHA를 남긴다. Actions workflow는 권한 있는 실행 표면이므로 사람의 독립 검토·승인 없이 merge하지 않는다.
3. GitHub 기본 토큰이 후속 검증을 생략하는지 **실제 repo 결과**로 확인한다. 재검증이 필요한 경우 사람의 승인된 push로 후속 검증을 실행한다. 최신 required Gate 확인 전 병합 금지.
4. 안정화 이후 별도 후보를 구현하지 않는다. 반복된 시간 지연, 외부 fetch 장애, 손실 사고 등 **관찰된 불편**이 생긴 항목만 좁은 별도 PR로 재검토한다.

## 공식 근거

- [GitHub `GITHUB_TOKEN`의 이벤트와 workflow recursion](https://docs.github.com/en/actions/concepts/security/github_token)
- [Required checks: 최신 커밋, 유효 trigger 및 `workflow_dispatch` 제한](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
- [Path-filter로 스킵된 required check가 Pending으로 남는 경우](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)
