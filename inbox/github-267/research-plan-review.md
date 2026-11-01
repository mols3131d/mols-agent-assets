# Research–Plan Loop Review — Chatbot Harness Fidelity

> 작업 범위: 조사와 개선 계획까지만. 리뷰는 단일 챗봇의 순차 관점 검토이며 독립 agent 평가나 실제 runtime eval이 아니다.

## 목표와 종료 조건

`mols-chatbot-bootstrap`의 **최소 변경 범위와 검증 방법**을 정하되, 대상의 네이티브 하네스·권한 경계를 유지하고 전체 자산 선로딩·상시 오케스트레이터·범용 라우팅 구조의 신설을 피한다.

종료 조건: (a) 기존 계약 대비 필요한 delta 식별, (b) capability/authority의 구분, (c) runtime test가 없을 때 주장 수준 결정, (d) 작업자에게 전달할 단계별 수정·평가 계획이 준비됨.

## Loop 1 — 기존 계약과 누락된 행동 대조

**Research:** [기존 Skill](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md), [fallback routes](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/references/routes.md), [github-context](../../src/rulesync/.rulesync/skills/github-context/SKILL.md), [기존 발견사항](findings.md), [서비스 조사](chatbot-runtime-landscape.md)를 대조했다.

**Plan 후보:** `SKILL.md`의 Contract/Workflow/Validation에 "현재 도구 기준 판단", "metadata 선택 ≠ canonical body 로딩", "runtime 관찰과 구조적 검증 구분"을 추가하고, 대표적인 positive/negative/failure case를 사용한다.

**Review:**
- **유효:** route가 파일을 가리킨다는 사실과 모델이 실제로 자산을 소비했다는 사실을 분리할 필요가 있다.
- **과한 부분:** 일반 작업마다 모든 tool inventory를 재열거하거나 필수 runtime eval을 gate로 만들면 저빈도 bootstrap의 목적과 충돌한다.
- **이미 해결됨:** fallback route는 선택한 source를 읽도록 안내하고 `github-context`는 범위 변경·reference 재사용을 이미 소유한다.
- **전환:** 별도 runtime orchestration 절차를 만들지 않고 **결함이 확인된 경계만** bootstrap 완료·판정 기준에 반영.

## Loop 2 — 반례·비효율·권한 관점에서 계획 재검토

**Research:** [Agent Skills 공식 스펙](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx)의 progressive disclosure, [ChatGPT 앱 권한](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt), [ChatGPT 분석 Python](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt), [Claude 원격 MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp), [MCP tools](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/server/tools.mdx)를 교차 확인했다.

| 반례/위험 | Review 결과 | 계획 보정 |
| --- | --- | --- |
| 대상 런타임이 Skill을 native 자동 로드함 | 수동 파일 fetch 강제는 불필요 | **동등한 source loading evidence**가 있으면 별도 fetch 불필요 |
| 입력이 단순 사실 질문이며 특정 Skill 대상 아님 | 모든 Skill scan은 비효율 | 작업과 관련된 후보 metadata만 확인; 선택 없으면 종료 |
| GitHub connector가 read만 가능 | tool 존재만으로 write가 가능하지 않음 | 계정/명의·권한·승인 별도 확인, write 작업은 하네스 외 권한 정책 적용 |
| Python 실행은 가능하지만 HTTP는 차단 | Python으로 repo를 당연히 fetch한다고 가정 불가 | 앱/브라우저 read를 우선, 격리 runtime은 수행 가능한 작업만 대체 |
| 선택한 Skill body를 읽었지만 작업에 적용하지 않음 | bootstrap 결함 단정 불가 | F3 행동 평가로 분리; route 조작으로 '보장' 주장 금지 |
| runtime first-hop을 외부에서 확인할 방법 없음 | 정적 문서만으로 end-to-end 보장 불가 | provisioning evidence와 observational evidence 분리하고 handoff |
| 특정 저장소에 `route/`·`.agents/route/`가 둘 다 존재 | 모든 대상의 동일 구조를 뜻하지 않음 | 로컬 관행을 universal schema로 승격하지 않음 |
| 같은 세션에서 이미 유효한 source를 로드함 | 재-fetch는 latency만 증가 | ref/경로/요청이 실질적으로 바뀔 때만 좁은 재평가 |

**Review 결론:** 위 반례를 견디는 가장 작은 접근은 **단일 Skill의 작은 계약 개선 + 기존 route mechanism 재사용 + runtime 가능 시 작은 behavioral evaluation**이다. 서비스별 adapter·새 독립 Skill·전수 tool 검사·CI 신설의 정당성은 확인되지 않았다.

## Loop 3 — 구현 인계 가능성 검토

**Plan 정교화:**

1. `Contract`: 현재 작업에 필요한 capability에 한해 실제 노출된 도구/권한을 판단한다. 공급자명·API/CLI 명세를 chat runtime의 권한으로 일반화하지 않는다.
2. `Workflow`: 복구 대상의 first-hop을 통해 task-relevant 라우팅 metadata를 읽고 **선택한 canonical body까지 도달하는 사용 가능한 경로**를 점검한다. 단, 이 Skill 자체가 평상시 라우터를 수행하지 않는다.
3. `Validation`: `configured`/`reachable`/`observed`를 구분한다. 관찰 불가능한 end-to-end 사용을 완료로 오인하지 않는다.
4. References: 기존 `routes.md`가 실제로 필요한 연결을 표현할 수 없다면 그 때만 수정; `tuning.md`, generator, CI는 별도 근거 없이는 그대로 둔다.
5. Behavior eval: 소수의 경우에 필요한 asset 선택·본문 로딩·적용과 불필요한 선로딩을 관찰. 툴 call의 특정 순서를 무조건 정답으로 고정하지 않는다.

**Review:**
- **Coverage:** discovery, loading, application, inaccessible-source, authority, efficiency를 다룬다.
- **Minimality:** 유지보수 규칙과 runtime 행동을 중복 복제하지 않으며 대상을 `mols-chatbot-bootstrap`으로 한정한다.
- **Evidence:** 이 단계에서 검증 가능한 것은 파일의 계약·계획 정합성이고 실제 모델의 준수율은 미검증이다.
- **Result:** 계획 단계의 요구사항을 충족. `plan.md`를 최종 작업 계획으로 갱신하고 구현 단계로 인계한다.

## 확인된 결정

- **P1:** 런타임 제약을 고려한 실제 first-hop 및 canonical asset loading reachability를 구분해 확인.
- **P1:** native-first와 최소·지연 로딩을 유지; 대상별 적용 규칙·route ownership은 대상 하네스에 맡김.
- **P2:** 실제 적용 성공을 주장할 때만 runtime 행동 근거 요구; 미실행은 `Not Verified`.
- **기각:** 전수 스킬 preload, 매 tool call 재라우팅, 범용 서비스 adapter, 새 상주 Skill, 독립 runner/CI 강제.
- **범위 밖:** baseline generator의 silent-skip, PR #266의 독립 maintainer 문서, 기존 project bootstrap 자체의 전면 재작성.

## 남는 불확실성과 다음 단계

- **미검증:** 모델·서비스별 실제 tool inventory, 선택 이후 body loading, behavior parity, 경로 전환 발생률.
- **다음 작업자:** [plan.md](plan.md)의 순서로 좁은 Skill delta → static review → 가능한 런타임의 3~5개 사례에서 관찰·평가 → 필요할 때만 후속 reference 정비.
- **중단 기준:** 구현이 새로운 라우팅 규칙의 소유권이나 상시 agent manager 역할을 만들기 시작하면 범위에서 제외하고 재검토.

## 후속 검토에 따른 목표 확장

앞 단계의 결론인 **작은 계약 개선 + 기존 route 재사용**은 `harness execution fidelity` 문제에 대한 판단이다. 이것만으로 **대상 런타임에 최적인 하네스 설계**가 완성됐다고 주장할 수는 없다. 이후 [architecture–plan review](architecture-plan-review.md)에서 현재 네이티브 기능만 쓰는 `no-op`, runtime pointer, 경량 selection bridge 및 실제 권한 기반 capability adaptation의 **대안 선택**, 컨텍스트/호출/설정·유지보수 비용, Skill activation/분리 경계를 추가 검토했다.

계속 유효한 계약: native-first, 필요한 본문만 지연 로딩, 불확실한 권한·실행 결과를 완료로 가장하지 않음. 새 작업의 범위·최종 인계는 [plan.md](plan.md)가 소유하며 이 문서의 초기 초안 결론을 구현 상한으로 해석하지 않는다.
