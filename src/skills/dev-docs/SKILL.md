---
name: dev-docs
description: ADR(Architecture Decision Record) 및 SPEC(Specification) 문서 관리 스킬
version: 1.0.0
---

# Development Documentation Skill (ADR & SPEC)

이 스킬은 프로젝트의 핵심 결정 사항을 기록하는 **ADR**과 상세 구현 설계를 정의하는 **SPEC** 문서를 관리하기 위한 규칙과 템플릿을 제공합니다.

## 1. 문서 유형 및 목적

| 유형 | 목적 | 생성 시점 | 권장 경로 | 템플릿 자산 |
| :--- | :--- | :--- | :--- | :--- |
| **ADR** | 아키텍처 결정 및 트레이드오프 기록 | 기술 스택 선택, 설계 패턴 결정 등 주요 의사결정 시 | `docs/adr/` | [`template-adr.md`](./assets/template-adr.md) |
| **SPEC** | 기능 요구사항, 데이터 구조, 인터페이스 설계 | 새로운 기능 구현 시작 전, 복잡한 로직 설계 시 | `docs/spec/` | [`template-spec.md`](./assets/template-spec.md) |

## 2. 의사결정 워크플로우

1. **문제 정의**: 해결해야 할 기술적 과제나 기능 요구사항 발생.
2. **ADR 작성**: 여러 대안 중 하나를 선택해야 하는 경우 ADR을 먼저 작성하여 결정 근거를 기록.
3. **SPEC 작성**: 결정된 사항을 바탕으로 구체적인 데이터 스키마, API 인터페이스, 로직 흐름을 SPEC에 기술.
4. **구현 및 검증**: SPEC을 바탕으로 코드를 작성하고, 문서의 검증 포인트를 통과하는지 확인.

---

## 3. 에이전트 행동 지침

### 문서 생성
- 새로운 문서를 생성할 때 반드시 이 스킬의 `assets/` 디렉토리에 있는 템플릿을 참조하여 작성하십시오.
- 문서명은 `[ID]-[제목].md` 형식을 권장합니다. (예: `ADR-001-use-postgresql.md`)
- 프론트매터(Frontmatter)의 `status` 필드를 정확히 관리하여 문서의 생명주기를 추적하십시오.

### 문서 연결
- 모든 문서는 상호 연결되어야 합니다.
- SPEC 문서에서는 배경이 된 ADR을 링크하십시오.
- ADR에서는 결정 이후 필요한 후속 작업(SPEC 작성, 코드 수정 등)을 명시하십시오.

### 변경 관리
- 결정이 변경되거나 사장(Deprecated)될 경우, 기존 ADR의 상태를 `superseded`로 변경하고 새로운 ADR로 연결하십시오.
- SPEC 문서가 최신 구현과 일치하지 않을 경우 즉시 업데이트하여 'Single Source of Truth'를 유지하십시오.
