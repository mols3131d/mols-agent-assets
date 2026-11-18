# PR #294 — 검증 행렬·배포 게이트

> 2026-11-16 로컬 에이전트용 verification contract. 설계는 [09-github-app-design.md](09-github-app-design.md), 실행 순서는 [10-implementation-handoff.md](10-implementation-handoff.md). 모든 항목은 아직 **신규 App write-back 아키텍처의 실행 검증이 아니다**.

## 증거 등급

- **Static:** YAML·shell·Python 소스와 권한 경계에 대한 정적 검토. 실제 GitHub event의 근거로 사용하지 않는다.
- **Deterministic:** pytest 또는 isolated repo/fixture에서 검증한 producer/writer 함수·실패 계약. GitHub 권한·Ruleset 동작의 근거로 사용하지 않는다.
- **E2E:** 승인된 실제 GitHub repository/branch/PR에서 source push → Actions → App commit → 최신 required `PR Gate`까지 관측. **Pass는 실제 run URL·SHA·최종 check 결론이 있을 때만** 기록한다.
- **Not Verified:** 준비·승인·권한·실행 근거가 없는 상태. 체크박스를 미리 채우거나 Static을 E2E로 승격하지 않는다.

## 구현 테스트: producer와 writer

| ID | 입력 / 공격·실패 상황 | 기대 결과 | 증거 |
| --- | --- | --- | --- |
| T01 | 변하지 않는 source commit / generated output 동일 | no-op, App token 발급·remote commit 없음 | Deterministic + E2E |
| T02 | `docs/*.md` 등 index 입력 변경 | 올바른 `INDEX.tsv`만 재생성·검증 | Deterministic + E2E |
| T03 | `catalog/` source 변경 | `catalog/INDEX.tsv`만 예상대로 갱신 | Deterministic |
| T04 | `SKILL.md`, subagent 또는 route lock/config 입력 변경 | 관련 `route/*.jsonl`/`.agents/route/*.jsonl` 결정적 갱신 | Deterministic |
| T05 | 생성 파일 직접 수정·삭제만 포함된 API commit | 설정한 trigger 정책대로 자동 복구 또는 **지원 안 하는 범위를 분명히 실패 보고** | Deterministic + E2E |
| T06 | 허용 목록 이외 path, path traversal, symlink, malformed metadata, 과도한 archive | Writer 거부, token/push 없음 | Deterministic |
| T07 | 다른 repo/fork/다른 workflow의 run·artifact; 실패/취소 producer | Writer 거부, 아무런 branch write 없음 | Deterministic |
| T08 | `workflow_run.head_sha`/artifact metadata와 실제 branch HEAD 불일치 | stale 작업 폐기, 최신 state를 훼손하지 않음 | Deterministic + E2E |
| T09 | 두 source push가 연달아 오고 워크플로가 경쟁 | 최종 branch의 출력이 최신 canonical source와 일치; 오래된 writer의 덮어쓰기 없음 | Deterministic + E2E |
| T10 | 원격 non-fast-forward/권한 거부/generator failure | failure 진단 가능, force push·검증 우회·credential fallback 없음 | Deterministic; E2E 조건부 |
| T11 | App 봇의 generated-only push가 Producer로 재진입 | 루프 없이 유한한 no-op 또는 안전한 skip; 정상 source push는 계속 처리 | Deterministic + E2E |
| T12 | App secret/variable 누락 또는 App 미설치 | writer fail-closed, 원격 변경 없음 | Deterministic + E2E 조건부 |
| T13 | user/API가 workflow/생성기 자체를 변경 | read-only producer에서 secret 접근 불가; writer는 기본 브랜치의 신뢰된 code만 실행 | Static + Deterministic |
| T14 | `main`, tag 또는 protected ref 대상 | 어떤 generated commit도 실행하지 않음 | Deterministic |
| T15 | producer artifact 변조로 기존 파일 제거·예상 밖 파일 추가 | Writer path/inventory/staged diff 검사에서 거부 | Deterministic |
| T16 | Read-only validator와 canonical generator의 영향 범위 불일치 | 해당 source 범위가 누락되지 않거나 안전하게 실패 | Static + Deterministic |

`T05`의 구체적 정책은 사용자 의도와 [설계](09-github-app-design.md)를 기준으로 agent가 결정해 구현·검증한다. 생성 파일만 잘못 바꾼 API 커밋은 local hook이 없으므로 복구를 지원하는 편을 우선 검토한다. App push에서 예상치 못한 재실행은 **결정적 no-op을 단정하지 말고** 실제 관측한다.

## GitHub E2E: ChatGPT 플러그인과 PR 동기화

모든 write E2E는 **사람의 별도 승인 + 격리 branch + 열린 테스트 PR**에서만 실행한다. `main` 또는 기존 PR #294 브랜치를 실험 대상으로 쓰지 않는다. 테스트마다 실행 연결·소유 계정이 `mols3131d`인지 먼저 확인한다. 다른 GitHub 계정/명의는 자동으로 선택하지 않는다.

| ID | 실제 행동 | 통과 판단 |
| --- | --- | --- |
| E01 | ChatGPT GitHub Plugin 또는 Contents API로 source 파일 **하나**를 수정 | webhook `push` → Producer → artifact → Trusted Writer, generated-only App commit, PR `synchronize` 발생 |
| E02 | 같은 Plugin에서 source 파일 **여러 개를 연속 커밋** | 마지막 실제 source SHA 기준 결과가 재생성되고 stale run이 덮어쓰지 않음 |
| E03 | **이미 열린 PR**의 source 수정 | App generated commit 이후 최신 PR head/merge candidate에서 기존 **required `PR Gate`**가 실제 성공 |
| E04 | 생성 결과 변경이 없는 source 수정 | generated commit 없음. 최신 source commit의 `PR Gate` 체크는 유효 |
| E05 | App 봇의 output-only commit | producer loop/무한 커밋 없음; PR Gate가 필요한 정상 이벤트로 실행됨 |
| E06 | 생성 파일만 삭제하거나 기존 projection을 직접 수정 | 채택한 output-only 복구 정책과 실제 동작이 일치 |
| E07 | Source push와 writer 사이 다른 API commit 추가 | stale artifact 거부; 이후 최신 source가 eventually 반영됨 또는 실패가 명확히 드러나 복구 가능 |
| E08 | GitHub App Secret·설치 설정을 **활성화 전에** 준비하지 않은 상태 | privileged writer가 정상적으로 fail-closed되고 source PR Gate가 가짜 성공으로 보이지 않음 |
| E09 | 실제 repository Ruleset 필수 체크 source 검사 | `PR Gate`의 결과가 GitHub가 요구하는 SHA·source·이벤트에 연결됨 |
| E10 | 새 bootstrapped writer가 default branch에서만 실행되는지 검사 | source branch의 writer YAML/script가 권한을 가진 실행 코드로 사용되지 않음 |

**핵심: E03 + E09가 없으면 기능상 완성 아님.** 원본 push의 PR Gate 성공, writer의 `workflow_run` job 성공, `workflow_dispatch` 통과는 **봇 커밋 후 required `PR Gate`**의 대체가 아니다.

## rollout 검증

- [ ] 현재 repository ruleset(required check 이름·strictness·source)와 Actions permissions를 **실제 설정에서** 확인했다.
- [ ] 독립적 human review가 privileged workflow·App scope·artifact trust boundary를 검사했다.
- [ ] default-branch **disabled writer bootstrap**을 어떤 PR/commit으로 도입했는지 추적 가능하다. 해당 merge는 사람의 별도 명시적 승인으로 수행했다.
- [ ] GitHub App 소유자/설치 scope/contents permission이 정확히 한 저장소로 제한되어 있다. 사용자 승인 없이 설치·수정하지 않았다.
- [ ] `main` 제한 Environment `generated-writeback`의 Variable `GENERATED_SYNC_APP_CLIENT_ID`와 Secret `GENERATED_SYNC_APP_PRIVATE_KEY`의 **존재·참조 성공 여부**만 확인했다. Source-branch Producer/PR Gate에서 Secret을 읽을 수 없는지 검증했으며, 실제 값을 로그·이슈·PR·Git에 남기지 않았다. 환경 기능이 불가하면 대안을 사람에게 별도 승인받는다.
- [ ] 승인된 isolated E2E에서 E01/E02/E03/E04/E05/E07/E09가 통과했다. 못 한 항목은 설명과 함께 Not Verified다.
- [ ] `PR Gate`와 `Branch Check`의 read-only admission/diagnostic 정책이 그대로 유지됐다.
- [ ] 장애·roll-back 경로(토큰 비활성/설치 중단/producer read-only 계속 유지)가 승인된 통제 범위에서 검증됐다.
- [ ] PR #294의 description `revision.base/head`와 최신 diff, Checks, proof link가 일치한다.
- [ ] merge 전 독립 사람 승인 및 main branch의 required Gate가 실제 충족되었고, **자동 merge는 없다**.

## evidence 기록 양식

E2E 시나리오별로 아래 최소값만 남긴다. 실행하지 않은 값은 비워 두지 말고 `Not Verified`로 표시한다. 민감한 인증 정보는 절대 포함하지 않는다.

| Field | 의미 |
| --- | --- |
| Case / outcome | 예: `E03: Pass / Fail / Not Verified` |
| Tested repository / actor | 실제 repo, branch 및 승인된 계정·App의 공개 bot slug |
| Source SHA / App SHA | source branch 입력 커밋과 bot generated-only commit |
| Run URLs | Producer run, Writer `workflow_run`, 최종 `PR Gate` |
| Final checked SHA | GitHub가 검사한 head 또는 PR merge candidate |
| Changed path inventory | generated-only인지, 예상 범위를 벗어난 파일은 없는지 |
| Approval and unresolved risk | 사람의 명시적 승인 근거(있을 때만), 미완료 조건 |

## 실패 시 판정과 복구

| 현상 | 운영 조치 |
| --- | --- |
| App installation token 생성 실패 | 설정/설치/권한 확인, 임의 PAT·다른 계정으로 우회 금지 |
| writer가 source branch code를 실행해야 함 | 구현 중단, trusted script 경계 재설계 |
| artifact가 오래됐거나 branch 경합 | 최신 HEAD 확인 후 artifact 폐기; 필요한 경우 **승인된 source 재시도** |
| 봇 커밋 후 최신 required check 없음 | 미완료·병합 중단, 이벤트 source와 SHA 확인. 가짜 check·bypass 금지 |
| 생성 drift·테스트 실패 | PR Gate는 실패 상태 유지, authoring/source를 수정하여 정상 검증 수행 |
| App push 반복 또는 scope 이상 | writer 활성화 중단/credential revocation은 **승인된 담당자**가 처리, 영향 기록 |

## 참고 문서

- [GitHub App 설계](09-github-app-design.md)
- [구현 인계](10-implementation-handoff.md)
- [GitHub 이벤트와 App token 공식 설명](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [PR Required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
