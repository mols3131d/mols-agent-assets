# Chatbot Runtime Skills

업체가 제공하는 hosted chatbot runtime에서 **bundle과 runtime 기능을 활용해야 하는 skill**을 둡니다.

## Placement

`skills-chatbot-runtime/`은 다음 중 하나라도 해당할 때 사용합니다.

- flat 단일 skill 파일이 **4,000 tokens 이상**이라 여러 Markdown 파일로 분리해야 합니다.
- Markdown 한 파일만으로 capability를 완결할 수 없습니다.
- references, assets, schemas, scripts, images 같은 bundled files가 필요합니다.
- host가 제공하는 tools, scripts, progressive loading 또는 기타 runtime 기능을 활용하는 편이 효율적입니다.

`SKILL.md`는 activation boundary와 공통 계약을 유지하고, 상세 context는 필요한 경우에만 bundled file에서 로드하는 방식을 우선합니다.

단일 Markdown 파일로 충분하고 4,000 tokens 미만이면 `../skills-chatbot/`의 flat variant가 더 단순한 기본 선택입니다.

사용자의 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile도 검토합니다.

## Naming

주책임이 **상황별 context 로딩**이면 `load-context-<topic>` 이름을 사용합니다. `load-context-github`처럼 runtime에서 references나 tools를 사용하더라도 핵심 responsibility가 context 주입이면 같은 prefix를 유지합니다.

실제 workflow 수행, artifact 생성, validation, transformation이 주책임이면 `load-context-`를 사용하지 않습니다.

## Target Variants

같은 capability가 `../skills/`, `../skills-chatbot/`, `skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.

runtime variant는 해당 host가 실제로 지원하는 references, assets, scripts, tools, progressive loading을 최대한 활용해 **초기 context와 실행 비용을 줄이고 필요한 capability를 늦게 로드**하도록 최적화합니다. 다른 profile의 제약을 그대로 가져와 runtime 이점을 포기하지 않습니다.
