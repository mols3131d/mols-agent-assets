# Chatbot Runtime Skills

업체가 제공하는 hosted chatbot runtime에서 **bundle과 runtime 기능을 활용해야 하는 skill**을 둡니다.

> [!NOTE]
> `skills-chatbot-runtime/`은 Agent Skills 표준의 공식 분류가 아니라, bundle·connector·tool·progressive loading을 활용하는 hosted chatbot harness를 위해 이 저장소가 만든 **비표준 repository-local target profile**입니다. 표준 Skill format과 호환되는 구조를 활용할 수 있지만 이 directory/profile 자체는 표준이 아닙니다.

## Placement

`skills-chatbot-runtime/`은 배포 capability가 다음 중 하나라도 해당할 때 사용합니다.

- flat 단일 skill 파일이 **4,000 tokens 이상**이라 여러 Markdown 파일로 분리해야 합니다.
- Markdown 한 파일만으로 실행 capability를 완결할 수 없습니다.
- 실행에 references, assets, scripts, images 같은 bundled resources가 필요합니다.
- host가 제공하는 tools, connectors, scripts, progressive loading 또는 기타 runtime 기능을 활용하는 것이 capability의 중요한 부분입니다.

`SKILL.md`는 activation boundary와 공통 계약을 유지하고, 상세 context는 필요한 경우에만 bundled file이나 runtime source에서 로드하는 방식을 우선합니다.

단일 Markdown 파일로 충분하고 4,000 tokens 미만이며 runtime 기능이 capability의 본질이 아니라면 `../skills-chatbot/`의 flat variant가 더 단순한 기본 선택입니다. 반대로 파일이 작더라도 `load-context-github`나 `load-context-notion`처럼 live connector/tool context를 읽는 것이 capability의 핵심이면 runtime placement가 자연스럽습니다.

Maintainer-only `docs/`, `evals/`, `tests/`, 개발용 validator는 배포 Skill과 분리할 수 있다면 그 존재만으로 runtime placement를 강제하지 않습니다. 작은 textual schema나 설정 예시는 별도 runtime resource보다 fenced code가 더 명확하면 인라인할 수 있습니다.

사용자의 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile도 검토합니다.

## Naming

주책임이 **상황별 context 로딩**이면 `load-context-<topic>` 이름을 사용합니다. 이 naming은 repository-local convention이며 Agent Skills 표준 요구사항이 아닙니다.

- 예: `load-context-github`, `load-context-notion`
- context-only Skill은 context discovery, selection, scoping, loading과 적용 경계까지만 소유합니다.
- context를 사용한 실제 구현, 작성, 검증, 리뷰, mutation과 최종 output은 downstream capability가 소유합니다.
- 실제 workflow 수행, artifact 생성, validation, transformation이 주책임이면 `load-context-`를 사용하지 않습니다.

## Target Variants

같은 capability가 `../skills/`, `../skills-chatbot/`, `skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.

runtime variant는 해당 host가 실제로 지원하는 references, assets, scripts, tools, connectors, progressive loading을 최대한 활용해 **초기 context와 실행 비용을 줄이고 필요한 capability를 늦게 로드**하도록 최적화합니다. 다른 profile의 제약을 그대로 가져와 runtime 이점을 포기하지 않습니다.
