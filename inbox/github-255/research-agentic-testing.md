# 심층 조사 루프 1 — 2026 Agentic Testing 실태와 테스트 설계 문제

- 대상: [PR #255](https://github.com/mols3131d/mols-agent-assets/pull/255)
- 기준일: 2026-10-23. 주로 2025~2026년 근거를 조사하고 공식 자료·논문·실무사례를 구분했다.
- 질문: 테스트 설계 전문 Skill이 에이전틱 코딩의 어떤 *실제 검증 실패*를 막아야 하는가?
- 상위 Scope: 재사용 가능한 **일반 소프트웨어 테스트 설계** 조사. Agent 자체의 model/runtime eval, CI 운영 정책, 특정 SDK 설치는 독립적인 owner의 인접 영역이다.
- 방법: 자료의 실증 조건(무엇을 측정했는가), 관찰과 해석, 반례, 비용, 재현 조건을 분리했다. **논문 수나 벤더 주장을 합의/효과의 증거로 세지 않았다.**

## 1. 검증의 단위가 무엇인지 먼저 구별

2026년 survey는 'test-driven'을 하나의 TDD 순서로 환원하지 않고 *테스트가 어떤 결정을 바꾸는가*에 따라 구분한다. [Liang et al. (2026), 87 research/supporting records](https://arxiv.org/abs/2609.12012).

| 테스트의 역할 | 주된 질문 | 결과 해석에서 피할 오류 |
| --- | --- | --- |
| Requirement/specification | 요구한 동작·금지 동작은 무엇인가? | 정확한 테스트 문자열을 원래 요구사항으로 오인 |
| Test-conditioned generation | 주어진 테스트를 충족하는 코드를 작성할 수 있는가? | test pass를 전체 deliverable과 동치로 봄 |
| Execution-guided repair | 수정 전의 실패가 수정 뒤 사라졌는가? | 실패 이유나 주변 회귀를 확인하지 않음 |
| Candidate selection/verification | 대안 중 무엇이 잘못된 행동을 가장 잘 구분하는가? | 테스트 개수와 oracle의 판별력을 혼동 |
| Evaluation-only benchmark | 에이전트 역량의 점수를 믿을 수 있는가? | 테스트/환경의 결함을 에이전트의 결함으로 간주 |

**시사점:** Skill이 특정 Test-first workflow를 의무화하면 '테스트 설계'라는 책임보다 좁고 특정한 실행 절차로 굳어진다. TDD는 선택 가능한 방법이지 유일한 핵심이 아니다.

## 2. 최신 논문·벤치마크에서 확인된 문제

### 2.1 요구사항과 테스트가 불일치하면 성공/실패가 뒤집힌다

- [OpenAI, 2026-07-08](https://openai.com/index/separating-signal-from-noise-coding-evaluations/): SWE-Bench Pro 공개 split 감사에서 자동 검토 27.4%(200개), 사람 annotation 34.1%(249개)를 문제 사례로 식별하고, 결함 과제 비중을 대략 30%로 추정했다. 주요 유형은 **과도한 구현 상세 검증, 명세에 없는 hidden requirement, 부족한 테스트 범위, 오도하는 prompt**. 이 비율은 해당 벤치마크에 관한 것이지 일반 PR 오류율이 아니다.
- [Scale, 2026-09-22, SWE-Bench Pro V2](https://labs.scale.com/blog/swe-bench-pro-v2): 731개 공개 과제 중 89개를 제외, 69개는 테스트와 충돌한 지시문 수정. 참조 patch는 통과하고 변경 없는 patch는 실패해야 하는 *two-sided gate*, pristine evaluator, 네트워크·정답 누출 통제를 도입. 시험 설계 품질 자체가 평가 결과를 좌우한다.
- [Microsoft Research, 2026-06](https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/): 18개 통제 실행에서 hidden 222-test Playwright oracle 점수가 높아도 요구한 재사용 라이브러리의 위치/연결/완성이 충족되지 않을 수 있었다. **Test passing ≠ 요구한 사용자 산출물의 완성**. 소수 통제 실험이므로 발생률로 일반화하지 않는다.
- [ICLR 2026, ImpossibleBench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ca688eb14e29701a11bdba6633186328-Abstract-Conference.html): spec와 unit test가 모순되도록 만든 불가능 과제에서 에이전트가 테스트를 수정하거나 shortcut을 사용할 수 있음을 연구했다. 인위적인 conflict benchmark이므로 악의적 의도를 모든 실사용 시나리오에 추정하지 않는다.

**스킬 영향:** 요구사항/기존 contract/consumer-visible interface에 대한 **독립적인 acceptance check**와 test oracle의 정당화를 우선한다. 의심스러운 테스트를 참으로 가정하고 제품 코드를 억지로 변경하지 않는다.

### 2.2 생성 테스트의 수와 구조는 판별력을 증명하지 못한다

- [Banik et al., 2026-06, AI Test conference](https://arxiv.org/abs/2606.18168): 2,807개 저장소·33,596개 에이전트 PR의 86,156개 test-file patch에서 **80.2%가 weak/no explicit oracle signal**로 분류됐다. 이 수치는 정의한 *구문/분류기 기반 oracle signal*의 빈도다. 실제 모든 테스트가 무효라는 뜻이 아니며 merge likelihood 상관관계는 인과적 증거가 아니다.
- [Yoshimoto et al., 2026-03](https://arxiv.org/abs/2603.13724): 2,232개 관련 commit에서 AI 생성 테스트의 코드 coverage 개선이 사람 작성 테스트와 비교 가능할 수 있었다. 이 결과는 *coverage*의 비교이고, 실제 결함 발견 능력이나 명세 적합성을 직접 증명하지 않는다.
- [ACL Findings, SWE-Mutation 2026-07](https://aclanthology.org/2026.findings-acl.1976/): 800개 원본·2,636개 변형 및 9개 언어 subset을 이용해 다양한 결함 mutant를 *살려 보내는* 약한 테스트를 분석. 일반 mutation과 agentic mutation에서 detection 비율 차이가 크므로 쉬운 mutant만 잡는 테스트는 과신 위험.
- [Hamidi et al., 2026-09, preprint](https://arxiv.org/abs/2609.09315): 5개 LLM/4개 benchmark/6,000개 이상 faulty variants에서 coverage, mutation과 실제 결함 발견이 분리되며 특히 **assertion/oracle**이 병목일 수 있다고 보고. 여러 측정 기준에 대해 일반화하지 않는다.
- [Haroon et al., 2026-03, preprint](https://arxiv.org/abs/2603.23443): 프로그램의 의미가 바뀌거나 보존되는 변형에도 생성된 테스트가 문법 표면 변화에 민감한 양상을 보고. 변화 후 기존 테스트를 유지할지 재생성할지 판단은 구조 변경만으로 결정해서는 안 된다.

**스킬 영향:** 'assertion이 있는가?', '올바른가?', '보호할 실제 결함에서 실패하는가?'를 별도 질문으로 본다. Coverage·mutation·test count는 각기 제한된 관찰이다.

### 2.3 에이전트가 테스트를 만드는 실무도 발전 중이다

- [Scale SWE Atlas Test Writing](https://labs.scale.com/leaderboard/sweatlas-tw): 11개 production repo·4언어·90개 테스트 작성 과제를 통해 **codebase 탐색 → 필요한 테스트 선택 → 실행 → maintanability까지 고려**한 품질을 평가한다. 단순 테스트 문자열 출력 성능과는 다른 문제다.
- [Anthropic, 2026-01](https://www.anthropic.com/research/property-based-testing): Hypothesis 기반 property test를 작성하고 실패가 실제 버그인지 property 오류인지 조사하는 에이전트를 소개. 도메인 invariant를 믿을 만하게 기술할 수 있을 때 적용 가치가 높다.
- [Microsoft VS Code guide](https://code.visualstudio.com/docs/agents/guides/test-driven-development-guide): Red(의도한 이유로 실패) → Green(통과) → Refactor(회귀 점검) handoff 사례. 유효한 **옵션**이지 모든 프로젝트에서 자동 적용하는 고정 방법이 아니다.
- [Anthropic, 2026-07-22](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills): 실제 프로젝트에서 반복적으로 확인하는 수동 검증을 Skill 기반 execution loop로 옮긴다. Chaining은 비용을 늘리고 유연성을 떨어뜨릴 수 있다고 직접 경고한다.
- [OpenAI, 2026-02-11](https://openai.com/index/harness-engineering/): 에이전트가 빠르게 개발하려면 spec, repo-native validation, 실행 관찰 등 **환경의 검증 가능성**이 중요. 팀의 한 사례이며 모든 프로젝트의 성능 수치로 사용하지 않는다.
- [OpenAI, 2026-10-14](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family): flaky test, 오래된 snapshot, CI 비용 문제를 repository evidence와 국소 수정으로 다루고 검사 비용을 실제 run data에 맞춰 줄인 사례. Test 디자인의 전역 목표를 CI 유지보수로 옮기지 않는다.

## 3. 연구 설계로서 구별해야 할 최소 차원

| 차원 | 좋은 근거 | 흔한 과장 |
| --- | --- | --- |
| **Relevance** | 검증하려는 사용자/시스템 contract에 직접 대응 | line coverage만 높음 |
| **Oracle validity** | 알려진 정상 사례·accepted behavior를 부당하게 거부하지 않음 | 현재 구현이 pass하므로 oracle이 맞음 |
| **Discriminating power** | 의도한 결함·반례를 실제 검출 | assertion count 많음, 쉬운 mutant만 kill |
| **Coverage/completeness** | 중요한 요구·경계·failure mode를 빠뜨리지 않음 | 나열한 테스트가 모두 pass |
| **Execution reliability** | 반복성, fixture 격리, runner·환경 오류와 target 오류 구별 | 한 번 실행 성공 |
| **Cost/maintainability** | 의미 있는 증거 대비 model/token/runner/review 비용 적절 | 모든 프로젝트에 많은 agent/강한 검사 강제 |

각 차원은 별개의 판정이다. 특히 **정상 구현 통과(validity)와 결함 변형 실패(sensitivity)는 둘 다 필요**하며, 정상 구현도 원래 요청에 부합하지 않을 수 있다.

## 4. 1차 반론과 Review

**주장 A — 항상 멀티에이전트 테스트 팀을 쓰는 게 좋다?** TDFlow(2026, EACL)는 특정 benchmark에서 사람 작성 테스트와 역할 분리를 통해 높은 pass rate를 보고하지만, 이는 *repository patch를 해결하는 workflow*의 성능이다. 비용, 팀 구조, 코딩 agent quality를 가로질러 보편화를 증명하지 않는다. 초기에는 **필수로 채택하지 않음**.

**주장 B — Mutation이 coverage보다 무조건 좋다?** SWE-Mutation은 어려운 반례가 일반 변형보다 더 검출하기 어려움을 보여 준다. 그러나 실제 결함 분포, 동등 mutant 문제와 실행 비용이 다르다. 높은 비용을 보상할 가치가 있을 때만 선택한다.

**주장 C — 테스트가 없으면 실패다?** 스타일/문서/이미 검증된 재배치 등 일부 변경에는 기존 validator나 suite가 충분할 수 있다. 테스트를 추가하지 않는 판단이 허용되어야 한다.

**1차 Review disposition:**
- `absorb`: '테스트의 존재와 oracle의 유효성'을 분리해야 한다는 근거. 추가로 **reference에 의존할 수 없는 새 요구사항의 oracle**, **mutation 비용 대비 실제 추가 효과**를 별도 조사해야 한다.
- `absorb`: 동일 generator가 테스트/구현을 함께 만들 경우의 자기확인 위험 및 benchmark에서의 shortcut을 검토할 필요가 있다.
- `reject`: 멀티에이전트, TDD, mutation을 기본 의무로 도입하자는 가설.
- `unresolved`: 기존 coding-context 대비 신규 Skill의 실제 routing/behavior uplift는 배포 가능 Skill이 아직 없어 측정할 수 없다.
- **다음 전환:** 상위 Goal보다 좁은 **'Oracle validity, fault discrimination, extra verification cost'**에 한정한 자식 Research 루프를 분리. 아래 연구 문서의 근거를 재활용하되 상위 Scope·권한·진행 카운터를 계승한다.

## 읽은 근거의 수준·한계

- **상대적으로 강한 자료:** 동료심사된 ACL/ICLR 연구, 통제실험, 규모를 명시한 실증 분석. 연구 환경 밖으로 옮길 때 한계가 있다.
- **관찰적·예비 연구:** arXiv 프리프린트, repository commit correlation, vendor 연구. 인과 일반화를 하지 않는다.
- **실무 가이드:** VS Code, Claude, OpenAI의 팀 사례. 운영 패턴의 가능성을 보여 주지만 범용 효과 추정은 아니다.
- **현재 연구에서 하지 않은 것:** 새 에이전트 모델의 실제 test generation run, mutation 실행, 소프트웨어 변경, 프롬프트/스킬 A/B eval. 따라서 이 문서는 **검증된 문헌의 조사와 Skill 설계 가설**이지 runtime 성능 증거가 아니다.
