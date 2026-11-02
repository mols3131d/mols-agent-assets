---
description: ChatGPT Chat용 OpenSpec CLI 호환 Skill의 설계 근거, 원본 소유권, 배포 조건과 검증 기준을 유지보수할 때 참고합니다.
---

# OpenSpec CLI Compatibility — Maintainer Guide

이 문서는 [`mols-openspec-cli-compat`](../../../src/.openai-chatgpt-chat/skills/mols-openspec-cli-compat/SKILL.md)의 **유지보수 맥락**을 소유한다. 실제 activation과 실행 행동의 정본은 `SKILL.md`이며, 이 문서 자체가 Chat 모드의 지침으로 자동 적용되지는 않는다.

## 목적과 책임 경계

OpenSpec의 CLI 기반 동작을 요구하는 작업에서 ChatGPT Chat 모드가 프로젝트의 로컬 CLI에 접근할 수 없는 경우가 있다. 목표는 CLI를 재구현하거나 성공을 모사하는 것이 아니라, **Chat이 실제 제공하는 도구를 조합하여 가능한 OpenSpec 작업을 완료하고, 재현 불가능한 필수 조건만 정확히 드러내는 것**이다.

- **OpenSpec**: CLI, 스키마, 템플릿, 워크플로·아티팩트 의미의 원본. 프로젝트의 실제 버전을 우선한다.
- **ChatGPT Chat 런타임**: 현재 세션의 도구·연결·승인 범위, Skill 발견과 호출, 실행 가능성.
- **이 Skill**: OpenSpec 요청의 Chat 도구 선택·조합, CLI 의존 단계의 충실도, 검증 근거와 인계.
- **대상 저장소**: Git ref, 프로젝트 정책, OpenSpec 설정과 실제 작업 상태.

범용 챗봇 하네스와 실행 대체 방법은 `mols-chatbot-bootstrap`이, OpenSpec 커스텀 프로파일·스키마의 설계는 `mols-openspec-customize`가 담당한다. 이 Skill은 두 책임을 복제하지 않는다.

## Chat 모드 런타임 조사 (2026-11-02)

공식 문서에서 확인한 기능은 **발견 후보**이지 개별 Chat 세션에 노출된 기능 또는 권한의 증거가 아니다. 계정·요금제·워크스페이스 설정·모드·연결별 권한과 승인에 따라 달라지므로 실행 직전에 관련 기능만 점검한다.

| Surface | 유용한 작업 | 검증·격리 경계 |
| --- | --- | --- |
| Chat의 Skill·Plugin | Chat에 설치된 Skill과 연결 앱 액션으로 OpenSpec 작업을 구성 | 저장소에 `SKILL.md`가 있어도 자동 설치·선택되지 않음; 사용하려면 Chat 호환 플러그인 배포 또는 승인된 별도 로딩 경로 확인 |
| 연결 앱(GitHub 등) | 현재 ref의 파일·PR·커밋·CI 조회와 지원되는 원격 변경 | 도구별 액션, 연결 계정, 실제 provider scope, 워크스페이스/사용자 승인이 서로 다름 |
| Chat Project·첨부 파일 | 프로젝트 지침, 업로드한 config/spec, 지원 앱 소스의 컨텍스트 | 대화에 보이는 파일이 최신 원격 ref와 같거나 remote write 가능한 것은 아님 |
| Python·데이터 분석 | 확보한 입력에서 YAML/JSON 파싱, 결정론적 변환·비교·검사 | Python 분석 환경은 외부 웹/API 요청 불가. 연결 앱과 동일한 작업 디렉터리·파일 상태를 공유한다고 가정하지 않음 |
| 웹 조회 | OpenSpec 공식 CLI·Skills와 버전 민감한 계약 확인 | 공개 upstream 문서는 프로젝트 설치 버전과 로컬 configuration 대신이 아님 |
| 기존 테스트·CI | 이미 실행된 프로젝트 검증 기록을 읽고 결과 재사용 | 정적/의미 검토, Chat의 로컬 테스트, 원본 CLI validation, CI 결과를 구분 |
| 예약 작업 등 | 명시적인 반복·후속 요청과 현재 사용 권한이 맞을 때만 검토 | 일반 OpenSpec 작업이 자동으로 백그라운드에서 계속 실행되는 것은 아님 |

**Chat ≠ Work ≠ Codex.** OpenAI는 Chat을 일반 대화 환경, Work를 별도 브라우저 기반 장기 작업 환경, Codex를 명령·테스트 및 코드 작업 환경으로 구분한다. Work 클라우드 브라우저나 Codex 터미널을 Chat에서 당연히 사용할 수 있다고 가정하지 않는다.

공식 출처: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt), [App permissions](https://help.openai.com/en/articles/20001495-managing-app-permissions-in-chatgpt), [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Data analysis](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt), [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex).

## 작성 원본과 배포

- 작성 원본은 `src/.openai-chatgpt-chat/skills/mols-openspec-cli-compat/SKILL.md` 한 곳이다. Rulesync 작성 원본이나 생성 projection을 추가로 유지하지 않는다.
- `src/.openai-chatgpt-chat/`는 **ChatGPT Chat 전용 원본의 관리 위치**이며, ChatGPT가 자동 탐색하는 네이티브 설치 경로라는 뜻이 아니다.
- OpenAI 공식 [Build skills](https://learn.chatgpt.com/docs/build-skills)에 따르면 웹·데스크톱·모바일 Chat의 재사용 Skill은 플러그인 배포를 통해 제공할 수 있다. 실제 설치·호출은 대상 Chat 환경에서 별도로 확인한다. Codex 또는 ChatGPT Work의 기능을 Chat에 투영해 가정하지 않는다.
- 초안 단계에서는 `SKILL.md`만 배포 가능한 최소 패키지로 유지한다. 반복되는 조건부 자료가 실제로 필요해질 때만 `references/`나 스크립트를 도입한다.

## 설계 결정

0. **OpenSpec 작업 intent에서 활성화.** 기존 초안은 CLI 불가가 확정된 후에만 활성화되는 형태여서 Chat의 파일 조회·분석·PR 작성 역량을 충분히 사용하기 어려웠다. 이번에는 Chat에서 OpenSpec 작업 요청을 처리할 때 적절한 도구 구성과 native/대체 선택을 담당하게 변경한다. native만으로 충분하면 추가 비용 없이 위임한다.
0. **도구 활용이 기본.** 실제 작업에 필요한 연결 저장소 조회 → 분석 환경 또는 직접 작성 → 연결 앱 원격 반영 → readback/diff/기존 CI 확인 순서 중 필요한 단계만 사용한다. Python이 원격 API와 직접 통신하지 못하는 경계를 존중한다.

1. **Native 우선.** 동일 프로젝트 상태에서 진짜 CLI를 실행할 수 있다면 호환 실행을 만들지 않는다.
2. **CLI 계약은 외부 정본.** 명령·옵션과 유효성 규칙을 이 문서에 복제하지 않고 [OpenSpec CLI](https://openspec.dev/docs/cli), [OpenSpec Skills](https://openspec.dev/docs/skills), 실제 프로젝트 버전을 확인한다.
3. **부분 대응의 유용성.** GitHub 연결을 통해 읽기·파일 변경이 가능하더라도 OpenSpec의 `status`, `instructions`, `validate` 의미가 자동으로 재현되지는 않는다. 관찰 가능한 정보와 추론을 분리한다.
4. **쓰기 위험의 비대칭성.** `sync`와 `archive`는 여러 파일과 정본 스펙에 영향을 줄 수 있으므로 읽기 대체보다 강한 증거·복구 경계를 요구한다. 충분하지 않으면 인계한다.
5. **계정과 실행 범위.** 연결 계정을 임의 전환하지 않는다. 프로젝트·ref·명의와 실제 쓰기 권한을 확인하고, 원격 변경 여부를 도구 결과로 확인한다.

## 검토 및 검증 계획

정적 검토는 가능한 실행 경로와 scope 차이를 검토하되, 실제 런타임 실행 성공을 대신하지 않는다. 주요 시나리오는 Chat의 GitHub 연결만 있는 경우와 Python 분석 환경까지 있는 경우, Work/Codex 기능이 없는 경우를 구별한다.

정적 검토는 frontmatter(`name`, `description`), 패키지 경로, 상대 링크, activation/near-miss, 권한 경계와 검증 표현을 대상으로 한다. 이를 실제 Chat 모드의 자동 선택, OpenSpec 실행 동등성이나 프로젝트 설치 성공으로 확대하지 않는다.

대표 도그푸딩 시나리오:

| 시나리오 | 기대 결과 |
| --- | --- |
| 해당 프로젝트에서 CLI가 실제로 사용 가능 | Native를 우선하고 대체하지 않음 |
| Chat에서 GitHub 조회·편집이 가능한 propose 요청 | 대상 ref·설정·기존 spec을 읽고 아티팩트를 실제 브랜치에 작성, 결과 diff 확인 |
| GitHub 읽기만 가능하고 변경 목록을 요청 | 관찰 가능한 파일 범위로 응답, 미확인 CLI 상태 고지 |
| 파일과 Python만 있고 원격 저장소 쓰기 불가 | 가능한 정적 검증·로컬 아티팩트 작성 후 원격 쓰기 미수행 사실을 인계 |
| 사용자 정의 스키마의 `status` 또는 `instructions` 요청 | 유효한 설정·의존성·템플릿 확보 전 동등성 주장 금지 |
| CLI 없는 상태에서 `validate` 요청 | 검토 결과와 미실행 CLI 검증을 분리 |
| 변경 충돌 또는 불완전한 상태의 `sync`/`archive` | 비가역적 부분 변경을 피하고 정확한 인계 |
| 쓰기 권한 또는 승인 부재 | 연결 전환 없이 Blocked 처리 |
| Chat 모드와 무관한 OpenSpec 커스터마이징 | 이 Skill 대신 전문 소유자 선택 |

추후 실제 ChatGPT Chat에서 설치·선택·행동 평가를 수행하고, 가능하면 **동일한 프로젝트 리비전·OpenSpec 버전의 CLI 결과**를 비교 기준으로 삼는다. 검증 결과는 관찰한 범위만 주장한다.

## 유지보수 기준

- 명령의 새 기능이 아니라 **현재 Chat 모드에서 재현할 수 없는 실행 의미**가 확인될 때에만 호환 지침을 확장한다.
- 빠르게 변하는 OpenSpec CLI나 ChatGPT 배포 절차는 외부 공식 원본을 찾아 확인하고, 장황한 명령 표나 런타임별 기능표를 Skill에 고정하지 않는다.
- 반복되는 동등성 판정이 충분히 검증되지 않았다면 실행 어댑터 코드를 만들지 않는다.
- 정본 `SKILL.md`와 이 문서만 변경하며, 사용자가 요청하지 않은 route·lock·플러그인 설치·CI 자동화를 추가하지 않는다.

현재 상태: **Chat 런타임 기반 개선 초안**. 실제 ChatGPT Chat 스킬 설치, 선택률, CLI 대비 동등성 평가는 아직 수행되지 않았다.
