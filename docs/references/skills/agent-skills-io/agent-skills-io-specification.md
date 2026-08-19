# Agent Skills Specification

이 문서는 외부 [Agent Skills Specification](https://agentskills.io/specification)의 repository reference입니다. Agent Skills output의 `SKILL.md`, front matter와 portable contract를 확인할 때 사용하며 **Tier 1 원문이 최종 authority**입니다.

이 저장소의 canonical Skill representation 자체는 current Rulesync schema가 소유합니다. Repository-local authoring 관행은 [Skill Authoring Conventions](../skill-authoring-conventions.md)가 소유합니다.

## Scope and Authority

Rulesync-managed Skill을 다룰 때 authority를 섞지 않습니다.

1. **Rulesync canonical contract** — source shape와 target namespace.
1. **Generated target contract** — 실제 target이 요구하는 format과 runtime semantics.
1. **Repository convention** — 외부 contract가 소유하지 않는 local authoring 관행.

`agentsskills` target을 검토할 때 이 문서의 Tier 1 규격을 적용합니다. 다른 target에 Agent Skills 규격을 자동으로 확장하지 않습니다.

Tier 2는 공통 표준을 하나 더 만드는 계층이 아닙니다. Target-specific discovery, activation, permissions, packaging, metadata 등은 해당 공식 원문에서 확인합니다. Vendor 규격은 빠르게 변하므로 이 저장소에 snapshot으로 복제하지 않습니다.

**Tier 2 registry에 포함됐다는 사실은 Tier 1 호환을 뜻하지 않습니다.** Vendor가 Agent Skills open standard 채택을 명시하지 않았다면 harness-local Skill contract로 취급하고 portability를 추정하지 않습니다.

## Tier 1 — Open Standard

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)

## Tier 2 — Official Target / Harness References

아래는 공식 원문으로 가는 registry입니다. 세부 규칙은 링크 대상이 소유합니다.

| Ecosystem | Official reference | Scope |
| --- | --- | --- |
| Anthropic / Claude | [Claude Platform Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Claude Code Skills](https://code.claude.com/docs/en/skills) | Claude API, claude.ai, Claude Code의 Skill 동작 |
| Microsoft / GitHub | [Microsoft Agent Framework — Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills), [GitHub Copilot — About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | Microsoft Agent Framework와 GitHub Copilot의 target-specific Skill 동작 |
| Google | [Gemini CLI — Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md), [Antigravity — Authoring Google Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) | Gemini CLI와 Google Antigravity의 discovery, authoring, installation/runtime behavior |
| OpenAI / ChatGPT & Codex | [Build skills](https://developers.openai.com/codex/skills) | Skill structure, discovery, activation, host metadata |
| xAI / Grok | [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills) | Grok shell Skill format, discovery, invocation |

새 major target이 실제 repository target이 되면 공식 링크만 추가합니다.

## Official Skill Authoring References

메이저 구현의 authoring 관행도 공식 가이드와 공개 Skill 원문을 직접 읽습니다. Host-specific convention을 Tier 1 규칙으로 승격하지 않습니다.

### Authoring Guides

- Anthropic — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Microsoft / GitHub — [Microsoft Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills), [GitHub Copilot — Adding agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- Google — [Gemini CLI — Creating skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md), [Gemini CLI — Skills best practices](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills-best-practices.md), [Antigravity — Authoring Google Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills)
- OpenAI / ChatGPT & Codex — [Build skills](https://developers.openai.com/codex/skills)
- xAI / Grok — [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills), including `Creating a Skill`

### Official Skill-Creator Skills

- Anthropic — [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- Microsoft / GitHub — Microsoft [`skill-creator`](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) for its Microsoft/Azure scope; do not treat it as a GitHub Copilot creator
- Google — Gemini CLI built-in [`skill-creator`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md); no verified Antigravity-specific official creator is listed, so use the official Antigravity authoring guide instead
- OpenAI — [`skill-creator`](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)

공식 creator Skill은 구현 사례와 authoring guidance입니다. Portable specification의 authority가 아니며 creator가 요구하는 추가 metadata, eval, file 또는 packaging은 해당 creator/target scope에서 해석합니다. 공식 creator Skill을 확인하지 못한 ecosystem에는 추정 링크를 추가하지 않습니다.

## Directory Structure

Agent Skills package는 최소한 `SKILL.md`를 포함하는 directory입니다.

```text
skill-name/
├─ SKILL.md
├─ scripts/       # optional
├─ references/    # optional
└─ assets/        # optional
```

`SKILL.md` 외 추가 file/directory도 허용됩니다. `scripts/`, `references/`, `assets/`는 일반적인 resource convention입니다.

## `SKILL.md` Format

`SKILL.md`는 YAML front matter 뒤에 Markdown body가 오는 형식입니다.

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

`description`은 discovery 단계에서 activation 판단에 사용되는 핵심 metadata입니다. 구체적인 capability와 사용 조건을 담습니다.

`compatibility`는 실제 environment requirement가 있을 때만 사용합니다. `metadata` key는 producer 간 충돌을 피할 수 있게 충분히 구체적으로 정합니다.

## Markdown Body

Front matter 뒤 Markdown body에는 고정 section schema가 없습니다. 모든 실행에 필요한 핵심 instructions를 두고 긴 상세는 필요한 resource로 분리합니다.

## Progressive Disclosure

1. **Metadata** — discovery에 `name`, `description`을 사용합니다.
1. **Instructions** — activation 시 `SKILL.md` body를 로드합니다.
1. **Resources** — 필요한 resource만 사용합니다.

Tier 1은 `SKILL.md` body를 5,000 tokens 미만, 500 lines 미만으로 유지할 것을 권장합니다. Repository-local token budget과는 별개입니다.

## File References

Skill 내부 file은 Skill root 기준 상대 경로로 참조합니다.

```markdown
See [API errors](references/api-errors.md).
```

Reference chain은 얕게 유지합니다.

## Validation

공식 reference validator를 사용할 수 있습니다.

```bash
skills-ref validate ./my-skill
```

이 검증은 Agent Skills format과 naming 같은 deterministic contract를 확인합니다. Rulesync canonical validity, 다른 target projection 또는 runtime trigger 품질을 대신하지 않습니다.

## Boundary

이 문서는 Agent Skills open standard를 요약하고 target 공식 원문으로 연결합니다. Repository-local package authoring과 maintainer convention은 [Skill Authoring Conventions](../skill-authoring-conventions.md)가 소유합니다.

Rulesync canonical schema와 target adapter behavior는 Rulesync가 소유하며 이 문서에 복제하지 않습니다.
