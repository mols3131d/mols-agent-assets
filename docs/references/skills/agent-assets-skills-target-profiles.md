---
type: reference
title: Agent Assets Skill Target Profiles
description: 이 저장소의 Skill target profile, flat/runtime 경계와 packaging 규칙을 정의한다.
---

# Agent Assets Skill Target Profiles

이 저장소는 동일한 Skill capability를 target harness에 맞춰 서로 다른 profile로 projection할 수 있다.

| Profile | Target |
| --- | --- |
| `skills/` | workspace/filesystem/shell/repository authority가 있는 agent runtime |
| `skills-chatbot/` | self-contained single Markdown만 받는 flat chatbot harness |
| `skills-chatbot-runtime/` | bundle, progressive loading, host-specific runtime surface를 활용하는 hosted chatbot runtime |

같은 capability가 여러 profile에 존재할 수 있다. target harness가 서로 독립된 payload를 요구한다면 이 semantic overlap은 의도적인 projection이며 DRY 위반으로 보지 않는다.

## Flat Chatbot Profile

`skills-chatbot/`은 다음 조건을 모두 만족하는 capability의 기본 target이다.

1. `<skill-name>.skill.md` 한 파일로 완결된다.
1. 배포 파일이 `<4,000 tokens`다.
1. 별도 runtime-required bundle이나 host-specific package surface가 필요하지 않다.

Skill이 host가 이미 제공하는 tool이나 connector를 사용하도록 지시한다는 사실만으로 runtime profile이 되는 것은 아니다. 필요한 행동 계약이 한 Markdown 파일에 완결되면 flat profile을 우선한다.

그 외에는 `skills-chatbot-runtime/`을 사용한다. 예를 들어 references/assets/scripts, host-specific tool schema나 integration resource, progressive loading 등 단일 Markdown 밖의 runtime surface가 실제 capability에 필요할 때다.

`<4,000 tokens`는 이 저장소의 로컬 budget이며 외부 표준이 아니다.

## Directory-Based Package

`skills/`와 `skills-chatbot-runtime/`은 필요할 때 directory-based package를 사용한다.

대표 구조:

```text
<skill-name>/
├── SKILL.md
├── references/
├── assets/
├── scripts/
└── ...
```

모든 디렉터리가 필수는 아니다. 실제 capability에 필요한 resource만 둔다.

## Personal Overlays

범용에 가까운 context loader와 개인 관행을 분리할 때는 base + personal overlay를 사용한다.

```text
load-context-<topic>
load-context-<topic>-<owner>
```

개인 대상에서는 둘을 함께 적용한다. 타인·팀·회사·공유 프로젝트에는 base만 적용한다. 단순 접근 권한, 참여 이력, 관리자 권한은 personal overlay의 활성화 근거가 아니다.

예:

- `load-context-github` + `load-context-github-mols`
- `load-context-notion` + `load-context-notion-mols`

Personal overlay는 base의 범용 계약을 복제하거나 대체하지 않는다. 개인 관행과 개인 공간에서만 필요한 추가 discovery/precedence/default만 소유한다.

## Runtime Resources

Runtime profile의 bundled resource는 capability가 실제로 필요할 때만 둔다.

- `references/`: 조건부 상세 지식
- `assets/`: templates, examples, images 등 실행/출력 resource
- `scripts/`: deterministic helper나 validation
- host integration resource: host-specific schema/configuration

Maintainer-only docs/evals/tests는 배포 capability와 분리할 수 있다면 runtime placement를 강제하지 않는다.

## Naming

Skill 이름은 packaging보다 responsibility를 나타낸다.

- `load-context-<topic>`: 특정 작업 전에 필요한 context를 선택·주입하는 loader
- `load-context-<topic>-<owner>`: base loader 위에 owner-specific personal convention을 추가하는 overlay
- workflow나 artifact 생성이 주책임이면 `load-context-`를 사용하지 않는다.

## Source of Truth

Portable `SKILL.md`와 front matter 규격은
[Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이
소유한다. 이 문서는 target profile에 필요한 repository-local extension만 정의한다.

Skill을 분리할지는 파일 길이가 아니라 activation intent와 responsibility로 판단한다. 세부 지식만 조건부로 달라지고 단일 파일 budget을 넘는다면 runtime `references/`를 검토한다.
