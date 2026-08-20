# 테스팅 및 품질 검증 가이드

이 문서는 repository verification의 **위치와 증거 수준**을 정의합니다. Workspace/source ownership은 [Rulesync Repository Conventions](references/common/rulesync.md)를 따릅니다.

## 구조

| 경로 | 역할 |
| --- | --- |
| `tests/scripts/` | repository automation의 deterministic test |
| `tests/skills/<skill>/` | Skill-specific deterministic test와 fixture |
| `tests/evals/` | eval fixture의 syntax/shape check |
| `evals/skills/<skill>/` | trigger, behavior, adversarial 등 model/evaluation fixture |
| `evals/regression/` | 여러 asset에 걸친 regression contract |

Repository verification은 deployable Skill package 밖에 둡니다. `scenarios/`도 독립 asset type이 아니라 그것을 소비하는 test/eval 쪽에 둡니다.

Generated `results/`는 기본적으로 일회성 output입니다. 별도 report/evidence로 지속 보존할 명확한 이유가 있을 때만 durable artifact로 승격합니다.

## 원칙

- Deterministic assertion으로 판정 가능한 계약은 model grader보다 우선합니다.
- Test/eval은 canonical asset을 검증하며 자체적으로 두 번째 source of truth가 되지 않아야 합니다.
- Skill/Subagent inventory, 문서의 특정 문장, 과거 migration 경로 같은 재생성 가능한 상태를 회귀 계약에 수동 복제하지 않습니다.
- Target-specific runtime claim이 성공 조건일 때만 실제 usage surface의 evidence를 요구합니다.
- Generated projection 성공만으로 runtime behavior parity를 주장하지 않습니다.

## Rulesync 검증

Reusable library의 기본 순서는 다음과 같습니다.

```text
rulesync doctor --strict
→ 관련 deterministic test / behavioral eval
→ 필요한 경우에만 target projection/runtime 검증
```

Repository `npm run rulesync:*` command는 `scripts/run_rulesync.py`를 통해 `src/rulesync/` workspace를 대상으로 실행합니다. Runner는 target path나 projection semantics를 재구현하지 않고 Rulesync CLI에 위임합니다.

Root repository workspace가 실제로 존재하면 library와 별도로 검증합니다.

## 기본 명령

```bash
npm run rulesync:doctor
uv run pytest
uv run ruff check .
```

구체적인 target 검증이 필요할 때만 다음을 추가합니다.

```bash
npm run rulesync:preview -- --targets <target>
npm run rulesync:validate -- --targets <target>
```
