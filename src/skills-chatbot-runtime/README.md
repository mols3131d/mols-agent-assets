# Chatbot Runtime Skills

업체가 제공하는 hosted chatbot runtime에서 **bundle과 runtime 기능을 활용해야 하는 Skill**을 둡니다.

> [!NOTE]
> `skills-chatbot-runtime/`은 Agent Skills 표준의 공식 분류가 아니라, bundle·progressive loading·host-specific runtime surface가 필요한 hosted chatbot harness를 위해 이 저장소가 만든 **비표준 repository-local target profile**입니다. 표준 Skill format과 호환되는 구조를 활용할 수 있지만 이 directory/profile 자체는 표준이 아닙니다.

## Placement

`skills-chatbot-runtime/`은 배포 capability가 다음 중 하나라도 해당할 때 사용합니다.

- flat 단일 Skill 파일이 **4,000 tokens 이상**이라 여러 Markdown 파일로 분리해야 합니다.
- Markdown 한 파일만으로 실행 capability를 완결할 수 없습니다.
- 실행에 `references/`, `assets/`, `scripts/`, images 같은 bundled resources가 필요합니다.
- host-specific tool schema, integration resource, progressive loading, script/runtime package처럼 **단일 Markdown 밖의 runtime surface**가 capability에 필요합니다.

`SKILL.md`는 activation boundary와 공통 계약을 유지하고, 상세 context는 필요한 경우에만 bundled file이나 runtime source에서 로드하는 방식을 우선합니다.

단일 Markdown 파일로 충분하고 4,000 tokens 미만이며 별도 runtime surface가 필요하지 않다면 `../skills-chatbot/`의 flat variant가 더 단순한 기본 선택입니다. Skill이 host가 이미 제공하는 tool이나 connector 사용을 지시한다는 사실만으로 runtime placement를 강제하지 않습니다.

사용자의 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 repository root의 `.agentsmesh/skills/` portable coding-agent profile을 검토합니다.

## Package Surfaces

Directory-based hosted-runtime Skill package에는 **실행 또는 의도적인 distributable self-validation에 필요한 surface만** 둡니다.

```text
skill-name/
├─ SKILL.md
├─ references/          # runtime when needed
├─ scripts/             # runtime when needed
├─ assets/              # runtime when needed
├─ templates/           # runtime when needed
├─ tests/               # only when package contract intentionally includes them
└─ ...                  # target-required runtime surface
```

- runtime이 필요로 하는 resource는 package 안의 명시적 runtime surface가 소유합니다.
- maintainer-only 문서를 runtime dependency로 만들지 않습니다.
- package-local `.docs/`를 maintainer documentation convention으로 사용하지 않습니다.
- `.evals/`, `.tests/` 같은 validation/development surface는 해당 target·package contract가 실제로 필요할 때만 사용하며 maintainer docs와 같은 개념으로 취급하지 않습니다.

## Maintainer Docs

특정 hosted-runtime Skill이 복잡하거나 훼손 위험이 크고 durable decision, baseline,
maintenance 또는 recovery 지식을 별도로 보존할 가치가 있을 때만 repository root의
`docs/skills/<skill-name>/`에 maintainer-only 문서를 둡니다.

이 surface는 **선택적**입니다.

- 단순하고 self-explanatory한 Skill에는 만들지 않습니다.
- 임시 조사, 작업 로그, 쉽게 재생성되는 상태는 durable docs로 승격하지 않습니다.
- runtime-required 문서는 `references/` 등 package runtime surface에 둡니다.
- maintainer docs의 존재만으로 runtime profile을 선택하지 않습니다.
- baseline이 필요하면 `docs/skills/<skill-name>/baseline/`을 사용할 수 있지만 mandatory schema가 아닙니다.

이 repository-root convention은 `.agentsmesh/skills/`과 hosted-runtime Skill 모두에 동일하게 적용됩니다. 차이는 runtime package shape이지 maintainer documentation의 소유 위치가 아닙니다.

## Naming

주책임이 **상황별 context 로딩**이면 `load-context-<topic>` 이름을 사용합니다. 이 naming은 repository-local convention이며 Agent Skills 표준 요구사항이 아닙니다.

- context-only Skill은 context discovery, selection, scoping, loading과 적용 경계까지만 소유합니다.
- context를 사용한 실제 구현, 작성, 검증, 리뷰, mutation과 최종 output은 downstream capability가 소유합니다.
- 실제 workflow 수행, artifact 생성, validation, transformation이 주책임이면 `load-context-`를 사용하지 않습니다.

Personal context overlay가 필요하면 flat profile의 `load-context-<topic>-<owner>` convention을 사용하고 base loader를 대체하지 않습니다.

## Target Variants

같은 capability가 `.agentsmesh/skills/`, `../skills-chatbot/`, `skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.

runtime variant는 해당 host가 실제로 지원하는 bundled resources와 runtime surface를 활용해 **초기 context와 실행 비용을 줄이고 필요한 capability를 늦게 로드**하도록 최적화합니다. 다른 profile의 제약을 그대로 가져와 runtime 이점을 포기하지 않습니다.
