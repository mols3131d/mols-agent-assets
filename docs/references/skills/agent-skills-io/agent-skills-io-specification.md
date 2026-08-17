# Agent Skills Specification

이 문서는 외부 [Agent Skills Specification](https://agentskills.io/specification)의
저장소 내 reference다. 이 저장소에서 portable Agent Skill의 `SKILL.md` 형식과
front matter 규격을 인용할 때 이 문서를 단일 owner로 사용한다.

Repository-local 확장은
[Personal Skill Standard](../agent-assets-skills-standard-personal.md)가 소유한다.

## Authority Tiers

Skill 규격은 다음 순서로 해석한다.

1. **Tier 1 — Open Standard**: [Agent Skills Specification](https://agentskills.io/specification)이
   portable Agent Skill 형식의 최상위 공통 기준이다.
1. **Tier 2 — Vendor / Harness Contract**: 실제 target runtime의 공식 문서가
   discovery path, activation, permissions, packaging, 추가 metadata 같은
   host-specific behavior를 정의한다.
1. **Local Extension**: Tier 1과 target harness의 mandatory contract를 만족한 뒤
   [Personal Skill Standard](../agent-assets-skills-standard-personal.md)를 적용한다.

Tier 2 규격은 빠르게 변하고 서로 다르므로 이 저장소에서 다시 문서화하지 않는다.
Target이 정해졌을 때 아래 공식 링크를 직접 확인한다.

이 문서의 요약과 Tier 1 원문이 다르면 Tier 1 원문이 우선한다. 특정 target
runtime에서는 해당 harness의 mandatory contract가 repository-local convention보다
우선한다.

## Tier 1 — Open Standard

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)

## Tier 2 — Official Vendor / Harness References

이 목록은 **공식 원문으로 가는 registry**다. 각 vendor 규칙을 이 문서에 복제하지
않는다.

| Ecosystem | Official reference | Use for |
| --- | --- | --- |
| Anthropic / Claude | [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Claude API, Claude Code, claude.ai의 Skill-specific behavior |
| Microsoft Agent Framework | [Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills) | Microsoft Agent Framework의 Skill provider, loading, execution behavior |
| GitHub Copilot | [About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | Copilot의 discovery location, supported surfaces, installation behavior |
| Google Gemini CLI | [Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md) | Gemini CLI의 discovery tier, activation, consent, installation behavior |
| OpenAI / ChatGPT & Codex | [Build skills](https://developers.openai.com/codex/skills) | ChatGPT/Codex의 Skill structure, discovery, activation, host metadata와 built-in creator |
| xAI / Grok | [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md) | Grok shell의 Skill format, discovery와 invocation behavior |

새 major harness가 Agent Skills를 공식 지원하고 실제로 이 저장소의 target이 되면
링크만 추가한다. vendor 규격의 snapshot 문서는 만들지 않는다.

## Official Skill Authoring References

메이저 구현의 authoring 관행을 조사할 때도 **공식 가이드와 공개 Skill 원문을 직접
읽는다**. 이들의 host-specific convention을 Tier 1 표준으로 승격하지 않는다.

### Authoring Guides

- Anthropic — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Microsoft — [Microsoft Agent Skills repository](https://github.com/microsoft/skills)
- GitHub Copilot — [Adding agent skills for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- Google — [How to use AI Agent Skills with Gemini CLI](https://codelabs.developers.google.com/gemini-cli/how-to-create-agent-skills-for-gemini-cli)
- OpenAI / ChatGPT & Codex — [Build skills](https://developers.openai.com/codex/skills)
- OpenAI / Codex — [Save workflows as skills](https://learn.chatgpt.com/use-cases/reusable-codex-skills)
- xAI / Grok — [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills), including its `Creating a Skill` section

### Official Skill-Creator Skills

- Anthropic — [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- Microsoft — [`skill-creator`](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) for Azure SDK and Foundry-oriented Skill authoring
- Google Gemini CLI — built-in [`skill-creator`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md)
- OpenAI Codex — [`skill-creator`](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md)

공식 creator Skill은 좋은 비교 자료지만 portable specification의 authority는 아니다.
특정 creator가 요구하는 추가 파일, metadata, eval 또는 packaging convention은 그
creator와 target harness의 scope로 해석한다.

공식 creator Skill을 확인하지 못한 ecosystem에는 추정 링크를 추가하지 않는다.

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

이 문서는 Tier 1 Agent Skills format을 요약하고 Tier 2 공식 원문으로 연결한다.
다음 repository-local extension은 여기서 정의하지 않는다.

- repository-local target profile
- flat chatbot token budget
- dot-prefixed maintainer surface
- `.docs/baseline/`
- repository-local naming convention
- host-specific non-standard metadata

이러한 확장은 [Personal Skill Standard](../agent-assets-skills-standard-personal.md)와
그 하위 reference가 소유한다. Client가 malformed YAML을 lenient하게 복구하는
방법 같은 구현 정책도 specification 자체와 구분한다.
