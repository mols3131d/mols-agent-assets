---
name: frontmatter-validate
description: >-
  Validate agent-asset YAML frontmatter, fields, constraints, and name alignment.
  Use before sharing or editing SKILL.md, RULE.md, or AGENT.md. Not for body
  structure or router-index generation.
---

# Frontmatter 검증

## 목표

`mols-markdown-scripts`의 공통 검증기를 사용해 에이전트 자산의
frontmatter를 검증한다.

## 절차

1. 자산 유형에 따라 대상 파일을 선택한다: Skill은 `SKILL.md`, Rule은
   `RULE.md`, Agent는 `AGENT.md`.
1. 자산 디렉터리 이름을 예상 `name`으로 사용한다.
1. 워크스페이스 루트에서 다음 명령을 실행한다.

```sh
uv run python src/skills/mols-markdown-scripts/scripts/validate_frontmatter.py \
  <asset-file> \
  --schema src/skills/mols-agent-asset-studio/references/agent-skill/frontmatter-schema.yaml \
  --expect name=<asset-directory-name>
```

1. 종료 코드 `0`이면 통과, `1`이면 검증 실패, `2`이면 실행 또는 schema
   오류로 처리한다.

## 검증

- `name`과 `description`이 존재하고 문자열이다.
- `name`은 kebab-case이며 자산 디렉터리 이름과 같다.
- `name`은 64자, `description`은 1024자를 넘지 않는다.
