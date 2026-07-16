# Document Inventory (Index)

## 1. Purpose (목적)

문서, 자산, 지식의 단일 진실 공급원(Single Source of Truth)을 제공하여 온보딩 속도를 높이고 기술 부채와 정보 탐색 시간을 줄입니다.

## 2. Core Methodology (핵심 원칙)

- **Strategic KM (Knowledge Management)**: 문서화 자체를 목적이 아닌, 팀원이 자주 묻는 질문이나 해결하려는 명확한 유즈케이스를 기반으로 지식을 정리합니다.
- **Clear Ownership**: 문서 관리가 방치되지 않도록 카테고리나 개별 문서에 명확한 소유자(Owner)를 지정합니다.
- **Automation where Possible**: 수동 엑셀 업데이트를 지양하고, 시스템과 연동되어 실시간으로 메타데이터나 리스트가 갱신되도록 자동화를 추구합니다.

## 3. Recommended Structure (권장 구조)

- **Index Table**: 문서 ID, 제목, 요약, 소유자, 최근 업데이트 날짜를 포함한 메타데이터 표.
- **Known Errors Database (KEDB)**: 미해결 이슈나 알려진 버그에 대한 문서 링크.
- **Onboarding Guides**: 환경 설정 및 필수 워크플로우 진입점(Entry point) 목록.

## 4. Best Practices (모범 사례)

- **Hierarchical & Searchable**: 폴더 구조를 논리적으로 배치하고 쉽게 검색 가능하도록 태그/인덱싱을 적용합니다.
- **Integrate into Workflow**: 문서화 작업을 별개로 취급하지 않고 CI/CD 파이프라인이나 Jira 티켓 완료 조건 등 일상적인 워크플로우에 통합합니다.
- **Regular Audits**: 정기적인 리뷰 사이클을 통해 유효 기간이 지났거나 잘못된 문서를 폐기(Decommission) 또는 갱신하여 문서 부패(Decay)를 막습니다.

## 5. Anti-Patterns (안티패턴)

- 아무도 읽지 않는 "완벽함을 위한 문서화(Documenting for the sake of completeness)".
- 버전 관리가 되지 않아 구버전 정보가 최신 정보와 섞여 혼란을 주는 경우.
- 작성자만 존재하고 지속적으로 관리하고 갱신할 책임자가 없는 상태.
