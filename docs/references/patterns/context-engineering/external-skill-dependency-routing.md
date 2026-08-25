---
description: 외부 Agent Skill dependency를 사용할 때 Rulesync declarative sources와 skills CLI 중 어떤 경로가 source semantics·lock·update·runtime delivery를 더 충실하게 보존하는지 판단할 때 참고하는 pattern입니다.
---

# External Skill Dependency Routing

외부 Agent Skill은 **도구를 하나로 통일하기보다 원본의 동작과 설치·업데이트 흐름을 가장 잘 보존하는 경로로 관리**합니다.

## Purpose

표준 Agent Skill이라도 Skill directory만으로 완결되는 경우가 있는 반면, directory 밖의 resource나 vendor별 설치 절차까지 필요한 경우도 있습니다. `SKILL.md`를 읽을 수 있다는 사실만으로 적합한 dependency 경로라고 판단하지 않습니다.

Rulesync와 skills CLI는 경쟁 도구가 아니라 서로 다른 상황에 맞는 선택지입니다.

## Core

- 외부 upstream을 계속 원본으로 유지할 자산은 이 저장소의 작성 원본으로 흡수하지 않고 dependency로 관리합니다.
- 같은 dependency의 선택과 lock/update는 한 경로에서만 관리합니다.
- 도구의 지원 여부보다 **필요한 파일과 동작이 빠짐없이 보존되는지**, **원하는 설치·업데이트 방식과 잘 맞는지**를 먼저 봅니다.
- 같은 결과를 보존한다면 더 단순한 경로를 선택합니다.

## Typical Routing

| 상황 | 보통 선택 | 이유 |
| --- | --- | --- |
| Skill directory가 필요한 resource를 자체 포함하고 Rulesync가 손실 없이 가져올 수 있음 | Rulesync declarative sources | 외부 Skill을 Rulesync의 source·lock·install·generate 흐름에서 함께 관리하기 쉬움 |
| 저장소가 이미 Rulesync로 여러 target에 자산을 생성하고 외부 Skill도 같은 흐름에 두고 싶음 | Rulesync declarative sources | 기존 Rulesync 배포 흐름을 그대로 활용할 수 있음 |
| 표준 Skill을 runtime의 project/global Skill 위치에 직접 설치하는 것이 목적 | skills CLI | target, scope, install, update를 Agent Skill 설치 흐름에서 직접 다룸 |
| Rulesync 변환이나 generation 없이 여러 agent에 표준 Skill을 설치하고 싶음 | skills CLI | 불필요한 중간 표현을 만들지 않음 |
| Skill 밖의 resource, symlink, 별도 agent·command·extension 또는 source-native installer가 필요함 | 설치 결과를 먼저 검증 | 어느 도구도 원본 동작을 온전히 보존하지 못하면 source-native 경로를 유지할 수 있음 |

Rulesync를 쓰고 있다는 이유만으로 모든 외부 Skill을 Rulesync source로 옮기지 않습니다. 반대로 표준 Agent Skill이라는 이유만으로 항상 skills CLI를 선택하지도 않습니다.

## Rulesync Example

다음처럼 Skill directory 자체가 실행에 필요한 내용을 완결하고 저장소가 Rulesync generation을 사용한다면 declarative source가 자연스럽습니다.

```text
upstream/
└─ skills/
   └─ review-pr/
      ├─ SKILL.md
      ├─ references/
      └─ scripts/
```

```text
rulesync.jsonc
    ↓
rulesync install
    ↓
rulesync.lock
    ↓
rulesync generate
    ↓
target runtime
```

구체적인 source 형식과 lock/update 동작은 Rulesync의 현재 공식 문서를 따릅니다.

## skills CLI Example

Rulesync authoring이나 generation이 필요하지 않고 표준 Skill을 runtime이 기대하는 위치에 직접 설치하는 것이 핵심이라면 skills CLI가 더 단순할 수 있습니다.

```text
upstream Skill
    ↓
skills add
    ↓
project or global Skill installation
    ↓
skills update
```

Project-scoped dependency에서는 `skills-lock.json` 같은 local lock이 설치 상태의 일부가 될 수 있습니다. Global 설치까지 같은 파일 구조로 일반화하지 않고 skills CLI의 현재 동작을 따릅니다.

## Fidelity Check

도구를 정하기 전에 **설치된 Skill이 실제로 필요한 자산과 동작을 모두 갖는지** 확인합니다.

예를 들어 다음 구조는 `SKILL.md` 하나만 가져와서는 충분하지 않을 수 있습니다.

```text
upstream/
├─ skills/humanize/
│  ├─ SKILL.md
│  └─ references -> ../../shared/references
├─ shared/references/
├─ agents/
├─ scripts/
└─ install.sh
```

다음 중 하나라도 빠지면 설치가 성공했더라도 원본 동작이 보존됐다고 보지 않습니다.

- Skill이 참조하는 resource가 설치 결과에도 존재하는가?
- Skill directory 밖의 script·agent·extension이 실제 동작에 필요한가?
- Symlink와 package-relative path가 설치 과정에서 보존되는가?
- Target과 scope가 upstream이 의도한 방식과 같은가?
- Update 후에도 같은 dependency와 필요한 resource가 유지되는가?

Rulesync나 skills CLI로 이 조건을 충족할 수 없다면 source-native installer를 유지하거나 upstream package가 더 self-contained해질 때까지 통합을 미룰 수 있습니다.

## References

- [Rulesync Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/main/docs/guide/declarative-sources.md)
- [skills CLI](https://github.com/vercel-labs/skills)
- [Agent Skills Specification](https://agentskills.io/specification)

## Boundary

이 패턴은 특정 repository의 mandatory dependency policy나 각 도구의 전체 CLI contract를 정의하지 않습니다. 실제 지원 범위, lock/update와 target 동작은 사용 시점의 upstream tool과 runtime을 확인합니다.
