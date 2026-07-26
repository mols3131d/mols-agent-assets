# Iceberg Code Review — Spec

> 구현·검증 **계약**. 실행 절차 정본은 skill 자산(`workflows/`, `command/`, `scripts/`, `templates/`).
> **왜**는 [decisions.md](decisions.md).

## Encoding

모든 리뷰 문서·템플릿 I/O: **UTF-8**.

## Output layout

| Item | Contract |
| :--- | :--- |
| Summary file | `<review_dir>/__summary__.md` |
| Detail file | `<review_dir>/{domain}-{detail}.md` (slug 규칙: skill scripts) |

## Summary content

- Summary에 **리뷰 범위에 맞춘** 테스트 결과 수치(Pass/Fail/Error/Skip 등)를 기록.
- 전체 스위트 강제 아님. 범위·실행 순서는 skill workflow 정본.

## Document contract

### Summary (`type: code-review-summary`)

| Kind | Names |
| :--- | :--- |
| Frontmatter (required) | `title`, `date`, `type` |
| Sections (required) | `Summary`, `Details` |

### Detail (`type: code-review-detail`)

| Kind | Names |
| :--- | :--- |
| Frontmatter | `title`, `type` required; `description` optional; `severity` ∈ `bug\|risk\|nit\|q`; `status` ∈ `open\|resolved\|dismissed` |
| Sections (required) | `Summary`, `Observation`, `Impact`, `Recommendation`, `Verification` |

작성 절차·문구 지침 = **templates** (placeholder + HTML 주석). 문서별 추가 workflow 없음.

Placeholder 문법: [placeholder.md](placeholder.md).

## Validation (automated)

스크립트가 검사하는 것만:

| Check | Rule |
| :--- | :--- |
| Placeholders | `{{[A-Za-z_]+}}` 잔존 시 fail |
| HTML comments | 본문 `<\!-- ... -->` 잔존 시 fail |
| YAML FM comments | **미검사** |
| Schema | type·required FM·required sections (`_schema`) |
| Extra FM keys | `allow_extra_frontmatter` (default `true`) |
| Extra sections | `allow_extra_sections` (default `true`) |

의미·리뷰 품질 판단 = 모델. 자동화는 구조·필수 조건만.

## Post-format

검증 성공 후 **rumdl** 포맷 시도 가능. 부재·실패 = **비차단** (경고만). 실행 문자열: config `RUMDL_EXEC`.

## Config keys

경로·init 동작 안내: [configure.md](configure.md).

| Key | Default | Role |
| :--- | :--- | :--- |
| `reviews_dir` | `docs/reviews` | 리뷰 루트 |
| `allow_extra_frontmatter` | `true` | 스키마 외 FM 허용 |
| `allow_extra_sections` | `true` | 필수 외 섹션 허용 |
| `RUMDL_EXEC` | `null` / init 탐지 | rumdl 실행 문자열 |

현재 구현 위치: skill-local `user_data/config.json` (공통 `.configs` 권장과 다를 수 있음 → skill 정책).
