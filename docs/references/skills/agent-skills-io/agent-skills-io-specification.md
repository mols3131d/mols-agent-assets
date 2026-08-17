# Agent Skills Specification

이 문서는 외부 [Agent Skills Specification](https://agentskills.io/specification)의
저장소 내 reference다. 이 저장소에서 portable Agent Skill의 `SKILL.md` 형식과
front matter 규격을 인용할 때 이 문서를 단일 owner로 사용한다.

Repository-local 확장은
[Personal Skill Standard](../agent-assets-skills-standard-personal.md)가 소유한다.
외부 specification과 이 문서가 다르면 외부 specification이 우선한다.

## Directory Structure

Skill은 최소한 `SKILL.md`를 포함하는 directory다.

```text
skill-name/
├─ SKILL.md
├─ scripts/       # optional
├─ references/    # optional
└─ assets/        # optional
```

`SKILL.md` 외의 추가 파일과 directory도 허용된다. `scripts/`, `references/`,
`assets/`는 일반적인 resource를 위한 권장 convention이다.

## `SKILL.md` Format

`SKILL.md`는 YAML front matter 뒤에 Markdown body가 오는 형식이다.

```markdown
---
name: pdf-processing
description: Extract PDF text and merge PDF files. Use when handling PDF documents.
---

# PDF Processing
```

### Front Matter

| Field | Required | Constraint |
| --- | --- | --- |
| `name` | Yes | 1–64자. `a-z`, `0-9`, `-`만 사용. 앞뒤·연속 `-` 금지. parent directory 이름과 일치. |
| `description` | Yes | 1–1024자. Skill이 무엇을 하고 언제 사용하는지 설명. |
| `license` | No | license 이름 또는 bundled license file reference. |
| `compatibility` | No | 제공 시 1–500자. product, system package, network access 같은 environment requirement. |
| `metadata` | No | string key → string value의 추가 metadata mapping. |
| `allowed-tools` | No | space-separated pre-approved tools. Experimental이며 client support가 다를 수 있음. |

`description`은 discovery 단계에서 Skill activation을 판단하는 핵심 metadata다.
구체적인 capability와 사용 조건을 담고, `Helps with PDFs`처럼 범위가 모호한
표현은 피한다.

`compatibility`는 실제 environment requirement가 있을 때만 사용한다.
`metadata`의 key는 다른 producer와 충돌하지 않도록 충분히 구체적으로 정한다.

## Markdown Body

Front matter 뒤의 Markdown body에는 고정된 section schema가 없다. Skill 실행에
필요한 instructions를 작성한다.

일반적으로 다음이 유용하다.

- step-by-step procedure
- input/output example
- common edge case
- validation과 recovery

활성화되면 `SKILL.md` 전체가 context에 로드되므로 상세 내용은 필요할 때
`references/` 등으로 분리한다.

## Progressive Disclosure

1. **Metadata** — startup에서 `name`, `description`을 로드한다.
1. **Instructions** — activation 시 `SKILL.md` body를 로드한다.
1. **Resources** — 필요한 `scripts/`, `references/`, `assets/`만 사용한다.

Specification은 `SKILL.md` body를 5,000 tokens 미만, 500 lines 미만으로 유지할
것을 권장한다. 이는 repository-local token budget과 별개의 권장치다.

## File References

Skill 내부 파일은 Skill root 기준 상대 경로로 참조한다.

```markdown
See [API errors](references/api-errors.md).
```

`SKILL.md`에서 reference chain은 얕게 유지하고 깊은 nested reference chain을
피한다.

## Validation

공식 reference validator를 사용할 수 있다.

```bash
skills-ref validate ./my-skill
```

이 검증은 `SKILL.md` front matter와 naming convention을 확인한다.

## Boundary

이 문서는 외부 Agent Skills format을 요약한다. 다음은 여기서 정의하지 않는다.

- repository-local target profile
- flat chatbot token budget
- dot-prefixed maintainer surface
- `.docs/baseline/`
- repository-local naming convention
- host-specific non-standard metadata

이러한 확장은 [Personal Skill Standard](../agent-assets-skills-standard-personal.md)와
그 하위 reference가 소유한다. Client가 malformed YAML을 lenient하게 복구하는
방법 같은 구현 정책도 specification 자체와 구분한다.
