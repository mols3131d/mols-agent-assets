# Chatbot Continuity — PR #260 개선 검토

## 변경 이유

기존 `mols-chatbot-continuity-design`은 예약 기능의 종류와 설계 단계는 열거했지만 **실행마다 무엇을 읽고, 압축하고, 재개할지**가 구체적이지 않았다. 프롬프트에 도구·안전 규칙·작업 내역을 계속 누적하면 재탐색·컨텍스트 오염·오래된 근거 재사용 위험이 생긴다.

## 선택한 설계

- Skill 이름을 `mols-chatbot-continuity`로 통일했다. 이 Skill은 예약 작업의 **실행 간 연속성 설계·설정**을 소유한다. 작업 안의 RPI는 `mols-loops`, GitHub 사실 확인은 `github-context`와 해당 도구의 책임을 유지한다.
- **네이티브 기능 우선**: 각 챗봇 서비스/계정/모드의 실제 스케줄·이벤트·연결 앱·권한을 확인하고 최소 구성만 제안한다. 4시간 운영 기간과 단일 실행 시간을 혼동하지 않는다.
- **컨텍스트 세 층**: (1) 안정적 목표/지침은 원본 참조, (2) 현재 진척은 live 대상과 revision, (3) 파일·diff·CI 등 작업별 근거는 필요할 때만 로드한다.
- **재개**: 매 실행 최신 상태를 확인하고 오래된 handoff를 재검증한다. 기존 PR/Issue 등 지속 표면에 기준점·변화·검증·차단·다음 시작점만 갱신한다. 전문 대화·로그·지침 복제, 임의 DB/데몬은 기본값으로 두지 않는다.
- **프롬프트 최소화**: 목표·상태 위치·작업/검증·권한·종료/인계만 담는다. 새 오케스트레이터는 복잡성과 이점이 입증될 때만 만든다.
- **대상**: `agentsskills`로 ChatGPT 소비를 지원하며 다른 챗봇 플랫폼의 호환성을 사실처럼 선언하지 않는다.

## 다관점 정적 검토

| 관점 | 기존 문제 | 개선 결과 |
| --- | --- | --- |
| Responsibility | 예약과 작업 내부 루프가 겹쳐 보임 | 트리거·실행·지속 상태의 owner 분리 |
| Context/efficiency | 실행 전 광범위한 capability 확인·전체 과거 context 로드 위험 | 결정에 필요한 capability만 검증, 세 층 기반 선택적 로드 |
| Continuation | '최소 상태'라고만 쓰고 재개 진실성 불명확 | live revision 대조, 동일 변경 중복 방지, 작은 checkpoint |
| Authority/safety | 승인·연속 실행 지원을 과신할 위험 | 실제 지원 여부와 설정 결과 검증, 승인 대기 시 중지 |
| Portability | 호스트별 지원 차이를 흐릴 위험 | portable 목적 + 런타임 live 확인 |

별도 reference/스크립트/DB를 신설하지 않았다. 이는 책임과 로딩 타이밍이 분리될 실질 이점이 입증되지 않았기 때문이다.

## 평가·검증 경계

- Canonical: `src/rulesync/.rulesync/skills/mols-chatbot-continuity/SKILL.md`
- Eval: `evals/skills/mols-chatbot-continuity/cases.json` — 기존 8개를 이름 변경 후 유지하고, context 선택 로드·stale handoff·단순 예약·프로젝트 파일 접근에 관한 4개를 추가.
- 파생 route: `route/skills.jsonl` — 공식 생성기의 name/description/source 형태에 맞춰 변경.
- 공식 참고: [ChatGPT Scheduled Tasks](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt), [ChatGPT Work](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex).
- 설계 참고: `mols-agent-asset`, `mols-documentation`, `mols-text-optimizer`의 뜻 보존·중복 축소 원칙, `catalog/patterns/context-engineering/progressive-context-routing.md`, `catalog/patterns/workflow/durable-progress-handoff.md`.
- 정적 내용 검토는 실제 행동 시험이 아니다. GitHub PR Gate 결과와 ChatGPT 예약 작업 실험을 별도로 구분해 기록한다. 사용자의 예약 작업은 이번 변경에서 생성하지 않는다.

## 다음 검증

1. PR Gate의 Rulesync·route drift·테스트 확인.
2. 실제 ChatGPT에서 예약 모드 + GitHub 앱의 접근/승인/중복 실행 동작을 작은 시험으로 평가(미수행).
3. Model/runtime eval은 `cases.json`의 positive/negative/behavior 사례를 대상으로 별도 실행(미수행).
