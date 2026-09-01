---
description: 저장소의 결정론적 검증, 도구 검증, PR Gate와 merge를 차단하는 테스트 근거를 확인할 때 사용하는 정책입니다.
---

# Testing

## Tool ownership

저장소에서 사용하는 도구 버전 선택과 여러 도구를 아우르는 작업 진입점은 `mise.toml`에서 관리합니다.

- mise는 `uv`, Node.js, rumdl, Lefthook, Biome, Rulesync, skills CLI와 저장소 수준 작업을 소유합니다.
- uv는 `.python-version`의 Python 버전, `pyproject.toml`의 Python 의존성, 환경과 `uv.lock`을 소유합니다.
- Ruff는 Python 개발 의존성으로 유지하며 uv를 통해 실행합니다.

Python은 의도적으로 `mise.toml`에 선언하지 않습니다. 필요할 때 `uv run`이 프로젝트 Python을 준비하고 사용합니다.

## Setup

```bash
mise install
mise run setup
```

`mise run setup`은 모든 Python 의존성 그룹, 저장소 내부의 잠금된 Rulesync 자산, 생성된 Agent Skill, `skills-lock.json`의 외부 Skill dependency와 Git hook을 설치합니다. 외부 Skill은 `mise run skills-sync`와 같은 read-only sync 구현을 사용하며, vendor별 payload·설치 방식은 source-native installer가 소유합니다.

## Formatting

일상 작업에서는 현재 변경만 포맷합니다.

```bash
mise run format-changed
```

`format-changed`는 `HEAD` 대비 staged·unstaged 변경과 untracked file 가운데 Ruff, rumdl 또는 Biome 대상 파일만 수정합니다. 삭제된 파일과 변경되지 않은 파일은 건드리지 않습니다.

저장소 전체를 명시적으로 정리할 때만 다음을 사용합니다.

```bash
mise run format
```

두 task 모두 각 도구를 소유하는 runtime을 통해 Ruff, rumdl과 Biome을 실행합니다. Pre-commit hook은 formatter를 실행하거나 수정된 working-tree 내용을 자동 stage하지 않습니다.

## Generated projections

Commit되는 index와 route는 작성 원본에서 다시 만들 수 있는 projection입니다. 직접 수정하지 않고 다음 entrypoint로 재생성합니다.

```bash
mise run generated-sync
```

현재 이 task는 `docs/**/INDEX.tsv`, 이 repository가 제공하는 Agent Asset의 `route/*.jsonl`, 이 repository가 사용하는 lock-backed Skill의 `.agents/route/*.jsonl`을 각 작성 원본에서 재생성합니다.

Pre-commit hook은 staged 변경에 영향받는 projection만 재생성하고 해당 generated output을 함께 stage합니다. 관련 source나 generated output에 별도의 unstaged 또는 untracked 변경이 있으면 working tree의 다른 작업을 섞지 않도록 자동 동기화를 중단합니다.

CI는 이 write-side automation을 다시 실행하지 않습니다. Generator와 hook의 선택·안전·staging 동작은 해당 script의 deterministic test가 검증하고, 실제 projection 갱신은 local write path가 소유합니다.

## Validation

```bash
mise run check
mise run test
```

Deterministic test는 이 repository가 구현한 **실행 가능한 동작**을 검증합니다. Generator, sync, validator, adapter와 deterministic하게 검사할 가치가 있는 Skill contract가 주 대상입니다. Test file 배치는 [Repository Layout](repository-layout.md)이 소유합니다.

현재 설정값을 그대로 다시 적는 snapshot test는 두지 않습니다. `.gitignore`, `.gitattributes`, tool version, workflow 문자열, 문서 배치·표현, Rulesync manifest/lock schema 같은 값은 각각 해당 config, 문서, upstream tool 또는 review가 소유합니다. 변경 가능한 선택값을 pytest assertion으로 한 번 더 고정하지 않습니다.

CI와 Git hook에서 project Python을 사용할 때는 `uv.lock`을 암묵적으로 갱신하지 않는 `--locked` 실행을 사용합니다.

## PR Gate

`main` 대상 모든 PR은 하나의 고정된 `PR Gate` job을 실행합니다. Workflow 수준 path filter를 두지 않아 required check가 skip 상태로 남지 않게 합니다.

PR Gate의 책임은 `tests/` 전체를 고정된 Python과 uv 환경에서 `uv --locked` semantics로 실행하는 것뿐입니다. Test selection routing보다 실행 가능한 repository logic의 전체 deterministic suite를 안전한 기본값으로 사용합니다.

Formatting, Rulesync validation, generated route/index drift 확인, repository toolchain validation, Promptfoo와 model/runtime evaluation은 PR Gate에서 반복하지 않습니다. 각각 local task 또는 Optional Validation이 실행 책임을 가집니다.

PR Gate는 `contents: read`만 사용하고 repository에 write-back하지 않습니다.

## Optional Validation

PR Gate에 상시 넣을 필요는 없지만 필요할 때 독립적으로 다시 확인할 수 있어야 하는 검증은 `Optional Validation` workflow에 둡니다.

현재 수동 실행에서 다음 검증을 각각 선택할 수 있으며 기본값은 모두 OFF입니다.

- `docs_indexes` — committed docs index drift 확인
- `routes` — distribution/repository route를 재생성하고 committed output과 비교
- `rulesync` — canonical Agent Assets를 Rulesync parser·processor·target adapter로 결정론적으로 검증

선택하지 않은 검증은 실행하지 않습니다. Markdown formatter, 전체 `mise run check`, Promptfoo와 model/runtime evaluation은 이 workflow에도 넣지 않습니다.

## Rulesync 검증

Rulesync CLI는 활발히 유지·개선하는 동안 `mise.toml`에서 `latest` alias를 사용합니다. 새 환경에서는 현재 배포 버전을 설치하고, 이미 설치된 환경에서 새 release를 가져올 때는 `mise upgrade "npm:rulesync"`를 사용합니다. 저장소가 유지보수 상태에 들어가거나 호환성·재현성 때문에 버전 고정이 실질적으로 필요해지면 그때 exact version으로 고정합니다.

`npm run rulesync:validate`는 `scripts/agent-assets/validate_rulesync.py`를 통해 reusable library workspace를 검증합니다. Validator는 Rulesync CLI의 schema나 projection semantics를 재구현하지 않고 다음 read-only pass를 실행합니다.

1. `doctor --strict`로 Rulesync configuration을 검증합니다.
2. configured `generate --dry-run`으로 현재 repository support surface의 source parsing과 projection을 검증합니다.
3. `generate --dry-run --targets "*"`로 개별 asset이 선언한 target까지 Rulesync processor와 adapter에서 검증합니다.

세 pass는 모두 Rulesync의 JSON output을 사용하며 warning도 validation failure로 취급합니다. `--dry-run`만 사용하므로 vendor projection을 쓰거나 삭제하지 않습니다. 개별 asset의 명시적 `targets`는 그대로 존중하며, 선언하지 않은 target의 compatibility까지 검증했다고 간주하지 않습니다.

직접적인 doctor와 target별 preview는 `scripts/run_rulesync.py`가 담당합니다. Root repository workspace는 reusable library와 분리된 declarative consumer입니다. Manifest와 lock의 schema·무결성 및 target별 projection semantics는 Rulesync가 소유하며, `mise run setup`의 `rulesync install --frozen`과 필요한 Rulesync validation으로 확인합니다. Pytest가 lock schema, 특정 target, source transport/path 또는 현재 selection을 별도 contract로 복제하지 않습니다.

## Evaluation

동작 계약, fixture 설계, Promptfoo의 역할, runtime/model 근거 해석은 [Evaluation](evaluation.md)이 소유합니다.

Promptfoo는 local evaluation backend입니다. 저장소 수준 entrypoint는 `mise.toml`이 소유하며 현재 mols-rpi eval은 다음처럼 실행합니다.

```bash
mise run eval-mols-rpi-smoke
mise run eval-mols-rpi
```

첫 명령은 fixture/provider/assertion의 Promptfoo integration을 직접 실행해 보는 local smoke이고, 두 번째는 설정된 runtime/model을 사용하는 behavioral evaluation입니다. 둘 다 PR Gate의 blocking evidence가 아닙니다.

## 기본 명령

```bash
mise exec -- npm run rulesync:validate
mise run check
mise run test
```

구체적인 target의 generation 결과를 확인할 때만 preview를 추가합니다.

```bash
mise exec -- npm run rulesync:preview -- --targets <target>
```
