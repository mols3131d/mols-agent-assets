# 부트스트랩 설계 스킬의 과잉 작업 유발 가능성 검토

> **대상:** [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256), head `824df8aae52e6db534145f1733eb95bcd0e9aa85` (2026-10-25).
>
> **성격:** 과업 실행량·조사 범위·검토 강도·산출물 범위에 대한 **정적 다관점 리뷰 및 개선 인계**. 저장소 운영 정책의 정본이나 모델 실행 결과가 아니다. 실제 작성 원본은 [SKILL.md](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md).
>
> **관련:** [기존 과설계/문구·구조 검토](https://github.com/mols3131d/mols-agent-assets/blob/dfa9f45ce7da69673f08d3e53df88f5a7a23fe7d/inbox/github-258/bootstrap-overengineering-review-2026-10-25.md), [안전성 반례 보고서](https://github.com/mols3131d/mols-agent-assets/blob/dfa9f45ce7da69673f08d3e53df88f5a7a23fe7d/inbox/github-258/bootstrap-isolation-review-2026-10-25.md), [개발환경 운영 정본](https://github.com/mols3131d/mols-agent-assets/pull/258). 이 문서는 특히 **스킬을 호출한 에이전트가 불필요한 일을 실제로 더 하게 되는지**에 초점을 둔다.

## 결론

**설계 단계에서 과잉 작업을 유발할 위험이 있다.** 스킬 자체가 도구 설치·환경 변경·코딩 실행을 지시하는 것은 아니지만, 작은 리뷰·단일 setup 보강·특정 설치 권한 검토에도 **전체 lifecycle 설계, 도구 전수 조사, 전 유형 권한 매트릭스, 모든 실패 반례 검토, 일률적인 구현 인계**가 필요하다고 해석될 여지가 있다.

**요구되는 개선은 새 기능이 아니라 작업량을 요청과 위험에 비례시키는 것**이다. 모든 예외를 선제 조사하는 대신, 해당 작업의 정확성과 권한 경계에 영향을 주는 사실만 확인한다. 기존 도구 관리자의 native 기능과 저장소의 정본을 우선하고, 더 조사해도 결정이 달라지지 않으면 멈춘다.

| ID | 판단 | 스킬에 있는 근거 | 실제 과업 비용/위험 | 최소 조치 |
| --- | --- | --- | --- | --- |
| W1 | 🟡 Medium | Procedure `Assign owners. For every managed item` | 요청 밖의 모든 도구·의존성에 선언/해석/설치/검증 owner를 반복 조사 | **영향받는 항목 및 직접 의존 항목으로 한정**; owner가 명확하면 그 이상 조사하지 않음 |
| W2 | 🟡 Medium | Procedure `Design two paths` | setup만 수정하려 해도 update resolver, lock diff, upgrade workflow까지 설계할 가능성 | **요청한 lifecycle만 상세 설계**; 다른 경로는 계약 충돌을 막는 최소 경계만 확인 |
| W3 | 🟡 Medium | `Decision Checks`의 fresh/re-run/update/failure/CI·multi-platform 7개 관점 | 단일 오류 리뷰에 모든 OS·네트워크·installer 실패를 조사하고 테스트 계획을 확대 | **적용 가능한 대표 반례**만 선택; 플랫폼 실증은 호환성 주장이 있을 때 |
| W4 | 🟡 Medium | `Handoff`의 고정된 7개 산출 요소와 `Stop at a design-ready handoff` | 단순 리뷰·의견 요청에도 설계서와 구현 인계, 검증 계획 과생성 | 리뷰는 **판단·근거·위험·최소 수정**으로 종료; 설계·인계는 요청 시만 |
| W5 | 🔵 Low | `Inspect current environment contract`와 installer authority/preflight | 설계만 하는데 실제 호스트의 설치 상태·OS를 모두 조사하거나 실행하고 싶어질 위험 | **필요한 repo manifest·정본 읽기부터**; host probe는 결론이 달라질 때만, 실행 전 권한 확인 |
| W6 | 🔵 Low | `Design for explicit installation consent` + `Decide missing-tool behavior` + Decision Checks | 실제 설치가 예정되지 않은 설계 리뷰에서 사용자에게 즉시 설치 허가를 요구할 오해 | **설계 결과에 미래의 설치 승인 지점만 표시**; 구현 요청과 설치 실행 허가는 별개 |
| W7 | 🟡 Medium (평가 공백) | [11개 Eval 사례](../../evals/skills/mols-dev-env-bootstrap-design/cases.json)는 대부분 복합 lifecycle 시나리오 | 짧은 요청을 적게 조사·짧게 답하는 능력을 측정하지 못함 | **기존 behavior case를 교체·보강**해 narrow review와 영향 없는 단계 생략을 관찰 |

**근거 수준:** W1–W6은 현재 Skill 텍스트에서 확인한 instruction pressure와 그로부터 **추론한 행동 위험**이다. 실제 target 모델이 추가 작업을 했다는 실행 trace는 없다. W7은 현재 fixture 구성의 직접 관찰이며, 실제 모델의 과업 확장 비율은 **미측정**이다.

## 작업량 검토 루프

### Loop 1 — 요청 → 필수 작업 매핑

세 가지 크기의 실제 요청을 가정해 Skill instruction과 비교했다.

| 요청 예 | 충분한 작업 | 스킬이 지나치게 확장할 수 있는 작업 |
| --- | --- | --- |
| **좁은 리뷰:** “현재 update가 dirty lock을 보호하는지만 검토해줘” | 관련 lock·Git 상태 검사·변경 보존을 확인하고 finding·근거·최소 보강 제시 | 전체 toolchain 조사, bootstrap 신규 설계, 설치 권한 매트릭스, 모든 OS 테스트 계획 |
| **부분 설계:** “Python 프로젝트의 최초 setup만 개선해줘” | 현재 Python 환경 owner/lock·설치 범위·재실행 안정성을 설계 | unrelated Node/npm/Rulesync 조사, 별도 update 기능 설계, 존재하지 않는 플랫폼 지원 설계 |
| **전체 설계:** “최초 환경 설정부터 명시적 bounded update까지 설계해줘” | 해당 repository의 관련 도구·잠금·권한·복구·검증 계약을 종합 설계 | 실제 설치·호스트 변경, 자체 manager/permission engine 신규 개발, 모든 잠재적 OS의 실행 검증 강행 |

세 번째처럼 **명시적으로 전체 lifecycle 설계**를 요청한 경우, 넓은 검토는 과잉이 아니다. 판단의 기준은 절차 수가 아니라 사용자가 실제로 요청한 결과를 만드는 데 필요한지다.

### Loop 2 — 세 관점의 반례 검토

**업무 효율 관점:** `For every managed item`은 매니페스트의 단순 도구 추가와 시스템 전체의 도구 감사를 구분하지 않는다. 특히 lock, installer, verifier 4개 owner를 항목마다 찾으려 하면 이미 native manager가 소유한 계약을 재설명하기 쉽다. **영향받는 owner 경계만 명시**하고, native 방식이 분명하면 추가 분해를 중단하는 편이 낫다.

**안전 관점:** 사용자 동의·전역 상태 보존·프로젝트 격리·부정확한 READY 방지는 **삭제하면 안 되는 불변 조건**이다. 다만 설계 리뷰 중에 실제 설치 명령을 실행하거나 승인을 획득할 이유는 없다. 위험에 맞는 설계상 승인 조건을 기록하면 충분하다. 반대로 나중에 **실제 설치를 실행**할 때에는 운영 정본에 따라 사용자 사전 허가가 필요하다.

**이식성 관점:** 모든 언어·OS·패키지 관리자가 Python `.venv`, mise, Git hooks처럼 작동하지 않는다. `CI and multi-platform usage` check도 매 작업에서 교차 OS 검증을 강제하는 규칙으로 해석해서는 안 된다. **실제 지원한다고 선언한 플랫폼과 변경 영역에서 확인할 것**을 제시하고, 사용자가 요청하지 않은 platform 추가는 제안 수준으로 제한한다.

### Loop 3 — 출력 계약·Eval과 비교

- Description은 이미 일반 package update·단일 도구 설치·CI-only 설계를 제외한다. 하지만 **일단 Skill이 선택된 후** 작업 범위를 줄이는 규칙이 약하다. Activation 축소만으로 W1–W4를 해결할 수 없다.
- `Procedure`의 6단계와 `Decision Checks` 7개는 큰 설계에는 유용하지만 **항상 순서대로 실행해야 하는 필수 체크리스트**인지 분명하지 않다. 작은 작업에서 불필요한 단계를 생략해도 된다는 한 문장을 추가하는 편이, `quick/full` 모드나 복잡한 work-budget 설정을 만드는 것보다 가볍다.
- 현재 11-case suite는 activation 3, negative 3, behavior 5이다. Behavior 중 `portable-owner-and-update-handoff`는 전체 setup/repair/update를 요청하며, `missing-host-and-home-installer`, `dirty-state-and-platform-evidence`도 여러 위험을 한번에 묻는다. **좁은 과업에서 범위 준수**를 측정하는 rubric은 없다.
- 지난 capability trial의 낮은 near-miss·behavior 점수는 알려져 있지만 **응답 길이·툴 호출 수·불필요한 설계 확대**를 측정한 증거는 아니다. 새로운 모델별 점수나 개선 효과는 주장하지 않는다.

## 권고할 최소 패치 (스킬 자체)

새 resource, agent, mode, schema, CLI option, 승인 엔진을 만들지 말고 기존 `SKILL.md`의 의미만 작게 정리하는 것이 좋다.

1. **Procedure 앞:** “요청 결과와 변경·검토 대상을 먼저 좁힌다. 관련 없는 도구·플랫폼·lifecycle 단계는 조사·설계하지 않는다. 필요 시만 추가 로드한다.” 같은 범위 규칙을 한 번 둔다.
2. **Assign owners:** `every managed item` 대신 **affected items and their direct prerequisites**로 한정한다. 새 owner 표가 없어도 정본으로 충분하면 링크만 제공한다.
3. **Design two paths:** **둘 다 요청된 경우에만** 상세 setup/update를 설계한다. setup-only라면 암묵적 upgrade 금지만, update-only라면 기존 locked setup 훼손 방지만 확인한다.
4. **Decision Checks:** 모든 7개 반례를 실행 목록으로 강제하지 말고 **해당 작업에 실제 적용되는 실패 경로만** 검토한다. 중요한 격리·승인 경계는 빠뜨리지 않는다.
5. **Handoff:** `Review → findings`, `Design → 필요한 설계안`, `Implementation handoff → 작업 범위·검증 인계`로 종료 결과를 요청에 맞춘다.
6. **평가:** 추가 Eval harness 없이 기존 behavior 1건을 **“좁은 bootstrap 리뷰”** 사례로 수정하거나 교체하고, `unrequested tools/platforms/update design are not expanded`를 한 가지 rubric으로 확인한다. 실제 결과를 실행·비교한 후 문구를 유지/되돌린다.

**중단 규칙:** 현재 질문에 답할 충분한 근거가 있고 추가 확인이 필수 제약 또는 결과를 바꾸지 않는다면 작업을 끝낸다. 한계는 `unknown/not verified`로 남기며, 이를 채우려고 요청 밖의 플랫폼 설치나 광범위한 실험을 새로 시작하지 않는다.

## 하지 않아도 되는 작업

- 모든 도구의 설치 경로·cache·버전을 정기적으로 전수 검사하는 별도 프로세스
- 모든 OS, 셸, 패키지 관리자마다 별도 bootstrap 설계·테스트 매트릭스 작성
- 설계만 요청받은 상황에서 설치 권한 요청, 실제 `setup/update` 명령 실행, user HOME 상태 변경
- 부족한 한두 개의 반례를 위해 새 Skill 하위 파일·권한 데이터 구조·독립 Eval runner·subagent 시스템 추가
- 단순 리뷰를 전체 lifecycle 개편·PR 변경·코딩 구현으로 확대

## 기존 보호·정본과의 관계

- 이 보고서는 설치 승인 자체를 약화하지 않는다. 실행 에이전트의 실제 설치 허가 기준은 [Development Environment](https://github.com/mols3131d/mols-agent-assets/pull/258)가 소유한다.
- [이전 안전 보고서](https://github.com/mols3131d/mols-agent-assets/blob/dfa9f45ce7da69673f08d3e53df88f5a7a23fe7d/inbox/github-258/bootstrap-isolation-review-2026-10-25.md)의 Git 상태·uv group·venv 격리 결함은 *실제 코드*의 독립된 개선 대상이다. 스킬 간소화 때문에 그 수정을 생략해서는 안 된다.
- Skill이 “설계만 한다”는 결정은 유지한다. 별도 구현 요청은 호출자의 일반 개발 작업이 소유하고, **설계 Skill의 선택만으로 저장소 파일·호스트 상태를 수정하지 않는다.**

## 검증과 인계

| 항목 | 상태 |
| --- | --- |
| GitHub PR #256 최신 head·Skill·설명/평가 fixture 직접 확인 | ✅ 확인 |
| 요청 유형별 과업 범위와 static instruction gap 비교 | ✅ 정적 검토 |
| 실제 Skill이 과도한 도구 호출·조사를 수행했는지 | ⚪ 미측정 |
| 새로운 좁은 과업 fixture의 모델 behavior 결과 | ⚪ 미실행 |
| Skill source·runner·CI 변경 | ⚪ 수행하지 않음 |

**최종 제안:** 기존 스킬을 더 능동적으로 만들기보다, 현재 좋은 안전 불변 조건은 보존하면서 **요청별 관련성·조사 중단 조건·종료 산출물** 세 가지를 명시한다. 리뷰에서 결함을 발견하면 최소한의 권고로 끝내고, 전체 lifecycle 설계가 요청된 때에만 넓게 작업하도록 한다.
