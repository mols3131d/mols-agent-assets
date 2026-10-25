# Chatbot Continuity Design — 조사·설계·리뷰

## 목표

ChatGPT 같은 챗봇의 네이티브 예약·이벤트·모니터링 기능을 먼저 활용하고, 프롬프트·실행 워크플로우·오케스트레이션·재개 루프를 **필요할 때만** 생성하는 Chatbot 중심 Skill을 도입한다. 사용자가 실제 예약 설정을 요청하지 않은 상황에서 자동화를 무단으로 활성화하지 않는다.

- PR: https://github.com/mols3131d/mols-agent-assets/pull/260
- Base: `b29aa490d0c251d5ca478fa5c787b90258f09d79`
- Canonical: `src/rulesync/.rulesync/skills/mols-chatbot-continuity-design/SKILL.md`
- Eval fixture: `evals/skills/mols-chatbot-continuity-design/cases.json`
- Derived discovery: `route/skills.jsonl`

## Research — 확인한 기능과 결정적 제약

1. **ChatGPT Scheduled Tasks**는 호스트의 지원 범위에서 일회성/반복 작업, 조건부 모니터링과 이벤트 기반 트리거를 제공한다. GitHub는 연결된 앱 후보이며, 승인 필요한 쓰기 동작은 작업을 중단시킬 수 있다. 이벤트 기반 GitHub 작업은 지원하는 PR 이벤트·Work 사용 조건·계정 권한에 의존한다. 프로젝트에서 예약 작업을 만들더라도 해당 프로젝트의 업로드 파일/프로젝트 파일에 접근할 수 없는 제약이 있다. 정확한 계정별 지원 여부는 실제 작업 생성 화면/도구로 확인해야 한다. 근거: https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
2. **ChatGPT Work**는 클라우드 브라우저와 연결 앱으로 장시간 작업이 가능하지만, 확인·로그인·승인이 필요하면 일시 중지될 수 있다. 단일 예약 실행에 4시간 연속 작업 보장은 없다. 근거: https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt 및 https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
3. 프로젝트의 `github-context`는 GitHub 객체의 최신 상태/적용 지침을 읽는 역할, `mols-loops`는 한 Run 내부의 RPI orchestration 역할을 맡는다. 예약 주기와 각 실행 간 continuation은 이 둘의 기본 책임이 아니다.
4. `catalog/patterns/workflow/durable-progress-handoff.md`는 소량의 이어받기 상태를 지속성 있는 기존 표면에 남기는 패턴을 제공한다. `chatbot-driven-development.md`는 목표 구체화·Work·검증을 연결하지만 실제 예약 실행 기능은 소유하지 않는다.

## Plan / 설계 결정

- **새 책임**: 제품별로 존재하는 지속 실행/스케줄/이벤트 기능을 찾아, 사용자의 작업을 그 호스트에서 실제로 가능한 유한 실행으로 조합하는 **설계·구성 Skill**.
- **적용 대상**: ChatGPT 호환 Skill discovery를 위한 `agentsskills` target. 다른 챗봇 서비스의 구현 여부는 별도 검증 없이 선언하지 않는다. 본문은 특정 서비스에 고정된 API나 요금제 수치를 복제하지 않는다.
- **최소 단위**: 단일 `SKILL.md`로 유지. 별도 스크립트·스케줄러·상태 저장소·대형 템플릿을 생성하지 않는다.
- **실행 책임 분리**: 실행 트리거/반복 = 호스트, 실행 안의 문제 해결 = 해당 도메인 Skill/agent, session 간 진척 = 기존 지속 표면.
- **운영 경계**: 시간·빈도와 단일 실행 지속 시간을 구분. 이미 처리된 PR/Issue/revision 식별, 작업 완료 시 중지, 승인 대기 시 보류, 예약 미생성 시 상태를 성공으로 표현하지 않음.
- **기본 결과**: 네이티브 실행 방식과 즉시 활용 가능한 실행 프롬프트, 필요한 경우 워크플로우/큐, 미해결 설정 조건을 제시. 실제 등록은 사용자가 요청하고 도구 권한이 확인된 경우에만.

## 예시 — ChatGPT + GitHub PR 반복 업무

예시 입력: "매일 새벽 2시에 PR #260 상태를 확인하고, 진행 가능한 보완을 남겨 줘. 병합하지 마."

기대한 생성물:

> ChatGPT의 해당 계정에서 지원되는 예약 작업 또는 GitHub PR 이벤트 트리거를 확인한다. 매 실행 시 PR #260의 최신 head SHA, 리뷰와 CI 상태를 GitHub 연결을 통해 확인한다. 이미 처리한 head나 동일한 blocker를 중복 코멘트하지 않는다. 허용된 범위에서 검토·수정 제안을 진행하되, 위험한 쓰기·새 권한·병합은 사용자 승인을 요구한다. 처리한 revision, 검증 결과와 다음 작업을 PR 또는 기존 인계 표면에 남긴다. PR이 완료·닫힘·차단되면 무리하게 반복하지 않고 종료·보류 상태를 보고한다.

이 문구는 **설계된 예시 프롬프트**이며 실제 Scheduled Task 생성 또는 실행 근거가 아니다.

## Review — 정적 관점 검토

| 관점 | 확인 내용 | 판정 |
| --- | --- | --- |
| 책임·중복 | 내부 RPI 알고리즘과 GitHub 도메인 작업을 재구현하지 않음 | 설계상 적합 |
| 실행 가능성 | 실제 서비스·플랜·도구 권한 확인 전 활성화 성공을 주장하지 않음 | 설계상 적합 |
| 효율 | 단일 Skill, 호스트 네이티브 우선, 외부 실행기 기본값 배제 | 설계상 적합 |
| 안정성 | 중복 실행·경합·승인·시간 제한·조기 종료를 명시 | 설계상 적합 |
| 이식성 | 보편적 책임과 서비스별 가변 기능을 분리 | 제한부 적합 |
| 행동 근거 | 실제 예약 트리거 및 GitHub 쓰기 권한으로 실행하지 않음 | 미검증 |

**보완 필요 / 의도된 경계**

- 특정 호스트의 스케줄링 지원과 도구 권한은 제품·계정에서 변할 수 있으므로 Skill에 고정된 기능 목록을 박지 않았다.
- `agentsskills` target은 ChatGPT 소비자에 맞춘 것이지 타 서비스의 호환성을 입증하지 않는다.
- 동작 eval은 `evals/skills/mols-chatbot-continuity-design/cases.json`의 긍정/부정 활성화와 4시간 연속 실행 착각, 승인·중복 실행·미지원 예약 등 8개 시나리오로 제시했다. **모델 trial은 아직 실행하지 않았다.**

## 검증과 인계

- ✅ GitHub branch와 draft PR 생성, canonical Skill 및 8개 eval fixture 저장.
- ⚪ `route/skills.jsonl`은 기존 생성기의 행 형식·정렬 규칙에 맞춰 갱신했으나, 공식 `mise run generated-sync` 실행과 drift check는 아직 미수행.
- ⚪ `npm run rulesync:validate`, local model eval 미수행.
- ⚪ ChatGPT의 실제 예약 작업 생성/자동 재개/GitHub mutation 테스트 미수행.

다음 단계: PR CI 결과 확인 → 필요한 수정 → 로컬 Rulesync / behavioral eval로 실제 runtime 근거 확보 → ChatGPT Scheduled의 제한된 계정 환경에서 수동 승인한 smoke 시험. **사용자 승인 없는 자동 예약 활성화·PR 병합은 범위 밖.**
