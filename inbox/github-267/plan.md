# Mols Chatbot Bootstrap — Improvement Plan

## Goal

챗봇의 저장소 하네스 호환성을 **진입점 접근 가능성**에 머무르지 않고, 해당 작업에 필요한 지침·Skill·Rule의 **선택적 발견 → canonical source 로딩 → 행동 적용**까지 지원하도록 `mols-chatbot-bootstrap`을 최소 보강한다.

이 PR의 초기 상태는 **계획·인계 단계**다. Skill 구현이나 런타임 통과를 완료했다고 주장하지 않는다. 판단 근거와 유지해야 할 경계는 [findings.md](findings.md)를 따른다.

## 변경 범위와 책임

| Surface | 의도 |
| --- | --- |
| `src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md` | 기존 lifecycle을 유지하면서 end-to-end harness fidelity와 lazy loading의 완료·검증 기준을 필요한 만큼만 명확히 한다 |
| 기존 `references/routes.md` | 기존 fallback route의 소비 절차가 이 요구를 충족하지 못하는 경우에만 최소 수정한다 |
| `docs/skills/mols-chatbot-bootstrap/` | 설계 이유·이식성 등 유지보수 판단이 정본으로 확정되면 반영한다. PR #266의 변경을 병합된 것으로 가정하지 않는다 |
| 대상 저장소의 `CHATBOT.md`, route, runtime-side instruction | 변경이 필요한 대상에 적용할 때 그 저장소의 권한과 기존 하네스를 확인한 뒤 별도 결정한다. 이 PR에서 일괄 변경하지 않는다 |

새 라우팅 구조, 에이전트 상주 오케스트레이터, 범용 생성기, 상시 검사 CI를 요구하지 않는다.

## 진행 계획

1. **Baseline 확인:** Skill이 이미 보장하는 native-first, no-op, target convention, optional references, runtime first-hop, validation 계약을 확인하고 중복 추가할 내용은 제외한다.
2. **실패 경계 명확화:** entrypoint를 읽어도 routing metadata나 선택한 canonical source를 읽지 않은 경우, 선택한 자산을 읽고 적용한 경우를 구분한다. 보강 문장은 필요 최소량으로 제한한다.
3. **소유권을 지킨 구현:** 부트스트랩 Skill은 호환 경로를 provision/review하고, 평상시 선택·로드·행동은 생성 또는 복구된 대상 하네스와 실제 canonical 자산이 담당하게 한다.
4. **검증:** 정적 문서 검토로 완료 조건과 기존 기능 보존을 확인하고, 실제 챗봇 런타임이 사용 가능할 때만 작은 대표 시나리오로 routing·loading·application을 관찰한다. 런타임 미확보 시 결과는 `Not Verified`로 둔다.
5. **마무리:** 중복·과설계가 생겼는지 review 후 필요한 문서만 정본화한다. 실제 소스 변경과 검증 근거가 준비되면 Draft PR을 리뷰 가능한 상태로 전환하도록 제안한다.

## 대표 평가 시나리오

| Case | 기대 행동 | 실패 신호 |
| --- | --- | --- |
| 관련 자산 없는 단순 작업 | 필요한 기본 지침만 고려하고 불필요한 Skill 본문은 로드하지 않음 | 전체 카탈로그/본문 선로드 |
| 특정 Skill이 필요한 작업 | route metadata로 선택한 뒤 canonical `SKILL.md` 본문과 필요한 reference만 읽고 적용 | metadata만 보고 본문 미로딩; 본문은 읽었으나 계약 무시 |
| 두 책임이 결합된 작업 | 독립적으로 필요한 자산만 선택·적용 | 한 자산만 적용하거나 전체 자산 로딩 |
| 작업 경로·ref·의도 변경 | 바뀐 범위의 적용 지침·자산을 재평가하고 유효한 로딩 결과 재사용 | 오래된 지침 계속 사용; 매 단계마다 전체 재로딩 |
| runtime first-hop 또는 필수 source 접근 불가 | 확인 가능한 범위를 설명하고 필요한 handoff 제공; 미검증을 성공으로 선언하지 않음 | 링크만 존재하는데 호환성 완료 주장 |

평가에서 특정 파일 fetch 순서를 하나로 고정하지 않는다. 기존 native discovery가 동등한 결과를 제공하면 추가 수동 fetch가 필요하지 않을 수 있다. **해당 런타임에서 필요한 계약이 실제로 사용됐는지**를 판정한다.

## Acceptance Criteria

- 실제 작업에 필요한 자산을 **선택적으로** 탐색·로드하는 경로가 설명 가능하고 사용 가능한 상태다.
- entrypoint, route metadata, canonical body, conditional references의 역할이 구분되며, 선택된 자산의 본문 로딩이 생략되지 않는다.
- 전체 자산 사전 로딩이나 매 요청·tool 호출마다 무조건 전수 탐색하도록 만들지 않는다.
- 기존 native 기능, target-specific authority, 사용자가 승인한 라우팅과 runtime-side 권한 경계를 보존한다.
- 기본 bootstrap lifecycle은 저빈도 provision/repair이며, 평상시 작업은 bootstrap Skill의 지속 로드에 의존하지 않는다.
- 실제 행동을 실행하지 않았다면 하네스 준수·runtime parity를 검증했다고 주장하지 않는다.

## 챗봇 서비스 런타임 조사

[주요 챗봇 서비스의 도구·플러그인·런타임 조사](chatbot-runtime-landscape.md)에서 ChatGPT, Claude, Gemini, Microsoft Copilot, Perplexity, Grok, Poe의 채팅·에이전트 모드를 구분하고, 연결 앱/MCP, 격리 코드 실행, 로컬·클라우드 컴퓨터, 브라우저 조작, 지속 작업과 계정·권한 제약을 정리했다.

이 조사 결과는 **capability 후보와 확인 질문**이지 모든 대상 런타임이 지원한다는 근거가 아니다. Skill에 서비스별 기능표를 복제하지 말고, 실제 사용 가능 도구와 권한을 작업별로 확인하는 범용 원칙만 필요한 경우 반영한다. 런타임 평가 시에는 특히 **웹 읽기만 가능 / 연결 도구 + 격리 Python / 컴퓨터·브라우저 조작 가능** 시나리오의 차이를 확인한다.

## Handoff / Current State

- **완료:** 대상 Skill 및 현재 하네스의 정적 검토, 핵심 문제와 비목표 범위 정리, 이 PR 준비, 주요 챗봇 서비스 공식 문서 기반 런타임 조사.
- **미착수:** `SKILL.md` 구현 변경, runtime behavioral eval, CI/validator 변경.
- **다음 작업:** 기존 Skill의 Validation과 Workflow에서 필요한 최소 delta를 제안하고, 대표 시나리오를 실제 사용 가능한 챗봇 런타임에서 검증한다.
- **관련 PR:** [#266 — 유지보수 문서의 범용성 기준](https://github.com/mols3131d/mols-agent-assets/pull/266) (별도 작업).
