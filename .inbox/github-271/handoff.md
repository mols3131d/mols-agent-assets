# PR #271 — ChatGPT Chat Agent Asset Skill Handoff

## 목표와 작업 경계

ChatGPT **Chat 모드**용 Agent Asset을 새로 작성하거나 기존 Rule·Skill·Subagent·워크플로를 Chat에 맞게 튜닝·검토·유지보수하는 `mols-chatgpt-chat-asset`을 개선한다. 일반적인 자산 제작 방법론을 다시 만들지 않고, **Chat 소비 표면·도구·권한·실제 설치와 호출**에 필요한 차이만 소유한다.

- 대상 PR: [#271](https://github.com/mols3131d/mols-agent-assets/pull/271) (Draft)
- Head: `mols/feat/chatgpt-chat-asset-authoring`
- Base: `mols/feat/chatgpt-openspec-cli-compat` ([#270](https://github.com/mols3131d/mols-agent-assets/pull/270)). Stacked PR이며 **#270 통합 전 #271을 main 대상으로 합치지 않는다**.
- 현재 작성 원본: `src/.openai-chatgpt-chat/skills/mols-chatgpt-chat-asset/SKILL.md`
- Maintainer 문서: `docs/skills/mols-chatgpt-chat-asset/README.md`
- 탐색 안내: `src/.openai-chatgpt-chat/README.md`

## 현재 완료된 범위

선택적인 Chat 전용 자산 작성·튜닝·관리 Skill과 유지보수 문서의 초안이 존재한다. `Skill`, `Project instructions`, `Plugin`/연결 앱 등 소비 표면을 사용자 목표에 따라 구분하며, 범용 `mols-agent-asset`과 하네스 구축 `mols-chatbot-bootstrap`의 책임을 복제하지 않도록 설계했다. 정적 frontmatter·링크·변경 파일 범위는 점검했지만 실제 Chat 설치·자동 선택·행동 평가와 공식 validator는 **미검증** 상태다.

## 다음 작업 순서

1. **기준 확인** — 두 PR의 현재 base/head, 실제 branch diff, README 링크를 먼저 재확인한다. #270의 head가 이동했으면 #271이 자동으로 최신 코드를 포함한다고 가정하지 않는다. 충돌 여부와 필요한 동기화는 별도 명시적으로 수행한다.
2. **공식 타깃 계약 재검증** — [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [Build skills](https://learn.chatgpt.com/docs/build-skills), [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt), [Agent Skills specification](https://agentskills.io/specification)을 해당 시점에 확인한다. Skill이 모든 플랜에서 네이티브 설치 가능하다고 주장하지 않는다.
3. **설계 리뷰** — Chat-only delta가 정확히 구분되는지, Skill 작성·튜닝과 일반 Chatbot harness 설정·일회성 실행이 겹치지 않는지, Project instructions/Plugin 연결 권한과 Codex/Work 기능을 혼동하지 않는지 검토한다. 이슈가 확인되면 가장 작은 수정으로 반영한다.
4. **검증/평가** — 공식 Skill validator, Markdown 검증, positive/negative/near-miss routing 시나리오, 실제 지원되는 Chat 환경의 설치·선택·도구 호출을 가능한 범위에서 실행한다. 불가능한 검증은 미수행으로 명시한다.
5. **PR 마무리** — Review에 필요한 관찰 결과, 남은 위험, `revision.base`/`revision.head`를 현행화한다. #270이 머지되면 그 후 #271의 base를 `main`으로 이동하되 파일 범위와 history 중복을 확인한다. 머지는 별도 명시적 승인 및 required gate 이후에만 한다.

## 반드시 보존할 경계

- 이 저장소의 `src/`는 **관리하는 원본**이지 자동 설치된 Chat Skill이 아니다.
- 외부 앱 설치·연결·배포와 원격 변경은 현재 승인된 동일 계정·명의만 사용한다.
- 기존 Rule의 selector, Subagent의 격리·독립성, CLI/Command의 실행을 프롬프트 텍스트만으로 재현했다고 주장하지 않는다.
- `.inbox/`는 작업 인계·근거를 위한 비정본이다. 실행 의미는 canonical `SKILL.md`가 소유한다.
- 새 범용 schema/generator/CI를 먼저 만들지 않는다. 이미 있는 검사·설치 경로를 재사용한다.

## 2026-11-02 인계 후 갱신

- #270 브랜치 이동을 감지해 구 버전 기준 쓰기를 중단하고 최신 HEAD를 다시 조회했다.
- 새로운 PR #271 commit은 #270 최신 HEAD와 #271 기존 HEAD를 모두 부모로 하는 **비강제 병합**이다. 최신 #270의 OpenSpec 동작과 문서를 유지한다.
- Chat runtime의 실제 Skill/Plugin/연결 도구·계정 권한, source/installed/selected/observed 구분과 공식 지원 계정 조건을 보강했다.
- #271의 review 대상은 Skill·maintainer guide·디렉터리 README·인계 2개 파일이며, inbox는 정본이 아니다.
- 실제 Chat 도그푸딩, 공식 validator 및 CI는 확인된 증거 없이 Pass 처리하지 않는다.
