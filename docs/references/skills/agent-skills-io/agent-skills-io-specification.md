# Agent Skills Specification

이 문서는 외부 [Agent Skills Specification](https://agentskills.io/specification)의
저장소 내 canonical reference다. Portable Agent Skill의 `SKILL.md`, front matter와
공통 format은 이 문서를 통해 참조하되 **Tier 1 원문이 최종 authority**다.

Repository-local 확장은
[Personal Skill Standard](../agent-assets-skills-standard-personal.md)가 소유한다.

## Authority

Skill 규격은 다음 순서로 해석한다.

1. **Tier 1 — Open Standard**: `agentskills.io`의 portable Agent Skills 규격.
1. **Tier 2 — Target / Harness Contract**: 실제 target의 공식 구현 규격과 제약.
1. **Personal Standard**: 외부 contract를 만족한 뒤 적용하는 repository-local 확장.

Tier 2는 공통 표준을 하나 더 만드는 계층이 아니다. Target-specific discovery,
activation, permissions, packaging, metadata 등은 해당 공식 원문에서 확인한다.
Vendor 규격은 빠르게 변하므로 이 저장소에 snapshot으로 복제하지 않는다.

**Tier 2 registry에 포함됐다는 사실은 Tier 1 호환을 뜻하지 않는다.** Vendor가
Agent Skills open standard 채택을 명시하지 않았다면 harness-local Skill contract로
취급하고 portability를 추정하지 않는다.

## Tier 1 — Open Standard

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)

## Tier 2 — Official Target / Harness References

아래는 공식 원문으로 가는 registry다. 세부 규칙은 링크 대상이 소유한다.

| Ecosystem | Official reference | Scope |
| --- | --- | --- |
| Anthropic / Claude | [Claude Platform Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Claude Code Skills](https://code.claude.com/docs/en/skills) | Claude API, claude.ai, Claude Code의 Skill 동작 |
| Microsoft Agent Framework | [Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills) | Skill provider, loading, execution |
| GitHub Copilot | [About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | 지원 surface, discovery, installation |
| Google Gemini CLI | [Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md) | discovery tier, activation, consent, installation |
| OpenAI / ChatGPT & Codex | [Build skills](https://developers.openai.com/codex/skills) | Skill structure, discovery, activation, host metadata |
| xAI / Grok | [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills) | Grok shell의 Skill format, discovery, invocation |

새 major target이 실제 repository target이 되면 공식 링크만 추가한다.

## Official Skill Authoring References

메이저 구현의 authoring 관행도 공식 가이드와 공개 Skill 원문을 직접 읽는다.
Host-specific convention을 Tier 1 규칙으로 승격하지 않는다.

### Authoring Guides

- Anthropic — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Microsoft — [Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills), [Microsoft Skills repository](https://github.com/microsoft/skills)
- GitHub Copilot — [Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- Google Gemini CLI — [Creating skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md), [Skills best practices](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills-best-practices.md)
- OpenAI / ChatGPT & Codex — [Build skills](https://developers.openai.com/codex/skills)
- xAI / Grok — [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills), including `Creating a Skill`

### Official Skill-Creator Skills

- Anthropic — [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- Microsoft — [`skill-creator`](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md)
- Google Gemini CLI — built-in [`skill-creator`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md)
- OpenAI Codex — [`skill-creator`](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md)

공식 creator Skill은 구현 사례와 authoring guidance다. Portable specification의
authority가 아니며, creator가 요구하는 추가 metadata, eval, file 또는 packaging은
해당 creator/target scope에서 해석한다. 공식 creator Skill을 확인하지 못한
ecosystem에는 추정 링크를 추가하지 않는다.

## Directory Structure

Skill은 최소한 `SKILL.md`를 포함하는 directory다.

```text
skill-name/
├─ SKILL.md
├─ scripts/       # optional
├─ references/    # optional
└─ assets/        # optional
```

`SKILL.md` 외 추가 file/directory도 허용된다. `scripts/`, `references/`, `assets/`는
일반적인 resource convention이다.

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

`description`은 discovery 단계에서 activation 판단에 사용되는 핵심 metadata다.
구체적인 capability와 사용 조건을 담는다.

`compatibility`는 실제 environment requirement가 있을 때만 사용한다.
`metadata` key는 producer 간 충돌을 피할 수 있게 충분히 구체적으로 정한다.

## Markdown Body

Front matter 뒤 Markdown body에는 고정 section schema가 없다. 모든 실행에 필요한
핵심 instructions를 두고 긴 상세는 필요한 resource로 분리한다.

## Progressive Disclosure

1. **Metadata** — discovery에 `name`, `description`을 사용한다.
1. **Instructions** — activation 시 `SKILL.md` body를 로드한다.
1. **Resources** — 필요한 resource만 사용한다.

Tier 1은 `SKILL.md` body를 5,000 tokens 미만, 500 lines 미만으로 유지할 것을
권장한다. Repository-local token budget과는 별개다.

## File References

Skill 내부 file은 Skill root 기준 상대 경로로 참조한다.

```markdown
See [API errors](references/api-errors.md).
```

Reference chain은 얕게 유지한다.

## Validation

공식 reference validator를 사용할 수 있다.

```bash
skills-ref validate ./my-skill
```

이 검증은 format과 naming 같은 deterministic contract를 확인한다. Runtime trigger
품질이나 실제 task 성공을 증명하지는 않는다.

## Boundary

이 문서는 Tier 1 format을 요약하고 Tier 2 공식 원문으로 연결한다. 다음은
[Personal Skill Standard](../agent-assets-skills-standard-personal.md)와 그 focused
reference가 소유한다.

- repository-local target profile
- flat chatbot token budget
- dot-prefixed maintainer surface
- `.docs/baseline/`
- repository-local naming convention

Host-specific field나 behavior는 Tier 2 원문이 소유하며 이 문서에 복제하지 않는다.
