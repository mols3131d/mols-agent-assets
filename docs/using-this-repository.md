---
title: 이 저장소의 자산과 지식 사용하기
description: 외부 프로젝트에서 src/, catalog/, route/의 에이전트 자산과 재사용 지식을 찾아 참조·설치·채택하는 방법을 안내합니다.
---

# 이 저장소의 자산과 지식 사용하기

이 저장소를 개발하지 않더라도 필요한 에이전트 자산과 재사용 지식을 다른 프로젝트나 런타임에서 활용할 수 있습니다. **외부 사용을 위한 진입 영역은 `src/`, `catalog/`, `route/` 세 곳**입니다. 필요한 원본만 선택하고, 설치·적용 여부와 프로젝트별 변경은 사용하는 쪽에서 결정합니다.

## 어디에서 시작할까?

| 목적 | 시작점 | 얻을 수 있는 것 |
| --- | --- | --- |
| 이 저장소가 제공하는 자산을 직접 살펴보기 | [`src/`](../src/) | 이 저장소가 작성·관리하는 자산의 원본 |
| 외부 Skill·Plugin이나 재사용 패턴·템플릿 찾기 | [`catalog/`](../catalog/README.md) | 외부 자산의 출처와 이 저장소가 작성한 패턴·템플릿 |
| 에이전트가 필요한 Skill·Subagent를 찾아 읽게 하기 | [`route/ROUTE.md`](../route/ROUTE.md) | 자산별 원본으로 연결되는 탐색 경로 |

**구분해야 할 점:** `src/`는 제공 자산의 작성 원본이고, `catalog/`는 항목에 따라 탐색 정보 또는 콘텐츠 원본입니다. `route/`는 파생된 탐색 정보일 뿐 자산 본문이나 설치 결과가 아닙니다.

## 빠른 예시: Skill 하나 사용하기

코드의 호출 흐름을 살펴보고 싶다면 [Skill 탐색 목록](../route/skills.jsonl)에서 `code-flow-map`을 찾고 [원본 `SKILL.md`](../src/rulesync/.rulesync/skills/code-flow-map/SKILL.md)를 확인합니다. 사용 목적에 따라 원문을 일회성으로 참조하거나, 아래 방식으로 프로젝트에 설치합니다.

에이전트가 스스로 찾도록 할 때는 [`route/ROUTE.md`](../route/ROUTE.md)를 진입점으로 제공할 수 있습니다. 런타임에서 네이티브 자산 탐색을 지원한다면 이를 우선 사용합니다.

## `src/`: 자산 원본 사용하기

- [Rulesync Skill](../src/rulesync/.rulesync/skills/) — 범용·대상별 Skill의 작성 원본. `SKILL.md`를 읽고 필요한 `references/`, `scripts/` 등 지원 파일도 함께 확인합니다.
- [Rulesync Subagent](../src/rulesync/.rulesync/subagents/) — Subagent 정의 원본. 대상 런타임이 Subagent를 지원하는지 확인하고 호환되는 위치에 가져옵니다.
- [ChatGPT Chat 전용 자산](../src/.openai-chatgpt-chat/README.md) — Chat 모드용으로 별도 관리하는 원본. GitHub에 있다고 해서 Chat 세션에 자동으로 설치되거나 활성화되지는 않습니다.

원본의 `targets`, 필요한 도구·권한·지원 파일을 확인하세요. 같은 `src/` 안에 있어도 자산마다 지원하는 런타임과 사용 방법은 다를 수 있습니다.

### 일회성으로 읽기

런타임이 URL을 읽을 수 있다면 필요한 Skill 원본을 직접 제공할 수 있습니다.

```text
https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/src/rulesync/.rulesync/skills/code-flow-map/SKILL.md
```

원문을 읽히는 것은 네이티브 Skill 설치·등록과 다릅니다. 지원 파일이 필요한 Skill이라면 같은 revision의 해당 파일에도 접근할 수 있어야 합니다.

### 대상 프로젝트에 설치하기

대상 프로젝트가 Rulesync를 사용한다면 필요한 Skill만 외부 source로 추가할 수 있습니다. 다음 명령은 **이 저장소가 아니라 자산을 사용하려는 프로젝트**에서 실행합니다.

```bash
# 대상 프로젝트에 Rulesync 설정이 없는 경우 한 번만 실행
rulesync init

rulesync add mols3131d/mols-agent-assets --ref main --path src/rulesync/.rulesync/skills --skills code-flow-map
rulesync generate
```

대상 프로젝트의 Rulesync target·feature 설정은 별도로 확인합니다. 의존성을 고정해 재현하려면 그 프로젝트에서 `rulesync.jsonc`와 `rulesync.lock`을 관리하고, 다른 환경에서는 `rulesync install --frozen` 후 `rulesync generate`를 실행합니다. 업데이트할 때는 `rulesync install --update`로 새 revision을 받아 변경 내용을 검토합니다.

Rulesync를 사용하지 않거나 네이티브 자산을 가져오는 경우에는 대상 런타임이 지원하는 설치·등록 방식을 사용합니다. 자산을 직접 수정해야 한다면 필요한 원본과 지원 파일을 가져오고, 그 이후의 수정은 대상 프로젝트에서 관리합니다.

## `catalog/`: 외부 자산과 재사용 지식 찾기

[카탈로그](../catalog/README.md)에서 목적에 따라 다음 자료를 선택합니다.

- [외부 Skill 목록](../catalog/skills.json)과 [외부 Plugin 목록](../catalog/plugins.json)은 출처를 찾기 위한 목록입니다. 설치 여부나 호환성이 보장되는 것은 아니며, 설치 방법은 각 원본·지원 도구에서 확인합니다.
- [패턴](../catalog/patterns/README.md)은 반복되는 문제에 적용할 설계·해결 방법을 참고하고 선택하기 위한 콘텐츠입니다. 프로젝트의 의무 규칙이 자동으로 되는 것은 아닙니다.
- [템플릿](../catalog/templates/README.md)은 결과물 양식과 작성 스펙을 함께 참고하여 필요한 부분을 재사용하는 콘텐츠입니다.

패턴이나 템플릿을 그대로 참조할 수도 있고, 실제 적용이 필요하면 대상 프로젝트의 상황에 맞춰 채택할 수 있습니다. 카탈로그의 *목록*과 패턴·템플릿의 *원본*을 구분하세요.

## `route/`: 에이전트를 통한 탐색

[`route/ROUTE.md`](../route/ROUTE.md)에서 시작하면 [자산 종류별 탐색 목록](../route/routes.jsonl)을 거쳐 현재 제공되는 [Skill](../route/skills.jsonl)과 [Subagent](../route/subagents.jsonl)의 원본으로 이동할 수 있습니다.

이 라우팅은 **이 저장소가 제공하는 Skill·Subagent를 찾는 용도**입니다. `src/`의 모든 자산이나 `catalog/`의 외부 항목을 포괄하는 설치 목록은 아닙니다. 라우팅의 `name`·`description`으로 후보를 고른 뒤 실제 동작은 링크된 원본에서 확인합니다.

## 사용 후 확인하기

- **적용:** 파일을 읽거나 복사했다는 사실과 런타임이 실제로 발견·실행할 수 있다는 사실을 구분합니다.
- **업데이트:** 최신 `main`을 따라갈지, 특정 commit SHA에 고정할지 선택하고 변경을 검토합니다.
- **출처:** `route/` 메타데이터를 자산 원본처럼 복사하거나 `catalog/`의 외부 자산 목록을 설치 상태로 해석하지 않습니다.
- **권한:** 이 저장소의 루트에는 현재 `LICENSE`가 없습니다. 기술적으로 읽거나 설치할 수 있다는 사실만으로 제3자의 복사·수정·재배포 권한이 부여되는 것은 아니므로 관련 라이선스와 허가를 별도로 확인합니다.
