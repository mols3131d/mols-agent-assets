# Chatbot Bootstrap — Asset Design Assessment

> PR #267 설계 평가 / 2026-11-02. **정적 자산 평가 및 작업 기록**이며 실행 Skill의 정본이나 런타임 평가 결과가 아니다.

## 결론

현재 `mols-chatbot-bootstrap`은 native-first, no-op, 최소 entry/route 구성, 선택적 canonical 본문 로딩, 변경 권한과 증거 수준 구분이 강하다. 그러나 **로컬 에이전트 하네스의 실행 의미를 챗봇에서 보존**하는 목적에 비추면, discovery/loading 바깥의 실행 책임과 구축 후 적용 지속성을 설계 단계에서 판정하도록 유도하는 지침이 약하다.

이 판단은 **실제 런타임 검증의 부재를 결함으로 계산하지 않는** 소스 기반 평가다. 결과를 모델 성능 또는 실제 provider 호환성 평가로 확대하지 않는다.

## 평가 축

| 축 | 판단 | 자산 기반 근거 |
| --- | --- | --- |
| Skill 책임·activation | 양호 | 저빈도 구축·복구와 일반 작업·CI·자동화의 경계를 나눔 |
| Native/no-op 및 최소 구성 | 강점 | 이미 충분하면 변경하지 않으며 별도 router·generator 강제를 금지 |
| 정본·권한 경계 | 강점 | canonical source와 runtime capability·쓰기 권한을 구분 |
| Skill/Rule 선택·본문 로딩 | 양호 | 선택된 본문과 필요한 조건부 reference까지 확인하도록 개선 |
| 실행 의미 보존 | 보강 필요 | 코드 실행·CLI·Subagent 등 원본의 실행 책임을 선택적으로 다룰 안내가 부족 |
| 구축 후 운영 지속성 | 보강 필요 | 새 작업, ref/path/object 변경 시 소비 하네스의 재선택·재평가 설계가 명확하지 않음 |
| 대체 실행 판정과 통지 | 보강 필요 | 네이티브/의미 보존 대체/부분 수행/생략/인계의 구분을 자산 작성 관점에서 다룰 필요 |

## 개선 백로그

| 중요도 | Finding / 작업 | 최소 완료 조건 |
| --- | --- | --- |
| P1 | 원본 하네스의 적용 가능한 책임을 `instruction / selection / execution / authority` 단위로 식별 | 추가 자산 유형 목록을 강제하지 않으면서 도구·Subagent·Command 등 필요한 실행 책임을 놓치지 않음 |
| P1 | 특정 실행 책임을 네이티브로 수행할 수 없을 때의 대체·부분·생략·인계 판단 | 별도 조건부 reference로 판정 기준, 지침 작성 방법, 사용자 인지·권한·증거 요구 정의 |
| P1 | 구축된 하네스가 다음 작업에서 scope/ref 변경을 반영하도록 설계 | 일반 작업 때 bootstrap Skill을 재호출·상주시키지 않고 로컬 소비 하네스에서 관련 원본을 재선택 |
| P2 | Activation의 탐색·로딩 편향 축소 | 하네스 자체의 구축·복구 요청 중 실행 fidelity 문제가 주요한 경우에도 선택 가능; 일반 코드 실행 업무에는 미선택 |
| P2 | 유지보수 README에서 대체 방식의 소유권과 판단 근거 유지 | SKILL과 참조의 실행 계약을 중복하지 않고 링크·변경 경계만 보존 |

## 대표 설계 사례

| 시나리오 | 기대되는 설계 판단 |
| --- | --- |
| 대상의 네이티브 하네스가 충분 | 변경하지 않음; 대체 실행 지침도 불필요 |
| repository instructions/Skills는 읽지만 독립 Subagent 호출 불가 | 역할 분해가 허용되면 순차 대체를 정의하되 **독립 실행/병렬/격리로 주장하지 않음**; 독립성이 필수면 인계 |
| Shell은 없고 실행 가능한 코드 환경만 있음 | 실제 의존성·입출력·부작용·권한을 충족할 때만 원본 실행 의미의 제한적 대체; 아니면 부분/인계 |
| Command/외부 API/예약 등 필수 기능 없음 | 임의 가상 실행·권한 우회 없이 미지원 내용을 드러내고 스킵 가능 여부와 인계 구분 |
| 새로운 PR/ref/path로 작업 변경 | 구축된 진입점과 선택 규칙이 원본 ref·적용 scope·필요한 Skill/Rule을 다시 판정 |
| 다른 계정만 쓰기 권한 있음 | 계정 전환 금지; 승인된 identity를 유지하고 읽기 분석·정확한 인계까지만 수행 |

## 범위 및 후속

현재 요구에 맞춰 인박스에는 평가 결과를 보존하고, **실행·대체 지침을 설계하는 기준은** [새 조건부 reference](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/references/execution-adaptation.md)에서 관리한다. `SKILL.md`에는 reference를 여는 조건과 필수 불변조건만 반영한다. 지속적인 설계 이유는 [maintainer README](../../docs/skills/mols-chatbot-bootstrap/README.md)로 보낸다.

독립 Subagent·동등 CLI 실행 등 실제 provider별 behavior는 런타임에서 관찰되기 전까지 확인되지 않았다. 평가 fixture나 CI를 선제적으로 확장하지 않는다.
