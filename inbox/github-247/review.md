# PR #247 리뷰 루프 보고서

## 결론

**판정: 준비 계획은 타당하지만 전체 PR은 아직 구현 전 Draft 단계다.** 확인된 High 이상 결함은 없으며, 문서/PR 상태에 대한 Low finding 1건과 구현 전에 닫아야 하는 의사결정·검증 과제 4건을 구분했다. 이 보고서는 구현 완료나 병합 승인을 의미하지 않는다.

- 대상: [PR #247](https://github.com/mols3131d/mols-agent-assets/pull/247) — ChatGPT + GitHub Plugin 기반 PR 리뷰 Skill 준비
- 기준 diff: `base=c93ba9306851c3a278f498ee0b04573c18401f14` → `head=9b99b3a97f6f8cec0add2f622f84c548f1101cd5` (보고서 작성 **전** 스냅샷)
- 검토 변경: [`inbox/github-247/plan.md`](https://github.com/mols3131d/mols-agent-assets/blob/9b99b3a97f6f8cec0add2f622f84c548f1101cd5/inbox/github-247/plan.md), 추가 45줄, 삭제 0줄, 다른 변경 파일 없음
- 범위: 준비 계획의 타당성, 기존 Agent Asset 및 저장소 정책과의 정합성, 실행 가능성에 관한 미해결 결정, 검증·게시 경계
- 제외: 아직 존재하지 않는 Skill 구현에 대한 correctness 판정, ChatGPT Skill 선택·실행의 실제 성공 판정, GitHub 리뷰 게시 및 merge

## 확인된 사실과 근거

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| PR 상태 | Draft, Open; 변경 파일 1개 | [PR #247](https://github.com/mols3131d/mols-agent-assets/pull/247) |
| 계획의 책임 분리 | `github-context`는 live context discovery, 새 Skill은 PR 분석과 결과 구성 | [계획](https://github.com/mols3131d/mols-agent-assets/blob/9b99b3a97f6f8cec0add2f622f84c548f1101cd5/inbox/github-247/plan.md), [`github-context`](https://github.com/mols3131d/mols-agent-assets/blob/main/src/rulesync/.rulesync/skills/github-context/SKILL.md) |
| 저장소 정책 정합성 | 원본 배치 결정을 미리 단정하지 않고, 권한·검증 근거를 구분함 | [작성 원본 정책](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/development/source-authority.md), [GitHub 정책](https://github.com/mols3131d/mols-agent-assets/blob/main/docs/development/github.md) |
| 기존 head의 CI | `Branch Check`, `PR Gate` 모두 성공 | [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/39160343091/job/117772171592), [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/39160345757/job/117772157965) |
| 구현 및 행동 평가 | `SKILL.md` 미추가, ChatGPT에서 실제 선택·행동 평가 미실행 | [PR 변경 파일](https://github.com/mols3131d/mols-agent-assets/pull/247/files), [계획의 현재 상태](https://github.com/mols3131d/mols-agent-assets/blob/9b99b3a97f6f8cec0add2f622f84c548f1101cd5/inbox/github-247/plan.md) |

CI 성공은 해당 **기존 head**의 repository check 결과다. 이 보고서가 새 커밋으로 추가되면 그 커밋의 체크 결과는 별도로 확인해야 하며, 기존 체크 통과를 Skill의 런타임 성능 근거로 취급하지 않는다.

## 리뷰 루프

| 루프 | 질문과 검토 방식 | 결과 및 다음 판단 |
| --- | --- | --- |
| 1 — 근거 중심 검토 | 전체 diff를 계획/정책/자산 책임과 대조. Verifier 관점으로 scope, authority, 검증 주장을 확인 | 준비 범위에서는 책임 중복·권한 위반을 확인하지 못함. CI 상태 표기의 최신성 문제 후보 1건 확인 |
| 2 — 반론·실패 경로 검토 | Challenger 관점으로 대형 diff, 부분 API 응답, 변경된 head, prompt injection, 게시 권한, Skill 실행 경로를 반박 사례에 대입 | 계획이 위험을 인식하지만 구체 방어는 후속 설계 결정임을 확인. 미구현을 현행 결함으로 오인하는 후보는 기각 |
| 종합 판정 | 기존 safeguards 및 `준비 단계` 범위로 candidate를 반증·중복 제거 | Low finding 1건 확정. 나머지는 실제 구현 전에 닫을 게이트로 분류 |

이는 ChatGPT 단일 문맥에서의 **순차적 역할 관점 대체**이며 실제 독립 Subagent 실행이나 병렬 DualVantage 수행이 아니다. 시나리오는 설계 반증을 위한 사고 실험이며 GitHub 게시·공격 재현·실제 Skill 행동 평가를 수행하지 않았다.

## 확인된 Finding

### 🔵 Low · F1 — PR 본문의 CI 상태 정보가 오래됨

- **관찰(verified):** PR 본문 `Validation`은 `PR Gate: Not Verified`로 기재하지만, 기준 head `9b99b3a97f6f8cec0add2f622f84c548f1101cd5`의 GitHub Check Runs에는 `PR Gate`와 `Branch Check`가 모두 `success`로 기록되어 있다.
- **영향:** PR 본문을 보는 리뷰어가 현재 검증 완료 여부를 잘못 판단할 수 있다. GitHub checks UI에는 올바른 결과가 있어 범위가 제한적이다.
- **조치:** PR 본문에서 기준 head의 체크 근거를 반영한다. 보고서 커밋 이후에는 **새 head의** 체크를 먼저 확인한 뒤 표기한다.
- **반증 가능 조건:** PR 본문을 현재 head 기준으로 이미 갱신했다는 사실이 확인되면 해당 finding을 종료한다.

## 구현 전 의사결정 및 검증 게이트

아래는 **현재 준비 문서의 실패 판정이 아니라** 전체 Skill의 완료 조건에 필요한 후속 과제다.

| 우선 | 게이트 | 완료 증거 |
| --- | --- | --- |
| P1 | **ChatGPT에서 소비 가능한 Skill 원본과 로딩 경로**: 재사용 Rulesync 또는 vendor-native 작성 원본을 하나로 확정하고 ChatGPT의 실제 사용 경로를 확인 | canonical source 경로, target 소비/선택 방법, 지원·미지원 범위, 실제 로딩 관찰 결과. 지원 경로가 없으면 완료 불가로 보고 |
| P1 | **diff coverage와 revision 일관성**: 페이지네이션·응답 잘림·파일 접근 실패를 구분하고 게시 직전 base/head를 재조회해 stale review를 막을 방법을 결정 | 전체/부분 검토를 재현 가능한 범위로 표시하고, 누락 파일을 숨기지 않으며, head 변경 시 게시 중단 또는 새 근거로 재검토하는 시나리오 결과 |
| P1 | **쓰기·신뢰 경계**: 외부 PR 본문/patch/comment를 비신뢰 입력으로 유지하면서 리뷰 본문·inline comment·승인/변경요청을 명시적 권한으로 구분 | 게시 지시 부재 시 원격 mutation 0건, 권한 없는 요청 거부, prompt injection 및 실패 시나리오의 실제 관찰 결과 |
| P2 | **평가 가능 완료 기준**: 정상/near-miss/대형 PR/일부 실패/변경 중 PR/게시 요청을 기대 결과와 실패 판정까지 구체화 | 정적 validation과 실제 ChatGPT+GitHub Plugin runtime eval의 실행 로그·결과·미검증 구분. 시뮬레이션은 별도 표기 |

**판단 근거:** [계획의 미결정 사항과 완료 기준](https://github.com/mols3131d/mols-agent-assets/blob/9b99b3a97f6f8cec0add2f622f84c548f1101cd5/inbox/github-247/plan.md), [Agent Asset 리뷰 기준](https://github.com/mols3131d/mols-agent-assets/blob/main/src/rulesync/.rulesync/skills/mols-agent-asset/references/common/review.md), [평가 evidence 규칙](https://github.com/mols3131d/mols-agent-assets/blob/main/src/rulesync/.rulesync/skills/mols-agent-asset/references/evidence.md). 계획은 이 위험들을 명시하고 있어, 구체적 해결 미작성 자체를 준비 단계의 결함으로 승격하지 않았다.

## 권장 진행 순서

1. 현재 PR을 Draft로 유지하고, 실제 ChatGPT Skill 소비·라우팅 가능성 및 GitHub Plugin API 응답·게시 도구 계약을 최소 시나리오로 확인한다.
2. 확인된 제약을 바탕으로 이름/activation/near-miss, canonical source와 평가 기준을 확정한다. 기존 `github-context` 및 repository GitHub 정책을 복제하지 않는다.
3. 전용 `SKILL.md`와 필요한 reference만 구현한다. 큰 diff·부분 증거·stale head·무단 게시에 대한 명시적 fallback을 포함한다.
4. 정적 검증과 실제 런타임 평가를 **분리**해 기록한다. 검증되지 않은 시나리오는 통과로 표시하지 않는다.
5. PR 본문과 checks를 새 head 기준으로 갱신한 후 review-ready/merge 여부를 다시 판단한다. 제어 표면 변경에 대한 독립 검토와 사람의 최종 승인 경계를 준수한다.

## 검증 및 남은 한계

- ✅ Pass — 기준 head의 실제 diff 1개 파일/45줄, 본문, 저장소 지침 및 관련 Skill 정책 확인
- ✅ Pass — 기존 head의 `Branch Check` 및 `PR Gate` 성공 확인
- ✅ Pass — 보고서에 구현 전 상태·검토 범위·근거 수준·미실행 검증을 구분함(문서 의미 검토)
- ⚪ Not Verified — 보고서가 포함된 **후속 head의** CI
- ⚪ Not Verified — Skill의 실제 ChatGPT activation, GitHub Plugin 동작과 behavioral eval
- ⚪ Not Verified — 실제 독립 Subagent 병렬/격리 실행, 동적 실패 시나리오 재현

**종료 조건:** 준비 계획 검토는 수렴했다. 새 근거 없이 관점이나 루프 수만 늘리지 않는다. 전체 PR 완성/병합 판단은 아직 보류한다.
