---
name: mols-chatgpt-chat-asset
description: >-
  Create, adapt, tune, review, validate, or maintain agent assets specifically
  for OpenAI ChatGPT Chat mode, including ChatGPT Skills, reusable instructions,
  project-scoped guidance, and compatibility adaptations of existing rules,
  agent/subagent prompts, workflows or tool-dependent skills. Choose Chat-native
  consumption and runtime capabilities without assuming Codex/Work features.
  Not for generic cross-platform asset authoring, ordinary ChatGPT usage,
  installation-only tasks, or provisioning a repository chatbot harness.
---

# ChatGPT Chat Agent Asset

ChatGPT **Chat 모드**에서 실제 소비할 수 있는 에이전트 자산을 생성·튜닝·관리한다. 핵심은 기존 자산의 의도와 계약을 보존하면서 Chat의 **네이티브 소비 표면, 가용 도구, 컨텍스트와 권한 경계**에 맞추는 것이다. 범용 Agent Asset 설계 방법론이나 Chat 런타임 전체의 하네스를 다시 정의하지 않는다.

## 판단 기준

- 대상은 일반 Chat이다. ChatGPT Work의 컴퓨터·클라우드 브라우저, Codex의 터미널·worktree, 로컬 에이전트의 hooks·commands·isolated subagents를 Chat의 기본 기능이라고 가정하지 않는다.
- 제품별로 지원 기능이 바뀌므로 대상 계정·워크스페이스·세션에서 실제로 노출된 Skill, Project 지침, 첨부/프로젝트 파일, 연결 앱, 코드 실행, 파일 출력과 권한을 **필요한 만큼만** 확인한다. 공식 문서의 가용성은 현재 세션에서의 설치·승인·실행 관찰과 구분한다.
- 원본 자산·표준·프로젝트 지침은 각각의 계약을 소유한다. 이 Skill은 Chat-specific delta와 소비 연결만 담당한다. 동일한 의미의 자산을 서로 다른 작성 원본 두 곳에서 관리하지 않는다.
- 외부로 부작용을 남기는 생성·설치·공유·계정 연결·GitHub 변경은 실행 계정, 대상과 허가된 범위를 먼저 확인한다. 계정·명의를 임의 전환하지 않는다.

## 제작·튜닝 흐름

1. **작업과 소비자를 확인한다.** 신규 제작, 기존 자산 이식·튜닝, 유지보수, 리뷰·검증 중 실제 요청을 판별한다. 대상 Chat 표면, 사용자/프로젝트 범위, 필요한 activation, 입력, 결과, 도구 의존성과 기존 원본을 확인한다. 리뷰만 요청되면 쓰기를 진행하지 않는다.
2. **적합한 Chat 소비 표면을 선택한다.** 반복적이고 선택 가능한 task workflow는 **Skill**을 우선 검토한다. 프로젝트 전체에 지속 적용할 짧은 계약은 **Project instructions** 등 실제 지원되는 지침 표면을 사용한다. 외부 서비스의 데이터/동작이 필수면 **연결 앱/MCP 도구 또는 Plugin**의 실제 제공·권한을 확인한다. 설정 범위가 사용자 개인이면 해당 설정의 사용 가능성과 주체를 따로 확인한다. 기존 GPT 등의 다른 제품 표면은 요청·지원 여부를 확인한 경우에만 고려한다. 한 요구를 모두 Skill로 옮기지 않는다.
3. **새 소유자나 변형이 필요한지 결정한다.** 적절한 기존 자산을 사용할 수 있으면 재사용·튜닝한다. Chat에만 필요한 독립적인 적용·설치·유지보수 범위가 있을 때에만 별도 자산/variant를 만든다. 프로젝트 전용 내용은 범용 Skill 본문으로 끌어오지 않는다.
4. **원본과 Chat의 차이를 좁힌다.** 기존 Skill/Rule/Subagent/Command의 trigger, 입력, 의존 파일·명령, 출력, 검증, side effect와 종료 조건을 구분한다. Chat에서 native 수행이 되면 그대로 재사용한다. 부족한 경우 실제 도구를 연결한 허용된 adapter, 안전한 부분 수행, 원본상 선택적인 생략 또는 사용자 인계를 명시한다. path/glob 기반 Rule, 독립 Subagent, 터미널 전용 script를 단순 설명으로 옮겼다는 이유만으로 같은 실행·자동 적용·격리 의미를 얻었다고 주장하지 않는다.
5. **작은 원본을 작성·수정한다.** Skill이라면 [Agent Skills specification](https://agentskills.io/specification)의 `SKILL.md`와 현재 [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)의 Chat 소비 계약을 따른다. `description`에는 사용자가 실제로 요청할 작업과 가까운 비대상 요청을 구분한다. 모든 activation에 필요한 지침만 본문에 두고, 조건부 참조·script·asset은 실제 로딩 또는 deterministic 이점이 있을 때만 추가한다. 규정된 메타데이터 외에 임의의 target field를 발명하지 않는다.
6. **런타임 도구를 목표에 맞게 연결한다.** 필요한 경우 저장소 연결 도구로 특정 ref를 읽고, 첨부·프로젝트 소스나 허용된 코드 분석기로 검토한 뒤, 승인된 원격 쓰기는 원본 연결 도구로 실행한다. Python/분석 sandbox와 연결 서비스의 네트워크·파일시스템·인증 상태가 같다고 전제하지 않는다. 허용된 네이티브 Creator/Editor/Plugin 경로가 있다면 새 generator·installer 구현보다 우선한다.
7. **검증하고 인계한다.** 패키지 규격·링크·출처·delta 보존을 검사하고, 대표 **positive / negative / near-miss** 요청으로 activation을 검토한다. 실제 Chat에서 가능한 경우 설치·선택·원본 로딩·도구 호출·권한 부족·행동 결과를 테스트한다. 정적 검사와 시뮬레이션을 실제 런타임 호환성으로 표현하지 않는다. 설치·공유가 요청 범위 밖이거나 기능이 없으면 소스 작성과 실제 활성화를 분리해 인계한다.

## Chat 전용 실패 모드

- **원본을 만들었지만 Chat에서 보이지 않음:** 저장소 내 `src/` 또는 로컬 Skill 경로는 Chat의 자동 설치 증거가 아니다. 대상 환경에서 직접 생성·업로드·설치 또는 Plugin 배포 등 실제 지원 경로와 권한을 확인한다. 특정 배포 방식을 모든 계정의 필수 경로로 고정하지 않는다.
- **Rule을 Chat 지침으로 변환:** repository selector, scope, inheritance, enforcement를 Project instructions만으로 재현할 수 있는지 분리한다. 항상 필요한 안전·권한 경계를 선택적 Skill activation에 맡기지 않는다.
- **Subagent나 command가 없는 경우:** 독립 실행·격리·병렬성·shell side effect가 필수인지 확인한다. 순차적 관점 검토나 문서화로 대체할 수 있어도 동등한 Subagent/CLI 실행이라고 주장하지 않는다.
- **Plugin, 앱 또는 외부 연결이 필요한 경우:** 실제 연결·승인된 서비스 계정과 노출 action을 확인한다. Skill text만으로 도구가 설치되거나 권한이 부여되지 않는다.
- **중복된 하네스 또는 과도한 패키지:** 첫 진입·routing 복구는 별도 하네스 owner가 맡고, 공통 자산 설계 규칙은 기존 owner를 따른다. Chat-specific 동작 차이가 없다면 포크·추가 router·CI·스크립트를 만들지 않는다.

## 산출과 검증 수준

사용자가 관리할 **canonical source**, Chat에서의 **실제 소비·활성화 경로**, 생성·수정된 내용, 보존/변경한 계약, 검증·미검증 범위, 필요한 최소 후속 작업을 구분해 제시한다. 지원 상태는 `작성됨`, `설치·연결 확인`, `실제 Chat 작업에서 적용 관찰`을 혼동하지 않는다. 전체 유지보수 요청에서도 실제 실패나 drift가 있는 부분에만 개입한다.

## 제외 범위

일반적인 Agent Asset의 작성·검증 방법론 자체, Chatbot 하네스 부트스트랩, Plugin/MCP 서버 개발 전반, ChatGPT Work·Codex 전용 기능 구축, 일반 콘텐츠 생성이나 일회성 OpenSpec 실행은 해당 책임 주체에 둔다. 이 Skill은 Chat 대상에만 필요한 작성·튜닝 판단을 담당한다.
