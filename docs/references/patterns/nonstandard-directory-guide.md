# Nonstandard Directory Guide

비표준 repository-local directory나 asset surface는 이름만으로 의미가 충분히 드러나지 않을 수 있습니다.

그럴 때는 가까운 위치에 `README` 같은 작은 guide를 두어 **왜 존재하는지와 어떻게 사용하는지** 설명하는 것을 고려할 수 있습니다.

Guide에는 필요에 따라 다음 정도를 둘 수 있습니다.

- 목적과 범위
- 중요한 contract나 authority boundary
- repository-local convention
- 권장사항
- 주요 자산이나 하위 구조 안내
- 필요하면 entrypoint, index 또는 routing guidance

모든 항목이 필요한 것은 아닙니다. 사람이 repository 밖의 암묵적 지식 없이 해당 directory를 이해하는 데 필요한 만큼만 둡니다.

`README.md`, Markdown, 특정 section 구성은 필수가 아닙니다. 외부 standard나 vendor가 이미 의미를 정의한 directory라면 그 내용을 다시 설명할 필요도 없습니다.

## Related Patterns

다음 패턴은 비표준 repository-local directory나 surface를 대표적으로 사용할 수 있어, 필요하면 이 guide와 함께 적용할 수 있습니다.

| Pattern | Example surface | Why related |
| --- | --- | --- |
| [Artifact Inbox](artifact-inbox.md) | `inbox/`, scoped inbox | working / non-canonical surface의 범위와 lifecycle을 설명할 수 있음 |
| [Asset Configuration Surface](asset-configuration-surface.md) | `.configs/`, scoped config surface | custom extension point의 목적, authority, 적용 범위를 설명할 수 있음 |
| [Chatbot Asset Surface](chatbot-asset-directory.md) | `.chatbot/` 또는 다른 chatbot-only surface | chatbot-only asset, profile, Skill, command와 공용/벤더별 경계를 설명할 수 있음 |
| [Routing & Index Assets](routing-index-assets.md) | `route/` 또는 routing 전용 surface | routing surface와 underlying canonical source의 책임 경계를 설명할 수 있음 |
| [Skill Source Workspace](skill-source-workspace.md) | `.docs/`, `.tests/`, `.eval/` 같은 maintainer surface | runtime source와 maintainer-only subdirectory의 역할을 설명할 수 있음 |

이 표는 적용 대상의 고정 목록이 아닙니다. 비표준 surface의 의미가 이미 충분히 자명하면 별도 guide가 필요하지 않을 수 있습니다.

이 패턴은 비표준 directory를 만들 것을 권장하는 것이 아니라, **이미 필요한 비표준 surface를 설명 가능한 상태로 유지하기 위한 작은 보완책**입니다.
