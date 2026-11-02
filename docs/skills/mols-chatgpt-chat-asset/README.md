---
description: ChatGPT Chat 전용 Agent Asset 생성·튜닝·유지보수 Skill의 책임, 표면 선택, 지원 근거와 검증 계획을 살필 때 사용합니다.
---

# ChatGPT Chat Agent Asset — Maintainer Guide

실행·activation 계약은 [`mols-chatgpt-chat-asset`](../../../src/openai-chatgpt-chat/skills/mols-chatgpt-chat-asset/SKILL.md)가 소유한다. 이 문서는 제품별 기능 변화를 반영할 **설계 판단과 검증 계획**만 유지한다.

## 책임과 자산 위치

ChatGPT **Chat** 환경은 사용 가능한 도구와 소비 가능한 자산 유형이 Codex CLI나 로컬 에이전트 하네스와 다르다. 범용 Skill/Rule/Subagent의 작성·튜닝 방법은 기존 `mols-agent-asset`이 맡고, 이 Skill은 **Chat 소비 표면 선택과 런타임-specific 의미 보존**에만 집중한다.

- `mols-agent-asset` — 공통 설계·튜닝·검토·검증 및 Eval의 방법론.
- `mols-chatbot-bootstrap` — 챗봇이 저장소의 정본과 필요한 실행 의미에 도달하도록 첫 진입점을 구축·복구하는 낮은 빈도의 하네스 작업.
- `mols-agent-asset-find` — 기존 Agent Asset 탐색·선택·로딩·설치·동기화.
- `mols-chatgpt-chat-asset` — Chat에 최적화된 새 자산 생성, 기존 자산의 target-specific 조정, **제작 대상의 소비 표면 결정**·패키징·유지보수.
- 특정 작업 Skill(예: OpenSpec CLI 호환) — 그 작업의 실제 domain 실행 의미.

작성 원본은 `src/openai-chatgpt-chat/skills/mols-chatgpt-chat-asset/SKILL.md` 한 곳이다. 이 경로는 **저장소에서 관리하는 vendor-native 원본**이며 자동 설치 경로가 아니다. 필요에 따라 이 스킬 자체도 Chat에 배포해 사용 가능하지만, 이 저장소의 작업에서 읽을 수 있다는 사실만으로 설치되었다고 주장하지 않는다.

## 리뷰 범위 — 제작 대상과 제작 스킬을 혼동하지 않기

**이 Skill이 만든/수정한 Agent Asset의 Chat 소비 계약**과 **이 제작 Skill 자체가 호출되는 하네스 경로**는 별개의 문제다. 리뷰에서 둘을 혼동하지 않는다.

- **평가 대상:** 사용자 요청에 맞는 Agent Asset 유형(Skill, Project instructions 등) 선택, 기존 원본의 의도·selector·격리·권한·검증 계약 보존, Chat 전용 조정의 정확성, 생성 패키지의 규격·최소성, **제작 결과물**의 지원되는 배포·선택·행동 검증 가능성.
- **평가 범위 밖:** `mols-chatgpt-chat-asset` **자체**를 누가 어떻게 발견·라우팅·로딩·설치하는지, 이 스킬이 `mols-agent-asset`·`mols-agent-asset-find` 등을 직접 호출하거나 로드하는 오케스트레이션, 저장소 first-hop/`CHATBOT.md` 구축. 이는 각 하네스·런타임 및 관련 owner가 담당한다. 인접 owner의 이름을 문서에 적은 것은 **책임 구분**이지 스킬 내 필수 호출 순서를 추가하라는 뜻이 아니다.
- **예외를 정확히 분리:** 이 스킬의 `description`이 사용자 제작·튜닝 요청을 포착하는지에 대한 activation 설계/평가는 정상적인 **Skill 품질 검토**이다. 그러나 발견·호출 인프라의 구성이나 설치 경로를 이 제작 스킬의 실행 책임으로 요구해서는 안 된다. 마찬가지로 제작 결과물의 소비 계약을 설계·검토하는 것은 허용되지만 설치만 요청한 별도 작업의 실행을 이 스킬에 부과하지 않는다.
- **리뷰 판정 게이트:** 지적한 문제의 주체가 *제작 결과물*인지 *제작 스킬을 소비하는 하네스*인지 먼저 분류한다. 하네스 쪽 문제를 이 스킬의 결함으로 표시하거나, 근거 없는 router·asset loader·Creator 호출 절차 추가를 개선안으로 제시하지 않는다. 실제로 제작·튜닝 산출물의 정확성에 영향을 준 문제만 이 Skill의 수정 후보로 남긴다.

## Chat 소비 표면과 기술 선택 근거

2026-11-02에 확인한 공식 문서 기준. 지원 계정과 UI, workspace permission은 변경될 수 있으므로 활성 환경에 대한 현재의 확인을 우선한다.

| 의도 | 검토할 Chat surface | 흔한 오해 |
| --- | --- | --- |
| 반복 가능한 선택적 작업 방법 | **Skill** (`SKILL.md`, 선택적 references/assets/scripts) | 저장소나 Codex용 `.agents/skills` 경로만으로 Chat에 자동 노출된다고 가정 |
| 한 프로젝트의 지속적인 컨텍스트·정책 | **Project instructions**, Project 파일·연결 소스 | Project instruction이 범용 Skill의 자동 선택 또는 scoped-rule glob을 보장한다고 가정 |
| 연결 앱과 함께 재사용·배포하는 능력 | **Plugin**, 앱/MCP tools | Skill만 작성하면 외부 도구와 OAuth 권한까지 생긴다고 가정 |
| 현재 사용자가 직접 설정할 전역 지침 | 해당 Chat 계정의 지원되는 설정 표면 | 저장소의 텍스트를 읽었다는 이유로 계정 설정이 변경됐다고 가정 |
| 기존 GPT 자산을 관리 | 해당 workspace에서 **실제 지원되는 경우에만** GPT 기능 | 개인 계정에서 신규 GPT 생성이 항상 가능한 것으로 가정 |
| 로컬 agent 명령·hook·독립 Subagent | 명세된 실행 의도가 가능한 **native tool 또는 제한적 대체 지침** | 역할별 문장·Python sandbox만으로 격리·독립 명령 실행까지 재현했다고 가정 |

공식 [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)는 해당 기능이 제공되는 **Business·Enterprise·Healthcare·Edu의 적격 계정/워크스페이스**에서 Chat 내 직접 생성·편집·업로드·설치 경로를 안내한다. **모든 개인 플랜에서 직접 설치할 수 있다고 가정하지 않는다.** [Build skills](https://learn.chatgpt.com/docs/build-skills)는 Agent Skills 표준, description 기반 활성화, Plugin 묶음 배포와 Codex 로컬 로딩 차이를 설명한다. **Plugin 배포만이 유일한 Skill 소비 경로라고 단정하지 않는다.** 같은 문서에서 기능 제공 범위가 구분되므로 작성 원본의 존재를 활성화 증거로 삼지 않는다.

[Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)는 파일과 프로젝트 지침의 역할을 소유하고, [Plugins](https://learn.chatgpt.com/docs/plugins)는 설치 가능한 Skill·도구 번들의 의미를 소유한다. [GPT creation and editing](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts)에 따르면 신규 GPT 작성·게시의 지원이 계정·워크스페이스와 시점에 따라 제한되므로, Skill 설계의 기본 출력으로 GPT를 선택하지 않는다.

## 설계 결정

1. **기능이 아니라 소비 목적에 맞춰 유형을 고른다.** `Agent Asset`은 Skill 하나를 뜻하지 않는다. 기존 Rule의 구조적 selector, Subagent의 격리, Command의 shell 실행과 같은 본래 동작을 Chat의 단순 Markdown로 무리하게 투영하지 않는다.
2. **Target delta만 작성한다.** 범용 제작 방법론은 기존 owner를 따르고, Chat-only 특성이 실제 선택·호출·컨텍스트·권한·검증에 영향을 주는 경우에만 새 지침을 만든다.
3. **도구 가능성과 권한을 분리한다.** 연결 앱, Project 파일, Python 분석, 웹, native Skill creator 등의 사용 가능성을 작업별로 판단한다. 설치·계정 전환·공유·원격 쓰기는 별도 승인 대상이다.
4. **검증 가능한 최소 패키지.** 단일 `SKILL.md`에서 시작한다. 선택적 runtime resource에 로딩 이점이 있을 때에만 `references/`·scripts를 추가한다. 정본을 Rulesync와 Chat-native 원본으로 중복 관리하지 않는다.
5. **관리와 실제 소비는 별개다.** 작성되었다(`authored`), 배포 경로가 연결되었다(`reachable`), Chat에서 선택·행동이 관찰되었다(`observed`)의 근거를 분리한다.

## Chat runtime 최대 활용 기준

별도 실행기를 새로 작성하기 전에 **현재 대상 Chat의 native Creator/Editor, Skill 및 Plugin 설치 상태, 연결 앱의 실제 read/write action, Project·첨부 파일, 웹, 코드·파일 분석** 중 작업의 목적에 필요한 것만 발견한다. 연결의 identity·permission, 읽기→분석→쓰기→readback 경계를 명시하며, 실행 도구가 존재한다는 이유로 사용자 승인이나 provider 권한을 추정하지 않는다.

동일한 외부 쓰기가 연결 앱에서 가능하면 임의의 CLI나 sandbox 네트워크 호출보다 해당 action을 우선 검토한다. 반대로 independent agent, shell, Rule selector가 필요한 경우는 capability가 실제 확인되지 않으면 부분 대체·인계로 제한한다. 최종 산출은 **canonical source**, **Chat consumer**, **필수 도구·권한**, **관찰 가능한 행동 검증**을 분리한다.

## 검증 계획

| 요청/상황 | 기대하는 결과 |
| --- | --- |
| "ChatGPT Chat 전용 Skill을 새로 만들어줘" | 제작 대상의 Chat 소비 계약과 최소 Skill 패키지를 올바르게 설계 |
| "기존 Rule을 Chat Project 지침으로 튜닝해줘" | selector·상시 적용·자동 enforcement 차이를 분리하고 보존 가능한 delta만 작성 |
| "Subagent를 Chat에서 똑같이 돌리도록 바꿔줘" | 독립성/격리 필수 여부 확인, 동등성 불가 시 명시적 제한·인계 |
| "GitHub 연결을 사용하는 Skill을 설계해줘" | 현재 연결 identity·action·permission을 명시적으로 확인하고 tool/text 역할을 분리 |
| "작성한 Chat Skill이 대상 환경에서 보이지 않아. 제작 결과물의 배포 계약을 검토해줘" | 원본·배포 요구·설치 상태·활성화 증거의 차이를 검토하되, 설치 실행은 별도 owner로 분리 |
| "범용 Codex Skill을 만들어줘" | Chat 대상 범위가 아니므로 이 Skill은 선택하지 않음 |
| "ChatGPT 첫 진입점과 전체 하네스를 고쳐줘" | `mols-chatbot-bootstrap`의 책임으로 분리 |
| "일반 글을 써줘" | Agent Asset 제작 요청이 아니므로 비활성 |

검증 단계는 (1) **정적 규격**: [Agent Skills specification](https://agentskills.io/specification)과 경로·메타데이터·링크, (2) **의미 검토**: 책임/trigger/near-miss/원본 차이, (3) **실제 Chat 평가**: 지원되는 계정·런타임의 설치/선택/도구 사용/부분 수행을 구분한다. 샌드박스에서 `SKILL.md`를 파싱한 것만으로 Chat 적용 성능이 검증됐다고 주장하지 않는다.

초안 범위 밖: Chat 계정/워크스페이스에 Skill 설치, Plugin 패키징과 게시, 독립적 행동 Eval 자동화, 별도 CLI 구현. 향후 실제 사용 중 재현되는 문제를 근거로 필요한 것만 추가한다.
