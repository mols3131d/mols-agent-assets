---
description: RPI Plan을 설계하거나 변경할 때 보존해야 할 핵심 결정사항을 정리한 maintainer 문서입니다.
---

# RPI Plan

RPI Skill의 Plan을 수정할 때 보존할 본질만 정리합니다. Runtime behavior의 canonical source는 `SKILL.md`입니다.

## Decisions

- Plan은 **Research와 Active Scope를 실행 가능한 다음 행동으로 변환하는 것**입니다.
- Goal을 향해 필요한 가장 작은 coherent path를 만듭니다.
- Consequential Work에는 Plan이 선행해야 합니다.
- Plan은 ordered Work, material assumptions, acceptance와 validation을 충분히 포함해야 합니다.
- Scope나 material premise가 바뀌면 affected Plan을 다시 검토하고 필요한 부분만 수정합니다.
- Plan은 방법론적 근거이지 operational permission이 아닙니다. 실제 side effect 권한은 별도로 확인합니다.
- 이미 유효한 Plan을 의식적으로 재사용하고 ceremony를 위해 다시 만들지 않습니다.

## Output

Plan artifact에는 Research/Scope와의 lineage, 결정된 Work 순서, acceptance와 validation만 명확히 남깁니다. 불필요한 설명이나 실행 로그를 계획에 섞지 않습니다.
