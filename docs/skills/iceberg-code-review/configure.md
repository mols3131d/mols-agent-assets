# Configuration Guide

Configure `iceberg-code-review`.

계약·기본값 표: [spec.md](spec.md). 공통 위치 권장: [../common/config.md](../common/config.md).

Hidden command. Not exposed in `SKILL.md` to save tokens. Send prompts below to agent to update.

## `/user_data/config.json`

### Fields

- `reviews_dir`: Review save path
- `allow_extra_frontmatter`: Allow custom frontmatter (`true`/`false`)
- `allow_extra_sections`: Allow custom sections (`true`/`false`)
- `RUMDL_EXEC`: Optional. Set by `initialize.py` (rumdl path or `uv tool run rumdl`). Not changed via configurator CLI.

> `command/init.md` / `scripts/initialize.py` create `user_data/config.json` on first setup.

## Prompt

### config help

```text
Read `command/config.md` in `iceberg-code-review` skill and explain available settings.
```

### config set

````text
Read `command/config.md` in `iceberg-code-review` skill and apply below:

```
reviews_dir: [path]
allow_extra_frontmatter: [true|false]
allow_extra_sections: [true|false]
```
````
