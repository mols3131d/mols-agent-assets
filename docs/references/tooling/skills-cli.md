---
title: skills CLI
description: 외부 Agent Skill dependency를 도입할 때 skills CLI를 사용하는 기준과 이 저장소의 integration boundary
---

# skills CLI

이 저장소는 외부 Agent Skill dependency를 가져올 때 Rulesync를 유일한 설치 경로로 강제하지 않습니다.

## 사용 기준

핵심 판단은 **Rulesync를 거치는 것이 실제로 더 단순하고 충실한가**입니다.

Rulesync declarative source가 원본 구조와 필요한 resource를 그대로 보존하면서 설치·업데이트를 단순하게 만들면 Rulesync를 사용할 수 있습니다.

반대로 다음과 같이 Rulesync를 거치는 비용이 더 크면 `skills add`를 허용합니다.

- 원본 Skill을 사용하기 위해 별도 repackaging이나 adaptation이 필요함
- supporting resource, symlink, package layout 등을 보존하기 위해 우회가 필요함
- Rulesync 형식으로 가져오는 과정이 실제 dependency 사용보다 복잡함
- 변환이나 복제로 인해 upstream provenance와 update 경계가 흐려짐

단순히 Rulesync에서 기술적으로 처리할 수 있다는 이유만으로 Rulesync를 선택하지 않습니다. 외부 dependency는 **가장 작은 변환으로 upstream 계약을 충실하게 유지하는 경로**를 우선합니다.

## Repository Integration

- `skills` CLI version은 [`mise.toml`](../../../mise.toml)이 고정합니다.
- 이 저장소에서 직접 사용하는 외부 Skill과 revision은 setup command가 선언합니다.
- `skills`가 만드는 local lock은 재생성 가능한 dependency state이며 이 저장소의 작성 원본이 아닙니다.
- 외부 Skill의 본문을 repository-owned canonical asset처럼 복제하거나 수정하지 않습니다.
- upstream을 계속 authority로 둘 수 없는 수준의 변경이 필요하면 dependency 설치가 아니라 migration/adaptation으로 다시 판단합니다.

외부 자산의 authority 선택과 Rulesync migration 경계는 [작성 원본과 권한](../../development/source-authority.md)이 소유합니다.

## Official Sources

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [CLI usage](https://github.com/vercel-labs/skills#cli)

CLI option, 지원 agent, source format, update semantics는 저장소 문서에 복제하지 않고 current upstream을 확인합니다.

## Boundary

- Rulesync source, import, fetch, convert → [Rulesync](rulesync.md)
- tool version과 setup entrypoint → [mise](mise.md)
- 외부 자산의 authority와 adoption 판단 → [작성 원본과 권한](../../development/source-authority.md)
