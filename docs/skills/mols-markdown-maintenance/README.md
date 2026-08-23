# mols-markdown-maintenance Maintainer Docs

`mols-markdown-maintenance`는 결정론적 Markdown 유지보수 방식의 선택과, 선택한 Markdown backend가 이미 제공하지 않는 작은 local delta를 소유합니다.

## Invariants

- Repository-native Markdown 도구와 설정이 요청된 동작을 이미 소유하면 이를 우선합니다.
- 표준 formatting, heading check와 link check는 로컬 wrapper script 대신 rumdl을 직접 사용합니다.
- Custom runtime code는 frontmatter schema validation과 frontmatter 기반 index generation으로 제한합니다.
- 의미가 달라질 수 있는 경우 deterministic validation이나 parsing을 LLM fallback으로 대체하지 않습니다.
- 필요한 도구가 없으면 명시적으로 실패합니다.
- Generated index는 projection으로 유지하며 source Markdown/frontmatter에서 다시 생성합니다.
- 의존성은 최소화하고 로컬 결정론적 동작으로 필요성을 설명할 수 있어야 합니다.

## Maintenance

변경될 수 있는 rumdl rule/configuration reference를 이 문서에 복제하지 않습니다. 여기에는 소유권 경계와 local invariant만 유지하고, backend의 정확한 semantics가 중요할 때는 현재 upstream authority를 확인합니다.
