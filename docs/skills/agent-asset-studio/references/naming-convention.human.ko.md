# 자산 명명 규칙 (Naming Convention)

## 1. Domain Prefixing (도메인 접두사 지정)

- **목적**: 디렉토리들이 항상 중첩된 계층 구조를 가지지 않으므로, 파일 분류 및 태깅(Tagging)을 위해 사용합니다.
- **규칙**: 파일명 맨 앞에 1~2개의 도메인 토큰(Domain tokens)을 붙입니다.
- **워크플로우 내 규칙**: 라우팅 스킬 내의 워크플로우에서는 라우팅 스킬 이름 자체로 이미 명확해진 도메인 토큰은 생략합니다.
- **예시**: `openspec-apply-change.md`, `agent-asset-studio.md`

## 2. Naming Types by Skill Complexity (스킬 복잡도에 따른 유형별 명명 규칙)

| 스킬 복잡도 유형 | 대상 스킬 설명 | 파일명 형식 | 예시 |
| --- | --- | --- | --- |
| **Verb (동사형)** | 단일 작업을 수행하는 단순 스킬 | `<domain>-<verb>-<details>.md` | `coder-generate-code.md` |
| **Object (객체형)** | 여러 작업을 묶은 복합 스킬 객체 | `<domain>-<object>.md` | `task-manager.md` |
| **Place (장소형)** | 능력을 통합하는 라우팅/허브 스킬 | `<domain>-<details>-<place>.md` | `reviewer-console.md` |

*참고: `<place>` 토큰에는 물리적/가상 장소를 뜻하는 단어(예: `studio`, `console`, `hub`, `portal`, `workspace` 등)를 사용해야 합니다.*
