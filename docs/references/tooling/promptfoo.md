---
title: Promptfoo
description: Promptfoo eval tooling의 official source routing과 repository-local entry points
---

# Promptfoo

이 reference는 Promptfoo의 option catalog나 사용법을 복제하지 않습니다. 변경이 잦은 CLI, configuration, provider와 grader semantics는 **official source를 직접 확인**합니다.

이 repository의 behavioral contract authority는 `evals/`이며, Promptfoo는 이를 실행하는 backend입니다. Repository-local 실행과 검증 경계는 [Testing](../../development/testing.md)을 먼저 봅니다.

## Start here

- [Getting started](https://www.promptfoo.dev/docs/getting-started/) — 전체 개념과 기본 eval 흐름
- [Configuration overview](https://www.promptfoo.dev/docs/configuration/guide/) — config를 작성하거나 구조를 나눌 때
- [Configuration reference](https://www.promptfoo.dev/docs/configuration/reference/) — field semantics와 정확한 schema를 확인할 때
- [Configuration schema](https://www.promptfoo.dev/config-schema.json) — editor validation이나 machine-readable schema가 필요할 때
- [Command line](https://www.promptfoo.dev/docs/usage/command-line/) — `eval`, filtering, cache, output 등 CLI option을 확인할 때

## Eval authoring

- [Test cases](https://www.promptfoo.dev/docs/configuration/test-cases/) — vars, metadata, external test files와 generator 구성
- [Assertions & metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/) — deterministic assertion과 available metric 선택
- [Providers](https://www.promptfoo.dev/docs/providers/) — target/provider syntax와 지원 backend 탐색
- [Python integration](https://www.promptfoo.dev/docs/integrations/python/) — Python provider, assertion, prompt, test generator 전체 진입점
- [Python provider](https://www.promptfoo.dev/docs/providers/python/) — custom runtime adapter 구현
- [Python assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/python/) — deterministic custom grader 구현

## Model grading

- [Model-graded metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/) — model grader 종류와 provider 설정
- [LLM rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/) — output-only semantic grading
- [Agent rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/agent-rubric/) — workspace나 tool evidence를 확인해야 하는 agentic grading
- [LLM as a Judge guide](https://www.promptfoo.dev/docs/guides/llm-as-a-judge/) — grader 설계와 재현성 관점의 실전 가이드

가능하면 deterministic assertion을 먼저 사용하고, semantic judgment가 필요한 경우에만 model grader를 추가합니다.

## Local and private operation

- [Security model](https://github.com/promptfoo/promptfoo/blob/main/SECURITY.md) — config, custom code, local UI와 trust boundary 확인
- [Ollama provider](https://www.promptfoo.dev/docs/providers/ollama/) — local target 또는 local grader 사용
- [Caching](https://www.promptfoo.dev/docs/configuration/caching/) — cache behavior와 storage 확인
- [Telemetry](https://www.promptfoo.dev/docs/configuration/telemetry/) — telemetry와 update check 제어
- [Sharing](https://www.promptfoo.dev/docs/usage/sharing/) — 결과 업로드 경계와 sharing 비활성화
- [FAQ](https://www.promptfoo.dev/docs/faq/) — offline/private 실행과 hosted feature의 data boundary 확인
- [Red team data handling](https://www.promptfoo.dev/docs/red-team/troubleshooting/data-handling/) — red team generation/grading에서 어떤 data가 외부로 나갈 수 있는지 확인

Promptfoo OSS는 sandbox가 아니며 config와 config가 참조하는 script/provider/dataset을 trusted code와 data로 취급합니다. 내부 또는 민감한 eval에서는 config만 보고 local-only라고 추정하지 않고, hosted generation, grading, sharing 등 외부 통신 가능성이 있는 기능은 current official documentation에서 다시 확인합니다.

## Automation and troubleshooting

- [CI/CD integration](https://www.promptfoo.dev/docs/integrations/ci-cd/) — CI gate와 자동 eval 설계
- [GitHub Action](https://www.promptfoo.dev/docs/integrations/github-action/) — upstream GitHub Action을 검토할 때
- [Troubleshooting](https://www.promptfoo.dev/docs/usage/troubleshooting/) — logs, provider failure, network와 local state 문제 조사

Stochastic eval을 CI blocking gate로 올릴지는 Promptfoo 기능과 별개의 repository policy 결정입니다.

## Red teaming

- [Red team quickstart](https://www.promptfoo.dev/docs/red-team/quickstart/) — red teaming 전체 흐름 진입점
- [Red team configuration](https://www.promptfoo.dev/docs/red-team/configuration/) — target, plugin, strategy와 attack provider semantics

Red Team 기능은 일반 behavioral eval과 목적과 grader/attack-provider 경계가 다르므로 필요한 작업에서만 확장합니다.

## Upstream

- [Official repository](https://github.com/promptfoo/promptfoo)
- [Releases](https://github.com/promptfoo/promptfoo/releases)
- [Examples](https://github.com/promptfoo/promptfoo/tree/main/examples)

Version-dependent behavior나 문서와 실제 동작이 의심되면 **official docs → release notes → source** 순으로 확인합니다.
