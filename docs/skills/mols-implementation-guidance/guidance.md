---
description: mols-implementation-guidance의 언어별 지침 분리와 평가 범위를 확인할 때 사용합니다.
---

# Implementation Guidance

언어 독립적인 판단은 Core에, 언어 고유의 실행 의미와 계약은 조건부 Reference에 둔다. 독립적인 선택 책임이 없는 언어 확장은 별도 Skill로 분리하지 않는다.

자동 Eval은 Skill의 선택·비선택에 한정한다. Reference 로딩이나 구현 결과의 품질은 이 Eval의 평가 대상이 아니다.
