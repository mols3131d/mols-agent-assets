# 의사결정 기록(Decisions) 작성 가이드

이 문서는 에이전트 자산 및 프로젝트 아키텍처 의사결정을 기록하는 `decisions.md` 파일의 포맷과 작성 지침을 정의합니다.

## 파일 위치 및 규칙

- **위치**: `docs/skills/<skill-name>/decisions.md`
- **목적**: 설계 결정과 그에 따른 이유, 영향을 일관된 구조로 기록 및 공유

## 포맷 구조

`src/skills/mols-documents-studio/templates/decisions-lite.template.md`에 따라 다음 구조를 사용합니다.

```markdown
# Decisions

## Proposed

### {{decision_title}}

- {{decision_details}}
- **Reason:** {{reason}}
- **Impact:** {{impact}}

## Accepted

### {{decision_title}}

- {{decision_details}}
- **Reason:** {{reason}}
- **Impact:** {{impact}}

## Superseded

### {{decision_title}}

- {{decision_details}}
- **Reason:** {{reason}}
- **Impact:** {{impact}}

## Deprecated

### {{decision_title}}

- {{decision_details}}
- **Reason:** {{reason}}
- **Impact:** {{impact}}
```

## 작성 원칙

1. **헤더 및 목록 구조**: 테이블 형식을 지양하고, `### {{decision_title}}` 헤더와 `-` 글머리기호 형태를 사용합니다.
2. **필수 메타데이터**: 각 결정 하위에 상세 설명(`{{decision_details}}`), 의사결정 동기/이유(`**Reason:**`), 미치는 영향(`**Impact:**`)을 반드시 작성합니다.
3. **상태 관리**: 상태에 맞춰 Proposed, Accepted, Superseded, Deprecated 섹션 하위로 배치합니다.
