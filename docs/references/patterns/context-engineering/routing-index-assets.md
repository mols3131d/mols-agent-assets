---
description: 문서·Agent Asset·코드 같은 큰 정보 표면에 별도 index/router를 두어 후보를 찾고 현재 task에 맞는 다음 context를 선택하게 할 때 참고하는 pattern으로, index와 routing의 역할·signal·authority boundary를 다룹니다.
---

# Routing & Index Assets

필요한 정보나 자산으로 빠르게 연결하고 **현재 작업에 필요한 context만 효율적으로 선택·로드**하기 위해, 내용 자체와 분리된 discovery / routing asset을 두는 패턴입니다.

Agent Skill이나 Rule뿐 아니라 문서, 코드, 설정, 연구 자료처럼 탐색 가능한 정보 표면에도 적용할 수 있습니다.

## Purpose

전체 source를 처음부터 읽지 않고도 어떤 후보가 있고 무엇을 더 확인하거나 선택해야 하는지 판단할 수 있게 해, 탐색 비용과 불필요한 context load를 줄입니다.

## Core

Index와 Routing은 겹칠 수 있지만 목적은 다릅니다.

- **Index**는 후보의 identity, 종류, 위치처럼 탐색에 필요한 정보를 제공해 **무엇이 어디에 있는지** 빠르게 파악하게 합니다.
- **Routing**은 task, domain, topic, applicability 같은 selection signal을 제공해 **현재 context에서 어떤 후보나 다음 surface를 선택할지** 판단하게 합니다.
- Path나 file list만으로도 유효한 Index가 될 수 있지만, semantic selection이 필요한 Routing이라면 소비자가 후보를 실제로 고를 수 있을 만큼의 signal이 필요합니다.
- Routing/index layer는 underlying source나 management authority를 대신하지 않고 **discovery, selection, navigation, context routing**에 집중합니다.
- 포맷, filename, directory 이름이나 배치보다 탐색 효율과 소비 주체에 맞는 표현을 우선합니다.

Routing signal의 형태는 고정하지 않습니다. Description, trigger, `when to use`, tag, rule, category나 사람이 읽는 짧은 설명처럼 현재 후보를 구분하고 선택하기에 충분한 표현이면 됩니다.

## Route Targets

Routing의 다음 대상은 repository 안의 canonical file에 한정되지 않습니다.

필요에 따라 다음과 같은 surface로 연결할 수 있습니다.

- repository-local file이나 directory;
- 외부 repository, package, URL 또는 catalog;
- framework나 runtime이 제공하는 native discovery/access surface;
- tool-managed source, registry 또는 management surface;
- 더 구체적인 routing/index asset.

**Discovery location, canonical authority와 runtime access location은 같을 수도 있고 다를 수도 있습니다.** Routing 정보가 generated projection이나 설치된 copy를 가리킨다는 이유만으로 그 위치를 authoring authority로 취급하지 않습니다. Authority 차이가 routing 판단에 중요하다면 소비자가 올바른 owner나 next surface에 도달할 만큼만 드러냅니다.

Installation, generation, synchronization, update나 다른 mutation은 이 패턴의 책임이 아닙니다. 필요하면 Routing에서 해당 작업을 소유하는 tool이나 capability로 연결할 수 있습니다.

## Naming and Layout

Directory와 filename은 이 패턴의 고정 schema가 아닙니다. 아래 이름은 **권장 또는 예시**이며 repository 구조, consumer, runtime 또는 기존 convention에 맞게 바꿀 수 있습니다.

| Form | Status | Typical use |
| --- | --- | --- |
| `route/` | recommendation | 별도 convention이 없을 때 shared 또는 repository-wide routing surface |
| `INDEX.*` | recommendation | 가까운 directory의 내용을 빠르게 훑기 위한 index |
| `ROUTE.md` | example | 사람이 읽기 쉬운 최소 entry router |
| `.agents/route/` | example | agent에만 필요한 routing을 별도 scope로 둘 때 |
| `.chatbot/route/` | example | chatbot에만 필요한 routing을 별도 scope로 둘 때 |

이 status는 이름 선택을 돕기 위한 설명일 뿐 compliance level을 뜻하지 않습니다. Framework, vendor 또는 repository가 더 적합한 native convention을 제공하면 그 이름과 위치를 사용할 수 있습니다.

작은 범위에서는 가까운 directory에 index 하나만 둘 수 있습니다.

```text
<dir>/
├─ INDEX.tsv
└─ ...
```

Repository 수준에서는 routing 전담 surface를 둘 수 있습니다.

```text
route/
├─ ROUTE.md
├─ docs.jsonl
├─ code.tsv
└─ topic-*.md
```

소비 주체에 따라 routing이 실제로 달라진다면 scope를 드러내는 directory를 사용할 수도 있습니다.

```text
repository/
├─ route/             # shared or repository-wide routing
├─ .agents/
│  └─ route/          # agent-oriented routing
└─ .chatbot/
   └─ route/          # chatbot-oriented routing
```

`.agents/route/`와 `.chatbot/route/`는 vendor 표준이나 자동 discovery path를 뜻하지 않습니다. 같은 패턴을 `routing/`, `index/`, vendor-native surface 또는 다른 project-local 이름으로 구현할 수도 있습니다.

File format도 목적에 맞게 선택합니다. `md`, `jsonl`, `tsv`, `json`, `yaml` 등 사람이 읽는 navigation과 machine-readable discovery에 적합한 표현을 사용할 수 있습니다.

별도 routing/index asset의 관리 비용을 정당화하기 어려운 작은 범위라면, entrypoint나 가까운 guide의 table, bullet, prose로 routing 정보를 직접 제공하는 편이 더 단순할 수 있습니다.

## Automation

가능하면 routing/index 정보를 수동으로 중복 작성하기보다 이미 존재하는 metadata를 활용한 자동화를 권장합니다.

- Markdown frontmatter
- manifest
- directory metadata
- file metadata
- 기타 구조화된 source

안정적으로 추출할 수 있는 정보는 script나 generator로 index와 routing asset을 생성·갱신할 수 있습니다. 사람이 직접 관리하는 정보는 자동으로 복원하기 어려운 routing intent나 선택 기준처럼 필요한 차이만 남기는 편이 좋습니다.

Generated routing/index는 underlying source나 tool-managed asset의 authority를 가져오지 않습니다. 생성 원천과 projection의 관계가 중요하다면 그 경계를 유지합니다.

## Extensions

규모가 커지면 하나의 index에서 domain/topic별 router, 계층형 route, generated index 등으로 확장할 수 있습니다. 반대로 작은 repository에서는 단일 index나 inline router만으로 충분할 수 있습니다.

Shared routing과 consumer-specific routing을 함께 둘 때는 실제 선택 기준이 다른 경우에만 분리하는 편이 좋습니다. 같은 candidate와 같은 routing intent를 여러 directory에 반복하지 않습니다.

## Considerations

- Routing asset이 stale하면 잘못된 후보나 surface를 선택할 수 있으므로 source나 관리 방식이 바뀔 때 함께 갱신하거나 검증하는 방법을 고려합니다.
- 사람이 읽는 탐색과 agent가 소비하는 context routing은 같은 source를 공유하거나 서로 다른 projection을 사용할 수 있습니다.
- 외부 candidate를 발견했다고 해서 현재 runtime에 설치·활성화·접근할 수 있다고 가정하지 않습니다.
- Generated 또는 installed asset이 존재한다는 이유만으로 그 위치를 canonical authority로 간주하지 않습니다.
- 자동화 비용이 수동 관리보다 크다면 단순한 수동 index나 inline routing이 더 적합할 수 있습니다.
- Directory나 filename이 널리 쓰이는 형태라는 이유만으로 runtime이 자동 discovery한다고 가정하지 않습니다.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Chatbot Repository Entrypoint](chatbot-repository-entrypoint.md) | Chatbot entrypoint의 inline routing이 커지거나 reusable/generated routing surface로 분리할 가치가 있을 때 이 패턴을 사용할 수 있습니다. |
| [Nonstandard Directory Guide](../documentation/nonstandard-directory-guide.md) | `route/` 같은 repository-local routing surface에 local guide가 필요할 때 참고합니다. |

## Boundary

Routing/index asset은 underlying 문서·코드·정책·동작이나 tool-managed asset의 canonical owner가 되지 않습니다. 다만 **routing에 필요한 identity, 위치, 분류, 선택 기준, routing intent와 next route**는 이 layer가 소유할 수 있습니다.

이 패턴은 특정 schema, generator, directory, filename, format, source type, manager taxonomy 또는 routing algorithm을 강제하지 않습니다. 예시 이름과 surface는 discovery/routing intent를 설명하기 위한 대표적인 형태이며, 실제 적용은 framework, runtime, source authority와 repository convention에 맞게 조정합니다.
