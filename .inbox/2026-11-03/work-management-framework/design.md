---
description: PR #284의 통합 STDD 설계 결정 기록입니다.
---

# STDD — Unified Change Design

## Decision

작업과 명세를 서로 독립된 모드로 취급하지 않는다. **단일 Change가 진행·의존·재개와 명세·테스트·구현·Review·완료를 통합**한다. 변경이 작으면 필수 파일을 늘리지 않고 같은 흐름을 축약한다.

```text
<work-root>/changes/<id>/work.md
<spec-root>/changes/<id>/specs/<domain-path>/spec.md   # 명세가 필요할 때
<spec-root>/specs/<domain-path>/spec.md                 # 검증 후 유지하는 정본
```

- `work.md`: 유일한 진행 상태 `todo/doing/done/cancelled`, 의존 Change ID, 완료 조건, 다음 행동.
- 명세 delta: 같은 Change ID 아래 필요한 도메인별 변경 근거. 여러 계층형 도메인을 허용한다.
- 완료: 관련 테스트·구현·Review와 필요한 최신 정본 반영까지 모두 확인해야 `done` 처리한다.
- 위치: 사용자 선택 root/ref. 다른 브랜치도 허용하지만 이중 상태나 cross-ref 원자성은 없다.
- 드랍: 별도 Task 객체·모드, mandatory 문서 단계, default 디렉터리, DB·CLI·manifest, 레거시 호환.

실행 지침의 정본은 `src/rulesync/.rulesync/skills/mols-stdd/`이며 이 문서는 결정 기록이다.
