# Chatbot Harness Design — Implementation Preparation Plan

> PR #267 작업용 정본 계획 · 2026-11-02. **계획/조사 상태**, Skill 소스 변경 및 실제 런타임 평가 미수행.

## Target Outcome

현재 `mols-chatbot-bootstrap`을 단순한 `CHATBOT.md` 연결 복구보다 발전시켜, **다양한 챗봇 런타임에서 원본 저장소의 하네스를 충실하고 효율적으로 활용하도록 필요한 최소 하네스 구성을 진단·설계·구축·복구하는 Skill**로 개선할 준비를 한다.

'최적'은 모든 서비스에 동일한 구조를 설치한다는 뜻이 아니다. 하네스 준수, 대상 authority와 실제 권한, 첫 진입점·canonical source 접근을 **필수 조건**으로 지키고, 그 범위 안에서 context/token, 호출/latency, 구성·유지보수·사용자 설정 비용을 줄이는 **환경별 최소 유효 설계**를 뜻한다. 이것은 실측하기 전까지 개선 가설이지 보장된 모델 성능이 아니다.

## Existing Evidence → Decisions

| 근거 | 판단 | 관련 자료 |
| --- | --- | --- |
| 기존 Skill의 native-first, no-op, 일회성 provisioning | **보존**. 일반 작업의 상주 orchestrator로 확대하지 않음 | [현재 Skill](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md) |
| `CHATBOT.md` 읽기와 실제 Skill body 로딩의 단절 가능성 | **보강**. first-hop/route/본문/적용의 완료 수준 구분 | [fidelity 조사](research-harness-fidelity.md), [findings](findings.md) |
| 서비스·모드마다 connector, Python, browser, computer, 저장소 접근 차이 | **조건부 적응**. 플랫폼 이름 대신 현재 exposed tool/권한 | [서비스 조사](chatbot-runtime-landscape.md) |
| N0 native-only vs N1 pointer vs N2 bridge vs N3 제한적 capability 대체 | **비교 선택**. 더 큰 토폴로지는 확인된 공백을 해결할 때만 | [설계 대안](harness-architecture-options.md) |
| 품질과 비용을 동시에 평가해야 '최적'을 주장할 수 있음 | **설계 평가 추가**. 실행 관찰 없이 성능 통과 주장 금지 | [평가 전략](harness-evaluation-strategy.md) |
| 기존 스킬과 별도 architect Skill의 activation 차이 | **결정 게이트**. 이름/책임 확대를 가정하지 않고 케이스 기반 판단 | [설계 대안](harness-architecture-options.md) |

## Scope and Ownership

**기본 변경 대상:** `src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md`의 목적·activation metadata, Contract, Workflow, Validation, Boundary. **모든 부분을 반드시 수정하라는 뜻은 아니다**. 현재 계약으로 해결된 사항은 수정하지 않는다.

**조건부 변경 대상:** `references/routes.md`는 현재 selector/source 소비로 표현할 수 없는 구체적 결함이 확인되면, `references/tuning.md`는 실제 자동화 필요 시에만. Maintainer document는 지속적으로 가치 있는 결정만 반영한다.

**명시적 비범위:** 이 PR에서 대상 저장소의 `CHATBOT.md`/router, branch·정본, 범용 generator/CI, 외부 tool/plugin 설치, 상시 scheduled agent, runtime-side project instruction, account connection을 임의로 변경하지 않는다. PR #266은 독립 maintainer 문서 작업이다.

**Skill 소유권 판정:** 현 스킬의 단일한 구축·복구 목적에 부합하는 경량 design comparison은 **우선 현 Skill에 포함**한다. 다음 경우에만 별도 design Skill 또는 rename을 재논의한다: 독립된 사용 의도가 반복 확인되고, 실제 activation 충돌·과도한 상시 context 또는 유지보수 이점이 입증됨. 분리/rename은 이번 단계에서 확정하지 않는다.

## Proposed Skill Behavior

1. **Input / scope:** user goal, target repository/path/ref, 현재 챗봇 mode, 승인·변경 가능 범위를 확인한다. 사용자가 이미 제공한 정보를 중복 질문하지 않는다.
2. **Discover relevant capability:** 실제 노출된 도구·연결·파일/코드·네트워크·브라우저·권한 중 **구축 결정에 영향을 주는 것만** 확인한다. 제품 소개 기능을 권한으로 가정하지 않는다.
3. **Inspect existing authority:** native discovery와 대상의 실재하는 instruction, routing, Skill/Rule/agent 소유권, scope 적용 여부를 확인한다.
4. **Compare smallest valid options:** N0/no-op → 기존 native + 최소 pointer → 필요 시 작은 selection bridge → 별도 필요한 capability 대체. 기존 구조가 충분하면 중단.
5. **Build/repair within authority:** 가장 작은 변경으로 필요한 first-hop 및 task-relevant canonical source의 로딩 경로를 구성한다. 실효 권한 없으면 정확한 사용자 handoff를 남긴다. router가 source body/policy를 복제하지 않는다.
6. **Verify in tiers:** `configured`(구성), `reachable`(접근), `observed applied`(실행 관찰)을 구분한다. 선택한 본문을 native 경로로 이미 로드한다면 별도 fetch를 강제하지 않는다.
7. **Outcome / handoff:** 채택한 구성과 이유, 실제 변경·필요한 사용자 설정, 검증된 범위·미검증·남은 위험을 간결히 제시한다. 일반 작업은 구축 Skill의 지속 로딩 없이 진행되도록 한다.

**Key guardrail:** 도구가 더 많다는 이유로 더 큰 하네스 구성을 채택하지 않는다. 도구·연결의 사용 가능성과 side effect를 남길 권한은 별개이며, 사용자 승인 없는 계정·명의 전환은 금지한다.

## Implementation Stages

| 단계 | 의도한 작업 | 완료 근거 |
| --- | --- | --- |
| D0 — Baseline | 현 Skill, 기존 reference, 대상별 authority 및 activation 근거 재확인 | 중복·기존 계약 보존 목록 |
| D1 — Scope | 구축/복구와 일반 agent-asset authoring/CI/장기 연속성의 Skill trigger 충돌 점검 | positive/negative/near-miss 분류 및 유지·rename·분리 판단 |
| D2 — Minimal revision | 핵심 목표·옵션 비교·capability relevance·lazy load·완료 수준을 작은 delta로 반영 | 변경된 Skill의 실제 문장과 반례 검토 |
| D3 — Review | task owner 및 efficiency 관점의 source review; 권한/의도치 않은 activation/중복 제거 | 정적 계약·링크·regression 결과 |
| D4 — Runtime evidence | 가능한 실제 chatbot runtime에서 소수의 유효·비유효·제약 사례 수행 | [평가 전략](harness-evaluation-strategy.md)의 observed evidence 또는 `not verified` |
| D5 — Close | 더 큰 장치가 필요한지 판단, 유지할 정본만 반영, 실제 변경 diff와 PR 인계 | 검증 범위·미해결 상태·최소성 설명 |

D0–D5는 작업 의존성이지 독립 PR·Skill·runner 또는 모든 환경에서 고정 실행해야 할 단계 수가 아니다.

## Acceptance Criteria

- 진입점 읽기 또는 route metadata 발견만으로 하네스 구축 성공을 주장하지 않는다.
- 네이티브만으로 충분한 대상에서 **no-op을 올바른 최적 결과**로 선택한다.
- 부분 native 지원 시 **누락된 책임만** 복구한다. 실제 task-relevant canonical Skill/Rule/conditional reference 접근을 확보한다.
- 모든 Skill·Rule·reference 선로딩, 반복적 전수 검사·fetch, 복제한 policy·새 router/CI 강제를 피한다.
- 하네스 정확성·권한 경계는 최우선, 컨텍스트/도구/설정·유지보수 비용은 그 제약 안에서 비교한다.
- 로컬과 다른 챗봇 환경에서 툴/connector/Python/shell/브라우저 기능을 추측하지 않는다.
- 증거가 없는 권한·실행 성공·model parity를 선언하지 않는다.
- 새로운 Skill 분리나 rename은 독립 trigger/ownership 근거가 있을 때만 채택한다.
- 최소 변경의 결과물을 사람이 사용할 수 있는 수준으로 설명하고 권한 밖 변경은 명확한 handoff를 제공한다.

## Working Artifacts / Handoff

- [findings.md](findings.md) — 핵심 문제·보존 제약
- [chatbot-runtime-landscape.md](chatbot-runtime-landscape.md) — 7개 서비스의 모드/도구 조사 (환경별 보장 아님)
- [research-harness-fidelity.md](research-harness-fidelity.md) — 로딩 경로·실패 단계 조사
- [research-plan-review.md](research-plan-review.md) — 초기 조사→계획→리뷰 기록
- [harness-architecture-options.md](harness-architecture-options.md) — 이번 작업에서 추가한 설계 대안·트레이드오프·책임
- [harness-evaluation-strategy.md](harness-evaluation-strategy.md) — 품질/비용 기준과 런타임 평가 계획
- [architecture-plan-review.md](architecture-plan-review.md) — 추가 설계·반례·최종 인계 리뷰

**현재 완료:** 전초 조사, 설계 후보, 구현·평가·비용 측정 계획, 문서 간 정합성 검토. **미완료:** `SKILL.md` 구현, 실제 서비스별 capability·behavior eval, 정본 승격, 병합. 다음 작업은 D0–D2에서 **현 스킬의 activation과 설계 범위**를 먼저 점검한 후 작은 Skill diff를 만드는 것이다.
