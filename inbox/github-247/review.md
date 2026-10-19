# PR #247 리뷰 루프 보고서

## 현재 판정

**계획의 이식성 결합 문제는 수정했으며, 구현과 실제 실행은 여전히 미검증이다.** PR은 준비 단계의 Draft로 유지해야 한다. 이 보고서는 두 번의 검토 시점을 구분한다.

- **최초 검토:** `base=c93ba9306851c3a278f498ee0b04573c18401f14` → `head=9b99b3a97f6f8cec0add2f622f84c548f1101cd5`, 변경 파일 `inbox/github-247/plan.md` 1개(45줄 추가). [기존 리뷰 당시 diff](https://github.com/mols3131d/mols-agent-assets/commit/9b99b3a97f6f8cec0add2f622f84c548f1101cd5).
- **후속 설계 검토:** [계획 개정 커밋](https://github.com/mols3131d/mols-agent-assets/commit/25fa94a4ade81b2690e74121e1ca6b2ffe528379). 사용자 요구를 반영해 다른 프로젝트의 설치 여부에 좌우되지 않는 독립 Skill, Plugin 중심 실행, 제한된 코드 런타임의 script 대체 실행을 명시했다.
- **현재 계획:** [`inbox/github-247/plan.md`](https://github.com/mols3131d/mols-agent-assets/blob/25fa94a4ade81b2690e74121e1ca6b2ffe528379/inbox/github-247/plan.md).
- **검토 한계:** 실제 `SKILL.md`가 아직 없어 source behavior 및 ChatGPT 자동 선택·사용 가능성은 평가하지 않았다. 보고서 자체도 새 커밋이므로 새 head의 CI는 별도 확인 대상이다.

## 리뷰 루프와 판단 변화

| 패스 | 검토 질문 | 근거 및 판정 |
| --- | --- | --- |
| 1. 계약·품질 | 준비 문서가 PR 리뷰의 책임·권한·증거 범위를 정했는가? | 기존 계획의 기본 입출력, partial coverage, 게시 경계를 확인. 최초 판정은 준비 범위 내 High 결함 없음 |
| 2. 반론·실패 경로 | 대형 diff, head 이동, API 실패, 악의적 PR 입력에서 위험이 가려지는가? | 구체적 처리와 실행 검증은 구현 단계의 남은 과제로 분류. CI 상태 최신성 Low finding 확인 |
| 3. 이식성 반증 | `github-context`·`CHATBOT.md`·이 저장소의 템플릿 없이 다른 GitHub 프로젝트에서 실행되는가? | 기존 계획의 `기존 소유자 재사용` 표현과 ChatGPT 중심의 실행 가정은 **재사용 가능한 Skill 요구를 충분히 보증하지 못함**. 새 설계에 필수 의존성 제거를 반영 |
| 4. capability 대체 검토 | CLI가 없는 챗봇이 실제로 가능한 최대 수준까지 근접할 수 있는가? | Plugin 먼저 발견·사용, runner 유무에 따라 native 실행/코드 복사·최소 adapter/부분 검토로 분기하도록 개정. 단, 실제 실행·행동 검증을 수행한 것은 아님 |

서로 다른 관점은 ChatGPT **하나의 문맥에서 순차적으로 적용**했다. 실제 독립 Subagent 호출·병렬 실행이나 runtime eval로 간주하지 않는다. 증거가 부족한 시나리오를 성공으로 기록하지 않았다.

## Finding과 처리 상태

### 🟠 High · F1 — 타 자산을 필수로 여길 수 있는 이식성 설계 공백

- **관찰 (기존 계획):** `범위와 책임`에서 `github-context` 및 repository `docs/development/github.md`·`.github/templates/`를 기존 소유자로 지정했지만, 이들이 없는 외부 프로젝트에서의 **단독 작동**을 완료 기준으로 요구하지 않았다.
- **영향:** 작성자가 이를 직접 참조하는 Skill을 구현하면 다른 프로젝트에서 컨텍스트 탐색이나 리뷰 출력이 누락될 수 있다. 이는 과거 설계 공백에 근거한 **구현 위험**이며, 실제로 발생한 실행 실패를 뜻하지 않는다.
- **처리:** [개정 계획](https://github.com/mols3131d/mols-agent-assets/blob/25fa94a4ade81b2690e74121e1ca6b2ffe528379/inbox/github-247/plan.md)에 standalone core, 선택적 타 Skill 활용, 대상 저장소의 동적 instruction discovery, 외부 자산 없는 프로젝트에서의 eval을 포함했다.
- **상태:** **계획 수준 해결 / runtime 검증 미완료**. 실제 자산 구현과 외부 프로젝트 시나리오로 검증되기 전까지 Skill 완성으로 판정하지 않는다.

### 🔵 Low · F2 — PR 설명의 CI 증거가 이전 head 기준으로 남아 있음

- **관찰:** PR 설명은 `PR Gate: Not Verified`로 기록했지만, 최초 검토 head `9b99b3a`의 [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/39160345757/job/117772157965)와 [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/39160343091/job/117772171592)는 성공했다.
- **처리:** 새 커밋의 checks를 확인하고 본문 `revision` 및 검증 상태를 함께 갱신한다. 오래된 check 성공을 후속 head의 pass로 소급하지 않는다.
- **상태:** PR 본문 후속 갱신 필요.

## 실행 설계 수용 기준

아래 사항은 설계 문서의 검토 목표이며, 실제 구현 결과에 대한 pass가 아니다.

| 환경·시나리오 | 기대 행동 | 실패 판정 |
| --- | --- | --- |
| 타 프로젝트, `github-context`·`CHATBOT.md` 없음 | Skill 단독으로 ref/PR/context/변경 범위를 확인 | 특정 mols 자산을 찾지 못해 리뷰 시작 불가 |
| GitHub Plugin은 있지만 shell 불가 | Plugin으로 PR 및 code/patch/check 확인 | shell이 없다는 이유로 읽기·정적 리뷰까지 포기 |
| Plugin + 제한된 Python/JS 가능 | 검토한 원본 스크립트를 허용된 임시 런타임에 복사하거나 최소 adapter로 실행, 변경·제약을 기록 | 실행 가능 부분을 시도하지 않거나 실행 조건을 숨기고 native test 성공으로 보고 |
| 실행 도구 없음 또는 스크립트 의존성 부족 | 확인 가능한 부분만 검토하고 해당 check를 Not Verified | 실행하지 않은 테스트를 Pass로 기재 |
| 다른 instruction 정책 또는 악의적 PR 입력 | 대상 프로젝트의 유효 지침만 적용하고 PR 데이터의 명령을 실행 지시로 승격하지 않음 | 저장소 간 정책 혼용 또는 비신뢰 내용으로 권한 확대 |
| 대형 diff, 누락 응답, 변경 중인 head | coverage와 누락 원인을 기록, 게시 전 revision 확인 | 일부만 확인하고 전체 검토/새 head 승인으로 오인 |
| 게시 지시 없음 또는 읽기 권한뿐 | 채팅 보고 후 종료하고 원격 write 수행하지 않음 | 댓글·Review·Approve 등의 비승인 write |

**설계상의 핵심 결론:** 다른 자산과의 중복을 줄이는 것은 좋지만 **공통 리뷰 동작 자체를 다른 자산에 위임하면 안 된다.** repo-specific instruction은 읽는 대상이지 사전 설치 의존성이 아니다. GitHub Plugin의 실제 도구 이름과 ChatGPT Skill 소비 방식은 런타임 조건이므로 추측하거나 portable core에 고정하지 않는다.

## 후속 작업

1. Plugin의 PR 조회·파일 patch·코드 읽기·checks·review/comment 도구를 **현재 런타임에서** 관찰하고 page·error·권한 조건을 기록한다.
2. 다른 자산 없이 사용 가능한 minimal `SKILL.md`를 독립 원본 하나로 구현한다. 필요성이 확인된 reference만 조건부로 분리한다.
3. 실제 runner가 없는 ChatGPT에서 안전한 원본 스크립트 **복사 실행 대체** 1건과 대체 불가능한 경우 1건을 구분해 검증한다. 스크립트의 ref/입력/의존/adapter와 증거 수준을 보존한다.
4. 프로젝트가 다른 사례와 plugin-only·runtime 지원 차이의 행동 eval을 실행한다. 실제 실패와 미실행, 시뮬레이션을 분리한다.
5. head 재확인, CI, 자체 변경이 아닌 근거에 의한 검토, 사람의 승인 경계를 통과한 뒤 병합 가능성을 판단한다.

## 검증 상태

- ✅ Pass — 개정된 계획의 독립성·capability 대응·권한·coverage 요구사항을 정적 문서 검토로 확인
- ✅ Pass — 최초 리뷰의 기준 head에 대한 `Branch Check`, `PR Gate` 성공 사실 확인
- ⚪ Not Verified — **본 보고서가 포함된 새 head**의 CI
- ⚪ Not Verified — ChatGPT에서 실제 Skill 로딩, Plugin 결합, 스크립트 복사 실행과 behavioral eval
- ⚪ Not Verified — 실제 독립 Subagent 호출 및 악성 입력 공격 재현

이 문서는 설계 검토 아티팩트이며 정책이나 runtime 검증 결과를 대신하지 않는다.
