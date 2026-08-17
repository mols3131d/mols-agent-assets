# Chatbot Skills

단일 Markdown 파일만으로 완결되는 **flat chatbot skill**을 둡니다.

> [!NOTE]
> `skills-chatbot/`은 Agent Skills 표준의 공식 분류가 아니라, 단일 파일만 전달할 수 있는 chatbot harness를 위해 이 저장소가 만든 **비표준 repository-local target profile**입니다. `<skill-name>.skill.md` 형식과 `<4,000 tokens` budget도 이 profile의 로컬 배포 규칙입니다.

## Placement

`skills-chatbot/`은 배포되는 capability가 다음 조건을 모두 만족할 때 사용합니다.

1. `<skill-name>.skill.md` **한 파일**로 완결됩니다.
1. 배포되는 단일 skill 파일이 **4,000 tokens 미만**입니다.
1. 실행에 필요한 references, assets, scripts, images 같은 runtime-required bundle이나 host-specific package surface가 없습니다.

다음 중 하나라도 해당하면 `../skills-chatbot-runtime/` profile을 사용합니다.

- 단일 skill 파일이 **4,000 tokens 이상**이라 내용을 여러 Markdown 파일로 나눠야 합니다.
- Markdown 한 파일만으로 배포 capability의 instruction surface를 완결할 수 없습니다.
- 실행에 references, assets, scripts, images 또는 다른 bundled resource가 필요합니다.
- host-specific tool schema, integration resource, progressive loading, script/runtime package처럼 **단일 Markdown 밖의 runtime surface**가 capability에 필요합니다.

Skill 본문이 host가 이미 제공하는 tool이나 connector를 **사용하도록 지시한다는 사실만으로 runtime placement를 강제하지 않습니다**. 별도 bundled/runtime resource 없이 행동 계약이 한 Markdown 파일에 완결되면 flat profile을 우선합니다.

Maintainer-only `docs/`, `evals/`, `tests/`, 개발용 validator도 배포 Skill과 분리할 수 있다면 그 존재만으로 runtime placement를 강제하지 않습니다. 작은 textual schema나 설정 예시는 명확성과 유지보수성을 해치지 않는 범위에서 fenced code로 flat file에 포함할 수 있습니다.

로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile도 검토합니다.

## Triggering

Agent Skills의 discovery contract에 따라 **front matter `description`이 activation을 소유**합니다. 무엇을 제공하는지와 어떤 user intent/task context에서 써야 하는지를 함께 적고, 인접 capability와 혼동될 때만 의미 있는 negative boundary를 추가합니다. Follow-up continuity나 target scope가 selection을 바꾸는 경우에도 `description`에서 해결합니다.

Skill 본문에는 `Trigger`, `Activation`, `When to use` 같은 activation 섹션을 두지 않습니다. 본문은 이미 Skill이 활성화되었다고 가정하고 contract, procedure, boundary, output 같은 post-activation behavior만 소유합니다.

Portable front matter 규격의 authority는 [Agent Skills Specification](../../docs/references/skills/agent-skills-io/agent-skills-io-specification.md)에 둡니다.

## Naming

주책임이 작업 workflow 수행이 아니라 **특정 상황에 필요한 판단 기준·제약·지식을 context로 주입하는 것**이면 `load-context-<topic>` 이름을 사용합니다.

이 naming도 Agent Skills 표준이 아니라 repository-local convention입니다.

- 예: `load-context-coding`, `load-context-human-writing`, `load-context-agent-assets`, `load-context-tech-doc-fidelity`
- context-only Skill은 필요한 context의 선택·적용 경계까지만 소유합니다.
- 그 context를 사용한 실제 작성, 구현, 검증, 리뷰, transformation과 최종 output은 downstream capability가 소유합니다.
- context를 활용하더라도 실제 workflow나 산출물 생성이 주책임인 Skill에는 이 prefix를 붙이지 않습니다.
- 이름은 packaging이 아니라 capability responsibility를 나타내므로 같은 규칙을 다른 target profile에도 적용할 수 있습니다.

Personal overlay의 이름과 activation 규칙은 [`agent-assets-skills-target-profiles.md`](../../docs/references/skills/agent-assets-skills-target-profiles.md)를 따릅니다. 예: `load-context-github-mols`, `load-context-notion-mols`.

## Target Variants

같은 capability가 `../skills/`, `skills-chatbot/`, `../skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.

flat variant는 외부 bundle 없이 **한 파일만 전달되는 harness에서 독립적으로 동작하도록 최적화**합니다. 다른 profile의 구조를 그대로 복제하기보다 flat target에서 가장 효율적인 형태를 우선합니다.
