---
name: create-index
description: Generate a new index from Markdown YAML frontmatter as CSV, a Markdown table, or a Markdown list.
---

# Create Markdown Index

## Goal

Create an index document from Markdown YAML frontmatter.

## Instructions

1. 대상 디렉터리의 기존 인덱스 명명·배치 관행을 먼저 확인한다. 대상 관행이
   사용자 요청과 다르면 사용자 요청을 우선한다.
1. Run `scripts/generate_index.py` with the target directory.
1. Select one format:
   - `csv`: machine-readable CSV with all fields quoted.
   - `table`: compact Markdown table.
   - `list`: headings and bullet lists for extensible human-readable output.
1. 대상 관행이나 사용자 요청에 맞는 출력 경로를 `--output`으로 지정한다.
   출력 파일명이 지정되지 않았으면 stdout으로 결과를 반환한다.
1. 대상 관행이 없고 파일명이 필요할 때만 `./INDEX.csv`를 기본 권장값으로
   사용한다. 이는 고정 규칙이 아니다.
1. Use `--require-fields` when missing frontmatter fields must fail generation.
1. Use `--unique-fields` when duplicated frontmatter values must fail generation.
1. Review the generated file and run the Markdown formatter if needed.

For `list`, group files by one or more frontmatter fields with `--group-by`.
The first field becomes `##`, the second becomes `###`, and the file title is
rendered below the deepest group. Group labels include field names by default.

```sh
uv run python scripts/generate_index.py <target-directory> --format list \
   --group-by status importance \
   --output <target-index-path>
```

Grouping options:

- `--group-label` / `--no-group-label`: include or omit field names.
- `--group-missing VALUE`: label missing values; default is `[unset]`.
- `--group-sort alpha|input`: sort groups alphabetically or preserve input order.

Grouping is supported only for the `list` format. Scalar and list frontmatter
values are rendered as text; list values are joined with commas.

Examples:

```sh
uv run python scripts/generate_index.py <target-directory> \
  --format csv --output <target-index-path>
uv run python scripts/generate_index.py <target-directory> \
  --format table --output <target-index-path>
uv run python scripts/generate_index.py <target-directory> \
  --format list --output <target-index-path>
```

Only Markdown files with YAML frontmatter are indexed. Existing files whose names
start with `INDEX` are excluded from input discovery.
