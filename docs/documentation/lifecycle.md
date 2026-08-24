---
description: repository에 남기는 durable knowledge, working artifact, archive와 Git history의 역할과 승격 기준을 정의합니다.
---

# Knowledge Lifecycle

Repository에 남기는 정보는 현재 authority와 보존 목적에 따라 구분합니다.

| Kind | Destination | Meaning |
| --- | --- | --- |
| Current durable knowledge | canonical source 또는 해당 policy/document owner | 현재와 미래의 판단을 계속 바꾸는 rule, decision, invariant, recovery knowledge와 non-obvious rationale |
| Working / handoff artifact | inbox current surface | 아직 canonical하지 않은 report, review, research, handoff, generated output와 임시 note |
| Retained non-canonical artifact | inbox archive surface | 현재 정본은 아니지만 artifact 원문 자체를 다시 참고할 가치가 있는 기록 |
| Repository change history | Git history와 PR | 변경 과정, 완료된 migration, 이전 canonical state와 일반 작업 이력 |

## Rules

- Durable knowledge를 inbox나 archive에만 남겨 current authority를 숨기지 않습니다.
- Working artifact에서 durable knowledge가 생기면 적절한 canonical source 또는 documentation owner로 승격합니다.
- 단순 과거 상태나 일반 작업 로그를 durable documentation 또는 archive에 중복 보관하지 않습니다.
- Archive는 artifact 원문 자체의 재사용 가치가 있을 때만 사용합니다.
- Archived artifact는 current policy나 guidance로 자동 로드하거나 지속 갱신하지 않습니다.
- Git history는 repository가 **어떻게 변했는지**를 보존하는 기본 기록입니다.

Inbox surface의 실제 path와 directory contract는 [`inbox/README.md`](../../inbox/README.md)가 소유합니다.
