# PR #271 — 검증·도그푸딩 계획

검증 수준을 **형식/정적 검증**, **설계·의미 검토**, **실제 Chat 동작 평가**로 구분한다. 앞 단계 통과를 다음 단계 성공으로 해석하지 않는다.

## 정적 검증

- `SKILL.md`의 name/description과 패키지 구조가 대상에 적용되는 Agent Skills 규격을 충족하는가?
- Chat 전용 신규·이식·유지보수 요청을 activation metadata가 포착하고 일반 Chat 사용·범용 자산 개발·하네스 구축을 잘 배제하는가?
- 유지보수 문서·디렉터리 README의 링크가 실제 경로를 가리키는가?
- 정본 소유권, 범위, 관리/설치 상태와 원격 권한 경계가 혼동되지 않는가?
- `#270`을 base로 할 때 본 PR에는 실제 작업 관련 파일만 남아 있는가?

## Routing/behavior 시나리오

| 사례 | 기대 판단·행동 | 현재 검증 |
| --- | --- | --- |
| "ChatGPT Chat 모드 전용 스킬을 만들어줘" | Chat consumer 계약 및 최소 Skill 원본 선택 | 미실행 |
| "기존 범용 Rule을 Chat Project instructions로 옮겨줘" | selector/상시 적용 차이를 드러내고 가능한 delta만 작성 | 미실행 |
| "Chat의 GitHub Plugin으로 동작하는 Skill을 설계해줘" | 설치/연결 identity, 액션·권한 탐색 후 필요한 텍스트/도구 분리 | 미실행 |
| "Codex CLI용 범용 Skill을 설계해줘" | 이 Skill 대신 범용 자산 제작으로 분리 | 미실행 |
| "ChatGPT 하네스 진입점부터 구축해줘" | `mols-chatbot-bootstrap` owner로 분리 | 미실행 |
| "독립 Subagent를 Chat에서 같은 권한으로 실행해줘" | 권한·격리 부재를 확인하고 동등 실행 주장 금지 | 미실행 |
| "Skill 파일을 GitHub에 작성했으니 설치됐지?" | 작성과 실제 설치·자동 선택의 차이를 보고 | 미실행 |
| "Chat Skill을 수정했는데 선택이 안 돼" | 원본·소비 경로·설치·activation을 단계별 진단 | 미실행 |

## 실행 방법과 완료 조건

실행 가능한 도구가 있으면 공식 validator를 재사용한다. 실제 Chat Skills가 지원되는 계정/워크스페이스에서는 설치 후 스킬을 지목하지 않은 요청의 선택률, 원본 리소스 로딩, 도구 권한 경계와 대표 결과를 비교한다. Chat 실행이 불가능하면 시나리오는 **static/simulated**만으로 보고하고, 수행하지 않은 CI/런타임 Eval은 `not verified`로 남긴다.

수정·평가가 끝나면 PR 본문은 해당 시점의 정확한 diff pair와 근거만 반영한다. 새 과제는 실제 결함과 사용자 목표에 관련될 때만 추가한다.

## 2026-11-02 정적 리뷰 기록

- ✅ 공식 Chat Skills 지원 대상(적격 Business/Enterprise/Healthcare/Edu), Plugin과 별도 provider 권한을 문서와 비교하고 범용 설치 가정을 제거.
- ✅ 기존 Skill 원본의 activation/owner 경계와 native 도구 재사용·부분 수행·인계 판단을 정적 점검. 이는 실행 Eval이 아님.
- ✅ 최신 #270에 추가된 OpenSpec 유지보수 문서·README 변경을 보존하는 비강제 병합을 수행.
- ⚪ 공식 `skills-ref validate` CLI, 저장소 CI, 실제 Chat 설치·암묵 라우팅·도구 호출은 이 세션에서 미실행.
