---
name: agent-skill-improve
description: 사용 시점: 기존 에이전트 스킬의 동작이나 구조를 개선하고자 할 때. 제외 대상: 요청 범위를 벗어난 동작 변경, 이름 변경, 또는 대대적인 재작성을 수행할 때.
---

# 에이전트 스킬 개선 (Improve Agent Skill)

## Goal (목표)

요청된 변경 사항 이외의 동작을 보존하면서 기존 에이전트 스킬 하나를 개선합니다.

## When to Use (사용 시점)

기존 스킬의 오류를 수정하거나, 동작을 변경하거나, 콘텐츠 및 구조를 업데이트할 때 이 워크플로우를 사용합니다.

## Instructions (지침)

- 프론트매터 요구 사항은 [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)를 읽으십시오.
- 프론트매터나 트리거 설명을 업데이트할 때는 [references/trigger-description-guide.md](../references/trigger-description-guide.md)를 참고하십시오.
- 구조적 요구 사항은 [references/agent-skill-directories.md](../references/agent-skill-directories.md)를 읽으십시오.
- 라우팅 아키텍처 변경의 경우에만 `references/routing-skill-structure.md`를 읽으십시오.
- 라우터 동작 변경의 경우에만 `references/routing-skill-algorithm.md`를 읽으십시오.
- 모든 구조적 변경 후에 `scripts/validate_asset.py`를 사용하십시오.
- 사용자가 명시적으로 요청하지 않는 한 이름을 변경하기 전에 중단하십시오.
- 요청된 범위 밖의 동작을 변경하기 전에 중단하십시오.
- 새로운 권한이 필요한 파괴적이거나 외부 작업을 수행하기 전에 중단하십시오.

## Workflows (워크플로우)

### Arguments from Context (컨텍스트 인자)

- 기존 스킬 경로
- 요청된 동작, 콘텐츠 또는 구조적 변경 사항

### Procedure (절차)

1. `rg --files <skill-dir>`로 대상을 검사하고 기초 유효성 검사를 실행합니다.
2. 프론트매터와 요청 사항 또는 실패한 검사 항목에 연관된 파일만 읽습니다.
3. 편집하기 전에 `references/agent-asset-backup.md`에 정의된 백업 프로토콜을 따르십시오.
4. 영향을 받는 트리거, 출력물, 제외 대상 및 제약 조건을 정의합니다. 연관 없는 모든 동작은 보존합니다.
5. 프론트매터나 트리거 조건을 수정하는 경우, `references/trigger-description-guide.md`를 참고하여 `USE WHEN:` 및 `EXCLUDES:` 형식을 준수하십시오.
6. 중복 검사에는 `rg "<term>" <skill-dir>`을, 컨텍스트 크기 검사에는 `wc -l <files>`와 같이 필요한 기능에 집중된 확인 방식을 선호합니다.
7. 요청된 문제를 해결하는 가장 작은 단위의 변경을 적용합니다. 기존 스킬의 전체 뼈대를 재구성하지 마십시오.
8. 인덱스나 레이아웃을 변경할 때는 `references/routing-skill-structure.md`를 읽으십시오. 선택, 모호성 또는 로딩 방식을 변경할 때는 `references/routing-skill-algorithm.md`를 읽으십시오.
9. `python3 scripts/validate_asset.py <skill-dir> --type skill`을 다시 실행합니다. 오류가 사라지고 경고가 수정되거나 명시적으로 수용될 때까지 요청되거나 실패한 영역만 수정합니다.

### Validation (검증)

- 요청된 동작이 작동하고, 연관 없는 트리거, 제외 대상 및 안전 제약 조건이 그대로 유지되어야 합니다.
- 프론트매터가 [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)의 사양과 일치해야 합니다.
- 파일 및 디렉터리 구조가 [references/agent-skill-directories.md](../references/agent-skill-directories.md)를 준수해야 합니다.
- 모든 참조된 경로와 라우트 `id`가 해당하는 `INDEX.csv`를 기준으로 정상적으로 확인되어야 합니다.
