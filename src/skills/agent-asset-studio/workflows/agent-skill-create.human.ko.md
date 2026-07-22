---
name: agent-skill-create
description: 사용 시점: 최소한의 구조를 갖춘 집중된 에이전트 스킬을 생성하고자 할 때. 제외 대상: 기존 스킬을 덮어쓰거나, 요청 없이 이름을 변경하거나, 외부 작업을 수행할 때.
---

# 에이전트 스킬 생성 (Create Agent Skill)

## Goal (목표)

해당 작업에 필요한 최소한의 구조와 컨텍스트 비용으로 집중된 에이전트 스킬 하나를 생성합니다.

## When to Use (사용 시점)

새로운 에이전트 스킬의 뼈대를 구성하고 초기화할 때 이 워크플로우를 사용합니다.

## Instructions (지침)

- 프론트매터 요구 사항은 [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)를 읽으십시오.
- 라우팅 스킬을 생성하기 전에 `references/routing-skill-structure.md` 및 `references/routing-skill-algorithm.md`를 읽으십시오.
- 사용자가 다른 위치를 요청하지 않는 한 `INDEX.csv`는 `workflows/` 아래에 둡니다.
- `scripts/init_asset.py`를 사용하십시오. 스캐폴딩(뼈대)을 수동으로 재구성하지 마십시오.
- 기존 대상을 덮어쓰기 전에 중단하십시오. 기존 스킬 수정은 `agent-skill-improve`로 라우팅하십시오.
- 명시적으로 요청되지 않은 경우 기존 스킬의 이름을 바꾸기 전에 중단하십시오.
- 새로운 권한이 필요한 파괴적이거나 외부 작업을 수행하기 전에 중단하십시오.

## Workflow: 에이전트 스킬 생성 (Create Agent Skill)

### Arguments from Context (컨텍스트 인자)

- 대상 경로 또는 목적지
- 의도된 작업, 트리거 요청, 출력물 및 거의 일치하지만 제외되는 항목(near-miss exclusions)

### Procedure (절차)

1. 대상이 존재하지 않는지 확인합니다. 대상 경로가 제공되지 않은 경우 이를 요청합니다.
2. 스킬의 단일 작업, 트리거, 출력 및 제외 대상을 정의합니다.
3. `python3 scripts/init_asset.py <name> --type skill --path <dir>`을 사용하여 대상 스캐폴딩을 만듭니다. 여러 워크플로우가 하나의 도메인을 공유하고 대개 선택적으로 로드되는 경우에만 `--routing-skill`을 추가합니다.
4. [references/agent-skill-directories.md](../references/agent-skill-directories.md)에 따라 필수 구조만 유지합니다.
5. [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)에 따라 프론트매터를 작성합니다.
6. 공통 실행 경로와 제약 조건은 `SKILL.md`에 배치합니다. 수동적 지식, 반복되는 논리, 재사용 가능한 출력 자료는 해당하는 리소스 디렉터리로 이동합니다.
7. 지침의 자율성을 위험 수준에 맞춥니다: 유연한 작업은 목표(goals)로, 경계가 있는 작업은 선호하는 절차(preferred procedures)로, 깨지기 쉬운 작업은 정확한 명령이나 순서로 정의합니다.
8. `python3 scripts/validate_asset.py <skill-dir> --type skill`로 유효성을 검사합니다.

### Validation (검증)

- 프론트매터가 [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)의 사양과 일치해야 합니다.
- 트리거는 의도된 요청을 선택하고 거의 일치하는 잘못된 요청은 거부해야 합니다.
- 참조된 모든 경로가 확인되어야 합니다. 빈 디렉터리, 사용되지 않는 예시, 중복된 규칙 또는 중첩된 검색 가능한 `SKILL.md` 파일이 남아있어서는 안 됩니다.
