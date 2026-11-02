---
description: ChatGPT Chat용 OpenSpec 실행 호환 Skill의 목적, 타깃 런타임 근거, 책임 경계 및 검증 시나리오를 유지보수할 때 사용합니다.
---

# OpenSpec CLI Compatibility — Maintainer Guide

실행 동작과 activation의 정본은 [`mols-openspec-cli-compat`](../../../src/openai-chatgpt-chat/skills/mols-openspec-cli-compat/SKILL.md)이다. 이 문서는 설계 선택과 검증 근거만 맡으며, 실제 Chat에서 자동으로 실행되는 지침은 아니다.

## 목표와 책임

Chat에서 OpenSpec의 **프로젝트 워크플로를 가능한 한 완료**하고, 원본 CLI·Skill과 동등하다고 입증하지 못한 단계만 구분해 보고하도록 한다.

- **OpenSpec 프로젝트와 공식 Skills/CLI** — root/store, 버전, schema, 설정, 각 단계의 artifacts·명령 의미를 소유한다.
- **Chat 세션** — 실제 노출된 Plugin/앱 액션, 파일, 코드 분석, 인증·승인·권한 범위를 소유한다.
- **이 Skill** — 원본 단계를 수행할 도구 선택과 상태 간 연결, 대체 가능성·검증·인계를 소유한다.
- **범용 하네스 및 커스터마이징** — `mols-chatbot-bootstrap`과 `mols-openspec-customize`가 맡는다. 그 내용은 복제하지 않는다.

## Chat 런타임과 배포 근거

2026-11-02에 확인한 공식 문서 기준. 제품 제공 범위는 변하므로 지원 기능 목록을 세션에서의 **실제 설치·작동 증거**로 간주하지 않는다.

| 기능 | OpenSpec에 유효한 활용 | 제한 및 확인 |
| --- | --- | --- |
| Chat Skills / Plugins | 공식 또는 호환 워크플로 호출, 함께 설치된 연결 앱 도구 사용 | 공식 [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)는 지원되는 계정·워크스페이스의 **Chat 직접 생성·편집·업로드·설치**를 설명한다. Plugin 배포는 유일한 경로가 아니며, 관리 원본 자체는 설치되지 않는다 |
| 연결 앱(GitHub 등) | 정확한 remote ref 조회, 변경 작성, PR 및 CI 상태 확인 | 실제 노출 액션, 연결된 서비스 계정과 쓰기 scope를 작업마다 확인한다 |
| Project/첨부 파일 | 프로젝트 지침·OpenSpec config·schema·artifact 로딩 | 업로드된 스냅샷이 최신 브랜치나 쓰기 가능한 working tree를 뜻하지 않는다 |
| Python/분석 | 파일을 확보한 뒤 구조 파싱, 의존성 검사, diff·변환 | 일반 Chat 분석 sandbox는 외부 네트워크/API에 접근할 수 없으므로 원격 GitHub와 같은 파일시스템/인증 상태로 간주하지 않는다 |
| 웹 및 공식 문서 | OpenSpec CLI/Skills의 버전 민감한 계약 확인 | 공개 문서는 설치 버전과 프로젝트별 schema/store를 대체하지 않는다 |
| 기존 테스트/CI | 프로젝트에서 실제 실행된 검증 재사용 | 정적 검사, 본래 CLI validation, 실제 CI, 수동 리뷰를 하나의 통과로 합치지 않는다 |

ChatGPT Work의 별도 컴퓨터·브라우저, Codex의 코드 작업 환경, 로컬 OpenSpec CLI는 Chat의 상시 기능이 아니다. 해당 환경으로 인계가 필요한 경우 사용자가 선택·승인할 수 있게 설명한다.

권위 있는 참고: [OpenAI Chat Skills](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [Plugins](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt), [Build skills](https://learn.chatgpt.com/docs/build-skills), [Data analysis](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt), [OpenSpec Skills](https://openspec.dev/docs/skills), [OpenSpec CLI](https://openspec.dev/docs/cli), [Schemas](https://openspec.dev/docs/customize-schemas).

## 주요 설계 판단

1. **Workflow 우선.** OpenSpec는 `propose`(planning만 생성), `apply`(코드 구현), `update`(기존 계획 수정·확인), `verify`(report-only), `sync`(정본 spec 업데이트), `archive`(확인 후 보관)를 구분한다. 이 구분을 일반적인 파일 수정으로 평탄화하지 않는다.
2. **Root 누락은 호출 의도에 따라 다르다.** 공식 Skill이 자동 선택되었다면 OpenSpec 없이 본래 요청을 처리할 수 있다. 명시적인 **OpenSpec Skill** 요청이면 초기화·외부 store·OpenSpec 없이 진행 중 선택을 먼저 요청한다. 반면 사용자가 직접 요청한 **CLI 명령**은 해당 명령의 원본 부작용 계약을 따른다. 예를 들어 `openspec new change`는 root가 없어도 암묵적 디렉터리를 만들 수 있으므로 실행·대체 전에 쓰기 권한과 사용자의 의도를 확인한다.
3. **도구 최소 조합.** 작업과 관련된 연결 앱·파일·검증만 찾는다. Remote read → 필요시 분석 → authorized write → remote readback을 명시하고, 원격 쓰기 도구가 없다고 무조건 아무 결과도 만들지 않는 것은 피한다.
4. **Computed CLI semantics는 추측하지 않는다.** `status/instructions/templates`의 schema dependency resolution, `validate` exit/result는 단순한 텍스트 검토로 대체되지 않는다. 가능한 확인 부분만 증거 수준대로 기록한다.
5. **손상 위험 분리.** `sync/archive`는 여러 파일·정본 데이터를 바꿀 수 있다. 승인, 충돌 검토, 복구 가능한 변경 단위가 없으면 실행을 멈춘다.
6. **작성 원본과 소비 분리.** `src/openai-chatgpt-chat/skills/mols-openspec-cli-compat/SKILL.md`는 하나의 관리 정본이며, Chat Skill 설치·선택은 별도의 관찰 대상이다. Rulesync와 두 번째 작성 원본을 만들지 않는다.

## 검증 계획과 관찰할 행동

| 상황 | 기대 결과 |
| --- | --- |
| 공식 CLI 또는 설치된 OpenSpec Skill이 정확한 상태에서 실행 가능 | 원본 기능 우선, 별도 adapter 강제하지 않음 |
| 명시적 OpenSpec Skill 요청이나 root 없음 | 쓰기 전에 init/store/비OpenSpec 진행 선택 요청 |
| CLI `openspec new change` 요청이나 root 없음 | CLI 원본의 암묵적 root 생성 부작용을 인지하고 허가된 쓰기 범위 확인 |
| Chat이 OpenSpec을 자동 선택했으나 root 없음 | OpenSpec 파일을 만들지 않고 원래 사용자 작업을 처리 |
| 읽기만 가능하고 상태 조회 요청 | 확인한 아티팩트만 기술, 계산된 CLI status와 구분 |
| GitHub로 proposal 작성 가능 | effective schema·선행 artifacts 확인 후 planning만 커밋; 코드 구현하지 않음 |
| apply 요청과 tracked task가 여러 파일로 분산 | 실제 task source를 확인해 구현된 항목만 체크 |
| 프로젝트 CLI 없는 validate 요청 | 부분 정적·의미 검사 후 CLI 미실행을 명시 |
| sync/archive와 충돌 또는 불완전한 작업 | 위험한 부분 쓰기를 피하고 정확한 차단·인계 사유 제공 |
| 승인되지 않은 다른 계정만 쓰기 가능 | 계정 전환 없이 읽기/부분 수행/blocked 보고 |

현재 `SKILL.md`의 형식·링크 및 대표 근거는 **정적 검토 대상**이다. 실제 Chat 설치·암묵 선택·툴 호출과 동일 프로젝트 버전의 CLI 대비 결과는 별도 **런타임 행동 평가**가 필요하다. 후속 검증 없이 정적 점검을 Chat 호환성 완료라고 주장하지 않는다.

## 유지보수

원본 CLI 명령·flags·스키마를 문서에 대량 복제하지 말고 공식 소스와 프로젝트에서 필요한 것만 확인한다. 실패가 반복해서 관찰되기 전에는 새 호환 스크립트, registry, 설치기, CI를 추가하지 않는다. 이 문서와 실행 원본의 책임을 분리하고, 타깃 Chat에 실제 설치했는지를 확인 가능한 evidence로만 기록한다.
