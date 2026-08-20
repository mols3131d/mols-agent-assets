# Template / Schema-Driven Assets

자산의 구조를 정의하는 template, schema 또는 metadata에 작성 지침과 제약을 함께 두어 **더 적은 문서와 더 적은 중복으로 자산을 생성·검증**하는 패턴입니다.

## Pattern

- Template은 섹션 구조, 필수 항목, 작성 의도를 가능한 한 직접 표현합니다.
- Schema나 metadata는 필드 의미, 제약, 허용값과 작성 기준을 가능한 범위에서 소유합니다.
- 같은 규칙을 별도 가이드에 반복하기보다 자산 구조를 정의하는 가장 가까운 owner에 둡니다.
- 생성기와 validator는 같은 template/schema/metadata를 재사용하는 것을 권장합니다.

## Why

- KISS — 자산 생성 시 별도 지침 탐색을 줄입니다.
- DRY — 구조 정의와 작성 지침의 중복을 줄입니다.
- SRP — 해당 구조의 규칙을 해당 구조 owner가 소유합니다.
- 자동 생성과 검증을 같은 contract에 연결하기 쉽습니다.

## Boundary

- Template이나 schema가 표현하기 어려운 rationale, 장기 원칙, 비전까지 억지로 넣지 않습니다.
- 설명이 길어지면 별도 maintainer documentation이나 baseline으로 분리합니다.
- Metadata를 단순 prose 저장소로 사용하지 않습니다.
