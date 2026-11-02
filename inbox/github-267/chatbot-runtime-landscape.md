# 주요 챗봇 서비스의 도구·플러그인·런타임 조사

> 조사 기준일: 2026-11-02. 주요 서비스의 **사용자용 채팅/에이전트 환경**을 대상으로 공급자 공식 문서를 확인했다. 표는 서비스의 최대 기능이나 모든 계정의 권한을 의미하지 않는다. 실제 기능은 제품 모드, 요금제, 지역, 클라이언트, 조직 설정, 설치 및 연결된 계정에 따라 달라진다. 별도 API나 코딩 에이전트의 기능을 일반 채팅에 전가하지 않는다.

## 결론과 적용 목적

`mols-chatbot-bootstrap`이 판단할 것은 “어느 서비스인가”만이 아니라 **현재 대화에서 어떤 기능과 권한이 실제로 노출·승인·실행 가능한가**이다. `CHATBOT.md`를 발견해도 작업에 해당하는 지침·Skill 본문까지 읽지 않았다면 하네스 적용이 끝난 것이 아니다. 반대로 로컬 에이전트 수준의 도구가 있더라도 불필요한 전체 자산 사전 로딩을 정당화하지 않는다.

제품별 기능표는 **탐색 후보를 제시하는 조사 자료**이지, 그 제품이 반드시 수행할 수 있다는 실행 계약이 아니다. 작업 시 런타임의 실제 tool inventory와 연결·권한 상태를 먼저 확인해야 한다.

## 비교 기준

- **파일 접근:** 업로드/첨부/연결 검색과 실제 파일·저장소의 경로별 읽기·쓰기 권한을 구분.
- **코드 실행:** 코드 *생성*과 격리된 Python 실행, shell/terminal, 로컬 컴퓨터 프로세스 실행을 구분.
- **네트워크:** 검색·커넥터 사용 가능 여부와 코드 실행 환경에서 임의 HTTP/API 호출 가능 여부는 다름.
- **외부 도구:** 내장 도구, 앱/커넥터/플러그인, custom MCP, 개발자 API/function-calling을 구분.
- **브라우저:** 검색 결과 조회, 페이지 열람, 로그인한 사이트의 클릭·입력·제출 및 로컬/클라우드 브라우저를 구분.
- **지속성:** 세션 임시 파일, 프로젝트 파일, 로컬 디렉터리, 영속 클라우드 컴퓨터 및 예약·이벤트 트리거를 구분.
- **안전·증거:** 계정 연결 사실만으로 특정 권한·명의·외부 쓰기·실제 실행 성공을 추정하지 않음.

**표기:** `제공` = 공식 문서에서 해당 모드 지원 확인, `조건부` = 플랜·클라이언트·설정·연결 등이 필요, `별도 제품` = 같은 공급자이나 현재 일반 채팅에 자동 적용되지 않음, `미확인` = 문서에서 일반 제공을 확인하지 못함(부재 단정 아님).

## 서비스별 비교

| 서비스 / 실행 모드 | 외부 도구·연결 | 코드·파일 런타임 | 브라우저/컴퓨터 작업 | 예약·지속성 | 하네스 관점의 경계 |
| --- | --- | --- | --- | --- | --- |
| **ChatGPT 일반 Chat** | 앱·플러그인, 웹 검색 등 조건부 | 파일 분석용 격리 Python 지원; 해당 Python의 직접 외부 HTTP 불가 | 일반 검색과 Work의 UI 자동화는 별개 | 프로젝트/선택된 task 기능은 별도 | 연결된 앱 권한 및 실제 노출된 도구 기준 |
| **ChatGPT Work / Codex** | Work에서 연결 앱·플러그인 활용 | Work 클라우드 컴퓨터, 별도 Codex 코딩 환경 | Work 클라우드 브라우저·멀티스텝 작업 | Work의 예약·이벤트 작업 제공 | Chat의 Python 환경과 Work/Codex 도구를 혼동 금지 |
| **Claude Chat / Desktop** | 원격 커넥터·MCP; Desktop 로컬 확장 | Chat 내 코드 실행·파일 생성; 네트워크는 계정/조직 정책에 종속 | 로컬 컴퓨터 접근은 별도 Desktop/Cowork 기능 | 일반 chat과 Cowork 예약을 구분 | 원격 MCP와 로컬 확장 서버는 접근 경로가 다름 |
| **Claude Cowork** | 커넥터·Skills·플러그인 | 클라우드 작업; Desktop을 통한 조건부 로컬 파일 접근 | 브라우저/컴퓨터 조작 조건부 | 클라우드 예약 작업 | Desktop 연결 종료 시 로컬 파일 접근 변화 |
| **Gemini Apps Chat** | Connected Apps·Google 서비스, GitHub 코드 가져오기 | 파일·코드 읽기는 가능; 범용 임의 shell은 확인되지 않음 | 기본 chat의 웹 검색과 task의 브라우저 별개 | Chat의 Scheduled actions | GitHub 가져오기는 snapshot·읽기 지향이며 PR 작업 아님 |
| **Gemini Tasks / Spark** | Connected Apps, Skills, 일부 custom MCP | 별도 remote computer/code execution | 별도 remote browser 제공 | 예약·트리거 기반 task | 구독·개인 계정·지역 등 접근 제한; Chat과 동일시 금지 |
| **Microsoft Copilot 개인용** | OneDrive/Outlook/Gmail/Drive 등 소비자 커넥터 | 일반 chat의 범용 Python/shell은 공식 근거 미확인 | Edge의 Browse with Copilot 조건부·지역 한정 | 전용 agent와 분리 | 기업용 Copilot 기능을 개인용에 일반화 금지 |
| **Microsoft 365 Copilot / Copilot Studio** | Graph·SharePoint·connector·agent tools·MCP | declarative agent의 Python code interpreter sandbox | Copilot Studio computer use, 기업용 원격 브라우저 등 별도 조건 | Copilot Studio workflow 등 구성에 따름 | 라이선스·관리자 정책·agent 설정에 종속 |
| **Perplexity Search / Research** | 웹 검색 및 근거 인용, 커넥터/파일 기능은 모드별 | 일반 검색에 임의 shell을 전제하지 않음 | 검색과 에이전트 브라우저 조작은 다름 | Computer와 구분 | 검색 기능만으로 저장소 수정 능력을 추정 금지 |
| **Perplexity Computer / Personal Computer** | 다수 커넥터·custom MCP·Skills | 코드 작업, 프로젝트 영속 파일; Personal Computer는 승인된 로컬 Mac/Windows 환경 | 브라우저 작업 및 로컬 앱 조작 가능 범위가 모드에 종속 | 백그라운드/반복 작업 지원 | local folder 권한과 cloud 작업 공간 별도 |
| **Grok Chat / Grok Bot** | Grok chat connectors·custom remote MCP | Chat의 임의 shell은 미확인; **Bot**은 영속 클라우드 terminal·파일시스템 | Bot cloud browser 및 computer use | Bot 일정/장시간 실행 | 여러 Bot의 클라우드 컴퓨터 공유는 권한 격리가 아님 |
| **Poe 일반 Bot / Script Bot** | Bot 종류마다 도구 상이; Server Bot은 자체 서비스 통합 | Script Bot은 Poe 호스팅 Python 3.11 격리 환경 | 일반 Bot에 UI 자동화 보장 없음 | Script Bot 실행 간 상태 비영속 | Python sandbox는 **Bot 제작자의 실행 환경**; 일반 Poe 대화의 공통 런타임 아님 |

아래 상세 설명과 공식 문서를 기준으로 읽는다. **`미확인`은 지원하지 않는다는 단정이 아니라 현재 조사에서 그 능력을 입증하지 않았다는 뜻**이다.

## 1. ChatGPT (OpenAI)

- **Chat:** 연결 앱·플러그인으로 외부 정보 조회와 지원되는 쓰기 작업이 가능하다. 사용 가능 여부는 플랜·지역·workspace·현재 대화의 실제 도구 노출에 종속된다. 첨부 파일 분석에는 상태를 유지하는 Jupyter/Python 환경이 쓰일 수 있으나 **이 Python 환경에서는 직접 외부 웹/API 요청이 불가능**하다. 웹 검색·연결 앱 도구는 별도의 경로다.
- **Work:** 연결 앱, 클라우드 브라우저(읽기, 클릭, 입력)와 복합 작업, Scheduled Tasks 및 지원되는 이벤트 기반 작업을 제공한다. 이용 자격·관리자 설정과 사용자 승인에 따라 달라진다.
- **Codex:** 같은 OpenAI 계열이라도 개발 작업용 별도 제품·실행 환경이다. Codex의 repository/terminal 권한을 Chat에 자동 승계하지 않는다.
- **Bootstrap 함의:** 직접 소스 코드를 실행할 수 있어도 네트워크 접근은 불가할 수 있다. 사용 가능한 연결 도구로 **정확한 ref의 본문을 읽고** 제한된 코드 런타임에서는 필요하다면 안전한 최소 스크립트 대체만 검토한다. Work나 Codex를 사용 중이라고 가정하지 않는다.

공식 근거: [데이터 분석 및 Python 제약](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt), [연결 앱](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt), [Work와 Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex), [Work 클라우드 브라우저](https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt), [예약·이벤트 작업](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt).

## 2. Claude (Anthropic)

- **일반 Claude Chat:** 코드 실행·파일 생성 환경을 제공한다. 개인 플랜에서는 승인된 패키지 소스 등에 대한 네트워크 접근이 가능하나 Team/Enterprise는 조직 설정으로 차단·제한할 수 있다. 이 코드 환경을 로컬 컴퓨터 shell과 동일시하지 않는다.
- **연결:** cloud SaaS에는 원격 connector/remote MCP, 컴퓨터의 파일·로컬 프로세스에는 Claude Desktop의 로컬 확장/로컬 MCP가 적합하다. 원격 MCP는 Anthropic 클라우드에서 접속하므로 localhost 서비스가 자동으로 연결되지 않는다. Skills와 plugins를 배포·활성화할 수 있다.
- **Cowork:** 웹·모바일·데스크톱에서 시작 가능한 다단계 작업 환경이다. 컴퓨터/브라우저 조작 및 로컬 파일 접근은 플랜·베타·Desktop 연동에 종속된다. 클라우드 예약 작업은 컴퓨터가 꺼져도 실행될 수 있지만 연결된 **로컬** 파일은 Desktop의 상태·세션 조건에 제약된다.
- **Bootstrap 함의:** 'Claude'라는 이름만으로 로컬 FS/MCP에 접근한다고 판단하지 말 것. 실제 source 로딩은 활성화된 connector·확장·작업 공간으로 증명한다.

공식 근거: [Chat 코드 실행·파일 생성 및 네트워크 설정](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude), [web/desktop connector 구분](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors), [remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp), [Cowork 환경 비교](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile), [Cowork 예약 작업](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork).

## 3. Gemini Apps (Google)

- **일반 Gemini Chat:** Connected Apps로 Gmail·Drive·Calendar·일부 외부 앱을 조회하거나 지원된 작업을 수행한다. 개인/업무 계정, 기기·지역·Keep Activity 설정별 차이가 있다.
- **GitHub 가져오기:** 웹 앱에서 저장소 또는 브랜치를 붙여 코드 질의가 가능하지만 **가져온 이후 변경 사항이 자동 동기화되지 않으며**, Git commit history·PR 메타데이터 조회 및 repository 쓰기는 이 GitHub 첨부 기능에 포함되지 않는다. 단순한 URL 제시만으로 해당 GitHub 앱을 통한 읽기가 되지도 않는다.
- **Schedules와 Skills:** 일반 Chat의 Scheduled actions와 Tasks의 예약·트리거는 별개의 기능이다. Gems에서 Skills로의 전환 중이며 Skills의 Canvas·Deep Research 등 다른 기능과의 결합에도 제한이 있다.
- **Tasks / Spark:** 별도 에이전트 작업 모드에서는 remote browser·remote computer/code execution, Connected Apps·Skills 및 조건부 custom MCP가 가능하다. 공식 문서상 특정 개인 Google 계정, 구독, 나이·지역 요건이 있다.
- **Bootstrap 함의:** 일반 Chat에서 GitHub 소스를 읽더라도 실제 ref·최신성 및 필요한 파일의 본문 접근을 검증한다. **Gemini API의 built-in Code Execution을 Gemini Chat의 일반 tool로 간주하지 않는다.**

공식 근거: [Connected Apps](https://support.google.com/gemini/answer/13695044), [GitHub 저장소 import 제약](https://support.google.com/gemini/answer/16176929), [Scheduled actions](https://support.google.com/gemini/answer/16316416), [Gemini Tasks 조건·실행 도구](https://support.google.com/gemini/answer/17094507), [Gems→Skills 전환](https://support.google.com/gemini/answer/18560919), [Gemini API 도구—소비자 앱과 구분](https://ai.google.dev/gemini-api/docs/tools).

## 4. Microsoft Copilot

- **개인용 Microsoft Copilot:** OneDrive·Outlook.com·Gmail·Google Drive 등 소비자 커넥터를 연결해 파일·메일·일정 검색에 활용할 수 있다. 해당 계정의 기존 권한만 사용한다. Edge의 **Browse with Copilot**은 현재 미국 Microsoft 365 Premium 구독자 등을 대상으로 순차 제공되므로 개인용 웹 채팅 전반에 UI 자동화가 있다고 볼 수 없다.
- **Microsoft 365 Copilot:** 개인용과 별개로 조직의 Microsoft Graph, SharePoint, Teams, Microsoft 365 Copilot connectors 및 declarative agents를 이용한다. Agent Builder의 **code interpreter는 Python sandbox**이며, 임시 파일 생성/다운로드 기능을 제공한다.
- **Copilot Studio:** agent tools로 AI prompts, MCP, 조건부 computer use를 지원한다. 별도의 **기업용 remote browser**도 있다. 라이선스, 라이브러리·워크스페이스 권한과 관리자가 설정한 agent 구성을 확인해야 한다.
- **Bootstrap 함의:** consumer Copilot ↔ Microsoft 365 Copilot ↔ Copilot Studio는 서로 다른 capability surface다. 'Microsoft Copilot' 하나로 묶어 Python, GitHub connector, local UI automation을 가정하지 않는다.

공식 근거: [개인용 커넥터](https://support.microsoft.com/en-us/microsoft-copilot/connecting-microsoft-copilot-to-other-services), [Edge 로컬 브라우저 조작](https://support.microsoft.com/en-us/edge/copilot/browse-with-copilot), [M365 Agent knowledge/도구](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/knowledge-sources), [Agent Python interpreter](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/code-interpreter), [Copilot Studio agent tools](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/agent-tools), [기업용 remote browser](https://learn.microsoft.com/en-us/microsoft-365/copilot/use-remote-browser-microsoft-copilot).

## 5. Perplexity

- **Search / Research:** 웹 근거 검색과 리서치를 목적으로 하는 채팅 표면이다. 검색 가능한 사이트가 있다는 사실만으로 로컬 디스크, 일반 shell, 외부 쓰기가 가능한 것은 아니다.
- **Perplexity Computer:** 코딩, 브라우저 자동화, 파일 생성, 다단계·병렬 작업, 스케줄/지속 작업, 다수 connector와 custom MCP 및 재사용 Skills를 지원한다고 공식 제품 문서가 설명한다. **Projects**는 영속 파일 시스템과 작업 간 문맥을 지원한다.
- **Personal Computer:** 데스크톱 앱에서 사용자가 연결한 폴더·로컬 앱·Comet 브라우저/기존 로그인 세션을 활용하는 별도 설정이며 OS 접근 권한과 승인이 필요하다. 공급자 문서의 '일반 Chat' 기능으로 환산하면 안 된다.
- **Bootstrap 함의:** 작업 수행을 Search가 맡는지 Computer가 맡는지 먼저 식별한다. durable files·커넥터·local folder에 대한 접근은 해당 task 및 계정의 실제 설정으로 확인한다.

공식 근거: [Perplexity Computer](https://www.perplexity.ai/products/computer), [시작 안내·Skills·connectors](https://www.perplexity.ai/en-GB/hub/getting-started), [Projects persistent filesystem](https://www.perplexity.ai/en-GB/hub/products/projects), [Personal Computer 설치·권한](https://www.perplexity.ai/personal-computer-setup).

## 6. Grok (xAI)

- **Grok 일반 Chat:** 파일 업로드, 이미지·비디오 생성, 음성, 이메일·드라이브·캘린더 connectors 및 custom remote MCP 도구가 공식 문서에 제시된다. custom MCP는 접근 가능한 외부 URL과 인증이 필요하다.
- **Grok Bot:** 별도 agent surface로, 영속 클라우드 컴퓨터에 browser·파일시스템·terminal이 있다. 백그라운드 작업, Bot 간 협업, 학습한 작업의 일정 재실행을 지원한다. 공식 문서상 같은 계정 내 Bot들이 클라우드 컴퓨터·파일·로그인을 **공유**하므로 Bot 간 격리된 자격 증명이라고 간주하면 안 된다.
- **Bootstrap 함의:** 일반 Grok 대화에 Bot의 shell 권한이 있다고 전제하지 않는다. Bot의 계정·공유 컴퓨터에 남는 작업을 하려면 권한과 side effect를 별도로 확인한다.

공식 근거: [Grok Chat](https://docs.x.ai/grok/overview), [Connectors·MCP](https://docs.x.ai/grok/connectors), [Grok Bot 컴퓨터·지속 작업](https://docs.x.ai/grok-bot/overview), [Bot 승인과 공유 경계](https://docs.x.ai/grok-bot/approvals-security-and-privacy).

## 7. Poe (Quora)

- **일반 Prompt Bot:** 기반 모델과 프롬프트로 구성되는 채팅 경험이며 사용자 요청 시 임의 Python/shell이 제공된다고 가정할 수 없다.
- **Script Bot:** Bot **작성자**가 Poe 호스팅 Python 3.11 Linux sandbox로 여러 모델 호출과 사용자 정의 로직을 구성한다. 각 실행마다 새 컨테이너가 생성되어 상태가 지속되지 않는다. 기본 Full Shield에서는 직접 외부 HTTP가 차단되고 허용된 Poe Bot 호출·CDN 경로를 사용하며, Half Shield에서 네트워크 범위가 달라진다.
- **Server Bot / API Bot:** 개발자가 외부 서버·엔드포인트를 제공하는 별도 제품 형태다. 도구 호출이 지원되어도 모델이 코드를 직접 실행한 것이 아니라 외부 서버가 수행한 것이다.
- **Bootstrap 함의:** Poe 사용자 채팅, Poe가 호스팅하는 Script Bot 실행, 개발자 Server Bot의 코드를 서로 다른 trust/runtime boundary로 취급한다. 해당 Bot에 실제로 연결된 capability만 활용한다.

공식 근거: [Bot 유형](https://creator.poe.com/docs), [Script Bot](https://creator.poe.com/docs/script-bots/quick-start), [Script Bot sandbox·네트워크](https://creator.poe.com/docs/script-bots/limitations), [Server Bot function calling](https://creator.poe.com/docs/server-bots/function-calling).

## `mols-chatbot-bootstrap` 설계에 반영할 운영 판단

1. **실제 capability 확인:** 플랫폼/모드/클라이언트 → 현재 노출된 도구와 설치된 커넥터 → 현재 연결 계정·권한 → 코드 실행 시 sandbox/네트워크/FS 조건을 **작업과 관련 있는 범위에서만** 확인한다. 전체 서비스 기능표를 매 실행 시 로드하지 않는다.
2. **최소 first-hop:** native instruction/Skill discovery가 충분하면 no-op. 부족하면 런타임이 실제로 읽는 확실한 instruction surface에서 대상 repository entrypoint를 연결한다. 외부 UI 권한을 임의 확보하지 않는다.
3. **선택적 route와 실제 body:** 관련 경로·작업을 토대로 route metadata를 좁힌 다음, 선택한 Skill·Rule·Subagent의 canonical source를 실제로 읽는다. 조건부 reference는 필요할 때만 로드한다. **메타데이터 접근 ≠ 본문 적용**이다.
4. **도구 대체 범위:** CLI가 없더라도 안전한 Python/JS 환경에서 원본 코드의 일부를 실행할 수 있는지 검토하되 sandbox의 네트워크·권한을 우회하지 않는다. connector가 있다면 이미 제공된 직접 API 연동부터 활용한다. 실제 subagent가 없다면 순차적 역할 검토와 독립 실행을 명확히 구분한다.
5. **계정·쓰기 안전:** 도구가 하나 이상 여러 계정과 연결될 수 있어도 작업 대상에 승인된 계정만 사용한다. 계정 전환·로그인·권한 요청·외부 기록을 도구 존재만으로 승인된 것으로 판단하지 않는다.
6. **평가의 3단계:** (a) 필요 자산 선택 및 불필요한 선로드 방지, (b) canonical source 실제 열람, (c) 해당 작업에 계약 적용. 실제 런타임 관찰 없이 정적 경로 검증만으로 end-to-end 성공을 주장하지 않는다.
7. **확인할 때만 최신 문서 재조회:** 서비스 기능은 변경이 잦다. 구체적 도구 선택이나 특정 권한에 대한 판단이 필요할 때 해당 공급자의 공식 문서를 다시 확인한다. 요금제별 고정 숫자·지원 목록을 Skill의 보편 계약으로 복제하지 않는다.

## 대표적인 false assumptions

| 잘못된 추론 | 올바른 확인 |
| --- | --- |
| 파일을 업로드할 수 있다 → 저장소 전체를 탐색할 수 있다 | 업로드된 snapshot만인지, 경로/branch/ref를 선택해 최신 파일을 읽을 수 있는지 확인 |
| 검색·웹 브라우징 가능 → shell의 임의 HTTP 요청도 가능 | 웹 도구와 코드 sandbox의 network egress를 따로 검증 |
| GitHub 연결됨 → PR·커밋 쓰기 가능 | 앱별 실제 action 목록·읽기/쓰기 권한 확인 |
| 모델이 Python 코드를 작성함 → 실제 실행됨 | 실행 도구·결과·파일 생성 관찰 |
| Skills 디렉터리 표시 → 해당 Skill을 로드함 | source의 실제 본문과 사용된 revision 확인 |
| Bot이나 agent가 여럿 있음 → 각각 독립 계정·격리 환경 | 공유 파일·세션·자격 증명과 실행 표면 검토 |
| 예약 기능 있음 → 현재 대화가 백그라운드 실행됨 | 별도의 예약 작업 생성·설정·결과 확인 |
| 한 공급자의 API/CLI 기능 있음 → 웹 Chat도 지원 | 제품 모드별 tool surface 재확인 |

## 근거 수준과 후속 조사

- **확인됨:** 각 공급자의 공식 문서에서 해당 제품 모드의 기능 및 제약을 확인했다.
- **미검증:** 개별 계정에서 기능 활성화 상태, 유효한 인증 범위, 실제 파일 열람·코드 실행·브라우저 조작 성공, 모델별 routing fidelity.
- **업데이트 권장:** 빠르게 변하는 Gemini Tasks/Skills, Copilot browser, Grok Bot, Claude Cowork와 ChatGPT Work는 실제 적용 시 공식 문서와 활성 tool inventory를 재검토한다.
- **후속 실험 최소셋:** 서로 다른 capability profile 세 가지로 fixture를 구성한다: (1) Web read만, (2) read connector + 격리 Python, (3) connector + 브라우저/컴퓨터 조작. 각 프로필에서 task-relevant canonical Skill body를 실제로 읽고 적용하는지와 불필요한 본문 선로드가 없는지를 확인한다. 추가 service-specific fixture는 관찰된 실패가 있을 때만 만든다.

이 문서는 **변경 가능한 외부 서비스 조사 결과**다. 지속적으로 지켜야 할 범용 행동 계약만 검토를 거쳐 `mols-chatbot-bootstrap`의 canonical Skill 및 해당 maintainer 문서로 승격하고, 제품별 요금제·UI 옵션은 이 조사 기록에 남긴다.
