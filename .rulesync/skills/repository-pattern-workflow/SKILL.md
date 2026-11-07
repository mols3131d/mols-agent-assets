---
name: repository-pattern-workflow
description: >-
  이 저장소의 catalog/patterns/에 재사용 가능한 패턴 문서를 신설하거나 기존
  패턴을 개편·리뷰할 때 후보 판정, 중복 조사, category 선택, 작성, 검토와
  검증을 연결한다. 다른 프로젝트에서 패턴을 적용하는 작업이나 일반 문서·정책·
  Agent Asset 자체의 작성에는 사용하지 않는다.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Repository Pattern Workflow

`mols-agent-assets`의 `catalog/patterns/`에 작성할 **패턴 문서의 작업 흐름**을 조정한다. 패턴의 의미·구조·작성 원칙은 [Patterns](../../../catalog/patterns/README.md), 일반 문서 품질은 `docs/documentation/`, 저장소 변경과 검증은 해당 로컬 정책이 소유한다. 이 Skill은 그 규칙을 복제하거나 외부 소비자에게 적용하지 않는다.

## 후보 판정

1. 현재 저장소·ref·작업 범위와 적용되는 지침을 확인한다. 제안된 해결 방식이 여러 상황에 **참고·변형해 쓸 수 있는 문제 해결 패턴**인지 판단한다. 일회성 작업 기록은 `.inbox/`, 저장소의 강제 규칙은 해당 정책 문서, Agent Asset의 실행 계약은 해당 작성 원본에 둔다. 패턴으로 부적합하면 억지로 문서를 만들지 않는다.
2. [Catalog Index](../../../catalog/INDEX.tsv)와 관련 category의 README·기존 capsule을 조사한다. 같은 문제를 이미 다루면 기존 문서의 개선·연결로 충분한지 먼저 판단하고, 새 문서가 맡을 **고유한 문제와 책임**이 있을 때만 분리한다.
3. 패턴의 *primary problem*으로 소유 category 한 곳을 정한다. 다른 영역과의 관련성은 링크로 표현한다. 기존 category로 충분하면 새 분류를 만들지 않는다.

## 작성

4. 문제·사용 맥락·적용하지 않을 상황을 구분하고, 패턴이 성립하는 **core**와 바꿀 수 있는 구현 선택지를 정리한다. 필요한 주장과 예시는 실제 근거·기존 자료를 확인하고, 판단·가정·외부 사실을 혼동하지 않는다. 오래됐거나 중복되거나 향후 판단 가치가 낮은 reference는 추가하지 않는다.
5. 단순한 경우 category 아래 `<pattern-name>.md`로 시작한다. 독립된 파일·resource가 실제로 필요할 때만 bundle로 확장한다. 문서 구성은 문제의 성격에 맞게 선택하며 정해진 section이나 template을 강제하지 않는다.
6. 독자가 독립적으로 이해할 수 있게 문제, 핵심 메커니즘, 적용 조건과 선택지를 작성한다. **권장·예시·옵션**과 본질적 불변조건을 구분하며, 패턴을 repository policy나 필수 실행 절차로 서술하지 않는다. 실질적인 한계·trade-off·대안은 다루되 형식만 채우기 위한 위험·장점·확장은 만들지 않는다. 작성·가독성에는 `mols-documentation` 등 관련 전문 Skill을 선택해 사용한다.

## 리뷰와 마무리

7. [Patterns의 Review](../../../catalog/patterns/README.md#review)를 기준으로 독립성, category 적합성, 중복·소유권, 강제 규칙처럼 읽힐 위험, 선택의 유연성, 근거와 reference의 유효성을 검토한다. 패턴을 처음 접하는 독자와 실제 적용하려는 독자의 관점에서 불명확한 부분을 수정한다. 반복 개선이 필요한 경우 `mols-loops`를 조합하되 이 절차의 책임을 대체하지 않는다.
8. 해당 문서의 frontmatter·내부 링크·Markdown 형식을 검토한다. 패턴 원본을 변경했다면 `mise run generated sync`로 `catalog/INDEX.tsv`를 재생성하고 `mise run generated validate`로 drift를 확인한다. 인덱스를 직접 수정하지 않는다. 수행한 검사와 미검증 항목을 구분하고, 필요한 정본 반영 후 전용 branch·PR로 인계한다.

## 경계

- 이 워크플로는 **패턴 문서 작성**을 조정하며 패턴 자체를 프로젝트에 도입하거나 필수 규칙으로 승격하지 않는다.
- 외부 표준·도구 동작, Agent Asset 작성 계약, GitHub 권한·Merge 조건과 생성기 동작을 재정의하지 않는다.
- `.inbox/` 자료와 기존 capsule은 조사 근거일 수 있지만, 인박스를 정본으로 삼거나 기존 패턴을 자동으로 강제하지 않는다.
- 실행할 수 없는 검증은 통과로 표현하지 않는다. 권한이 없거나 원본·근거가 불충분하면 가능한 범위만 수행하고 이유와 다음 조치를 남긴다.
