# PR #294 — 심층 리뷰 보고서 (2026-11-12)

> **판정: Draft 유지 / 머지 보류.** 생성기 재사용·generated-only stage는 정적으로 적절하다. 다만 봇 커밋 이후 최신 PR 필수 검증 공백, 승인 전 쓰기 워크플로 실행 위험, 신규 쓰기 경로 E2E 미확인이 남아 있다. 이 보고서는 사람의 승인이나 GitHub PR Review를 대신하지 않는다.

| 항목 | 값 |
| --- | --- |
| 대상 | [PR #294](https://github.com/mols3131d/mols-agent-assets/pull/294) |
| 브랜치 | `mols/chore/generated-sync-on-push` |
| 비교 base | `fa5be3bd63e9c29c30017b9e8c833018c092b9a7` |
| 리뷰 기준 head | `e533656aea161764c5d7f1aceb5fd1390cd09e21` |
| diff | [generated-sync.yml](../../.github/workflows/generated-sync.yml) 1개와 `.inbox/github-294/` 문서 5개 |
| 방법 | 원격 diff, generator·CI·GitHub 정책 및 이전 리뷰의 교차 정적 검토 |
| 직접 실행 | 신규 Actions E2E·로컬 테스트 미실행 |

증거 등급: `CONFIRMED`는 직접 확인된 상태·소스 불일치, `SUPPORTED`는 소스와 외부 계약이 뒷받침하는 실제 발생 가능 조건, `HYPOTHESIS`는 추가 확인이 필요한 주장이다.

## Findings

| ID | 중요도 | 증거 | 영향 |
| --- | --- | --- | --- |
| [R1](#r1) | High | SUPPORTED | 봇 커밋 이후 required `PR Gate`의 최신 후보 검증이 누락될 수 있음 |
| [R2](#r2) | High | SUPPORTED | 사람 승인 전에도 브랜치 `push`가 write-capable Actions를 시작할 수 있음 |
| [R3](#r3) | Low | CONFIRMED | PR 본문의 revision·변경 파일 수가 실제 상태와 다름 |

<a id="r1"></a>
<details>
<summary><strong>R1 · 봇 커밋 이후 PR Gate 검증 공백</strong> — High / SUPPORTED</summary>

- **위치:** [generated-sync.yml](../../.github/workflows/generated-sync.yml) 62–73행. `GH_TOKEN`으로 생성 결과를 원본 브랜치에 push한다. 기존 [pr-gate.yml](../../.github/workflows/pr-gate.yml)은 `pull_request` 이벤트만 감시한다.
- **발생 조건:** 열린 PR의 source push 후 봇 커밋이 추가되고, 사용자의 별도 유효 이벤트가 없는 경우.
- **영향:** 이전 SHA에 대한 체크 통과가 생성 파일을 포함한 최종 후보의 검증을 뜻하지 않는다.
- **근거:** [GitHub 공식 GITHUB_TOKEN 이벤트 계약](https://docs.github.com/en/actions/concepts/security/github_token). 기본 토큰의 일반 `git push`는 후속 `push`/`pull_request` 실행을 만들지 않는다. 토큰이 PR 자체를 생성·갱신할 때의 승인 대기 예외는 구분한다.
- **검증:** 정적 근거 확보, 열린 PR에서 봇 커밋 후 최신 체크 E2E는 **Not Verified**.
- **최소 대응:** 원본 push → 생성 파일 봇 커밋 완료 → 첫 PR 생성 순서를 기본 운영안으로 유지한다. 이미 열린 PR은 승인된 정상 이벤트 후 최신 head/merge candidate의 필수 체크를 확인한다. 수동 운영의 수용 여부를 사람이 결정한다.
- **재현:** 격리된 열린 PR에서 source 변경 → generated-only bot commit → 새 SHA/merge candidate의 `PR Gate` 상태와 run URL 확인 → 승인된 후속 이벤트로 재검증.

</details>

<a id="r2"></a>
<details>
<summary><strong>R2 · 승인 전 쓰기 워크플로 실행 가능성</strong> — High / SUPPORTED</summary>

- **위치:** [generated-sync.yml](../../.github/workflows/generated-sync.yml) 4–23행. `on.push`는 `main` 외 관련 경로에 반응하고, `contents: write`를 요청한다. job 조건은 ref만 제한한다.
- **발생 조건:** workflow 파일이 존재하는 작업 브랜치에 관련 source push가 발생하고 저장소 Actions 정책상 실행이 허용되는 경우. [GitHub push 이벤트 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push)는 기본 브랜치에 병합되지 않은 workflow에도 적용됨을 명시한다.
- **영향:** Draft 상태 자체는 실행 차단 장치가 아니므로, 승인 전 자동 쓰기가 저장소 [통제 표면 정책](../../docs/development/github.md)에 어긋날 수 있다.
- **검증:** YAML·공식 이벤트 계약 정적 확인. 실제 저장소 Actions 설정·별도 승인 통제 존재 여부는 **Not Verified**.
- **최소 대응:** 사람이 workflow의 trigger, 생성 대상, 권한·credential 사용을 독립 검토하고 테스트 실행을 승인한 뒤 실행한다. 승인 전에 source push로 write 테스트를 개시하지 않는다.
- **확인:** 실제 저장소 승인·실행 제약과 workflow 활성 상태를 별도로 확인해 기록한다. Draft에 의존하지 않는다.

</details>

<a id="r3"></a>
<details>
<summary><strong>R3 · PR 본문 메타데이터 불일치</strong> — Low / CONFIRMED</summary>

- **위치:** [PR #294 본문](https://github.com/mols3131d/mols-agent-assets/pull/294).
- **근거:** 실제 head는 `e533656aea161764c5d7f1aceb5fd1390cd09e21`이고 본문의 `revision.head`는 `5a0c39101a3aa25ea4e302633302b9cc3501f47f`이다. 실제 변경은 workflow 1개 + 리뷰 문서 5개인데 본문에는 문서 4개라고 적혀 있다.
- **영향:** 이전 체크를 최신 체크로 오해하거나 리뷰 범위를 축소할 수 있다.
- **검증:** PR 메타데이터와 변경 파일 목록 직접 대조.
- **최소 대응:** 리뷰·인계 파일 반영 후 PR 설명의 `Changes`와 `revision.base/head`를 최신화하고 해당 SHA의 checks를 다시 조회한다.

</details>

## 별도 승인·검증 게이트

- **G1 · 사람 승인: Not Verified.** `contents: write`를 가진 workflow는 사람이 변경한 통제 표면을 독립 검토하고 명시적으로 승인해야 한다. AI 리뷰·CI 통과는 대체 근거가 아니다.
- **G2 · 신규 write 경로 E2E: Not Verified.** no-op에서 무커밋, source 변경에서 generated-only bot commit, push 권한, 최신 required check, 경합·실패 복구를 승인된 격리 브랜치에서 검증해야 한다.
- **경계:** 추가 PAT/App/secret, force push, `main` 직접 push, Ruleset 완화는 현재 변경에 없다. 이 정적 확인은 원격 E2E 통과 근거가 아니다.

## 구현·CI 확인

| 대상 | 판정 |
| --- | --- |
| 브랜치·태그 ref 제한 | 정적 확인: `refs/heads/*` 및 `main` 제외; 기존 F2 수정 유지 |
| 생성·검증 | 정적 확인: 공식 `scripts.generated_artifacts sync` / `validate --all` 사용 |
| 출력 stage | 정적 확인: docs/catalog의 `INDEX.tsv`, `route/*.jsonl`, `.agents/route/*.jsonl`만 stage |
| no-op | 정적 확인: staged diff 없으면 commit 생략 |
| 입력 경로 filter | 현 generator와 대조 시 확정 누락 미발견; 신규 source 도입 시 재검토 필요 |
| `PR Gate` | **Pass:** [run 42682286312](https://github.com/mols3131d/mols-agent-assets/actions/runs/42682286312), 리뷰 기준 head 연관 run의 job step 성공 |
| 신규 `Sync Generated Artifacts` E2E | **Not Verified** — 이 검토에서 실행하지 않음 |
| 별도 Git pathspec/로컬 테스트 | **Not Verified** — 이 검토에서 실행하지 않음 |
| 사람 승인·실제 설정 | **Not Verified** |

## 조치와 종료 조건

1. R2·G1의 독립 승인과 실제 실행 통제부터 확인한다. 승인 전 쓰기 가능한 실행을 시작하지 않는다.
2. 승인된 격리 브랜치에서 no-op, generated delta, 봇 커밋, 열린 PR의 최신 필수 check를 재현한다.
3. R1의 제한적 운영 모델과 사람의 후속 검증 비용을 수용할지 결정한다. 더 큰 인증·워크플로 재설계는 별도 승인에 맡긴다.
4. R3의 본문 메타데이터를 최종 작업 head 기준으로 갱신한다.
5. 사람 승인 및 최신 required checks 확인 후에만 Draft 해제·squash merge를 검토한다.

세부 실행은 [심층 리뷰 인계](review-handoff-2026-11-12.md)에 둔다. [2026-11-10 독립 리뷰](review-report-independent-2026-11-10.md)는 이전 revision에 대한 스냅샷으로 유지한다. 이 보고서가 커밋된 뒤 생성되는 새 head의 검증은 별개다.
