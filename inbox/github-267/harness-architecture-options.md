# Chatbot Harness Architecture — Design Research and Selection

> 작업용 설계 후보. 2026-11-02. `SKILL.md`의 새 계약을 확정하거나 특정 서비스의 도구를 보장하는 문서가 아니다. 정본 편입 전 실제 대상/런타임 평가가 필요하다.

## 목표 재정의

목표는 **챗봇이 현재 제공된 환경에서 로컬 에이전트 하네스의 적용 가능한 계약을 최대한 충실하게 준수하도록, 필요한 최소 구성으로 하네스를 구축·개선·복구**하는 것이다.

단순한 `CHATBOT.md` 생성이나 route 연결은 가능한 구현 수단이지 성공 조건이 아니다. 반대로 로컬 에이전트와 동일한 shell/파일·서브에이전트 권한을 제공하는 것은 이 Skill의 목적도 권한도 아니다. 제품명과 기능 소개가 아니라 **현재 작업 세션의 실제 capability·authorization·대상 저장소의 원본 하네스**를 사용한다.

**최적의 의미:** 필수 조건(올바른 정본·scope·권한·관찰 가능한 실행 경로)을 만족하는 후보 중, 현재 작업의 성공 가능성과 사용성을 해치지 않으면서 불필요한 구성·도구 호출·컨텍스트·유지보수 비용이 작은 구성을 택한다. 임의의 숫자 가중치를 합산해 단일 최적값이라고 주장하지 않는다.

## Hard constraints / Soft objectives

| 분류 | 판단 기준 | 배제 사례 |
| --- | --- | --- |
| Hard: authority | 저장소·런타임·사용자 승인에 맞는 instructions/Rule/Skill의 정본 소유권 유지 | router가 규칙을 자체 재정의 |
| Hard: executable first-hop | 필요한 경우 런타임이 실제 읽는 surface에서 하네스까지 연결 | 존재하지만 런타임이 읽지 않는 `CHATBOT.md` |
| Hard: selective canonical load | 작업에 필요한 자산 본문과 조건부 reference 접근 가능 | route description만 보고 완료 |
| Hard: account/side effect | 실제 연결·권한·승인과 실행 명의 확인, 범위 밖 변경 금지 | 다른 계정으로 자동 전환 |
| Hard: evidence | 구성 성공·접근 가능·실제 적용을 구분 | 링크 확인을 행동 평가 통과로 표시 |
| Soft: context | 불필요한 사전 로딩과 중복 지침 최소화 | 모든 Skill·Rule 본문 주입 |
| Soft: tool/latency | 반복 fetch·라우터 hop·revalidation 줄이기 | 매 tool call 전체 목록 재스캔 |
| Soft: maintenance | projection/CI/adapter/수동 목록 최소화 | 작은 repo에 신규 generator + 별도 CI |
| Soft: portability/UX | 다른 런타임에서 적은 변경·명확한 handoff | 단일 벤더 디렉터리/특정 UI 강제 |

수치 점수나 token 예산은 **측정 가능한 런타임에서만** 만들고, 모델·계정·환경이 다른 결과를 직접 같은 척도라고 하지 않는다.

## 후보 토폴로지와 선택 사다리

가장 단순한 유효 구성을 우선한다. 다음 단계는 이전 구성이 **구체적 실패를 해결하지 못할 때만** 고려한다.

| 후보 | 조건·구성 | 장점 | 도입을 정당화할 근거 |
| --- | --- | --- | --- |
| **N0 Native-only / no-op** | 런타임이 적용 지침·자산의 필요한 discovery/load를 이미 제공 | 별도 bootstrap·router·상주 context 없음 | 이미 동작함을 확인; 문제 없으면 종료 |
| **N1 Runtime pointer** | 자동 진입점 발견만 부족해 기존 저장소 하네스로 runtime-side pointer 연결 | 최소 1-hop 복구 | 실제 사용 가능한 instruction surface가 존재하며 그 pointer가 필요한 경우 |
| **N2 Lightweight selection bridge** | 진입점 후 task-relevant asset 선택·scope가 결여되어 기존 index 또는 소형 route 추가 | 필요한 본문만 읽어 context 절약 | 기존 네이티브·인덱스가 다루지 못하는 선택/Rule 연결 공백 |
| **N3 Bounded capability adaptation** | shell/파일 read/코드 실행 등의 제약 때문에 선택된 작업을 수행할 수 없음 | connector·read API·격리 스크립트 실행 등 **승인된** 대안으로 제한적 실행 | 실제 재현 가능한 gap, 동등하거나 제한된 실행 범위, 지속 자산 필요성 |

**N3는 N2 위에 무조건 쌓는 고정 단계가 아니다.** 각각 독립적으로 부족한 책임만 복구한다. 예를 들어 native Skill loading은 충분하지만 repository read connector만 없는 경우 해당 read capability를 연결하면 된다.

`CHATBOT.md`, `AGENTS.md`, `route/ROUTE.md`, `.agents/route/` 등의 파일명·분리는 **대상에서 확인된 경우에만** 사용한다. 일부 환경은 project instructions, custom connectors, hosted skills 또는 내부 catalog로 같은 역할을 수행한다. 로컬 저장소 구조를 전역 필수 배치로 승격하지 않는다.

## 하네스 구성 요소의 책임 배치

| 책임 | 기본 owner | 최적화 기준 |
| --- | --- | --- |
| Runtime에서 읽히는 첫 시작점 | 해당 서비스의 project/system/workspace/native instruction 또는 승인된 pointer | 확보된 지침 surface를 우선, 권한 부족은 정확한 handoff |
| 상시 적용 repository policy 및 path-scoped instruction | 원본 저장소·해당 runtime이 정의하는 적용 메커니즘 | 항상 필요한 구조적 규칙은 optional Skill로 숨기지 않음 |
| Task별 Skill selection 및 conditional reference | native Skill loader 또는 대상의 기존 route/index | metadata로 좁히고 선택한 canonical body만 로드 |
| Rule applicability | authoritative selector/scoping semantics | 가짜 glob·추측한 우선순위 금지 |
| 전문 역할·Subagent | 원본 Asset의 호출·권한·handoff 계약 | 실제 독립 실행 없으면 순차 모사와 제한 명시 |
| GitHub live context | 기존 `github-context` 등 적용되는 target context mechanism | source/ref/path 변경 시에만 관련 범위 갱신 |
| 도구·연결·코드 실행 | runtime/plugin/connector/native tool | 기술적 가용성과 해당 계정의 실효 권한·approval 분리 |
| Bootstrap 생성/정비 | `mols-chatbot-bootstrap` 또는 추후 결정된 동일 목적의 설계 Skill | 저빈도 구축·검증 이후 상시 실행 경로에서 빠짐 |

**필수 보존:** source assets의 지침 본문을 route/entrypoint에 복제하지 않는다. 단일 entrypoint, 0개 router, 가족별 route, target-native 자동 Skill loader 등 서로 다른 구성도 모두 유효한 후보다.

## 적용 대상별 예시 판정

1. **네이티브 Skill/Rule 지원이 충분한 런타임:** N0. 추가 `CHATBOT.md`/JSONL 생성을 '표준화'라는 이유로 권장하지 않는다.
2. **GitHub connector로 파일을 읽지만 project instruction이 repository entrypoint를 자동 발견하지 못하는 채팅:** N1. 저장소에 이미 router가 있으면 URL과 실제 loading expectation만 연결한다.
3. **Skill은 네이티브인데 특정 경로 Rule만 누락되는 환경:** Skill route 재구축 대신 해당 Rule applicability만 복구한다. N1/N2가 **필수는 아님**.
4. **웹 검색과 격리 Python은 있으나 Python egress가 없는 환경:** connector/file read로 원본을 가져온 뒤 실행 가능한 로컬 순수 알고리즘만 임시 실행. HTTP 요구·실행 불가 조건을 숨기지 않는다.
5. **권한 있는 Cloud Browser/Computer를 제공하는 환경:** UI 조작은 native 기능이지만 외부 변경·인증·계정 선택은 별도 승인 대상. '가능'과 '허용'을 구분한다.
6. **엔트리포인트를 읽을 수 없는 환경:** 연결 설정 자체를 할 수 없다면 N1을 설치한 척하지 않고 사용자에게 최소 handoff를 남긴다.

## 설계 선택 알고리즘(새 전역 설정이 아닌 판단 순서)

1. **Scope 고정:** 대상 저장소/경로/ref, 요청 결과, 기존 하네스 원본을 확인한다.
2. **가장 작은 관련 capability만 관찰:** entrypoint 읽기, source 조회, 실행 도구, 설정/승인 상태 등 결과를 바꾸는 조건만 확인한다.
3. **현재 경로를 시험:** native discovery가 충분한지, task-relevant source까지 접근 가능한지 먼저 본다. 충분하면 no-op.
4. **결손 책임만 선택:** first-hop / applicable instruction / Skill·Rule selection / canonical loading / tool capability 중 확인된 누락만 복구한다.
5. **대안을 비교:** N0 또는 기존 mechanism 재사용이 유효하면 다른 구성을 버린다. 비슷한 품질이면 router hop과 새 파일·설정이 적은 후보를 선호한다.
6. **영향 최소화:** 사용자가 승인한 tuning·branch·기존 스킬을 보존하고 필요한 경로에만 변경한다.
7. **주장 수준 검증:** 구조적 구성, 실제 접근성, 런타임이 선택·적용한 증거를 분리해 완료/부분완료/handoff를 판단한다.

이 순서는 문맥상 변경 불가능한 체크리스트가 아니라 **중요한 의존성을 놓치지 않는 의사결정 근거**다. 대상 runtime이 동등한 native 결과를 제공하면 중간 파일 단계나 수동 도구 호출을 강제하지 않는다.

## 스킬 경계 재검토: 기존 Skill 확장 vs 별도 설계 Skill

| 선택지 | 얻는 것 | 위험 | 현재 판단 |
| --- | --- | --- | --- |
| **A. 현 `mols-chatbot-bootstrap`에 경량 설계 비교를 포함** | bootstrap·repair와 같은 이유로 선택되는 capability를 한곳에 유지 | 장황한 범용 harness architect가 되어 activation 확대 | **우선안:** 기존 책임에 실제 도움 되는 후보 비교만 포함 |
| **B. 별도 `mols-chatbot-harness-design` 신설** | 신규 구축/진단과 실무적인 bootstrap 구현의 독립 activation 가능 | 중복 workflow·혼란·추가 로딩/유지보수 | 현재는 보류. 독립 사용 사례가 실제로 확인되면 재평가 |
| **C. 기존 Skill을 범용 하네스 아키텍처 설계로 전면 재정의·rename** | 넓은 요구를 한 Skill로 표현 | 외부 호출 경계·라이프사이클·기존 사용자 회귀 | **보류:** activation·호환성을 검증한 뒤 결정 |

**결정 게이트:** 새로운 스킬을 만들거나 이름·description을 바꾸기 전, 현 스킬의 intended use(부트스트랩/복구), broad design use(처음부터 최적 구조 설계), near-miss(일반 코드 아키텍처/CI/메모리/자동화) 각각에서 선택 경계를 확인한다. 지금 단계에서는 **보완 가능한 동일한 목적의 bounded 설계**를 우선하고, 독립 소유권이 증명되면 분리를 제안한다.

## 외부 근거 및 증거 수준

- [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx): metadata → 필요 시 body → 조건부 references의 점진적 로딩. 최적화의 근거이지 모든 런타임이 해당 스펙을 자동 적용한다는 보장은 아님.
- [Anthropic — steering instructions, skills, hooks, subagents](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more): 항상 적용하는 지침과 필요할 때 선택하는 Skill의 책임 차이, 컨텍스트 비용 분리.
- [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions): repository-wide/path-specific instruction 및 AGENTS.md 지원은 클라이언트·기능에 종속. 공통 파일 이름만으로 지원과 우선순위를 추정할 수 없음.
- [OpenAI ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt): project instruction·files·대화 컨텍스트가 별도 surface이며 GitHub 저장소의 파일을 자동으로 모두 따라 읽는다는 근거는 아님.
- [서비스별 tool/runtime 조사](chatbot-runtime-landscape.md), [하네스 로딩 조사](research-harness-fidelity.md): 제품/모드별 조건부 capability, 정적 계약과 실제 행동 근거 구분.

본 문서의 N0–N3는 **연구용 설계 옵션**이지 새로운 저장소 스키마, runtime feature 목록이나 모든 제품의 필수 구현 단계가 아니다. 실제 운영 품질·비용에 대한 비교 우위는 [평가 전략](harness-evaluation-strategy.md)의 실측 전까지 가설이다.
