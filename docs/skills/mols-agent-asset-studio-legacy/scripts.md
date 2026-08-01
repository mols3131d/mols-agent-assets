# Mols Agent Asset Studio 스크립트

공통 Markdown 처리는 `mols-markdown-scripts`에 위임한다. Asset Studio에는
도메인 특수 로직이 필요할 때만 adapter를 둔다.

## `markdown_support.py`

`mols-markdown-scripts/scripts/frontmatter.py`와
`mols-markdown-scripts/scripts/generate_index.py`를 연결하는 내부 adapter다.

- `read_markdown(path)`: YAML frontmatter와 본문을 읽는다.
- `write_workflow_index(workflows_dir, output_path)`: workflow의
  `name,description` frontmatter로 `INDEX.csv`를 생성한다.

frontmatter 검증과 일반 인덱스 생성은 다음 공통 스크립트를 직접 사용한다.

```sh
uv run python src/skills/mols-markdown-scripts/scripts/validate_frontmatter.py <file>
uv run python src/skills/mols-markdown-scripts/scripts/generate_index.py <workflows-dir> \
  --format csv --fields name description \
  --require-fields name description --unique-fields name --max-depth 0 \
  --output <workflows-dir>/INDEX.csv
```
