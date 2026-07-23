# Decisions

## Proposed

## Accepted

### **[design] 템플릿 및 설정 파일 주도 설계를 통한 스킬 지침 최소화**

- DECISION | **Drive skill behavior via template and config files** - 스킬 자체의 고정 지침을 최소화하고, 동작 규칙을 템플릿과 스키마(콘픽) 파일에 위임하여 주도하도록 설계합니다.
- REASON | **Customization requirements per user and project** - 각 사용자 또는 프로젝트마다 칸반 프런트매터 규격, 자릿수, 규칙 등이 다르므로 이를 스킬 코드에 하드코딩하지 않고 유연하게 커스텀할 수 있어야 하기 때문입니다.
- IMPACT | **High adaptability and decoupled configuration** - 스킬 핵심 로직의 수정 없이도 프로젝트의 고유한 요구사항에 따라 템플릿과 설정 파일을 손쉽게 교체하여 즉시 맞춤형 동작을 정의할 수 있습니다.

### **[design] 설정 파일 지정을 통한 사용자 정의 지침 연동**

- DECISION | **Reference user-defined instruction files in configuration** - 템플릿과 스키마(콘픽) 파일로 표현하기 부족한 세부 규칙은 사용자가 지정한 별도의 지침 파일(디렉토리 또는 glob 패턴 지원)을 따르도록 하고, 이 지침들의 경로를 콘픽 파일 내에서 지정하게 합니다.
- REASON | **Supporting domain-specific and project-specific rules** - 단순 스키마 유효성 검사를 넘어 상태 전이 조건, 작업 분할 정책 등 프로젝트별 도메인 지침까지 완벽하게 지원하고 통제하기 위함입니다.
- IMPACT | **Extended agent guidance and dynamic rule loading** - 에이전트가 동작 시 해당 콘픽에 지정된 glob 경로의 마크다운 지침을 동적으로 로드해 지킬 수 있으므로, 규칙 준수 성능이 크게 향상됩니다.

## Superseded

## Deprecated
