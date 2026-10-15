# `mouse-sensitivity` 개선 Run — Prepare

## Goal

PR #239의 `mouse-sensitivity` Skill을 기존 책임은 유지하면서 더 범용적이고, 더 적은 context로 동작하며, profile contract와 텍스트가 일관된 상태로 다듬는다.

## Active Scope

### In scope

- `src/rulesync/.rulesync/skills/mouse-sensitivity/`
- `route/skills.jsonl` generated projection 동기화
- `inbox/2026-09-20/`의 Loops working artifact
- PR #239 설명과 validation 상태 갱신

### Out of scope

- 사용자 개인 profile의 repository 저장
- 게임별 감도 coefficient/database의 repository 내장
- JSON Schema, validator, converter 구현
- 마우스 hardware/polling/sensor tuning
- 게임 그래픽·네트워크·성능 최적화

## Governing context

- `CHATBOT.md` → root `AGENTS.md` → `.agents/route/ROUTE.md`
- `github-context`, `mols-loops`, `mols-agent-asset`
- Agent Asset 설계/개선 원칙: responsibility, applicability, loading, ownership을 우선하고 conditional detail은 독립 loading 가치가 있을 때만 reference로 분리
- `mols-text-optimizer`: 더 구체적인 owner가 소유한 의미와 구조를 보존하면서 wording cost만 줄이는 보조 pass로 사용
- Generated route는 canonical source가 아니라 projection이며 공식 generator semantics를 따라 동기화

## Work units

1. **Gaming scope** — FPS/TPS 중심으로 좁아진 일반 gaming contract를 pointer/cursor 게임까지 수용하도록 보완한다.
2. **Entrypoint reduction** — `SKILL.md`에서 conditional gaming/profile detail을 references로 내리고 activation과 core judgment만 남긴다.
3. **Profile contract** — example과 실제 사용자 profile의 ownership을 분리하고, field naming/order와 optional semantics를 정리한다.
4. **Reference refinement** — desktop/gaming/FPS/TPS/conversion/profile 간 중복과 stale burden을 줄인다.
5. **Text optimization** — 의미·강도·routing·technical token을 보존하면서 중복 wording을 줄인다.
6. **Projection/validation** — `route/skills.jsonl`을 generator semantics에 맞춰 동기화하고 PR Gate와 semantic review를 확인한다.

## Acceptance

- 일반 `games` activation이 pointer/cursor 게임에서도 오해를 만들지 않는다.
- FPS/TPS는 독립 Skill이 아니라 조건부 reference로 남는다.
- `SKILL.md`가 모든 activation에 필요한 instruction 위주로 축소된다.
- config는 `version → mouse → mousepad → os → displays → games` 순서로 읽기 흐름이 명확하고, game input context는 genre처럼 닫힌 enum으로 오해되지 않는다.
- default example의 게임은 Counter-Strike 2, Overwatch 2, Valorant다.
- 실제 사용자 Apex Legends/Overwatch 설정은 reusable package나 inbox에 저장하지 않는다.
- 정확한 cross-game conversion은 요청/필요 시 외부 조사로 처리하며 converter DB나 수학 구현을 내장하지 않는다.
- generated projection drift가 해소되고 deterministic checks가 통과한다.

## Readiness

`READY`. 현재 PR branch와 base가 식별됐고, 최근 PR Gate 실패 원인은 `route/skills.jsonl` drift로 확인됐다. 각 Work unit은 기존 branch 안에서 독립적으로 검토 가능한 bounded edit다.
