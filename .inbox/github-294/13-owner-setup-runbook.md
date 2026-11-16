# PR #294 — 사람이 해야 할 GitHub App 설정·승인 절차

> 로컬 에이전트가 [작업 패키지](12-next-steps-handoff.md)의 A0/A1을 준비한 **다음** 사용하는 실행 체크리스트. App·Secret·Writer를 설정/활성화하기 전에는 현재 저장소·계정·PR·권한·실제 코드의 상태를 확인한다. 이 문서는 승인 기록이 아니며 아래 체크박스는 모두 미완료다.

## 시작 전

- 대상: `mols3131d/mols-agent-assets`, PR [#294](https://github.com/mols3131d/mols-agent-assets/pull/294). **다른 GitHub 계정·조직·연결로 임의 전환 금지.**
- 필요한 것: GitHub 소유 계정 `mols3131d`의 설정 관리 권한, 로컬 에이전트가 준비한 Producer/Writer 코드와 독립 보안 리뷰, 테스트할 별도 branch 및 열린 테스트 PR.
- **지금 당장 App을 먼저 등록할 필요는 없다.** 먼저 Agent A1의 안전한 코드와 bootstrap 제안을 리뷰한다. 사람의 승인 전 write-capable workflow를 실행시키지 않는다.
- GitHub App **사용을 설계 방향으로 선택한 것**과 App 설치·워크플로 활성화·봇 push·최종 merge에 대한 **실행 승인**은 각각 다르다.

## H1. 코드·권한 검토 및 bootstrap 승인

- [ ] 소유 계정/저장소를 확인하고, [다음 단계 인계](12-next-steps-handoff.md) 및 [상세 설계](09-github-app-design.md)를 읽었다.
- [ ] 기존 `generated-sync.yml`의 기본 토큰 직접 push가 안전하게 제거될 계획인지 확인했다. **현재 이 워크플로는 source path push에서 원격 write를 시도할 수 있다.** 로컬 에이전트의 첫 원격 구현 커밋이 이를 실행하지 않는지 승인 전 확인한다.
- [ ] bootstrap PR에서 **기본 브랜치에 도입할 Trusted Writer가 비활성/fail-closed**인지, PR 브랜치 script·Artifact를 높은 권한으로 실행하지 않는지 독립 검토했다.
- [ ] Writer가 App 토큰을 얻기 전 repo/ref/run SHA·artifact 경로·허용 generated-only diff를 검사하는지, 브랜치 HEAD 이동 시 force push 없이 중단하는지 확인했다.
- [ ] 실제 repository Rulesets와 required `PR Gate`의 체크 이름·source·보호 규칙, App bot의 branch push 제한을 GitHub 설정에서 확인했다. 조회 불가하면 승인하지 않는다.
- [ ] bootstrap **별도 PR의 squash merge** 여부를 사람으로서 명시적으로 결정했다. `main` 직접 push나 Ruleset bypass 없이 반영한다.

**확인할 이유:** `workflow_run` Writer는 workflow 파일이 **기본 브랜치에 존재해야 실행**된다. bootstrap 없이 PR #294 브랜치에만 파일을 추가하고 “운영 E2E 완료”라고 볼 수 없다. [GitHub 공식 이벤트 설명](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run).

## H2. GitHub App 및 Secret 준비

H1의 설계 검토가 끝나고 등록이 승인되면 아래를 실행한다.

1. [GitHub App 생성](https://github.com/settings/apps/new)을 열고 **소유자 `mols3131d`**로 앱을 등록한다. 이름은 사용 가능한 것으로 정한다(예: `mols-generated-sync`). 사용 목적은 CI 산출물의 제한적 commit이며, **Webhook 사용 안 함**, OAuth 사용자 로그인/서버 호스팅 불필요, 다른 계정의 설치를 허용하지 않는 private App을 선택한다.
2. Repository permission은 **Contents: Read and write**와 자동 부여되는 **Metadata: Read**만 사용한다. `Workflows`, `Checks`, `Pull requests`, `Administration` 권한은 요구하지 않는다. Ruleset bypass actor로 등록하지 않는다.
3. App의 **Install App** 화면에서 `mols3131d`를 선택한 뒤 **Only select repositories → `mols-agent-assets` 하나**를 지정하고 설치한다. `All repositories`로 넓히지 않는다.
4. App의 **Client ID**를 확인하고 private key(PEM)를 생성한다. **PEM 파일은 로컬 에이전트, PR, Issue, 로그, Artifact, 채팅에 제공하지 않는다.** 생성 직후 저장·폐기·교체 책임은 소유자에게 있다.
5. **우선 권장:** 저장소 `Settings → Environments`에 `generated-writeback` 환경을 만들고, **Deployment branches and tags = Selected branches and tags → Branch `main`만** 허용한다. 이 설정은 **Writer 실행 job ref**만 제한하며, Writer가 다른 branch에 push하는 대상 검증을 대체하지 않는다.
6. 해당 Environment의 **Secret** `GENERATED_SYNC_APP_PRIVATE_KEY`에 PEM 전체 내용을 넣는다. Client ID는 같은 Environment의 **Variable** `GENERATED_SYNC_APP_CLIENT_ID`에 설정한다. 로컬 에이전트는 job의 `environment` 참조 코드만 작성하고 실제 값을 보지 않는다. **Repository-level Secret보다 이 방식이 안전하다.**
7. 선택한 환경을 사용하는 Writer job이 `main`에 한정되며, Producer/PR Gate와 다른 branch workflow에서 Secret을 받을 수 없는지 확인한다. App 토큰 발급은 `actions/create-github-app-token`의 검증된 SHA로 고정하고, `owner` 인자를 비워 두어 **현재 저장소 하나에 국한**한 토큰을 요청한다. 권한은 `permission-contents: write`로 제한한다.

> [!IMPORTANT]
> GitHub **public** 저장소는 모든 현행 요금제에서 Environment Secret과 branch 제한을 사용할 수 있다. **private** 저장소는 GitHub Pro/Team/Enterprise 등의 지원 요금제가 필요하다. 현재 저장소의 visibility·계정 플랜을 실제 설정에서 확인하고 **Environment Secret이 불가능하면 작업을 멈춰 대안을 심사**한다. 일반 Repository Secret으로 조용히 대체하지 않는다. [GitHub 환경 기능](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments).

**인증 참고:** [공식 create-github-app-token 사용법](https://github.com/actions/create-github-app-token) · [App 등록](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app). 실제 구현에 사용할 이름과 버전은 로컬 Agent가 최신 공식 명세에 맞춰 고정한다.

## H3. 격리 쓰기 E2E를 명시적으로 승인

- [ ] **독립 테스트 브랜치 + 열린 테스트 PR**을 준비했다. 기존 PR #294 브랜치나 `main`을 write-back 실험 대상으로 사용하지 않는다.
- [ ] bootstrap Writer는 기본값 **disabled**이며, 테스트에서는 사람이 지정한 branch만 대상이 되도록 정확한 ref allowlist를 확인했다. App 설치/Secret 등록만으로 모든 branch의 Writer가 실행되게 두지 않는다.
- [ ] 테스트 범위(생성 파일·source 경로·봇 push 권한·테스트 후 복구 절차)를 확인하고 **실제 쓰기 E2E 실행을 명시적으로 승인**했다.
- [ ] 승인된 범위에서 enable 또는 test mode를 활성화한 후 [검증 행렬](11-verification-plan.md)의 `E01`~`E09` 핵심 항목을 확인했다. 필요한 경우 로컬 에이전트는 분석을 보조하지만, 기존 권한을 넘어 계정/설정을 바꾸지 않는다.
- [ ] **source SHA → App generated commit SHA → PR `synchronize` → 실제 required `PR Gate` 성공**이 일치하는 run URL·SHA·changed files를 확인했다. Source 커밋의 이전 성공이나 Writer job의 성공만으로는 불충분하다.
- [ ] ChatGPT GitHub Plugin/Contents API의 **연속 수정**, no-op, stale SHA, bot loop, Secret 접근 금지, 생성 파일만 커밋을 테스트했다.
- [ ] 테스트 완료 후 scoped enable 값을 되돌리거나 운영 허용 범위를 별도로 승인했다. 필요하면 App 설치 비활성/키 폐기·교체 등 롤백을 준비했다.

`Environment`에 Required reviewers를 설정하면 **각 Writer 실행마다 사람 승인**이 필요할 수 있다. 이는 완전 무인 운영과 충돌한다. 단계적 시험에서는 선택적으로 사용할 수 있으나 **운영 자동화에서는 main-only 환경 + 사전 코드 검토 + 최소 권한 + branch 검증**과의 균형을 실제 지원 기능에 맞춰 결정한다. 리뷰어 보호를 임의로 해제하지 않는다.

## H4. 최종 리뷰 및 운영 승인

- [ ] 로컬 에이전트가 최신 PR body의 낡은 “App/Secret 불필요” 안내를 실제 설계·구현·현재 head/base에 맞춰 갱신했다.
- [ ] 독립 보안 검토와 실제 required `PR Gate`가 최종 후보를 통과했다. 필요한 Ruleset review/Code Owner 요건도 만족했다.
- [ ] Writer는 source branch의 임의 코드를 실행하지 않고, 실제 GitHub App installation token만 후속 `PR Gate` 자동 재실행을 유발하는 데 사용한다.
- [ ] App 설치/환경 Secret에 대한 키 회전·접근 최소화·중지 방법과 실패 run 진단 방법이 기록됐다.
- [ ] 사람의 별도 승인으로 **PR #294의 Draft 해제와 squash merge**를 결정했다. 자동 머지 금지.

## 문제가 생겼을 때

| 문제 | 사람이 할 일 |
| --- | --- |
| App 설치·토큰 발급 실패 | App 소유 계정·설치 저장소·Contents 권한·Client ID·환경 Secret 존재를 확인; PAT/타 계정으로 우회하지 않음 |
| Workflow가 실행되지 않음 | bootstrap이 `main`에 있는지, Producer event/path filter와 Writer `workflow_run` 이름·상태를 조회 |
| 생성 봇 커밋 후 PR Gate 없음 | 해당 최신 head/merge SHA의 실제 required check 확인; 누락 시 병합 금지 |
| 뜻밖의 branch write/Secret 노출 위험 | Writer enable을 끄고 App 설치/키를 격리·교체, 증거 보존, 독립 검토 후 재개 |
| Private 저장소에서 Environment 기능 없음 | 사전 승인된 다른 비밀관리 방식이나 플랜 변경을 검토; 자동으로 Repository Secret 사용 금지 |

**기록할 것:** 실제 승인 단계, App 공개 slug(이름만), 설치 범위, 현재 branch/SHA, E2E run URL·결론, 미검증 조건. **기록하지 말 것:** 개인키, Access token, API 응답의 credential, 민감한 설정값.

이 문서는 실행 체크리스트다. 등록·승인·실험을 실제로 수행한 뒤에만 각 항목을 체크한다.
