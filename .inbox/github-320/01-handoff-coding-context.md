# Coding Context 로컬 작업 제안

## 목표

[PR #320](https://github.com/mols3131d/mols-agent-assets/pull/320)을 불필요한 기능·지침 확장 없이 머지 준비 상태로 만든다. [정적 리뷰 결과](00-review-coding-context.md)는 검토의 출발점이며 확정 요구사항이나 독립 리뷰의 대체물이 아니다.

대상 브랜치: `mols/refactor/coding-context-core`. 검토 당시 HEAD: `73cd2aeba5fb4474783d089ecfb23f563ea70f99`. 시작 시 현재 PR base/head, 작업 공간, 미완료 항목을 다시 확인하고 기존 작업을 보존한다.

## 작업 제안

| 작업군 | 수행 범위 | 완료 근거 |
| --- | --- | --- |
| 평가 후보 정합성 | R1의 fixture 의도와 runner 계약을 확인하고 필요 최소한으로 갱신 | 현행 metadata 또는 명시적인 고정 비교 조건, 관련 fixture 검사 |
| 레거시 은퇴 | 정확한 `coding-context` 이름·경로의 직접 참조, 소비자 설정·lock·생성물·문서·평가 자료를 조사; `mols-coding-context`와 구분 | 확인한 소비자 및 revision, 필요한 이관·설치 사본 처리 또는 미확인 범위 |
| Routing 평가 | 기존 evaluator로 Core·Python 선택, 비선택, 동반 선택만 평가 | fixture·config 검증 및 실제 모델 routing 결과 또는 미검증 사유 |
| 검증·리뷰 | 저장소의 공식 생성·검증 경로 및 현재 HEAD CI 확인; 변경 지침에 의존하지 않는 독립 리뷰 | 검증 결과, 독립 리뷰의 기준 revision과 finding disposition |

소비자 조사와 평가 준비는 독립적으로 병렬 수행할 수 있다. 쓰기 작업은 충돌하지 않는 작업 공간과 소유 범위에서 수행하고, 통합된 최종 diff를 다시 검토한다. 외부 소비자 변경은 대상·권한·영향을 확인하고 필요한 승인 범위 안에서 처리한다.

## Routing 평가의 범위

- 일상 코딩의 Core 선택, 비코딩의 비선택, Python 고유 판단이 필요한 작업의 동반 선택과 부수적 언급의 비선택을 검증한다.
- 실제 에이전트의 로딩·재사용 및 결과물 개선은 routing Eval의 보장 범위가 아니다. 응답 기반 Behavior Eval, 별도 평가 프레임워크 또는 원격 모델 호출은 추가하지 않는다.

[Core 유지보수 기준](../../docs/skills/mols-coding-context/guidance.md#evaluation), [Python 유지보수 기준](../../docs/skills/mols-coding-context-python/guidance.md#evaluation), [평가 정책](../../docs/development/evaluation.md)을 참고한다. 필요한 권한이나 runtime이 없으면 미검증 사유를 기록한다.

## 실행 및 종료

기존 하네스와 적용 가능한 mols-loops에 따라 진행한다. 변경과 검토를 반복하되 finding은 근거, 실제 계약, 중요도를 먼저 확인한다. 불필요한 방어코드나 추가 체크리스트·스킬·문서를 만들지 않는다. 실제 실패 근거가 없는 신규 Python 판단은 채택하지 않는 결정도 유효하다.

독립 리뷰는 수정된 지침에 의존하지 않는 별도 실행 문맥에서 최신 diff를 검토한다. 지원되는 경우 검증 관점과 반증 관점을 병렬화하고, 확인된 실질적 finding만 수정한 뒤 다시 독립 리뷰한다. 독립 실행을 재현할 수 없다면 완료로 처리하지 않는다.

- [x] R1: mols-test-design의 이전 Core 후보 description 6개를 갱신. 실제 실행은 별도 확인.
- [ ] 레거시 소비자 이관 조건 충족 또는 실제 차단 범위 식별.
- [ ] Core·Python routing Eval 실행 및 결과 확인; 미검증 결과를 성공으로 기록하지 않음.
- [ ] 최종 HEAD의 저장소 검증·PR Gate 및 독립 리뷰 완료, 미해결 실질적 finding 없음.
- [ ] PR 본문에 현재 revision, 수행한 검증, 남은 위험과 완료 여부 반영.

목표는 머지 준비까지다. 사람의 명시적 승인 없이 머지하거나 Draft를 완료 상태로 오인하지 않는다. 필수 조건을 충족할 수 없으면 무한 반복하지 말고 진행 근거와 차단 사유를 인계한다.
