---
title: Skill Package and Target Boundaries
description: 이 저장소의 canonical Skill package shape와 target-specific boundary convention
---

# Skill Package and Target Boundaries

이 문서는 [Personal Skill Standard](agent-assets-skills-standard-personal.md)가 위임한 **repository-local Skill package와 target boundary**를 소유한다.

Agent Skills specification의 portable contract가 우선하며, 이 문서는 repository-local extension만 정의한다.

## Canonical Placement

Rulesync가 표현할 수 있는 Skill은 chatbot/agent, flat/runtime으로 나누지 않고 다음 canonical path를 사용한다.

```text
src/rulesync/.rulesync/skills/<skill-name>/SKILL.md
```

`src/rulesync/`는 격리된 native Rulesync workspace이며, 그 안의 `.rulesync/`가 canonical asset source다. Repository root에는 `.rulesync/`를 두지 않으므로 `mols-agent-assets`가 보관한 distribution asset이 이 저장소 자체의 runtime Skill로 자동 discovery되지 않는다.

특정 target semantics가 현재 Rulesync contract로 표현되지 않아 custom source가 실제로 필요한 경우에만 `src/rulesync/`의 peer source를 검토한다.

## Single-File by Default

모든 Skill은 `<skill-name>/SKILL.md` package로 시작한다.

`SKILL.md` 하나로 activation과 runtime behavior가 완결되면 **single-file Skill**로 유지한다.

- 파일 길이만으로 supporting file을 만들지 않는다.
- runtime이 존재한다는 이유만으로 다른 Skill profile로 분류하지 않는다.
- chatbot과 agent를 Skill placement taxonomy로 사용하지 않는다.
- target harness의 mandatory package contract가 있으면 그 contract가 우선한다.

Single-file Skill은 여러 Markdown 문서의 책임을 한 파일에 유지할 수 있다. **`# ≈ one Markdown file responsibility`**를 기본 heuristic으로 사용하며, 독립적인 top-level responsibility가 여러 개면 복수의 `#`을 허용하고 권장한다.

- 모든 heading은 하나의 명확한 책임을 가진다.
- `##` 이하는 부모 책임을 점진적으로 분해한다.
- 같은 depth는 가능한 한 비슷한 추상화 수준을 유지한다.
- 공통 invariant는 가장 가까운 공통 상위 boundary에 한 번만 둔다.
- 의미 없는 미세 분할은 하지 않는다.

### Front Matter Triggering

Skill activation 정보는 front matter `description`에 집중한다. `description`은 selection contract이며 capability, task context, 필요한 핵심 negative boundary를 구분할 수 있어야 한다.

다른 Skill과의 prerequisite, fallback, handoff, execution order 같은 orchestration은 본문에서 다룬다. 본문은 이미 Skill이 선택·활성화되었다고 가정한다.

## Deployable Surface

실행에 실제로 필요할 때만 package를 확장한다.

```text
skill-name/
├─ SKILL.md
├─ references/          # runtime when needed
├─ scripts/             # runtime when needed
├─ assets/              # runtime when needed
├─ templates/           # runtime when needed
└─ ...                  # target-required runtime surface
```

- runtime behavior에 필요한 knowledge/resource는 package 내부의 명시적 runtime surface가 소유한다.
- maintainer-only 문서를 runtime dependency로 숨기지 않는다.
- `src/rulesync/.rulesync/skills/<skill-name>/` 아래에는 repository verification 자산인 `tests/`, `evals/`, `scenarios/`, 생성된 `results/`를 두지 않는다.
- `src/rulesync/.rulesync/skills/<skill-name>/` 아래에는 non-runtime을 숨기기 위한 dot-prefixed path를 두지 않는다.

## Repository Verification Surface

Skill 검증 자산은 deployable package와 분리한다.

```text
tests/skills/<skill-name>/
├─ test_*.py
└─ scenarios/            # deterministic test fixtures when needed

evals/skills/<skill-name>/
└─ ...                   # trigger, behavior, adversarial, model eval fixtures
```

- deterministic correctness test는 `tests/skills/<skill-name>/`이 소유한다.
- deterministic test가 소비하는 scenario/fixture는 해당 test directory 아래에 둔다.
- behavioral/model evaluation fixture는 `evals/skills/<skill-name>/`이 소유한다.
- `scenarios/`를 독립적인 repository top-level asset type으로 만들지 않는다. 소비하는 test/eval이 소유한다.
- test/eval이 생성한 `results/`는 durable artifact로 명시적으로 승격하지 않는 한 commit하지 않는다.

Generated target package에 repository verification 자산이 나타나면 generation 자체가 성공했더라도 regression이다.

## Target Boundaries

Skill 종류와 execution target을 같은 taxonomy로 취급하지 않는다.

- Skill은 Skill이다.
- target runtime이 richer하다는 이유만으로 별도 Skill type/profile을 만들지 않는다.
- 같은 canonical Skill을 target이 일부만 표현할 수 있다면 capability 차이를 explicit limitation으로 다룬다.
- target-specific semantics가 capability의 본질이고 현재 Rulesync가 안전하게 표현할 수 없다면 그때만 custom/non-standard source를 검토한다.

Rulesync target projection은 canonical source가 아니다. Read-only native check는 `src/rulesync/`에서 직접 수행하고, generation은 workspace의 temporary copy에서 검증하며 결과를 commit하지 않는다.

Rulesync의 target-specific front matter section은 projection adapter 입력이지 portable Agent Skills 표준의 일부가 아니다. Portable field는 Tier 1 contract를 우선하고, target extension은 실제 target이 필요할 때만 namespaced section에 둔다.

## Repository Maintainer Docs

특정 Skill에 durable maintainer documentation이 실제로 필요하면 repository root의 `docs/skills/<skill-name>/`을 사용한다. 단순하고 self-explanatory한 Skill에는 만들지 않는다.

다음과 같은 경우에만 검토한다.

- source만으로 purpose, architecture 또는 중요 invariant를 복구하기 어렵다.
- 잘못된 refactor·단순화로 핵심 의도가 훼손될 위험이 크다.
- durable decision, recovery, migration 또는 compatibility 지식이 필요하다.
- 별도 baseline이 향후 회귀·복구 비용을 의미 있게 낮춘다.

Runtime-required 지식은 maintainer docs가 아니라 Skill package가 소유한다.

## Context-Only Naming

주책임이 workflow가 아니라 상황별 context discovery/loading이면 `load-context-<topic>` naming을 검토한다. 실제 구현·mutation·검증·최종 output까지 소유하는 Skill에는 사용하지 않는다.

Context-only Skill은 activation intent에 따라 scope baseline loader 또는 conditional loader로 운용할 수 있다. 개인 관행을 범용 loader와 분리할 때는 `load-context-<topic>-<owner>`를 personal overlay로 사용하며, personal scope는 current target별 evidence로 판단한다.

## Boundary

Portable `SKILL.md`와 front matter 규격은 [Agent Skills Specification](agent-skills-io/agent-skills-io-specification.md)이 소유한다. 이 문서는 repository-local package shape와 target boundary만 정의한다.

Skill을 분리할지는 파일 길이가 아니라 activation intent, responsibility, 실제 runtime resource 필요성으로 판단한다.
