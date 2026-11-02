# Chatbot Continuity — PR #260 설계·도그푸딩 인계

## 결정

`mols-chatbot-continuity`는 챗봇의 실제 예약/이벤트/모니터링 기능을 이용해 지속 작업을 **설계하고 요청 시 구성**하는 Skill이다. 네이티브 기능을 우선하고, 실행 내부 RPI 및 GitHub 작업 실행은 기존 전문 자산/도구에 맡긴다.

## Reference 분리 검토

기존 `SKILL.md`는 매 실행에 필요한 실행 방식 선택과, 일부 복잡한 작업에서만 필요한 재개·경합 처리 절차를 한 번에 로드했다.

- **본문에 유지**: activation, 호스트 기능 확인, 가장 단순한 네이티브 실행 선택, 얇은 컨텍스트 원칙, 생성할 프롬프트/설정 결과.
- **조건부 reference로 이동**: `references/resumable-work.md`. 같은 목표를 여러 번 이어받는 경우의 지속 표면 선정, live revision 대조, 증분 로딩, 최소 checkpoint, 재시도/중복/경합, 중단.
- **분리하지 않음**: 특정 서비스의 변동 많은 지원 표·API/플랜 목록, 예시 프롬프트 묶음, 일반 GitHub/domain workflow. 관련 official/current authority 또는 기존 domain asset으로 확인한다.

**컨텍스트 효과**: 독립적인 정기 업무에서는 본문만 읽고 끝날 수 있다. 복잡한 다회 실행에서만 추가 reference를 로드한다. 정량 token 절감 수치는 측정하지 않았다.

## 사용·개선 방향

사용자가 별도 behavior eval을 원하지 않으므로 `evals/skills/mols-chatbot-continuity/cases.json`을 PR에서 제거했다. Model trial, eval runner, 새로운 회귀 fixture를 계획하지 않는다. **실제 도그푸딩 피드백**으로 불필요한 로딩·중단/재개 실패·기능 오인 같은 관찰된 문제만 이 Skill에 반영한다.

프로젝트 instruction, 연결 앱 권한, 사용자 승인과 제품 기능은 이 Skill이 새로 정의하지 않는다. ChatGPT 예약/Work 실제 사용 가능 여부는 사용 시 호스트에서 확인한다.

## 검증 및 후속

- Source: `src/rulesync/.rulesync/skills/mols-chatbot-continuity/SKILL.md`
- Conditional: `src/rulesync/.rulesync/skills/mols-chatbot-continuity/references/resumable-work.md`
- Derived discovery: `route/skills.jsonl` — Skill description을 변경했다면 공식 generator drift 확인
- GitHub PR Gate의 소스/파생/Rulesync 구조 검증과 사용자 dogfooding은 구분한다.
- 자동 예약 활성화 및 `main` 병합은 이번 작업에서 하지 않는다.
