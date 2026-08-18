---
title: Project EXODUS 완료 보고서
description: mols-agent-assets의 portable coding-agent 자산을 AgentsMesh canonical source와 검증 가능한 target projection으로 이전한 결과 보고서
---

# Project EXODUS 완료 보고서

> **Status:** COMPLETE  
> **Gate:** PASS  
> **Migration branch:** `agent/refactor/agentsmesh-migration`  
> **Implementation PR:** #40  
> **AgentsMesh:** `0.32.0`

## 결론

Project EXODUS의 **repository / harness migration은 완료**됐다.

portable coding-agent Rule과 Skill의 source authority는 `src/`에서 `.agentsmesh/`로 이전됐고, GitHub Copilot과 Antigravity target projection은 실제 pinned AgentsMesh CLI로 생성·검증된다.

```text
.agentsmesh/
  ↓ AgentsMesh 0.32.0
  ├─ GitHub Copilot
  └─ Antigravity
```

저장소는 더 이상 이 두 harness의 Rule/Skill 배치 형식을 독립적으로 소유하지 않는다. AgentsMesh가 canonical representation, generation, drift와 round-trip projection을 담당한다. 저장소는 Agent Asset semantics, repository tests와 eval contract를 계속 소유한다.

이번 완료 판정은 **LLM runtime behavior parity를 주장하지 않는다.** 실제 모델 trigger quality, task success, model judgment와 production trace는 별도 runtime eval 영역이다.

# 최종 Authority

| Surface | Authority |
| --- | --- |
| `.agentsmesh/rules/` | portable coding-agent Rule canonical source |
| `.agentsmesh/skills/` | portable coding-agent Skill canonical source |
| `agentsmesh.yaml` | active target / feature selection |
| `.github/copilot-instructions.md`, `.github/skills/` | generated Copilot projection |
| `.agents/rules/`, `.agents/skills/` | generated Antigravity projection |
| `src/agents/` | target-specific Agent exception |
| `src/skills-chatbot/` | flat hosted-chatbot Skill source |
| `src/skills-chatbot-runtime/` | runtime hosted-chatbot Skill source |
| `src/prompts/` | Prompt source |
| `src/rules/chatbot-repo-skill-routing.md` | hosted-chatbot-specific Rule source |
| `evals/` | cross-asset evaluation contracts |
| `tests/` | executable repository verification |

Generated target files는 source가 아니다. 수정은 `.agentsmesh/`에서 시작한다.

# 이주된 자산

## Rules

repository-wide contract와 기존 global Korean-language policy를 `.agentsmesh/rules/_root.md` 하나로 통합했다.

별도 `language-ko` additional Rule은 Copilot에서 global Rule semantics를 보존하지 못해 제거했다. 이는 단순 정리가 아니라 실제 `agentsmesh lint`가 발견한 projection fidelity 문제를 수정한 결과다.

## Skills

다음 11개 portable Skill을 `.agentsmesh/skills/`로 이전했다.

- `caveman-ko`
- `clarify-code`
- `mols-agent-asset-studio`
- `mols-documents-studio`
- `mols-markdown-dashboard`
- `mols-markdown-for-human`
- `mols-markdown-scripts`
- `mols-mermaid-chart`
- `mols-mermaid-diagram`
- `mols-rule-dry`
- `vcs-git-commit`

Skill discovery index도 `.agentsmesh/skills/INDEX.jsonl`을 portable source index로 사용하도록 이전했다.

# 명시적 예외

EXODUS는 directory 통일 자체를 목표로 하지 않았다. AgentsMesh가 의미를 자연스럽게 보존하지 못하는 자산은 억지로 옮기지 않았다.

## Target-specific Agents

`src/agents/`는 유지한다.

현재 active target인 Copilot과 Antigravity는 project Agent capability가 동등하지 않으며, 기존 review Agent는 VS Code-specific tool identifiers와 delegation semantics를 가진다. 특히 `review-lead`의 reviewer delegation을 삭제하거나 가짜 portability로 바꾸지 않았다.

## Hosted chatbot profiles

다음은 AgentsMesh coding-target contract 밖에 남는다.

- `src/skills-chatbot/`
- `src/skills-chatbot-runtime/`
- `src/prompts/`
- `src/rules/chatbot-repo-skill-routing.md`

portable Skill을 참조하는 chatbot routing과 Mermaid Skill의 canonical repository link는 새 `.agentsmesh/skills/` authority를 가리키도록 갱신했다.

# 퇴역한 구세계

다음 legacy surface를 제거했다.

- `src/skills/`
- `src/rules/language-ko.md`
- `src/skills/rulesync-agent-assets/`
- `tests/skills/rulesync-agent-assets/`
- orphan `tests/skills/iceberg-code-review/`
- orphan `tests/skills/mols-kanban-markdown/`
- migration-only `.agentsmesh/_legacy/`
- stale `pyproject.toml` `iceberg-code-*` Python paths
- migration-only write-back workflow

초기에는 `src/` 전체를 `.agentsmesh/_legacy/src/`에 동일 Git tree로 보존한 뒤, 책임 매핑과 cutover가 끝난 후 삭제했다. Git history가 최종 rollback point다.

# 검증 체계

## AgentsMesh gate

영구 PR gate는 pinned `agentsmesh@0.32.0`으로 다음을 실행한다.

```text
npm ci
  ↓
agentsmesh lint
  ↓
agentsmesh check
  ↓
agentsmesh generate --check
  ↓
Copilot import → generate → diff
  ↓
Antigravity import → generate → diff
```

최종 Finalize run에서 전 단계가 성공했다.

특히 round-trip gate는 generated target output을 임시 repository에 복사한 뒤 `agentsmesh import --from <target>`으로 canonical configuration을 재구성하고 다시 generate하여 원본 target output과 비교한다.

## Repository regression

`evals/regression/agentsmesh-exodus.json`이 migration topology와 authority contract를 기록하고, `tests/test_agentsmesh_exodus.py`가 다음을 deterministic하게 검증한다.

- active target / feature set
- canonical Rule과 Skill 목록
- target projection coverage
- explicit exception 존재
- retired legacy surface 부재
- pinned AgentsMesh version과 generated lock version 일치

`targeted-tests.yml`은 AgentsMesh canonical/output/config 변화가 이 EXODUS regression test를 실제로 선택하도록 연결됐다.

최종 Targeted PR Tests도 성공했다.

# 실제로 깨진 것과 수정한 것

EXODUS는 단순 파일 이동으로 끝나지 않았다. 실제 generator/importer를 돌리면서 두 개의 concrete fidelity issue를 발견했다.

## 1. Global language Rule의 Copilot projection gap

초기 `language-ko.md`는 non-root additional Rule이었고 glob이 없었다.

AgentsMesh lint는 Copilot에서 이런 Rule이 생성되지 않는다고 경고했다. 따라서 global language preference를 `_root.md`로 옮겨 두 Tier A target 모두에서 실제 적용 가능한 repository-wide contract로 만들었다.

## 2. Skill-local `.gitignore` round-trip gap

첫 Copilot round-trip에서 164개 파일이 정상 import됐지만 `mols-markdown-dashboard/.gitignore` 하나가 importer를 통과하지 않았다.

해당 파일은 `.venv`, cache, `__pycache__`를 무시하는 maintainer convenience였고 runtime Skill contract가 아니었다. 별도 workaround나 adapter를 만들지 않고 canonical Skill에서 제거했다.

수정 후 Copilot과 Antigravity round-trip 모두 성공했다.

# Tooling Cutover

다음 repository tooling도 새 authority를 따르도록 변경했다.

- `scripts/generate_skill_indexes.py`
- Skill index generator tests
- `.github/workflows/skill-indexes.yml`
- `.github/workflows/targeted-tests.yml`
- `pyproject.toml`
- `mols-agent-asset-studio` repository tests
- root / source / development / testing / Rule projection documentation

따라서 `.agentsmesh/skills/`는 단순 보관 위치가 아니라 실제 discovery, CI와 verification이 따라가는 canonical source다.

# RPWR 실행 기록

## Prepare

- **P1:** repository authority, migration PR, RPWR/Agent Asset/GitHub rules를 재확인하고 migration 가능 상태를 판정했다.
- **P2:** AgentsMesh `0.32.0`, schema v1과 target implementation을 확인하고 local network 제약 때문에 실제 CLI evidence는 GitHub Actions에서 확보하도록 결정했다.

## Improve

- **I1:** Copilot + Antigravity를 Tier A로 고정하고 공통 Native 영역인 Rules + Skills부터 이주했다.
- **I2:** `.agentsmesh/` canonical source와 exact dependency pin을 만들고 index/test/import path를 새 authority로 이전했다.
- **I3:** 실제 AgentsMesh generation을 실행해 두 target projection과 `.lock`을 생성했다.
- **I4:** README, AGENTS, development/testing/reference 문서 authority를 cutover했다.
- **I5:** EXODUS deterministic regression contract와 executable pytest를 만들었다.
- **I6:** old portable source, Rulesync와 orphan verification debt를 제거했다.
- **I7:** legacy staging을 제거하고 target-specific Agent exception을 명시했다.
- **I8:** 실제 lint/round-trip에서 발견된 global Rule projection gap과 Skill `.gitignore` importer gap을 수정하고 재검증했다.

## Finalize

- **F1:** generator/drift 검증 후 round-trip을 추가하면서 concrete failure를 발견해 `RETRY`했다.
- **F2:** failure를 canonical source에서 해결한 뒤 `lint`, `check`, `generate --check`, Copilot round-trip, Antigravity round-trip, targeted repository tests를 모두 통과해 **PASS**했다.

# 완료 상태

이제 portable coding-agent 자산의 기본 작업 흐름은 다음 하나다.

```text
edit .agentsmesh/
  → agentsmesh lint
  → agentsmesh generate
  → agentsmesh check / generate --check
  → repository tests / applicable evals
  → commit canonical + generated outputs
```

다음 단계인 Langfuse 또는 다른 eval/observability platform 도입은 **EXODUS 완료 조건이 아니다.** 그것은 runtime behavior, experiment, trace와 score를 다루는 별도 후속 capability다.

> **Harness engineering은 AgentsMesh에게 넘어갔다.**  
> **이 저장소는 Agent Asset의 의미와 품질을 개발한다.**
