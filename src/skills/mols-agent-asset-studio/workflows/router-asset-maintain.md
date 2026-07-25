---
name: router-asset-maintain
description: >-
  Create or refresh a router's name,description INDEX.csv from workflow
  frontmatter. Use when its workflow set, fields, or descriptions change. Not
  for general Markdown indexes without router conventions.
---

# 라우터 자산 생성 및 갱신

## 목표

라우터의 `workflows/INDEX.csv`를 직접 편집하지 않고
`mols-markdown-scripts`로 재생성한다.

## 라우터 계약

- 각 워크플로는 `workflows/<name>.md`에 둔다.
- 파일의 frontmatter는 `name`, `description`을 포함한다.
- 파일명 stem과 frontmatter `name`은 같아야 한다.
- `INDEX.csv` 필드는 `name,description`만 사용한다.

## 절차

1. 라우터 생성이면 `SKILL.md`와 `workflows/`를 만들고 워크플로 모듈을
   작성한다. 기존 Skill 통합이면 대상 workflow를 수동으로 선별·이동한다.
2. 각 워크플로 frontmatter를
   [frontmatter-validate.md](frontmatter-validate.md) 절차로 검증한다.
3. 워크스페이스 루트에서 다음 명령으로 인덱스를 생성하거나 갱신한다.

```sh
uv run python src/skills/mols-markdown-scripts/scripts/generate_index.py \
  <skill-directory>/workflows \
  --format csv \
  --fields name description \
  --require-fields name description \
  --unique-fields name \
  --max-depth 0 \
  --output <skill-directory>/workflows/INDEX.csv
```

4. CSV의 각 `name`에 대응하는 `workflows/<name>.md`가 있는지 확인한다.
5. 같은 명령을 다시 실행했을 때 diff가 생기지 않는지 확인한다.

## 검증

- `INDEX.csv`는 스크립트로만 생성된다.
- 헤더는 `name,description`이다.
- 누락·중복 `name`이 없고 모든 대상 파일이 존재한다.
