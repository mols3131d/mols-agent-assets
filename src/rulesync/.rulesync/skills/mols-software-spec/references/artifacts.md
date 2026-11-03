# Artifact Contract

산출물의 **종류·의미**는 이 Reference와 [Artifact Registry](../assets/artifacts.json)가 정의한다. **어떤 순서로 언제 만들지는 Workflow의 책임**이다. 하나의 단계가 여러 산출물을 사용하거나 같은 산출물을 여러 번 갱신할 수 있으며, 단계와 파일을 1:1로 고정하지 않는다.

| ID | Kind | Minimum useful content or evidence |
| --- | --- | --- |
| `proposal` | document | 변경 이유, 목표, 범위, 성공 조건 또는 해결하려는 위험 |
| `research` | document | 확인한 현황·근거, 대안과 제약, 불확실성 |
| `plan` | document | 선택한 접근, 영향 영역, 중요한 의존성, 구현·검증 전략; 스펙 전 계획은 잠정적 |
| `specification` | document | 관찰 가능한 요구 동작, 제약·불변식, 수락 조건과 중요 경계 |
| `test-design` | document | 수락 조건별 테스트 시나리오·oracle, 기존 검증과 미포함 위험 |
| `test-implementation` | code | 실제 테스트 경로, 변경된 assertion과 실행·실패 증거 |
| `code-implementation` | code | 실제 제품 코드 경로·commit 및 스펙과 검증 증거 |

문서 종류는 사용자에게 별도 파일 생성을 강제하지 않는다. 기존 spec store, Issue, design docs 또는 프로젝트가 제공하는 문서 위치에 **동일한 의미의 정본**이 있으면 참조해 재사용한다. 내용과 출처를 확인하지 않은 채 파일 존재만으로 완료를 선언하지 않는다. 다중 파일의 테스트·코드 구현은 한 항목의 Markdown 파일로 복제하지 않는다.

`review`는 **단계이자 판정 활동**이며 기본 Artifact ID가 아니다. 리뷰 findings와 evidence는 기존 PR·Issue 또는 프로젝트가 정한 현재 작업 근거에 기록할 수 있다. 기계적 routing이 필요할 때는 Workflow Reference의 JSON report를 입력으로 사용할 수 있으나 이를 별도의 영구 저장 파일로 중복 관리할 필요는 없다.

새 저장소에 기존 소유자가 없다면 `spec/changes/<change-id>/`를 문서의 기본 위치로 **제안**한다. 코드와 테스트는 원래 프로젝트의 적절한 경로에 둔다. 새 폴더 생성을 요청·승인받지 않았거나 기존 schema/store가 있으면 생성하지 않는다. 변경 완료 후 장기 스펙 정본에 반영할지는 실제 프로젝트가 정한다.
