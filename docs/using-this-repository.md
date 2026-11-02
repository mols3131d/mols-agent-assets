---
title: 에이전트 자산과 지식 사용하기
description: 이 저장소의 Agent Asset이나 reusable knowledge를 외부 repository·runtime에서 찾고, 직접 사용·설치·고정·가져오는 방법을 선택할 때 사용합니다.
---

# 에이전트 자산과 지식 사용하기

다른 프로젝트나 에이전트 런타임에서 이 라이브러리의 **필요한 자산과 지식만** 찾아 사용할 수 있습니다. 전체 저장소를 복제하지 않고도 필요한 원본을 직접 참조하거나 가져올 수 있습니다.

## 빠르게 시작하기

1. 아래에서 필요한 자산이나 지식의 **탐색 경로**를 선택합니다.
2. 설명을 읽고 실제 **원본**을 확인합니다. Skill은 `SKILL.md` 외에 필요한 `references/`, `scripts/` 등의 파일도 확인합니다.
3. 일회성 참고, 프로젝트 의존성으로 설치, 직접 가져와 수정 중 **사용 목적에 맞는 방법**을 선택합니다.

| 필요한 것 | 탐색 시작점 |
| --- | --- |
| 이 저장소가 제공하는 Skill | [Skill 목록](../route/skills.jsonl) |
| 이 저장소가 제공하는 Subagent | [Subagent 목록](../route/subagents.jsonl) |
| 다른 곳에서 제공하는 Skill·Plugin | [외부 자산 카탈로그](../catalog/README.md) |
| 반복해서 적용할 설계·해결 패턴 | [패턴 라이브러리](../catalog/patterns/README.md) |
| Markdown 결과물 양식 | [템플릿](../catalog/templates/README.md) |
| Agent Asset 설계 지식 | [설계 참고 자료](development/agent-assets/README.md) |
| 도구·명세의 공식 자료를 찾는 정보 | [도구·명세 참고 자료](development/tooling/README.md) |

예를 들어 코드 흐름을 파악하는 Skill이 필요하다면 [Skill 목록](../route/skills.jsonl)에서 `code-flow-map`을 찾아 [원본 `SKILL.md`](../src/rulesync/.rulesync/skills/code-flow-map/SKILL.md)를 엽니다. 처음부터 모든 Skill을 설치할 필요는 없습니다.

에이전트가 이 저장소에서 제공하는 자산을 직접 찾게 하려면 [Agent Asset 탐색 진입점](../route/ROUTE.md)을 알려줄 수 있습니다. 라우팅 목록은 탐색용이며, 실제 사용 방법은 링크된 원본에 있습니다.

## 사용할 방법 선택하기

| 사용 목적 | 권장 방식 |
| --- | --- |
| 한 번만 참고하거나 시험하기 | 필요한 원본 URL과 지원 파일을 직접 읽기 |
| 프로젝트에서 반복 사용하기 | 해당 런타임의 네이티브 설치 기능 또는 지원되는 의존성 관리 도구 사용 |
| 프로젝트별로 동작을 수정하기 | 필요한 원본과 지원 파일을 가져와 대상 프로젝트가 직접 관리 |
| 패턴·참고 지식 활용하기 | 원문을 링크하거나 검토 후 대상 프로젝트의 문서·규칙에 필요한 내용만 채택 |

원본의 `targets`, 필요한 도구, 의존성, 실행 권한과 대상 런타임 지원 여부를 확인합니다. 목록에 있다고 해서 모든 런타임에서 바로 실행되거나 자동으로 적용되는 것은 아닙니다.

## Skill 사용하기

### 설치 없이 읽기

런타임이 URL을 열 수 있다면 필요한 Skill의 원본을 제공해 일회성 작업에 참고하도록 할 수 있습니다.

```text
https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/src/rulesync/.rulesync/skills/code-flow-map/SKILL.md
```

이 방식은 **문서를 읽는 것**이며, 런타임의 네이티브 Skill 등록·발견을 보장하지 않습니다. 추가 참조 파일이나 스크립트가 필요한 Skill은 동일한 revision의 해당 파일에도 접근할 수 있어야 합니다.

### 프로젝트에 설치하기

대상 프로젝트가 Rulesync를 사용한다면 이 저장소의 재사용 Skill을 필요한 이름으로 선택해 설치할 수 있습니다. **아래 명령은 이 저장소가 아닌, 자산을 사용하는 대상 프로젝트에서 실행**합니다.

```bash
rulesync init
rulesync add mols3131d/mols-agent-assets --ref main --path src/rulesync/.rulesync/skills --skills code-flow-map
rulesync generate
```

`rulesync init`은 아직 Rulesync 설정이 없는 프로젝트에서만 필요합니다. 생성 대상(target)과 기능은 대상 프로젝트의 설정에 맞춰 선택합니다. 선택할 Skill이 여러 개라면 `--skills`에 이름을 쉼표로 구분해 전달할 수 있습니다.

설치 상태를 재현해야 하는 프로젝트는 `rulesync.jsonc`와 `rulesync.lock`을 함께 관리하고, 다른 환경에서는 잠긴 revision으로 다시 설치합니다.

```bash
rulesync install --frozen
rulesync generate
```

새 upstream 버전을 받아들이려면 `rulesync install --update`로 잠금을 갱신한 뒤 변경된 Skill과 실제 런타임 동작을 확인합니다. 명령과 옵션, 지원 대상은 [Rulesync 공식 문서](https://rulesync.dyoshikawa.com/)를 기준으로 확인합니다.

Rulesync를 사용하지 않는 프로젝트는 대상 런타임이 지원하는 네이티브 Skill 설치·등록 방식을 우선합니다. [외부 Skill 카탈로그](../catalog/skills.json)의 항목은 각 원본과 지원 설치 도구를 확인해야 하며, 위 명령을 그대로 적용할 수 있다고 가정하지 않습니다.

## Subagent 또는 수정할 자산 가져오기

[Subagent 목록](../route/subagents.jsonl)에서 원본을 선택하고, 대상 런타임의 Subagent 정의 형식과 배치 위치를 확인한 후 필요한 파일을 가져옵니다. Rulesync를 쓰는 대상 프로젝트라면 해당 원본의 호환성을 확인하고 `.rulesync/subagents/`에 배치해 생성할 수 있습니다. 다른 런타임에서는 그 런타임의 네이티브 경로를 사용합니다.

Skill을 직접 복사해 수정할 때는 `SKILL.md`만 가져오지 말고 **해당 Skill 디렉터리의 필요한 지원 파일을 함께 보존**합니다. 가져온 뒤의 변경과 업데이트는 대상 프로젝트가 관리합니다.

## 패턴과 참고 지식 활용하기

[패턴](../catalog/patterns/README.md)은 반복되는 문제의 해결 방식을 선택할 때, [템플릿](../catalog/templates/README.md)은 결과물 형식을 재사용할 때 활용합니다. [Agent Asset 설계 지식](development/agent-assets/README.md)과 [도구·명세 참고 자료](development/tooling/README.md)는 필요한 주제만 찾아 읽습니다.

- **참고:** 원문을 링크하거나 에이전트가 필요한 때 읽도록 합니다.
- **채택:** 프로젝트 상황에 맞는 내용을 검토한 뒤, 실제로 적용할 범위와 규칙을 대상 프로젝트에서 명시합니다.

참고 문서를 읽었다는 사실만으로 대상 프로젝트의 필수 규칙이 되지는 않습니다. 원문을 재현 가능한 기준으로 인용해야 한다면 `main` 대신 해당 commit SHA로 URL을 고정합니다.

## 가져온 뒤 확인할 것

- 실제 런타임이 자산을 **발견하고 사용할 수 있는지** 확인합니다. 파일 복사, 설치 성공, 목록 등재는 실제 동작 검증과 다릅니다.
- 원본이 요구하는 **지원 파일·도구·권한**이 빠지지 않았는지 확인합니다.
- 최신 변경을 계속 추적할지, **특정 revision에 고정**하고 검토 후 업데이트할지 결정합니다.
- 탐색용 `route/` 파일, 다른 프로젝트의 로컬 설정, 생성된 vendor 출력물을 자산 원본 대신 복사하지 않습니다.

> [!IMPORTANT]
> 현재 이 저장소에는 루트 `LICENSE`가 없습니다. 이 가이드는 기술적인 사용 방법을 설명할 뿐, 제3자의 복사·수정·재배포 권한을 부여하지 않습니다. 외부 사용이나 재배포 전에는 해당 자산의 라이선스 또는 권한을 별도로 확인하세요.
