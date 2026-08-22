---
title: Promptfoo
description: Promptfoo eval tooling의 official source routing과 repository-local entry points
---

# Promptfoo

이 reference는 Promptfoo 사용법이나 option catalog를 복제하지 않고, 자주 확인할 current official source로 라우팅합니다.

Repository-local eval 정책은 [Evaluation](../../development/evaluation.md), PR Gate와 deterministic verification은 [Testing](../../development/testing.md), 실행 config는 [`evals/promptfoo/`](../../../evals/promptfoo/), adapter와 runner는 [`scripts/evals/`](../../../scripts/evals/)에서 확인합니다.

## Core lookup

| Need | Source |
| --- | --- |
| Config field와 schema | [Configuration reference](https://www.promptfoo.dev/docs/configuration/reference/), [schema](https://www.promptfoo.dev/config-schema.json) |
| Test case와 data | [Test cases](https://www.promptfoo.dev/docs/configuration/test-cases/) |
| Assertion과 metric | [Assertions & metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/), [Python assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/python/) |
| Python adapter와 generator | [Python integration](https://www.promptfoo.dev/docs/integrations/python/), [Python provider](https://www.promptfoo.dev/docs/providers/python/) |
| Provider 탐색 | [Providers](https://www.promptfoo.dev/docs/providers/) |
| CLI, env, cache option | [Command line](https://www.promptfoo.dev/docs/usage/command-line/), [Caching](https://www.promptfoo.dev/docs/configuration/caching/) |
| Local model 또는 grader | [Ollama](https://www.promptfoo.dev/docs/providers/ollama/) |
| Result와 export schema | [Output formats](https://www.promptfoo.dev/docs/configuration/outputs/) |
| Failure와 debug | [Troubleshooting](https://www.promptfoo.dev/docs/usage/troubleshooting/) |

## Model grading

- [Model-graded metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/) — model grader 종류와 provider 설정
- [LLM rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/) — output semantic grading
- [Agent rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/agent-rubric/) — workspace나 tool evidence를 포함하는 agentic grading
- [Trajectory goal success](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/#trajectorygoal-success) — traced agent run의 goal outcome grading
- [LLM as a Judge](https://www.promptfoo.dev/docs/guides/llm-as-a-judge/) — grader 설계와 재현성

## Trust and data boundaries

- [Security model](https://github.com/promptfoo/promptfoo/blob/main/SECURITY.md) — config, custom code와 local interface의 trust boundary
- [Telemetry](https://www.promptfoo.dev/docs/configuration/telemetry/) — telemetry와 update check
- [Sharing](https://www.promptfoo.dev/docs/usage/sharing/) — result sharing과 upload boundary
- [Red team data handling](https://www.promptfoo.dev/docs/red-team/troubleshooting/data-handling/) — hosted generation/grading의 data flow

Promptfoo OSS config와 config가 참조하는 code/data는 sandboxed input으로 간주하지 않습니다. 민감한 eval에서는 실제 provider, grader, hosted feature와 sharing 경로를 current source에서 다시 확인합니다.

## Automation

- [CI/CD integration](https://www.promptfoo.dev/docs/integrations/ci-cd/)
- [GitHub Action](https://www.promptfoo.dev/docs/integrations/github-action/)

## Red teaming

- [Quickstart](https://www.promptfoo.dev/docs/red-team/quickstart/)
- [Configuration](https://www.promptfoo.dev/docs/red-team/configuration/)

## Upstream

- [Repository](https://github.com/promptfoo/promptfoo)
- [Releases](https://github.com/promptfoo/promptfoo/releases)
- [Examples](https://github.com/promptfoo/promptfoo/tree/main/examples)

Version-dependent behavior가 의심되면 **official docs → release notes → source** 순으로 확인합니다.
