---
name: agent-skill-validate
description: 사용 시점: 스킬의 필수 필드와 기본 파일 구조를 검증하고자 할 때. 제외 대상: 검증 실패 사항을 수정하거나 효과성을 평가할 때.
---

# 에이전트 스킬 검증 (Validate Agent Skill)

## Goal (목표)

스킬을 직접 편집하지 않고, 스킬의 필수 필드 및 기본 파일 구조를 검증합니다.

## When to Use (사용 시점)

검증 스크립트를 사용하여 스킬의 구조적 적합성과 프론트매터를 점검할 때 이 워크플로우를 사용합니다.

## Instructions (지침)

- 프론트매터 요구 사항은 [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)를 읽으십시오.
- 구조적 요구 사항은 [references/agent-skill-directories.md](../references/agent-skill-directories.md)를 읽으십시오.
- 구조적 검증에는 `scripts/validate_asset.py`를 사용하십시오.
- 라우팅 스킬의 경우에만 `references/routing-skill-validation.md`를 읽으십시오.
- 사용자가 수정을 함께 요청하지 않는 한 검증 실패 사항을 직접 수정하지 마십시오.
- 대상 디렉터리나 검증기(validator) 스크립트를 사용할 수 없는 경우 중단하고 보고하십시오.

## Workflows (워크플로우)

### Arguments from Context (컨텍스트 인자)

- 기존 스킬 디렉터리

### Procedure (절차)

1. `python3 scripts/validate_asset.py <skill-dir> --type skill`을 실행합니다.
2. 프론트매터가 [references/agent-skill-frontmatter.md](../references/agent-skill-frontmatter.md)의 사양과 일치하는지, 파일/디렉터리 구조가 [references/agent-skill-directories.md](../references/agent-skill-directories.md)를 준수하는지 확인합니다.
3. 라우팅 스킬의 경우, 단일 `INDEX.csv` 파일을 찾아 라우트 ID가 고유한 상대 경로인지 확인하고, 인덱스 디렉터리를 기준으로 각 ID가 스킬 내부의 실존하는 파일로 연결되는지 확인합니다.
4. 합격(pass) 또는 불합격(fail)을 보고합니다. 실패 항목의 경우 해당 필드 또는 경로와 검증기 메시지를 함께 표기합니다.

### Validation (검증)

- 명령어가 종료 코드 `0`으로 끝나고 `status: pass`를 반환해야 합니다.
- 실패한 모든 검증 항목이 보고되어야 하며, 어떤 파일도 수정되지 않아야 합니다.
