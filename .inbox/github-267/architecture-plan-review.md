# Architecture–Plan Review — Preparing the Chatbot Harness Design Skill

> 2026-11-02. 기존 [Research–Plan loop](research-plan-review.md)의 후속 설계 검토. 단일 챗봇의 근거 대조/다관점 순차 검토로, 독립 Subagent 실행이나 실제 runtime eval은 수행하지 않았다.

## Goal / Scope / Evidence

**Goal:** 단순 `CHATBOT.md` 연결기에서 발전해, 대상 환경에서 **안전하고 실제 작동하며 컨텍스트·도구·운영 비용이 작은 하네스**를 제안·구축·검증할 수 있는 Skill의 전초 계획을 완성한다.

**In scope:** Skill 책임·activation 비교, runtime별 구조 선택, Tool/Plugin/Code 활용, task-scoped loading, 비용·회귀 평가 설계, 구현 인계. **Out of scope:** 실제 Skill source 수정, 임의 repository 하네스 구축, 연결 계정 전환, CI/agent 신설.

**Evidence:** [기존 스킬](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md), [Agent Asset 설계 기준](../../src/rulesync/.rulesync/skills/mols-agent-asset/SKILL.md), [서비스 기능 조사](chatbot-runtime-landscape.md), [harness fidelity 조사](research-harness-fidelity.md), [공식 Agent Skills spec](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx), [Copilot instructions 공식 문서](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions), [Anthropic harness 구성 가이드](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more). `verified`는 문서·제품 설명의 확인이지 실제 모델 성능 증거가 아니다.

## Loop 1 — 구조·비용 중심의 문제 재정의

**Research:** 기존 연구는 F0–F3(first-hop → discovery → canonical body → application) 충실도에 집중한다. 그것만으로도 잘못 설계된 복잡한 router·중복 context·잘못된 capability selection을 '성공'으로 볼 위험이 있다.

**Plan:** `N0 Native-only / N1 Pointer / N2 Selection bridge / N3 필요한 기능 대체`를 후보 **집합**으로 정의하고, 필수 계약을 만족하는 가장 작은 유효 구성을 선택한다. 복잡성은 필요할 때만 추가하고 N3를 N2 뒤의 필수 단계로 만들지 않는다.

**Review / 반례:**
- native Skill 지원이 충분한 제품은 신규 router 생성 없이 **no-op이 정답**이다.
- File read connector만 가능한 환경도 로그인된 Browser가 있다는 이유로 권한을 확장하지 않는다.
- 복잡한 저장소에서 router가 필요할 수 있으나 모든 저장소에 route JSONL을 강제하면 오히려 비용이 증가한다.
- 최적성은 '모든 서비스 지원'이나 '모든 파일 로드'가 아니라 상황별 비교로 판정해야 한다.

**결과:** topology와 도구 선택, hard constraints와 soft cost를 [harness-architecture-options.md](harness-architecture-options.md)로 분리. 기존 계획의 `목표` 및 `완료` 기준 확장.

## Loop 2 — Skill 책임·activation·기존 하네스 충돌 검토

**Research:** 현 `mols-chatbot-bootstrap`은 저빈도 provision/repair용으로 설계됐다. 범용 하네스 설계로 scope를 너무 넓히면 일반 architecture, `mols-agent-asset`, `github-context`, `mols-loops`와 충돌한다.

**대안:**

| 후보 | 기대 이점 | 우려 | Disposition |
| --- | --- | --- | --- |
| 기존 Skill에 구축/복구 목적의 **설계 비교**를 소폭 포함 | 같은 사용자 의도의 하나의 경량 end-to-end capability | 핵심 본문이 길어질 수 있음 | **우선 시도** |
| 독립 `mols-chatbot-harness-design` 추가 | 독립 activation/ownership이 입증되면 명료 | 유사한 과정 두 벌, 설치·컨텍스트 비용 | **보류, 사례 기반 판정** |
| 기존 Skill 전체 rename/대규모 scope 확장 | 새 목표를 전면 드러낼 수 있음 | 기존 호출자와 compatibility 회귀 | **현재 확정하지 않음** |

**Review / 반례:**
- 대상 runtime의 실제 권한·사용 가능한 API가 아니라 공급자의 판매 페이지 기능표를 기준으로 설계하면 허위 완료가 된다.
- 필수 안전/authority 규칙을 optional Skill에 숨기면 activation이 누락될 때 보호가 사라진다.
- 스킬을 매 일반 작업마다 호출하도록 설계하면 저빈도 bootstrap의 경계가 무너진다.

**결과:** 구현 전에 **intended bootstrap/repair**, **new harness design**, **near-miss 일반 agent asset 구성/CI/자동화**의 trigger를 검토한다. Skill 분리 여부는 결과에 따라 재결정한다. 설계 후보는 target-independent policy를 소유하지 않는다.

## Loop 3 — 사용성·검증·과설계 관점에서 역검토

**Research:** 공식 Agent Skills는 metadata → Skill body → 조건부 resource 로딩을 분리한다. 런타임별 path instruction/agent instruction 지원과 우선순위도 다르다. 실제 도구와 연결 계정이 같은 이름의 제품 내에서도 변경될 수 있다.

**Plan:** 작업 관련 capability만 확인하고, 현재 하네스 재사용 → 최소 변경 → 세 수준의 검증(`configured`/`reachable`/`observed applied`)으로 진행. 품질·비용은 hard-constraint 준수 후에 비교한다.

**Review / failure probes:**

| 검증할 위험 | 계획에서의 대응 |
| --- | --- |
| 정확하지만 과도하게 복잡한 경로 | 같은 결과를 얻는 N0/N1 후보와 비교 |
| 컨텍스트 절약을 위해 필수 instruction을 생략 | hard constraint로 분리, 비용 절약을 핑계로 생략 금지 |
| 능력 없는 runtime에 Python/CLI/network 있다고 추론 | 실제 session tool과 sandbox 제한 확인 |
| 코드·구성 변경을 아직 실행하지 않았는데 성공 보고 | structural claim과 runtime behavior 분리 |
| 엉뚱한 계정/명의로 connector write | 지정된 계정·권한·승인 검증, 불확실하면 write 중지 |
| 소수 사례의 우연한 모델 출력으로 범용 성능 주장 | 대표 case + 제품/모드별 증거 범위 한정, 측정 없는 '최적' 주장 금지 |
| PR의 목표가 문서 준비에서 구현으로 몰래 바뀜 | 현재 PR은 조사/계획에만 집중, Skill diff는 별도 요청/후속 단계 |

**결과:** [harness-evaluation-strategy.md](harness-evaluation-strategy.md)의 평가 프로필·지표와 [plan.md](plan.md)의 D0–D5 인계에 반영.

## 최종 반영 결정

**채택:** 환경별 최소 유효 topology 비교, 현재 활성 도구/권한만 확인, canonical body와 행동의 실제 검증, context/tool/maintenance 비용 비교, no-op 결과, 정확한 handoff.

**제외:** 전수 자산 로딩, 필수 범용 router/adapter, 서비스별 Skill fork, 상시 agent manager, 무조건 CI/eval runner 설치, 이름만의 자동 최적화 점수, 계정 자동 변경.

**조건부:** 초기 Skill의 변경 범위·메타데이터/rename·별도 설계 Skill 분리, runtime별 behavioral eval의 확대. 추가 구현 이전에 필요한 증거부터 확보한다.

## Review Gate / Handoff

| Gate | 현 상태 |
| --- | --- |
| 동일 목적의 기존 Skill과 source owner 확인 | **정적 검토 완료** |
| 설정 후보와 사용자 가치·운영 비용 비교 기준 | **계획 완료** |
| 반례/비용/권한/범용성 위험 처리 | **계획 완료** |
| 실제 `SKILL.md`의 새로운 activation·절차 구현 | **미착수** |
| 여러 런타임의 실측 비교와 end-to-end 평가 | **미검증** |

**다음 실행자:** [plan.md](plan.md)를 진입점으로 삼아 D0–D2에서 최소 Skill 변경을 설계한다. 기존 원본의 모든 책임을 다시 구현하지 않으며, 테스트나 평가가 불가능한 조건은 `not verified`로 남긴다. 사용자 요청의 명시적 범위 밖 외부 계정·권한·서비스 변경은 수행하지 않는다.
