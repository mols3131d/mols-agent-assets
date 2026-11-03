---
title: Skill Authoring Conventions
description: Agent Skill 작성·리팩터링에서 표준 외에 적용하는 mols의 패키지, description, context, naming과 metadata 관행을 확인할 때 사용합니다.
---

# Skill Authoring Conventions

공통 설계는 [Agent Asset Design Principles](../design-principles.md), 정확한 필드·패키지·발견·대상 계약은 [Agent Skills Specification](specification.md)에서 연결하는 공식 자료가 소유합니다. 여기에는 그 계약 이후에도 필요한 **mols의 Skill 전용 관행**만 둡니다.

## Package

실제 entrypoint가 정해지면 **single-file `SKILL.md`** 를 기본으로 합니다. 길이나 책임 수만으로 분리하지 않고 다음 요구가 있을 때만 보조 파일을 추가합니다.

- 조건부 세부 사항을 분리해야 context 비용이 줄어드는 경우
- 실행할 script·template·schema·static asset이 필요한 경우
- 런타임이 별도 resource로 읽어야 하는 자료가 있는 경우

보조 자료는 deployable Skill package 안에 두고, repository-only test·eval·maintainer 문서는 해당 host의 검증·문서 영역에 둡니다. 보조 파일이 또 다른 Skill entrypoint로 오인되지 않게 하며, 보조 파일 때문에 별도 manifest나 directory taxonomy를 만들지 않습니다. Chatbot/agent 또는 flat/runtime을 별도 Skill 유형으로 나누지 않습니다.

하나의 `SKILL.md`에서는 여러 최상위 `#` heading을 독립 책임 경계로 사용할 수 있습니다. `##` 이하는 부모 책임의 세부사항으로 두고 같은 깊이는 비슷한 추상화 수준을 유지합니다. 공통 불변조건은 가장 가까운 공통 owner에 한 번만 정의합니다. 파일 분리는 실제 loading·resource·ownership 이득을 기준으로 결정합니다.

## Description과 발견

`description`은 **capability와 적용 조건을 드러내는 routing contract**로 작성합니다.

- 필요한 경우 가까운 sibling Skill과 구별되는 제외 범위를 명시합니다.
- 선택에 영향을 주지 않는 prerequisite·fallback·handoff·실행 순서·검증 방법은 body에 둡니다.
- 다른 Skill의 이름만으로 선택 범위를 정의하지 않습니다. 명시적인 composition·delegation·handoff에서는 이름을 참조할 수 있습니다.

Description 최적화와 trigger eval은 [Specification](specification.md)의 creator guidance를 따릅니다. 대상의 listing·truncation·discovery 방식은 해당 런타임 계약이 소유합니다.

## Context와 naming

조건부 resource는 핵심 본문의 가까운 판단 지점에서 **언제 무엇을 읽는지** 알 수 있게 연결합니다. 일반적인 구성 방식은 [Progressive Context Routing](../../../../catalog/patterns/context-engineering/progressive-context-routing.md)을 따릅니다.

일반 명명 규칙은 [Naming](../naming.md)이 소유합니다. Skill의 주책임이 실행이 아니라 **도메인별 맥락 탐색·로드**일 때만 `<domain>-context` 확장을 사용할 수 있습니다. 구현·변경·검증·출력 생성이 주책임이면 사용하지 않습니다. 이 접미사는 별도 자산 유형이나 metadata·runtime capability를 뜻하지 않습니다.

## Target metadata와 검증

유효한 target-specific metadata는 현재 projection 대상이 아니어도 임의로 삭제하지 않습니다. 한 대상의 field를 공통 portable contract로 확대하지도 않습니다.

- Metadata의 의미는 대상 계약, source-to-target 보존·변환은 작성 프레임워크가 소유합니다.
- 작성 원본이 필요한 target requirement를 표현하지 못하면 shadow source·local superset을 만들지 않고 [Source Authority](../../source-authority.md)에 따라 원본 형식을 재검토합니다.
- Rulesync-managed Skill의 구조 검증은 [Validation](../../validation.md), behavioral evidence는 [Evaluation](../../evaluation.md)이 소유합니다. 정적 검사 통과를 전체 호환성이나 행동 품질의 증거로 보지 않습니다.

## Boundaries

- Instruction 행동 표현 → [Instruction Design](../instruction-design.md)
- Skill 표준·target/source 공식 문서 → [Specification](specification.md)
- Rulesync 작성 원본·workspace → [Rulesync](../../tooling/rulesync.md)
- 유지보수 문서 → [Agent Asset Management](../agent-asset-management.md#유지보수-문서)
- 테스트와 PR Gate → [Testing](../../testing.md)
