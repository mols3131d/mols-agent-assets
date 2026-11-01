# Research — Chatbot Harness Fidelity and Capability Adaptation

> 상태: 정적 소스·공식 제품 문서 기반 조사(2026-11-02). 대상 챗봇을 실제 실행한 평가 결과가 아니다.

## 연구 질문과 결론

**RQ1.** 왜 진입점을 읽는 것만으로 하네스 준수를 보장하지 못하는가?  
**RQ2.** 챗봇마다 다른 tool/connector/runtime에서 어떤 적응이 필요한가?  
**RQ3.** 전체 자산 선로딩 없이 실제 Skill·Rule 적용을 확인하려면 무엇을 평가해야 하는가?

**결론:** `mols-chatbot-bootstrap`은 이미 네이티브 우선, no-op, 단계적 탐색, 대상별 관행 존중, 저빈도 provisioning을 규정한다. 새 범용 프레임워크보다 **현재 런타임의 사용 가능한 기능·권한 확인 → 필요한 first-hop 복구 → 작업 관련 canonical 자산 본문 로딩 경로 확인 → 미관찰 시 미검증 보고**의 누락된 판단 경계를 좁혀 보강하는 편이 타당하다.

## 소스 근거: 기존에 있는 것과 빈틈

| 검토 대상 | 정적으로 확인한 계약 | 추가로 확인해야 할 공백 |
| --- | --- | --- |
| [Skill](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md) `Lifecycle` | 일회성·저빈도 provision/repair, 이후 독립적인 대상 하네스 | 개선 후 일반 작업마다 Skill 재호출을 요구하지 않아야 함 |
| 같은 Skill `Contract` | native 우선, 기존 구조 존중, `AGENTS.md`·Skill·Rule별 누락만 복구, 권한 밖 runtime-side surface는 handoff | 사용 가능한 connector/코드 실행/파일 read가 서로 다른 제약을 가질 때 **현재 작업에 의미 있는 기능만** 확인한다는 기준이 명료하지 않음 |
| 같은 Skill `Workflow` | 엔트리포인트·라우트 최소 복구, 생성·CI 선택적 사용 | 링크가 읽힌 뒤 **선택한 자산의 canonical body까지 이어지는 실제 소비 경로** 확인 단계를 더 직접적으로 표현할 여지 |
| 같은 Skill `Validation` | entrypoint/actionable route·의미적 선택·권한 경계 검증, first-hop 미관찰은 미완료 | route reachability를 runtime asset-loading/application success로 과장하지 않도록 증거 수준을 분리할 필요 |
| [fallback routes](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/references/routes.md) | 별도 route가 필요한 대상에서만 사용, `_meta.instructions`로 선택한 source 로드, 모든 body 미로딩 | 이미 필요한 행동을 표현함. 기본 수정 대상 아님 |
| [github-context](../../src/rulesync/.rulesync/skills/github-context/SKILL.md) | 대상 경로의 적용 지침·자산만 load, 같은 ref의 이미 로드한 자산 재사용, material scope 변화 시 갱신 | 이 동작을 bootstrap에 중복 소유시키지 말 것 |
| [기존 작업 조사](chatbot-runtime-landscape.md) | 주요 7개 서비스의 Chat/Agent/Desktop/API 및 connector/sandbox 차이를 조건부로 분류 | 제품의 소개 기능과 현재 세션에서 실제 제공·승인된 tool을 구분해야 함 |

**관찰 수준:** 위 항목은 파일 내용과 공식 문서에서 `verified`된 계약과 제품 설명이다. “대상 챗봇이 Skill 본문을 종종 생략한다”는 문제 가설은 사용자 경험 기반의 설계 입력이지, 해당 모델·제품에 대한 반복 실행으로 `verified`된 성능 측정은 아니다.

## 외부 규격·공식 서비스 근거

1. [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx): `name`/`description`를 통한 후보 발견 → 선택된 `SKILL.md` 전문 로딩 → 작업에 따라 `references`/`scripts` 선택 로딩이 핵심. 모든 자산 body를 기본 컨텍스트에 넣으라는 의미가 아니다.
2. [MCP Tools 사양](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/server/tools.mdx): 도구의 노출 여부를 목록/스키마로 발견하고 실제 호출은 별개다. 등록된 도구가 있다는 사실을 실효 권한·성공으로 해석하지 않는다. MCP가 없는 runtime에 `tools/list` 구현을 강요하지 않는다.
3. [ChatGPT connected apps](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt), [account connection](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt): 앱 사용 가능성과 외부 action은 plan/workspace/role/연결 계정·승인에 종속되며 연결 사실이 새 권한을 자동 부여하지 않는다.
4. [ChatGPT data analysis](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt): Python/Jupyter가 있어도 그 sandbox에서 외부 web/API 요청을 직접 할 수 없다. 검색 tool·connector·Python을 동일한 실행 surface로 취급하지 않는다.
5. [Claude 파일 생성·실행 환경](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude), [remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp): 코드 sandbox egress, 원격 connector, Desktop 로컬 MCP가 다른 권한·네트워크 경계를 가진다.
6. 서비스별 추가 사례·출처는 [runtime landscape](chatbot-runtime-landscape.md)에 있다. 이 조사 문서의 상세 요금제·기능은 빠르게 변하므로 portable Skill의 고정 사양으로 가져오지 않는다.

## Capability 판단의 최소 단위

'ChatGPT/Claude/Gemini' 같은 제품 이름이 아니라 **현재 활성 작업 surface**의 필요한 능력만 판단한다.

| 필요한 질문 | 가능한 증거 | 금지할 추론 |
| --- | --- | --- |
| 저장소 source를 읽을 수 있는가? | 현재 노출된 read connector/파일·브라우저 + 정확한 ref 파일 열람 | GitHub 연결됨 = 모든 ref·파일 최신 읽기 가능 |
| 실행 가능한 코드 환경인가? | 실행 도구와 sandbox 결과 | 코드를 작성할 수 있음 = shell 실행 가능 |
| 외부 네트워크가 가능한가? | 별도 network capability·허용 domain 확인 | web search 가능 = Python HTTP 허용 |
| 파일을 지속적으로 쓸 수 있는가? | 도구 제공 write surface·권한·저장 위치 | 임시 파일 다운로드 = repo 변경 |
| 외부 account action이 허용되는가? | 현재 계정 연결·권한·사용자 승인 | plugin 설치 = 모든 external mutation 승인 |
| runtime의 첫 진입점이 실제 주입되는가? | 지원되는 instruction surface 확인 또는 직접 관찰 | 저장소에 `CHATBOT.md` 존재 = 서비스가 자동 읽음 |

**비용 절감:** 하네스 task와 무관한 기능은 확인하지 않는다. 이미 관찰한 현재 session의 capability를 활용하고 작업 목표·필수 권한·런타임이 달라질 때 관련 부분만 재확인한다.

## Failure taxonomy와 분리 기준

1. **F0 / First-hop:** 실행 runtime이 repository entrypoint를 읽지 못함 → runtime-side 지정 또는 좁은 handoff. 권한이 없다면 미완료.
2. **F1 / Discovery:** entrypoint는 읽었으나 현재 작업·경로에 필요한 route/instruction 후보를 찾지 못함 → 실제 target routing 계약을 따라 복구.
3. **F2 / Canonical loading:** route 메타데이터만 읽었고 선택한 Skill/Rule 본문을 읽지 못함 → 선택한 source의 full body를 소비하도록 대상 하네스에 연결; 불필요한 asset은 건드리지 않음.
4. **F3 / Application:** 본문 열람은 관찰됐으나 행동 미준수 → runtime/model/자산 행동 평가로 분류. bootstrap 만의 문제라고 단정하지 않음.
5. **F4 / Capability/authority:** 필수 tool·파일·연결·권한 없음 → 승인된 native 대안의 기능적 동등성을 따져 제한적 복구 또는 handoff. 무단 권한·계정 전환 금지.
6. **F5 / Evidence gap:** 실제 실행을 관찰하지 못함 → 구조적 reachability와 runtime compatibility의 판정을 분리.

**중요:** F2와 F3를 하나의 오류로 취급하면 라우터 변경으로 모델의 실행 불이행까지 해결했다고 잘못 보고할 수 있다.

## 대안 비교

| 접근 | 기대 효과 | 위험·비용 | 판단 |
| --- | --- | --- | --- |
| A. 모든 지침·Skill·reference를 미리 읽음 | 선택 누락을 일부 줄일 수도 있음 | 컨텍스트 낭비, 충돌·희석, stale 지침, 장황한 loading | **배제** |
| B. 제품별 feature matrix·adapter를 `SKILL.md`에 상주시킴 | 서비스별 사례를 즉시 참고 | 빠른 노후화, 불필요한 제품·버전·권한 가정 | **배제** |
| C. 기존 Skill에 capability-aware 결정과 F0–F3 완료 수준을 최소 문장으로 반영 | 기존 경로 재사용, portable delta, 저렴한 유지보수 | 실제 eval 없이 효과 확정 불가 | **권장** |
| D. 별도 상주 오케스트레이터/라우터·검증 CI 신규 구축 | 일부 상황에서 자동화 | 이 Skill의 lifecycle·owner 침범, 설치·관리 비용 | **배제** |
| E. runtime별 소수 관찰 사례로 Routing+Behavior Eval | 실패 단계와 회귀를 분리 가능 | 대상 실행 환경·로그 접근 필요 | **조건부 후속** |

## Research → Plan 루프에서 새로 확인할 판단

- **H1:** source route를 열게 하는 문구는 이미 fallback reference에 있다. 따라서 보강은 router schema가 아니라 bootstrap Workflow/Validation의 **소비 경로 검증 요구**부터 검토한다.
- **H2:** 임의의 모델 행동을 '보장'할 수 없다. `provisioned`, `reachable`, `observed applied` 등 주장의 증거 수준을 분리하고, 실험하지 않은 항목은 `Not Verified`로 남긴다.
- **H3:** Capability discovery는 전수 목록 체크가 아니라 **해당 first-hop/원본 로딩을 성립시키는 능력만** 확인하는 방식이어야 한다.
- **H4:** Chatbot에 없는 tool을 임의로 구현·설치해 해결하지 않는다. 기존 connector/native 기능 또는 안전한 제한적 실행/정확한 handoff를 선택한다.
- **H5:** PR #266의 portable maintainer 문서와 PR #267의 runtime execution fidelity는 별도 ownership이며 상대 PR의 merge를 전제하지 않는다.

## 미확인 사항 및 증거 한계

- 해당 runtime이 실제로 선택한 `SKILL.md`를 읽지 않은 사례의 trace/재현 조건: **미확인**.
- ChatGPT 외 6개 서비스의 특정 계정에 설치·노출된 도구 또는 동일 fixture에서의 행동: **미실행**.
- Tool availability만으로 user approval/write permission이 성립하는지: **성립하지 않음**.
- 부속 generator 파싱 이슈는 직접적인 harness execution fidelity의 blocker가 아니므로 이번 범위에서 분리.

이 조사 결과의 구현·검증 순서와 acceptance는 [plan.md](plan.md)를 정본 working plan으로 사용한다.

## 설계 범위로의 연결

이 조사는 entrypoint/route/body/application의 **실행 충실도** 및 런타임 권한 경계를 연구한 부분 결과다. 더 넓은 목표인 '**현재 대상 환경에서 가장 단순하고 효율적인 유효한 챗봇 하네스 구축**'을 달성하려면, 이것에 더해 [harness architecture options](harness-architecture-options.md)의 no-op/브리지 대안 비교와 [evaluation strategy](harness-evaluation-strategy.md)의 context·tool·maintenance 비용·사용성 평가를 적용한다. 실행 충실도만으로 최적성을 증명하지 않으며, 초기 작은 계약 개선안은 변경 범위 검토의 출발점이다.
