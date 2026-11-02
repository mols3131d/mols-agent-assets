---
title: 이 저장소의 자산과 지식 사용하기
description: 외부 프로젝트에서 src/, catalog/, route/의 에이전트 자산과 재사용 지식을 찾아 참조·설치·채택하는 방법을 안내합니다.
---

# 이 저장소의 자산과 지식 사용하기

이 저장소의 에이전트 자산과 재사용 지식을 **다른 프로젝트나 에이전트 런타임에서 사용**하려는 사람을 위한 가이드입니다. 외부에서 가져다 쓸 대상은 `src/`, `catalog/`, `route/` 세 디렉터리에 있습니다. 이 저장소 자체의 개발환경이나 운영 설정은 가져올 대상이 아닙니다.

## 필요한 것 찾기

| 원하는 것 | 시작점 | 구분할 점 |
| --- | --- | --- |
| 이 저장소가 관리하는 Skill·Subagent 등의 원본 | [`src/`](../src/) | 자산마다 대상 런타임과 필요한 지원 파일이 다름 |
| 외부 Skill·Plugin의 출처, 재사용 패턴·템플릿 | [`catalog/`](../catalog/README.md) | 외부 자산 목록은 탐색 정보이고, 패턴·템플릿은 이곳의 작성 원본 |
| 에이전트가 제공 Skill·Subagent를 작업에 맞게 탐색 | [`route/ROUTE.md`](../route/ROUTE.md) | 탐색용 메타데이터이며 자산 원본이나 설치 상태가 아님 |

사람이 직접 고를 때는 `src/`와 `catalog/`에서 시작합니다. 에이전트에 탐색 경로를 제공하려면 [`route/ROUTE.md`](../route/ROUTE.md)를 알려주고 그 파일이 안내하는 후속 목록과 원본을 차례로 읽도록 합니다. `route/`는 [Skill](../route/skills.jsonl)·[Subagent](../route/subagents.jsonl)를 탐색하며, `src/`의 모든 자산이나 `catalog/`의 외부 항목까지 나열하지는 않습니다.

## Agent Asset 사용하기

### Skill을 읽거나 시험하기

예를 들어 코드 호출 흐름을 살펴보려면 [`code-flow-map` Skill](../src/rulesync/.rulesync/skills/code-flow-map/SKILL.md)을 읽습니다. URL을 읽을 수 있는 에이전트에는 아래 원본을 직접 제공할 수 있습니다.

```text
https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/src/rulesync/.rulesync/skills/code-flow-map/SKILL.md
```

이는 **문서를 읽히는 방법**이지 런타임에 Skill을 설치·등록하는 방법이 아닙니다. 해당 Skill이 참조하는 `references/`, `scripts/` 등 지원 파일이 있다면 같은 revision에서 함께 접근할 수 있어야 합니다.

### 프로젝트에서 반복 사용하기

대상 런타임의 **네이티브 설치·발견 기능을 우선**합니다. Rulesync를 사용하는 프로젝트라면 [Rulesync Skill 원본](../src/rulesync/.rulesync/skills/)에서 필요한 Skill만 의존성으로 추가할 수 있습니다. 아래 명령은 **자산을 사용할 프로젝트**에서 실행합니다.

먼저 해당 프로젝트에 `rulesync.jsonc`가 없다면 `rulesync init`으로 초기화하고, 대상 런타임에 맞는 target을 설정합니다.

```bash
rulesync add mols3131d/mols-agent-assets --ref main --path src/rulesync/.rulesync/skills --skills code-flow-map
rulesync generate
```

이후 같은 잠금 버전으로 설치하려면 소비자 프로젝트의 `rulesync.jsonc`와 `rulesync.lock`을 관리하고 `rulesync install --frozen` 다음 `rulesync generate`를 실행합니다. 원본 업데이트는 `rulesync install --update`로 잠금을 갱신한 뒤 변경을 확인합니다. 명령과 설치 옵션은 [Rulesync 공식 문서](https://rulesync.dyoshikawa.com/)를 기준으로 합니다.

### Subagent·런타임 전용 자산 가져오기

[Rulesync Subagent 원본](../src/rulesync/.rulesync/subagents/)이나 [ChatGPT Chat 전용 자산](../src/.openai-chatgpt-chat/README.md)은 각 런타임에서 지원하는 형식·설치 경로·권한을 확인하고 가져옵니다. 원본 파일이 존재한다는 사실만으로 해당 런타임에서 자동 설치되거나 실행되는 것은 아닙니다.

수정해서 사용한다면 필요한 파일과 지원 리소스를 함께 가져오고, 이후의 프로젝트별 변경은 소비자 프로젝트가 소유합니다.

## 패턴·템플릿 또는 외부 자산 활용하기

- [패턴](../catalog/patterns/README.md)은 문제에 맞는 설계·해결 방식을 선택·변형할 때, [템플릿](../catalog/templates/README.md)은 결과물 양식과 작성 스펙을 재사용할 때 참고합니다. 내용을 읽는 것과 프로젝트 규칙으로 채택하는 것은 별개입니다.
- [외부 Skill 목록](../catalog/skills.json)과 [외부 Plugin 목록](../catalog/plugins.json)은 원본 출처를 찾기 위한 카탈로그입니다. 실제 설치 가능 여부와 설치·업데이트 방법은 각 원본 및 대상 플랫폼에서 확인합니다.

## 사용 후 확인하기

- **적용 여부:** 원본을 읽거나 복사·설치한 뒤 대상 런타임이 실제로 발견하고 사용할 수 있는지 확인합니다. 카탈로그 등재나 라우팅만으로 적용이 보장되지는 않습니다.
- **버전:** 최신 `main`을 참조할지 commit SHA에 고정할지 결정합니다. 재현성이 중요하면 원본과 지원 파일을 같은 revision으로 맞추고 업데이트 시 변경을 검토합니다.
- **사용 권한:** 현재 이 저장소 루트에는 `LICENSE`가 없습니다. 기술적인 접근·설치 방법이 복사·수정·재배포 권한을 자동으로 부여하지는 않으므로 해당 자산의 라이선스나 별도 허가를 확인합니다.
