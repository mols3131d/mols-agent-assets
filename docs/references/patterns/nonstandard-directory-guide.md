# Nonstandard Directory Guide

Repository에 표준이나 외부 convention만으로 의미를 알기 어려운 **repository-local directory 또는 asset surface**를 둘 때, 그 위치에 README 같은 guide를 함께 두어 목적과 사용법을 설명하는 패턴입니다.

Guide의 핵심은 directory를 표준화하는 것이 아니라 **repository 밖의 암묵적 지식 없이도 그 surface의 의미와 운영 방식을 이해할 수 있게 하는 것**입니다.

## Purpose

비표준 directory는 repository 안에서는 유용한 책임 경계가 될 수 있지만, 이름이나 위치만으로 다음을 알기 어려울 수 있습니다.

- 왜 이 directory가 존재하는가
- 무엇을 여기 두고 무엇은 다른 owner에 두는가
- 내부 자산이 어떤 관계를 가지는가
- 반드시 지켜야 하는 계약이 있는가
- repository-local 관행이나 권장사항이 있는가
- 어디서부터 읽거나 어떤 자산을 선택해야 하는가

이런 정보가 코드 밖의 개인 지식이나 과거 대화에만 남으면 유지보수와 onboarding 비용이 커질 수 있습니다. 가까운 위치의 guide는 그 directory 자체에 필요한 durable context를 보존하는 데 도움이 됩니다.

## Core

```text
nonstandard repository-local surface
        +
nearby explanatory guide
        ↓
purpose / scope / local rules / navigation을 필요에 맞게 설명
```

Guide는 특정 schema를 채우는 문서가 아닙니다. **그 directory를 안전하고 일관되게 이해·사용하는 데 실제로 필요한 내용만** 소유합니다.

`README.md`는 사람이 발견하기 쉬운 대표 구현이지만 필수 filename이나 format은 아닙니다. 다른 guide, entry document, manifest 또는 catalog가 같은 책임을 맡을 수도 있습니다.

## Possible Responsibilities

Guide에는 필요에 따라 다음 책임을 둘 수 있습니다.

- **Introduction** — directory가 왜 존재하고 어떤 문제를 해결하는지
- **Scope** — 무엇을 포함하고 무엇은 다른 canonical owner에 남기는지
- **Contract** — 의미나 안전한 사용을 위해 지켜야 하는 경계
- **Conventions** — naming, layout, lifecycle, loading 같은 repository-local 관행
- **Recommendations** — 유용하지만 상황에 따라 바꿀 수 있는 권장 기본값
- **Assets** — 내부 자산이나 하위 surface의 책임
- **Usage** — 대표적인 사용 방식이나 workflow
- **Maintenance** — 추가·변경·정리할 때 알아야 할 기준
- **Compatibility / Authority** — 외부 standard, vendor-native source 또는 다른 canonical owner와의 관계

이 목록은 고정 section schema가 아닙니다. Directory의 역할이 단순하면 소개와 scope 몇 줄만으로 충분할 수 있습니다.

### Contract, Convention, Recommendation

성격이 다른 내용을 함께 둘 때는 강도를 구분하면 해석 비용을 줄일 수 있습니다.

```text
contract
→ 지켜야 하는 의미·권한·안전 경계

convention
→ 이 repository가 일관성을 위해 채택한 관행

recommendation
→ 상황에 맞게 바꿀 수 있는 권장 선택
```

모든 directory에 세 종류가 모두 필요한 것은 아닙니다.

## Entrypoint and Navigation

설명 guide는 필요하면 동시에 **entrypoint, index, catalog 또는 routing guide** 역할을 겸할 수 있습니다.

예를 들어 README에서:

- 먼저 읽을 자산을 안내하거나
- 작업 종류에 따라 다른 하위 문서로 route하거나
- 주요 파일과 책임을 간단히 소개할 수 있습니다.

반대로 별도 entrypoint나 자동 discovery mechanism이 이미 있다면 guide는 설명과 local policy만 소유해도 됩니다.

설명 역할과 entrypoint 역할은 서로 대체하거나 배제하지 않습니다. 같은 문서가 둘을 겸할지 분리할지는 directory의 규모와 사용 방식에 따라 선택합니다.

## Example

예를 들어 repository-local `.chatbot/` surface가 있다면 다음과 같은 README를 둘 수 있습니다.

```markdown
# Chatbot Assets

이 directory는 coding agent와 다른 chatbot-only guidance와 compatibility asset을 보관합니다.

## Scope

공통 repository behavior는 기존 canonical owner에 둡니다. 이곳에는 chatbot-specific delta만 둡니다.

## Contract

Permission-like profile은 실제 runtime permission을 부여하지 않습니다. 실제 capability는 runtime의 permission mechanism이 소유합니다.

## Conventions

현재 task에 필요한 profile, Skill 또는 command만 선택적으로 로드합니다.

## Recommendations

공통 guidance를 복제하기보다 기존 owner로 route하는 구성을 권장합니다.

## Start Here

현재 작업에 맞는 내부 자산을 선택하고, 공통 repository guidance가 필요하면 기존 canonical owner로 이동합니다.
```

이는 `.chatbot/`이나 위 section 구성을 요구하는 예시가 아닙니다. 다른 비표준 directory에도 같은 원리를 상황에 맞게 적용할 수 있습니다.

## Recommended Default

비표준 directory를 새로 도입했을 때 **이름과 주변 context만으로 목적과 사용법이 충분히 자명하지 않다면**, 가까운 위치에 작은 guide를 두는 것을 우선 고려할 수 있습니다.

처음에는 다음 정도만 있어도 충분합니다.

```markdown
# <Surface Name>

<왜 존재하는지>

## Scope

<무엇을 두고 무엇은 두지 않는지>
```

실제 계약, 관행, 권장, navigation 요구가 생길 때만 확장합니다.

## Considerations

- 모든 custom directory에 README를 기계적으로 추가하면 오히려 maintenance noise가 될 수 있습니다.
- Child asset의 상세 behavior를 README에 복제하면 drift가 생길 수 있으므로 surface-level 의미와 관계에 집중하는 편이 좋습니다.
- 외부 vendor나 framework가 이미 directory semantics를 정의한다면 그 standard를 README가 다시 정의하지 않습니다. 필요한 local delta만 설명할 수 있습니다.
- README가 index를 겸하더라도 파일 목록 전체를 수동으로 복제할 필요는 없습니다. 안정적인 탐색 기준만 안내하는 편이 나을 수 있습니다.
- Directory가 사라지거나 책임이 바뀌면 guide도 같은 ownership boundary에서 함께 정리합니다.

## Boundary

이 패턴은 새로운 비표준 directory를 만들 것을 권장하는 패턴이 아닙니다. **이미 필요해서 존재하는 repository-local surface를 설명 가능한 상태로 유지하는 방법**을 다룹니다.

또한 `README.md`, Markdown, 특정 section 이름, directory 위치 또는 naming convention을 강제하지 않습니다.
