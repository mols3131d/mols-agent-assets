# Chatbot Runtime Skills

업체가 제공하는 hosted chatbot runtime에서 **bundle과 runtime 기능을 활용해야 하는 skill**을 둡니다.

> [!NOTE]
> `skills-chatbot-runtime/`은 Agent Skills 표준의 공식 분류가 아니라, bundle·progressive loading·host-specific runtime surface가 필요한 hosted chatbot harness를 위해 이 저장소가 만든 **비표준 repository-local target profile**입니다. 표준 Skill format과 호환되는 구조를 활용할 수 있지만 이 directory/profile 자체는 표준이 아닙니다.

## Placement

`skills-chatbot-runtime/`은 배포 capability가 다음 중 하나라도 해당할 때 사용합니다.

- flat 단일 skill 파일이 **4,000 tokens 이상**이라 여러 Markdown 파일로 분리해야 합니다.
- Markdown 한 파일만으로 실행 capability를 완결할 수 없습니다.
- 실행에 `references/`, `assets/`, `scripts/`, images 같은 bundled resources가 필요합니다.
- host-specific tool schema, integration resource, progressive loading, script/runtime package처럼 **단일 Markdown 밖의 runtime surface**가 capability에 필요합니다.

`SKILL.md`는 activation boundary와 공통 계약을 유지하고, 상세 context는 필요한 경우에만 bundled file이나 runtime source에서 로드하는 방식을 우선합니다.

단일 Markdown 파일로 충분하고 4,000 tokens 미만이며 별도 runtime surface가 필요하지 않다면 `../skills-chatbot/`의 flat variant가 더 단순한 기본 선택입니다. Skill이 host가 이미 제공하는 tool이나 connector 사용을 지시한다는 사실만으로 runtime placement를 강제하지 않습니다.

사용자의 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile도 검토합니다.

## Package Surfaces

Directory-based Skill package에서 **dot-prefixed directory(`.*`)는 non-runtime maintainer surface**로 사용합니다. 이 convention도 repository-local이며 외부 표준이 아닙니다.

```text
skill-name/
├─ SKILL.md
├─ references/          # runtime
├─ scripts/             # runtime when required
├─ assets/              # runtime when required
└─ .docs/               # non-runtime
   ├─ baseline/          # durable intent / requirements / decisions / directives
   └─ ...                # maintenance or working docs
```

- runtime이 필요로 하는 resource는 dot directory 아래에 두지 않습니다.
- 기존 Skill 내부 `docs/`는 `.docs/`로 사용합니다. repository root의 `docs/`는 별개입니다.
- `.docs/baseline/`은 원래 purpose/essence, requirements, invariants, important decisions, recovery directive를 보존합니다.
- `DIRECTIVE.md`, `intent.md`, `requirements.md`, `decisions.md`는 예시이며 고정 schema가 아닙니다.
- working log나 임시 조사처럼 쉽게 폐기 가능한 정보는 baseline에 넣지 않습니다.
- `.evals/`, `.tests/` 등 다른 dot directory도 non-runtime validation/development surface로 사용할 수 있습니다.
- packaging/deployment는 dot directory를 runtime payload에서 제외하는 것을 기본으로 합니다.

Maintainer-only 파일이 존재한다는 이유만으로 runtime placement를 강제하지 않습니다. 반대로 실행 중 읽어야 하는 문서를 `.docs/`로 옮겨 runtime dependency를 숨기지 않습니다. 그런 문서는 `references/` 같은 runtime surface에 둡니다.

## Naming

주책임이 **상황별 context 로딩**이면 `load-context-<topic>` 이름을 사용합니다. 이 naming은 repository-local convention이며 Agent Skills 표준 요구사항이 아닙니다.

- context-only Skill은 context discovery, selection, scoping, loading과 적용 경계까지만 소유합니다.
- context를 사용한 실제 구현, 작성, 검증, 리뷰, mutation과 최종 output은 downstream capability가 소유합니다.
- 실제 workflow 수행, artifact 생성, validation, transformation이 주책임이면 `load-context-`를 사용하지 않습니다.

Personal context overlay가 필요하면 flat profile의 `load-context-<topic>-<owner>` convention을 사용하고 base loader를 대체하지 않습니다.

## Target Variants

같은 capability가 `../skills/`, `../skills-chatbot/`, `skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.

runtime variant는 해당 host가 실제로 지원하는 bundled resources와 runtime surface를 활용해 **초기 context와 실행 비용을 줄이고 필요한 capability를 늦게 로드**하도록 최적화합니다. 다른 profile의 제약을 그대로 가져와 runtime 이점을 포기하지 않습니다.
