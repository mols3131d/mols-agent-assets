# Kanban Board

## 1. Purpose (목적)

진행 중인 작업의 흐름(Flow)을 시각화하고, 병목을 파악하며, 팀의 작업 속도와 컨텍스트 스위칭을 최적화합니다.

## 2. Core Methodology (핵심 원칙)

- **Visualize Actual Workflow**: 단순히 To Do/In Progress/Done이 아니라, 코드 리뷰, QA 등 팀의 실제 작업 단계를 반영하여 컬럼을 구성합니다.
- **WIP Limits (Work-In-Progress)**: 특정 컬럼이나 개인당 동시에 진행할 수 있는 작업의 수를 제한하여 컨텍스트 스위칭을 줄이고 완료(Done)에 집중합니다.
- **Pull System**: 일이 위에서 아래로 푸시(Push)되는 것이 아니라, 여력이 생길 때 이전 단계에서 다음 단계로 작업을 끌어오는(Pull) 방식을 유지합니다.

## 3. Recommended Structure (권장 구조)

- **Backlog**: 향후 진행할 우선순위가 정렬된 대기열.
- **Ready for Dev**: 개발 시작 전 요구사항이 명확히 정의된 상태.
- **In Development**: 개발이 활발히 진행 중인 상태.
- **Code Review**: PR이 생성되어 동료의 리뷰를 대기 중인 상태.
- **QA/Testing**: 테스트 환경에서 검증 중인 상태.
- **Done**: 배포 완료 및 최종 확인된 상태.

## 4. Best Practices (모범 사례)

- **Definition of Ready & Done**: 각 단계를 넘어갈 때의 명확한 진입/완료 조건(예: 테스트 코드 통과, 리뷰어 1명 이상 승인)을 수립하여 모호함을 없앱니다.
- **Review and Improve**: 리드 타임(Lead Time)과 사이클 타임(Cycle Time) 지표를 주기적으로 분석하여 병목(예: 멈춰있는 코드 리뷰)을 해결합니다.

## 5. Anti-Patterns (안티패턴)

- WIP 한도를 설정하지 않거나 무시하여 'In Progress' 컬럼에 작업이 무한정 쌓이는 경우.
- 실제 프로세스를 반영하지 않는 획일화된 보드 템플릿 사용.
