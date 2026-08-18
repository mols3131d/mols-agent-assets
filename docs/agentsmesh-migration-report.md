# Project EXODUS 완료 보고서

## 상태

**Repository / harness migration: COMPLETE**  
**Post-migration hardening: COMPLETE**  
**Finalize gate: PASS**

Project EXODUS는 portable coding-agent Rule과 Skill의 canonical authority를 legacy `src/` workspace에서 AgentsMesh로 이전하고, hosted-chatbot 및 target-specific 예외를 명시적으로 보존했다.

후속 심층 RPWR 검증에서는 초기 완료 상태가 AgentsMesh 자체의 round-trip에는 일관됐지만 repository-local package-surface contract를 완전히 검증하지 못했다는 사실을 발견했다. 해당 finding과 후속 authoring-route drift를 수정하고 현재 final head에서 다시 검증했다.

# 최종 Authority

```text
.agentsmesh/rules/   → portable coding-agent Rule canonical source
.agentsmesh/skills/  → portable coding-agent Skill deployable canonical source
agentsmesh.yaml      → active target / feature selection

docs/skills/<skill>/ → maintainer-only guide / baseline / decision / recovery
```

Active Tier A target은 GitHub Copilot과 Antigravity이며, AgentsMesh가 관리하는 active feature는 Rules와 Skills다.

`agentsmesh`는 repository `package.json` / `package-lock.json`에서 정확히 `0.32.0`으로 고정한다. `agentsmesh.yaml`의 YAML schema도 같은 0.32.0 release commit `ac8e24449c34f19925721dc60a0d902f5217b1e3`에 pin한다.

# 이주 범위

## Portable Rules와 Skills

- portable Skill 11개를 `.agentsmesh/skills/`에서 관리한다.
- repository-wide Rule contract는 `.agentsmesh/rules/_root.md`가 소유한다.
- global Korean language policy는 root Rule에 포함한다.
- Skill index authority는 `.agentsmesh/skills/INDEX.jsonl`이다.

## Generated targets

AgentsMesh가 다음 target projection을 생성한다.

```text
Copilot
├─ .github/copilot-instructions.md
└─ .github/skills/

Antigravity
├─ .agents/rules/
└─ .agents/skills/
```

Generated projection과 `.agentsmesh/.lock`은 source authority가 아니다. `.gitattributes`에서 `linguist-generated`로 표시해 GitHub review에서는 canonical change를 우선적으로 볼 수 있게 한다.

# 명시적 예외

다음은 AgentsMesh coding-target contract 밖에 남는다.

- `src/agents/`
- `src/skills-chatbot/`
- `src/skills-chatbot-runtime/`
- `src/prompts/`
- `src/rules/chatbot-repo-skill-routing.md`

`src/agents/`의 review Agents는 VS Code-specific tool identifier와 delegation semantics를 가지며 Antigravity가 동등한 project Agent capability를 제공하지 않으므로 가짜 portability로 바꾸지 않았다.

# 퇴역한 구세계

다음 legacy surface를 제거했다.

- `src/skills/`
- `src/rules/language-ko.md`
- `rulesync-agent-assets`
- Rulesync root test scope
- orphan `iceberg-code-review` / `mols-kanban-markdown` test scope
- stale `iceberg-code-*` Python path
- `.agentsmesh/_legacy/`
- migration-only write-back workflow

Git history가 rollback point다.

# Post-EXODUS 심층 검증과 Hardening

## Finding 1 — Maintainer surface가 target package에 배포됨

심층 검증에서 `.agentsmesh/skills/` 아래의 `.docs/`가 Copilot과 Antigravity projection에 그대로 포함되는 것을 발견했다.

Repository target-profile contract는 dot-prefixed maintainer directory를 non-runtime surface로 정의했지만 AgentsMesh `0.32.0`은 Skill supporting file을 재귀 수집하며 `.git`, `node_modules`, `.DS_Store`와 일부 boilerplate 외의 임의 `.docs`를 제외하지 않는다.

따라서 기존 round-trip 성공은 잘못된 package surface까지 충실하게 왕복시킨 self-consistency evidence였고, repository-local package fidelity 자체를 증명하지는 못했다.

### 해결

AgentsMesh-managed portable Skill은 이제 deployable canonical subtree와 maintainer surface를 분리한다.

```text
.agentsmesh/skills/<skill>/  → target에 실제 배포 가능한 파일만
docs/skills/<skill>/         → maintainer guide / baseline / decisions
```

다음 maintainer 문서를 byte-preserving move 또는 placement-only 수정으로 외부화했다.

- clarify-code baseline decisions
- mols-documents-studio baseline decisions
- mols-markdown-scripts baseline decisions
- mols-markdown-dashboard architecture / maintenance / review history / baseline directive

Dashboard package-local `tests/`는 별도로 재검토했다. 해당 Skill의 durable baseline이 self-contained quality gate와 pytest를 distributable package contract의 일부로 명시하고 있으므로 이번 hardening에서는 유지했다.

## Finding 2 — package-surface regression 부재

기존 EXODUS regression은 canonical Skill 목록과 projection coverage는 검증했지만 supporting file의 deployability를 검사하지 않았다.

### 해결

`evals/regression/agentsmesh-exodus.json`에 package-surface contract를 추가하고 `tests/test_agentsmesh_exodus.py`가 canonical과 모든 active projection을 재귀 검사한다.

현재 contract는 deployable Skill subtree의 dot-prefixed path를 금지한다. `.docs`, `.gitignore` 같은 non-runtime hidden surface가 다시 들어오면 generation이나 round-trip이 성공해도 repository test가 실패한다.

## Finding 3 — schema provenance drift

CLI/package는 `agentsmesh@0.32.0`에 pin돼 있었지만 YAML language-server schema는 moving `master`를 가리켰다.

### 해결

schema URL을 upstream 0.32.0 release commit에 pin해 runtime toolchain과 authoring schema provenance를 같은 revision에 묶었다.

## Finding 4 — read-only workflow credential persistence

Permanent AgentsMesh verification workflow는 `contents: read`였지만 checkout credential persistence를 명시적으로 끄지 않았다.

### 해결

`actions/checkout`에 `persist-credentials: false`를 설정했다. Migration refresh에만 사용한 temporary write workflow는 generated state 재생성 직후 제거했다.

## Finding 5 — generated diff review noise

Canonical + Copilot + Antigravity projection을 같은 PR에 보존하기 때문에 generated file이 review surface 대부분을 차지했다.

### 해결

`.gitattributes`의 `linguist-generated`를 사용해 generated projection, AgentsMesh lock과 derived Skill indexes를 GitHub diff에서 기본적으로 접히게 했다. Generated artifact를 삭제하거나 authority로 승격한 것은 아니다.

## Finding 6 — hosted-chatbot 문서가 퇴역한 portable 경로를 안내함

Finalize self-review에서 `src/skills-chatbot/README.md`와 `src/skills-chatbot-runtime/README.md`가 여전히 퇴역한 `../skills/` profile을 portable coding-agent source로 안내하는 것을 발견했다.

### 해결

두 문서의 portable profile route를 repository root `.agentsmesh/skills/`로 교정했다. Runtime profile 문서에는 package-local `.docs/` convention이 AgentsMesh-managed portable Skill에 적용되지 않으며, 해당 maintainer surface는 `docs/skills/<skill-name>/`이 소유한다고 명시했다.

# 검증 체계

Permanent AgentsMesh PR gate는 pinned `agentsmesh@0.32.0`으로 다음을 실행한다.

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

Repository targeted test는 EXODUS regression을 포함해 다음을 검증한다.

- active target / feature set
- canonical Rule과 Skill 목록
- target projection coverage
- deployable Skill package surface
- explicit exception 존재
- retired legacy surface 부재
- pinned AgentsMesh version과 generated lock version 일치

이 검증은 구조·projection·drift·regeneration·round-trip·repository package contract를 증명한다. 실제 LLM trigger quality, task success, behavior parity, trace와 score는 증명하지 않는다.

## 최종 재검증 결과

Post-EXODUS hardening과 Finalize remediation을 모두 포함한 final head에서 다음 permanent checks가 다시 성공했다.

- `Targeted PR Tests` — PASS
- `AgentsMesh` — PASS
  - pinned toolchain install — PASS
  - `agentsmesh lint` — PASS
  - `agentsmesh check` — PASS
  - `agentsmesh generate --check` — PASS
  - Copilot `import → generate → diff` — PASS
  - Antigravity `import → generate → diff` — PASS

최종 branch에는 migration-only write workflow가 남아 있지 않으며 permanent AgentsMesh workflow는 `contents: read`와 `persist-credentials: false`를 사용한다.

# 최종 작업 흐름

```text
edit .agentsmesh/
  → agentsmesh lint
  → agentsmesh generate
  → agentsmesh check / generate --check
  → repository tests / applicable evals
  → commit canonical + generated outputs
```

Maintainer-only portable Skill 문서는 `docs/skills/<skill>/`에서 관리하고 target package에 포함시키지 않는다.

# RPWR 기록

## Initial EXODUS

- Prepare: 2 loops
- Improve: 8 loops
- Finalize: 2 loops
- 첫 Finalize에서 round-trip finding으로 retry
- 두 번째 Finalize에서 PASS

## Post-EXODUS deep hardening

세 캠페인으로 수행했다.

1. **Validation** — authority, upstream parser behavior, generated package surface, CI, round-trip, reproducibility와 완료 주장을 재검증했다. 초기 verdict는 `Revise`였다.
2. **Improvement Research** — wrapper/plugin 없이 package placement, regression, provenance, CI hardening과 reviewability를 강화하는 최소 설계를 선택했다.
3. **Development** — maintainer surface 외부화, regression 강화, schema pin, checkout hardening, generated diff metadata를 구현하고 pinned generator로 target output과 lock을 재생성했다.

Development Finalize 1에서는 stale hosted-chatbot portable route를 발견해 `RETRY`했고, Finalize 2에서 bounded remediation 후 final head의 permanent checks를 다시 통과해 **PASS**했다.
