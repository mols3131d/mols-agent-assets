---
description: 저장소 개발 판단에서 효과성, 운영 편의성, 단순성, 추상화와 변경 범위의 기본 원칙을 적용할 때 사용하는 상위 개발 정책입니다.
---

# Development Principles

이 문서는 이 repository의 개발 작업에서 여러 구현이 모두 유효할 때 **어떤 선택을 우선할지** 정하는 공통 판단 기준을 소유합니다.

정확성, 안전, 명시적 요구사항, 호환성, 표준과 repository의 구체적인 정책은 이 문서보다 우선합니다. 그 제약을 만족하는 선택지 사이에서는 다음 순서를 기본 판단축으로 사용합니다.

**효과성 → 운영 편의성 → 단순성 → 기술적 아름다움**

## Principles

- **운영 편의성을 기술적 아름다움보다 우선합니다.** 두 선택이 필요한 동작과 제약을 모두 만족한다면, 기술적으로 더 정교하거나 우아한 설계보다 배포·실행·관찰·진단·복구·변경이 쉬운 쪽을 우선합니다. 기술적 아름다움은 운영 비용을 늘리지 않거나 그 이익이 증가한 비용을 분명히 상쇄할 때 선택합니다.
- **복잡성이 필요성을 증명해야 합니다.** KISS와 YAGNI를 기본값으로 삼습니다. abstraction, configuration, extension point, dependency, automation, caching, concurrency, infrastructure 같은 복잡성을 먼저 추가하지 않습니다. 현재 요구사항, 실제 변동성, 관찰된 문제나 명확한 계약이 필요성을 증명할 때만 도입합니다.
- **DRY는 안정된 지식에 적용합니다.** 코드나 표현이 반복된다는 이유만으로 공통화를 강제하지 않습니다. 같은 개념이나 규칙이 하나의 책임으로 함께 변경되어야 할 때 authoritative owner를 하나로 모읍니다. 아직 공통 개념과 ownership이 안정되지 않았다면 작은 local duplication이 성급한 abstraction보다 낫습니다.
- **SRP는 크기가 아니라 변경 이유와 책임으로 나눕니다.** 함수·파일·모듈을 작게 만들기 위해 기계적으로 분리하지 않습니다. 책임, 소유자, lifecycle, 변경 이유가 실제로 다를 때 경계를 나눕니다. 반대로 독립적으로 변경되어야 하는 책임을 편의상 하나의 owner에 묶지 않습니다.
- **가장 작은 coherent change를 만듭니다.** line count가 아니라 conceptual surface를 최소화합니다. 요청한 변경 밖의 동작은 correctness, safety, compatibility 또는 명확한 단순화를 위해 필요하지 않다면 보존합니다. 관련 없는 cleanup과 speculative future-proofing을 함께 넣지 않습니다.
- **기존 시스템에 맞는 좋은 기본값을 우선합니다.** 기존 boundary, caller, data flow, failure behavior, test와 local convention을 먼저 확인합니다. 동등하게 좋은 선택지가 있다면 새로운 pattern이나 option을 추가하기보다 이미 정착한 방식을 사용합니다. 기존 방식이 실제 비용이나 제약의 원인이라면 관성적으로 보존하지 않습니다.
- **유지보수성과 운영 비용을 실제 비용으로 봅니다.** coupling, duplicated knowledge, hidden behavior와 이해·수정·검증·진단에 필요한 노력을 함께 평가합니다. pattern의 수, 추상화 정도나 기술적 순수함을 품질의 대리 지표로 사용하지 않습니다.
- **근거에 비례해 검증합니다.** 요구사항과 stylistic preference, 실제 failure와 hypothetical risk, 현재 요구와 미래 가능성을 구분합니다. 변경된 observable contract와 material failure path를 가장 저렴하고 충분한 수준에서 검증하며, 실행하지 않은 검증을 통과했다고 주장하지 않습니다.

## Boundaries

이 문서는 구체적인 실행 규칙을 다시 정의하지 않습니다.

- VCS와 Git → [VCS / Git](vcs-git.md)
- GitHub 협업과 merge → [GitHub](github.md)
- 작성 원본과 authority → [작성 원본과 권한](source-authority.md)
- 파일과 directory 배치 → [Repository Layout](repository-layout.md)
- Formatting → [Formatting](formatting.md)
- 구조·파생 계약 검증 → [Validation](validation.md)
- deterministic test와 PR Gate → [Testing](testing.md)
- Agent Asset behavior evidence → [Evaluation](evaluation.md)

더 좁은 정책이 구체적인 결정을 소유하면 해당 정책을 따릅니다. 이 문서는 그 사이에서 선택이 남을 때 적용하는 공통 판단 기준입니다.
