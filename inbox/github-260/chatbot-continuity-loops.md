# Chatbot Continuity — 개선·최적화 루프 (PR #260)

## Prepare

- **목표**: `mols-chatbot-continuity`의 실행 간 연속성 결함을 고치고 불필요한 텍스트·컨텍스트 비용을 낮춘다.
- **기준**: PR #260의 `a007be0c2d143307c3f1c30cc0cc4a648a763216`에서 시작. 적용 스킬: `mols-loops`, `mols-agent-asset`, `mols-text-optimizer`; 문서 품질·context 분리 관행 참고.
- **범위**: canonical `SKILL.md`, 조건부 `references/resumable-work.md`, derived `route/skills.jsonl` 및 이 인박스 기록만 변경.
- **제외**: 별도 모델 eval/fixture, 예약 실실행, 신규 데몬·DB·작업 프레임워크, PR 병합. 사용자의 실제 도그푸딩으로만 행동 품질을 개선한다.

## Loop 1 — 개선 (Research → Plan → Work → Review)

**확인한 결함과 대응**

| 문제 | 조치 |
| --- | --- |
| 조건부 참조가 연속 목표만 대상으로 보여 독립 이벤트 중복 처리를 놓칠 수 있음 | 중복 이벤트·재시도·동시 쓰기도 reference 로드 조건에 포함 |
| ID/revision 조회만으로 동시 쓰기 멱등성을 보장하는 듯한 표현 | 실제 직렬화·조건부 갱신 등 지원 수단 확인, 미지원이면 충돌 쓰기 보류 |
| 실행 내 업무 종료와 반복 예약 비활성화 혼동 | 완료·기한 이후 호스트의 예약 중지 또는 사용자 조치를 별도 결과로 설계 |
| 일반 대화에서 가능했던 앱·상태 접근이 예약 모드에서도 될 것이라는 가정 | 해당 계정·예약 실행 모드의 읽기/쓰기·승인 경계 확인 |

**Work**: `366fc94ec596b53663b64902f49bbf07f8eded16`에 수정·인박스 체크포인트 기록.

**Review**: 품질/안전 관점에서 중복 쓰기·예약 잔존의 잘못된 확신을 제한하고, 라우팅 관점에서 간단한 정기 보고의 참조 로드를 막았다. 실제 실행 검증이 아닌 **정적 의미 검토**다. 개선할 남은 영역은 용어·절차의 반복과 description의 다소 장황한 선택 신호.

## Loop 2 — 최적화 (Research → Plan → Work → Review)

**목표**: 기능적 의미와 위험 경계를 유지하면서 항상 로드되는 `SKILL.md`와 조건부 reference의 표현을 압축한다.

**Work**:
- description은 사용 의도/제외 대상 중심으로 줄이고, 실행 전 확인 절차를 본문에 남겼다.
- 생성 프롬프트의 필수 항목을 한 위치에 모았다. 단순 예약에 reference·큐를 강제하지 않는다.
- reference의 저장 상태·재개 단계·충돌 처리에서 중복 서술을 정리하되, **동시성은 조회만으로 해결되지 않음**, **미확인 쓰기 재실행 금지**, **예약 비활성화 별도**는 보존했다.
- 새로운 reference나 도메인 특화 예시 템플릿을 추가하지 않았다.

**다관점 정적 Review**:
- **Owner/activation**: 예약 실행 간 설계·구성에 집중하고, 내부 RPI·단순 알림·일회성 작업과 분리.
- **Context/효율**: 메타데이터→작은 본문→필요할 때 재개 reference로 점진 로딩. 원본·현재 상태·근거를 구분하고 전문 이월을 피함.
- **안전/적대적 상황**: 중복 트리거, 동시 쓰기, 결과 불명확, 승인이 필요한 변경, 미지원 호스트 기능의 경계 유지.
- **운영**: 완료/기한과 실제 자동화 중지를 구별. 호스트가 할 수 없는 조작의 성공을 주장하지 않음.

독립 Subagent 호출이나 실제 호스트 시험을 수행하지 않았으므로 다관점 검토는 **단일 맥락에서 순차적으로 수행한 정적 리뷰**다. 형식적 3차 루프는 만들지 않는다.

## Finalize — 구조 확인과 도그푸딩 인계

- Canonical: `src/rulesync/.rulesync/skills/mols-chatbot-continuity/SKILL.md`
- Conditional: `src/rulesync/.rulesync/skills/mols-chatbot-continuity/references/resumable-work.md`
- Derived route: `route/skills.jsonl`. 재생성·정합성 검사는 기존 CI가 소유한다.
- **검증**: GitHub PR Gate / Branch Check의 새 head 결과를 확인해야 한다. 정적 리뷰를 런타임 성능이나 모델 eval로 해석하지 않는다.
- **다음 단계**: 사용자 도그푸딩에서 관찰되는 실제 오동작(예약 불가, 상태 접근 불가, 재시도·중단 실패, 불필요한 context 로딩)만 좁게 수정. 별도 행동 eval 없음.
