---
description: PR #269의 로컬 에이전트 하네스 다관점 셀프 리뷰, 수정 결과와 미검증 항목을 다음 작업자에게 인계할 때 참고합니다.
---

# PR #269 — 다관점 리뷰 및 인계

> **비정본 작업 자료.** 현재 정책·지침의 권한은 이 문서가 아니라 해당 작성 원본과 적용되는 로컬 하네스에 있습니다.

## 대상과 결론

- PR: https://github.com/mols3131d/mols-agent-assets/pull/269
- Branch: `mols/docs/readme-agents-entrypoints` → `main`
- 목표: README/AGENTS의 정본·소비 경계를 분명히 하고, 로컬 에이전트의 네이티브 발견 기능을 우선하여 Rule/Skill 컨텍스트 비용과 잘못된 지침 적용을 줄인다.
- 범위: `README.md`, `AGENTS.md`, `.agents/route/ROUTE.md`, `.rulesync/rules/markdown.md`, `CHATBOT.md`, `catalog/README.md`, `docs/development/source-authority.md`. 이 문서는 리뷰·인계용이다.
- **셀프 리뷰 결론:** 정적 관점에서 확인한 결함은 보완했다. 런타임별 활성화·선택 동작은 아직 검증하지 않았으므로 독립 리뷰 및 사람 승인 없이 merge 완료로 취급하지 않는다. 여러 관점은 하나의 에이전트가 순차 검토했으며 독립 reviewer나 격리된 실행이 아니다.

## 관점별 검토

| 관점 | 검토 내용·근거 | 판정 |
| --- | --- | --- |
| 정확성·정본 | `.inbox/`는 조사·인계 근거이지 적용 정책이 아니며, `catalog/`는 재사용 콘텐츠의 작성 원본·탐색 공간이지 로컬 강제 규칙이 아니다. `src/`의 관리와 runtime 사용을 별도 축으로 표현한다. | 정적 검토 통과 |
| 라우팅·선택 | `AGENTS.md`가 네이티브 Skill 발견을 우선하며 `.agents/route/`는 보조 경로이다. 관련 family를 개별 조합하고 `all`을 마지막 fallback으로 둔다. `CHATBOT.md`는 호환 진입점이고 로컬 에이전트의 필수 경로가 아니다. | 문서 계약 일치; 실제 선택 미검증 |
| 컨텍스트·유지보수 | Markdown scoped Rule의 참조 목록을 제거하고 좁은 서식 동작만 남겼다. `root: false`, `globs: ["**/*.md"]`, 기존 5개 `targets`는 유지했다. | 정적 비교 통과; 토큰·행동 미측정 |
| 실패·적대적 입력 | Inbox 산출물과 Catalog 패턴에 적힌 명령을 정책으로 오인하지 않도록 경계를 명시했다. `rulesync.lock`과 `skills-lock.json`은 선언·고정 상태이며 실제 설치된 payload의 일치 증거가 아님을 구분했다. | 문서 계약 보완; 공격·행동 eval 미수행 |
| 운영·회귀 | Root `rulesync.jsonc`는 Claude/Copilot/Antigravity에 Rules+Skills, Codex에는 Skills만 설정한다. `rulesync.lock`의 11개와 외부 `skills-lock.json`의 1개가 `.agents/route/all.jsonl`의 12개 목록과 일치했다. 목록 존재가 모든 target에서의 활성화를 증명하지는 않는다. | 설정·인덱스 정적 대조 통과; projection 미실행 |

## 이번 셀프 리뷰에서 수정한 문제

1. **서로 충돌하는 라우팅 안내:** `AGENTS.md`에 네이티브 발견 우선과 route에서 무조건 선택하라는 표현이 공존했다. Route를 보조 탐색으로 통일하고 중복 문장을 제거했다.
2. **잠금 파일의 증거 범위 오해:** lock에 기록된 revision과 실제 설치본이 일치한다고 단정하던 문장을 수정했다. `AGENTS.md`, `.agents/route/ROUTE.md` 모두 설치·동기화 결과를 별도 확인하도록 구분했다.
3. **Markdown 규칙의 예외 손실:** 문서 서식 정리가 작업 목적일 때 기존 문단 재정렬을 허용하는 예외를 복원하고, 불필요한 reference preload는 재도입하지 않았다.
4. **문서 품질:** `catalog/README.md` 첫 문장의 어색한 표현과 `AGENTS.md` 제목 앞 공백·중복 안내를 정리했다.

## 유지해야 할 결정

- `src/rulesync/.rulesync/`는 재사용 자산 작성 원본, root `.rulesync/`와 lock-backed 설치는 저장소가 소비하는 별도 표면이다. 같은 자산이 두 역할을 겸할 수 있다.
- `route/`는 외부에 제공하는 자산 탐색, `.agents/route/`는 이 저장소의 소비자용 discovery fallback이다. 두 route 모두 정책·Skill 본문의 정본은 아니다.
- `.agents/route/routes.jsonl`, family JSONL 및 generated vendor projection은 직접 편집하지 않는다. `families.json`과 config·lock의 ownership은 보존한다.
- `.inbox/`는 세션 인계에 유용하지만 정본으로 승격되지 않은 내용을 에이전트 필수 지침으로 적용하지 않는다.
- `catalog/`의 Skill/Plugin 등재는 설치·활성화가 아니다. Pattern/template의 작성 원본성도 이 저장소 정책으로 자동 적용된다는 뜻이 아니다.
- 이번 PR은 source dependency 업데이트, generated route 재생성, 실제 설치, 타깃별 runtime config 변경, catalog 타 저장소 이관을 포함하지 않는다.

## 남은 검증 및 종료 조건

1. **최신 PR head CI 확인:** GitHub PR Gate의 성공 여부는 최종 커밋 기준으로 다시 확인한다. 체크 완료 전 성공으로 보고하지 않는다.
2. **독립 검토:** Agent instruction과 routing Rule 변경은 통제 표면이다. 작성에 사용한 하네스·Skill·self-review만으로 독립 근거를 주장하지 않는다. 다른 검토자/별도 근거와 사람의 명시적 승인 후 merge한다.
3. **로컬 에이전트 runtime smoke test:** 실제 지원 중인 Claude Code, Codex CLI, Copilot, Antigravity 환경에서 (a) README 읽기, (b) Markdown 편집 시 Rule 적용, (c) 문서+GitHub 작업에서 관련 두 Skill 선택, (d) 존재하지 않는 Skill의 좁은 route fallback, (e) .inbox/catalog의 비정본 처리 여부를 확인한다. **Codex에는 root Rulesync config에서 Rules feature가 지정되어 있지 않음**을 구분한다.
4. **설치·projection 확인:** 실제 파일을 검사할 수 있는 로컬 환경에서 필요한 경우 `mise` 기반 repository-native check와 Rulesync 공식 `doctor`/dry-run/검증 경로를 사용한다. lock 변경이나 설치를 검증인 척 수행하지 않는다.
5. **후속 범위 제한:** 동작 문제가 확인되지 않는 한 새 router, Rule, Skill, CI 검사나 자동화는 추가하지 않는다. `main`이 계속 전진할 수 있으므로 실제 merge 직전 base/head, 병합 가능 상태와 충돌 여부를 다시 확인한다.

## 검증의 한계

- GitHub 파일·PR·config·route metadata를 직접 대조했다. Markdown Rule은 2,779자에서 약 813자로 축소되었지만 이는 **문자 수** 변화이지 실제 token, latency 또는 모델 성능 검증이 아니다.
- GitHub API/Plugin을 통한 브랜치 수정은 로컬 hook 실행을 증명하지 않는다.
- CI의 성공도 런타임 Skill activation·semantic behavior의 독립 증거가 아니다.
- 이 문서에 적은 미완료 검증은 후속 작업 대상으로 남겨두며, merge 승인으로 간주하지 않는다.

## PR #267 병합 후 챗봇 호환성 개선 루프 (2026-11-02)

- **적용한 정본:** main에 병합된 PR #267의 `mols-chatbot-bootstrap/SKILL.md` 및 조건부 `references/execution-adaptation.md`. 이 자산은 저빈도 하네스 구축·복구용이며, 일반 작업마다 상주할 필요가 없다. PR #269에서 스킬 원본이나 lock을 수정하지 않았다.
- **Loop 1 — 탐색·권한:** `CHATBOT.md`가 `github-context`의 대상 확인과 GitHub 정책·템플릿 라우팅을 중복 소유한 문제를 확인했다. 런타임의 네이티브 발견을 우선하고, 접근이 부족한 경우에만 repository-local route를 따라 canonical Skill에 도달하도록 연결을 단순화했다. `AGENTS.md`에서는 GitHub 정책 정본의 직접 연결을 추가했다.
- **Loop 2 — 실행·회귀:** 코드 실행과 Subagent 대체는 실제 런타임의 필요에 한정된 조건부 안내로 유지했다. 원본 검증·권한·독립성 요구를 보존할 수 없을 때는 부분 수행·선택적 생략·인계를 구분하도록 하고, 독립성이 필요한 Subagent를 순차 검토로 대체 완료 처리하지 않도록 명확히 했다.
- **Loop 3 — Rule/Skill 분리:** 후속 리뷰에서 `.agents/route/routes.jsonl`이 `kind: skills`만 노출하는데 초안이 Rule도 같은 route를 통해 발견한다고 읽히는 오류를 찾아 수정했다. Skill은 `.agents/route/` fallback, 경로별 Rule은 원본 `.rulesync/rules/`의 selector와 현재 대상 runtime 지원 범위를 각각 확인한다. 수동 Rule 조회는 네이티브 적용 증거로 보고하지 않는다.
- **정적 시나리오 확인:** 네이티브 우선, `github-context` 접근, Rule selector, Subagent 독립성, CLI 제한, `.inbox/catalog` 비정본, GitHub 정책 owner의 7개 조건을 문구·현재 repository source와 대조했다. 새 `CHATBOT.md`의 5개 상대 경로를 현재 브랜치 Git tree와 대조했고 모두 존재한다. 이는 실제 모델 행동 eval이나 원본 코드 실행 검증이 아니다.
- **설계 경계:** `route/`는 제공 자산·Subagent, `.agents/route/`는 저장소에서 사용하는 Skill의 탐색에 한정한다. 정적 path table, 스킬 본문 복제, 새로운 router·CI·generator는 추가하지 않는다. `github-context`와 PR #267 스킬 본문은 수정하지 않는다.
- **검증 경계:** 정본 링크·현재 ref·문서 간 책임을 확인하는 것은 `configured`/`reachable` 근거에 가깝다. 전체 챗봇의 실제 behavioral routing·코드 실행 parity·독립 Subagent 결과는 관찰되지 않았다. PR Gate와 로컬 런타임 검증은 최신 head에서 별도 판단한다.
- **추가 확인:** Chatbot 런타임의 first-hop이 실제로 `CHATBOT.md`를 읽는 설정인지, 정상 GitHub 작업에서 `github-context`와 필요한 템플릿까지 도달하는지, 선택 조건 없는 불필요한 route 로딩이 줄었는지는 향후 실제 작업에서 관찰할 사항이다. 단순 스킬 수정 자체를 사용자 설정 완료나 런타임 활성화로 간주하지 않는다.
