---
title: 공통 레퍼런스
description: 여러 자산과 workflow가 공유하는 최소 repository-local convention, principle, authoring, tooling reference
---

# 공통 레퍼런스

`common/`은 둘 이상의 자산이나 repository workflow에서 같은 의미로 재사용되고, upstream 또는 더 좁은 feature owner가 없는 **durable knowledge**만 소유합니다.

문서 수가 적은 현재는 flat structure를 기본으로 합니다. 분류용 directory는 여러 독립 문서가 실제로 생겨 탐색 비용을 줄일 때만 추가합니다.

| 문서 | 책임 |
| --- | --- |
| [Rulesync](rulesync.md) | Rulesync와 이 저장소의 workspace·source 경계 |
| [Naming](naming.md) | flat namespace의 관리와 충돌 방지 |
| [CHATBOT Compatibility](chatbot-compatibility.md) | chat runtime의 누락된 harness behavior 보정 |
| [Design Principles](design-principles.md) | YAGNI, SRP, DRY, KISS, Progressive Disclosure 판단 |
| [Instruction Authoring](instruction-authoring.md) | LLM이 적용할 behavioral instruction 작성 |
| [Front Matter CMS](front-matter-cms.md) | repository configuration과 official source routing |

사람용 일반 문서 작성 원칙은 `load-context-human-writing`이 소유하며 여기서 별도 복제하지 않습니다. Skill-specific reference는 `../skills/`가 소유합니다.

새 common 문서를 만들기 전에 **여러 책임에서 정말 같은 의미로 재사용되는지** 확인합니다. 미래의 공통화를 예상해 abstraction이나 taxonomy를 미리 만들지 않습니다.
