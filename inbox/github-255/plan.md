# mols-test-design — PR #255 작업 계획

## 목표와 경계

**Goal:** 개발 에이전트가 테스트를 새로 설계하거나 기존 테스트의 적정성을 판단할 때, 중요한 observable behavior를 가장 작은 유효 검증으로 보호하도록 돕는 독립·이식 가능한 `mols-test-design` Skill을 완성한다.

**In scope**
- 책임 경계/activation/near-miss 설계 및 근거 조사
- canonical Rulesync Skill source와 필요한 최소 supporting references
- Skill을 옮겨도 독립적으로 이해·유지할 수 있는 maintainer 문서
- behavior/trigger fixture 및 적용 가능한 deterministic·runtime evaluation
- 공식 generator를 통한 필요한 derived discovery 갱신
- 리뷰·개선과 병합 준비

**Out of scope**
- 모든 언어·프레임워크 테스트 방법론의 재작성, 범용 test runner·CLI 신규 구현
- 특정 저장소의 테스트를 이 PR에서 대량 작성·변경
- `mols-ci-design`, `mols-coding-context`, `mols-agent-asset`의 책임 재정의
- GitHub Actions, Ruleset, CI policy 자체 변경
- 계획하지 않은 외부 Skill dependency 또는 vendor-specific package 생성

## 진행 단계

### 1. Prepare — 완료된 초기 기반

- [x] 최신 `main` 기반 전용 브랜치와 Draft PR #255 생성
- [x] [Goal](../../docs/skills/mols-test-design/goal.md)에 유지할 목적과 경계 초안 기록
- [x] [Research](research.md)에 repository-local 근거 및 검토할 가설 기록
- [x] 기존 자산의 responsibility/activation과 repository routing을 검토해 static 설계 공백 확인 (동작 개선 효과는 미검증)

### 2. Research — 심층/중첩 조사 완료 (설계 uplift eval은 미실행)

- [x] 2025~2026년 vendor 원문, 동료심사 연구, 벤치마크 품질 감사와 실무 사례 비교
- [x] 테스트 유형 나열보다 oracle·contract·반례·실행 근거 중심 최소 원칙 추출
- [x] 신규/기존 테스트, 위험도 높음/낮음, 코드/비코드, 실행 가능/불가능의 경계 정리
- [ ] 새 Skill이 coding-context만 적용했을 때보다 나은지 **비교 behavior eval** 수행 (설계 공백에 대한 정적 분석은 완료)
- [x] overfitting·weak oracle·over-mocking·불필요한 멀티에이전트 등 안티패턴과 반례 기록
- [x] [부모 심층 조사](research-agentic-testing.md) — 최신 논문과 benchmark·vendor 사례의 주장/한계 비교
- [x] 1차 Review가 제기한 **test oracle 유효성·fault discrimination·cost** gap을 [strict-subset 자식 루프](research-oracle-validation.md)로 독립적으로 좁혀 조사
- [x] [루프 리뷰](research-loop-review.md) — 자식 결과를 부모로 인계하고 결과를 바꾼 반론/기각/미확인 구분
- [x] 일반 코딩 Skill 대비 test-specific 설계 책임·이식성·runtime 부재의 evidence 경계 재검토

### 3. Design — Contract 확정

- [x] activation description과 negative/near-miss boundary 정의
- [x] 역할: test surface 선택, scenario/oracle 선정, fixture/isolation, quality/gap review
- [x] 출력: 질문 난이도에 맞춰 최소 충분 설계 또는 review 결과; 고정 양식 강제하지 않기
- [x] 테스트 실행 여부와 evidence claim의 명확한 구분
- [x] reference의 독립 loading 이점을 검토하고 single-file Skill 유지
- [x] 범용 원칙과 repository-/tool-specific contract를 분리하기

### 4. Implementation — Canonical Skill

- [x] `src/rulesync/.rulesync/skills/mols-test-design/SKILL.md` 신규 작성
- [x] conditional reference 효용이 없어 추가하지 않음
- [x] `docs/skills/mols-test-design/`에 goal·evaluation 기준 보존
- [x] canonical source metadata를 사용해 기존 route generator와 동일한 형식의 distribution route 생성·정합성 점검 (전 저장소 generated validator는 미실행)
- [x] 불필요한 config, 새로운 framework, 자산 간 hard dependency 도입하지 않음

### 5. Validate & Evaluate — 근거에 맞는 품질 판정

- [x] GitHub PR Gate의 Rulesync structural validation PASS; 별도 로컬 실행은 미실행
- [x] GitHub PR Gate에서 repository-owned deterministic test, source/Rulesync 및 affected projection validation PASS 확인 (로컬 `mise run test`는 미실행)
- [x] positive 5, negative 6의 trigger fixture 준비 (실제 model eval은 별도)
- [x] 10개 behavior fixture 및 assertion 준비 (실제 model eval은 별도)
- [ ] 실제 model/runtime eval이 가능하면 조건·결과·revision을 기록하고 불가능하면 미검증으로 표시
- [ ] 테스트가 fixture 자체에 과적합하지 않는지 새 scenario 및 반례로 확인
- [x] commit `f824a78b`의 [PR Gate run](https://github.com/mols3131d/mols-agent-assets/actions/runs/39958075540) 성공 확인; 이후 변경 head는 재확인

### 6. Review & Finalize — 완성 판단

- [x] 설계 책임, 이식성, context 비용과 도구 의존성 관점의 순차 정적 리뷰 ([review](review.md))
- [ ] 검증과 리뷰에서 발견한 중요한 문제만 개선, 필요하면 반복
- [x] maintainer 문서에 평가 목적·근거와 유지보수 기준만 두고 runtime instruction 복제 여부 점검
- [x] [Research](research.md), 이 문서와 PR 본문의 작업 단계·근거 상태 정합화 (최신 head 기준 상태는 후속 확인)
- [ ] Draft 해제 가능 조건 재검토; 최종 머지는 별도 사용자 지시에 따름

## Acceptance criteria

1. Skill이 **독립적인 일반 소프트웨어 테스트 설계 판단**을 소유하면서, coding/CI/Agent eval의 기존 owner와 충돌하지 않는다.
2. 실제 의도가 테스트 설계/충분성/품질 판단인 요청에는 적절히 선택되고, 일반 코드 작성·CI orchestration·Agent eval에 무분별하게 활성화되지 않는다.
3. 가장 적은 유용한 수준에서 중요한 정상·경계·실패/회귀 사례와 oracle을 제안하며, 의미 없는 테스트·mock·coverage·수준 고정을 피한다.
4. 대상 언어, 프레임워크, 저장소, 다른 이 레포 Skill을 모르는 환경에서도 핵심 설계 결정을 내릴 수 있다.
5. 설계·검토 근거와 실행·검증·평가 근거를 혼동하지 않고, 미실행 테스트에 통과 판정을 내리지 않는다.
6. 관련 source, route, 문서와 eval 계약이 일관되고, 실제 실행한 필수 검사에서 blocker가 없다.

## 운영 기록 규칙

- `research.md`: 근거, 비교, 대안과 남은 불확실성
- `plan.md`(이 문서): 범위, 진행, 완료 조건과 다음 행동
- 중요 리뷰 결과는 실제로 필요해질 때 별도 `review.md`로 기록
- 실행 결과는 정확한 commit/ref, command, 범위, 성공·실패·미실행을 명시
- **현재 상태(2026-10-23):** 심층·중첩 조사, portable single-file Skill 작성, 21개 eval fixture, distribution route 갱신, maintainer 문서와 [정적 리뷰](review.md) 반영 완료. 제한된 정적 검사는 통과했지만 repository-native `mise`/Rulesync 검증과 실제 model/runtime A/B Eval은 아직 수행하지 않았다. PR Gate는 `f824a78b`에서 PASS를 관찰했으며 후속 문서 커밋의 실행 결과는 재확인한다. Draft를 유지한다.


### 7. Independent Testability 심층 고도화 — 2026-10-23

- [x] 모듈 분할이 아닌 **다른 작업자의 내부 변경과 독립적인 테스트 소유·실행 경계**를 목표로 한정
- [x] [중첩 심층 검토](review-test-independence.md)에서 실제 consumer/provider 계약·트랜잭션 검증을 제거하면 안 된다는 반례 검증
- [x] canonical Skill과 description에 안정 계약, cross-component 내부 결합, 독립 test/fixture·state와 실행 비용의 판단 반영
- [x] 평가 fixture에 positive/negative/near-miss·behavior 13개 보강 — 총 34개(8/8/18)
- [x] canonical description과 distribution route 일치/정렬, fixture JSON·중복 ID·7 target, 자산 독립성의 제한된 정적 검사
- [x] 리뷰에서 발견한 모호한 activation 문구를 수정하고 다시 확인
- [ ] 현재 HEAD PR Gate의 성공 확인 및 [review](review-test-independence.md)에 execution evidence 기록
- [ ] 실제 routing·behavior model Eval 및 기존 coding-context-only baseline과 비교 (실행 환경/조건이 갖춰진 경우)

**Done의 의미:** 신규 판단과 adversarial regression fixture가 반영되고 재검토됐다는 것이며, 실행하지 않은 실제 model behavior나 framework 전체 호환성을 주장하지 않는다. 이 고도화는 새 아키텍처 Skill, Pact 의존성, 폴더 분리나 CI 개편을 추가하지 않는다.
