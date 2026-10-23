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
- [ ] 이전 자산과의 중복·독립 선택 가치, 현재 배포/라우팅 경로 재확인

### 2. Research — 판단에 필요한 근거 확보

- [ ] 공신력 있는 테스트 설계·테스트 오라클·격리·flakiness 참고 자료와 실무 사례 비교
- [ ] 테스트 유형 나열보다 판단을 돕는 최소 원칙 추출
- [ ] 신규/기존 테스트, 위험도 높음/낮음, 코드/비코드, 실행 가능/불가능의 경계 정리
- [ ] 테스트 설계 전문 Skill 신설이 단순 coding-context 보강보다 나은지 반례로 검증
- [ ] 유지보수 비용과 false confidence를 높이는 안티패턴 및 반대 사례 기록

### 3. Design — Contract 확정

- [ ] activation description과 negative/near-miss boundary 정의
- [ ] 역할: test surface 선택, scenario/oracle 선정, fixture/isolation, quality/gap review
- [ ] 출력: 질문 난이도에 맞춰 최소 충분 설계 또는 review 결과; 고정 양식 강제하지 않기
- [ ] 테스트 실행 여부와 evidence claim의 명확한 구분
- [ ] reference는 conditional loading 이득이 있을 때만 추가하기
- [ ] 범용 원칙과 repository-/tool-specific contract를 분리하기

### 4. Implementation — Canonical Skill

- [ ] `src/rulesync/.rulesync/skills/mols-test-design/SKILL.md` 신규 작성
- [ ] 실제 독립 가치가 있는 경우에 한해 `references/` 작성
- [ ] `docs/skills/mols-test-design/`에 유지보수 판단·eval 기준 보존
- [ ] canonical source 수정 후 공식 generator로 필요한 route/index 재생성, 직접 편집 금지
- [ ] 불필요한 config, 새로운 framework, 자산 간 hard dependency 도입하지 않기

### 5. Validate & Evaluate — 근거에 맞는 품질 판정

- [ ] Rulesync structural validation 및 frontmatter·routing 경계 확인
- [ ] `mise run test`와 적용 가능한 repository-native validation 실행
- [ ] positive/negative/near-miss trigger cases로 과도·부족 activation 검토
- [ ] behavior cases로 정확한 테스트 설계, 과잉 테스트 방지, 경계·비실행 상태 처리 검토
- [ ] 실제 model/runtime eval이 가능하면 조건·결과·revision을 기록하고 불가능하면 미검증으로 표시
- [ ] 테스트가 fixture 자체에 과적합하지 않는지 새 scenario 및 반례로 확인
- [ ] `PR Gate`의 실제 결과와 변경 반영 여부 확인

### 6. Review & Finalize — 완성 판단

- [ ] 설계 책임, 이식성, token/context 비용, 도구 불필요 의존성 다관점 리뷰
- [ ] 검증과 리뷰에서 발견한 중요한 문제만 개선, 필요하면 반복
- [ ] 문서가 원본 instruction을 복제하지 않는지 최종 점검
- [ ] [Research](research.md), 이 문서와 PR 본문의 근거/진행 상태 정합화
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
- **현재 상태:** PR 준비 단계. Skill source, runtime eval, 최종 CI 판정은 아직 완료되지 않음.
