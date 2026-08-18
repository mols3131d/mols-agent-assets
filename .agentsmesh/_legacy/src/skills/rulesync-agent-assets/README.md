# Rulesync Agent Assets

여러 coding-agent harness의 agent customization asset을 하나의 authority에 맞춰 유지하거나,
한 harness의 native asset을 다른 harness로 이식해야 할 때 호출하는 Skill이다.

호출자는 Rulesync 명령이나 변환 포맷을 알 필요가 없다. 어떤 source를 유지하고 싶은지,
어떤 target이 필요한지, 어떤 asset 범위를 다룰지만 전달하면 된다. Repository policy가
source 선택을 제한한다면 그 authority가 먼저 적용된다.

## Call This Skill When

다음과 같은 결과가 필요할 때 호출한다.

- 하나의 Rulesync canonical source에서 여러 harness용 asset을 생성한다.
- 한 harness의 native asset을 authoritative source로 유지하면서 다른 harness로 이식한다.
- 여러 harness의 agent customization asset을 같은 source authority에 맞춰 동기화한다.
- 기존 portable asset을 변환 없이 그대로 재사용할 수 있는지 확인한다.
- 변환 또는 재사용에서 어떤 의미가 보존되고 어떤 부분이 손실·근사·simulation되는지
  확인한다.

단일 harness 안에서 파일 하나를 수정하는 작업에는 이 Skill이 필요하지 않다.

## What To Tell It

가능하면 다음 정보를 제공한다.

| Information | Meaning |
| --- | --- |
| Source | 유지하고 싶은 authoritative asset 또는 harness |
| Targets | 결과가 필요한 harness |
| Asset scope | rules, agents, skills, hooks 등 옮길 범위 |
| Scope | project-local인지 user-global까지 필요한지 |
| Constraints | source 유지, simulation 허용 여부 등 |

모든 항목을 반드시 명시할 필요는 없다. Repository가 source authority나 project scope를
이미 정의했다면 그 policy가 우선한다.

## Source Authority

Source는 다음 순서로 해석한다.

1. Repository 또는 project authority가 허용 가능한 source 범위를 정한다.
2. 그 범위 안에서 caller가 source를 명시하면 그 선택을 따른다.
3. Caller가 source를 생략하면 기존 ownership 또는 명시된 project default를 사용한다.
4. 그래도 충돌하거나 모호하면 Skill이 임의 선택하지 않고 중단해 알려준다.

Repository의 source-of-truth 정책 자체를 바꾸고 싶다면 asset port와 별개의 의도로 요청해야
한다. 변환 요청만으로 ownership migration을 암묵적으로 수행하지 않는다.

## Typical Calls

Canonical source에서 여러 harness로 배포:

```text
이 Rulesync 자산을 Copilot, Codex, Claude Code, Antigravity용으로 동기화해줘.
```

한 native harness를 source로 유지하면서 이식:

```text
현재 Copilot rules와 agents를 source로 유지하고 Codex와 Claude Code용 자산을 만들어줘.
```

특정 asset만 제한해서 이식:

```text
Antigravity rules만 Copilot으로 옮겨줘. Skills나 hooks는 건드리지 마.
```

호환성 확인까지 요청:

```text
이 Claude Code 설정을 Codex와 Antigravity로 옮길 때 의미가 손실되는 부분도 같이 확인해줘.
```

## What The Skill Decides

호출 의도와 repository authority 안에서 다음을 판단한다.

- 기존 source를 target이 실제로 발견하고 필요한 의미를 지원하는지
- reuse, canonical fan-out, native bridge 중 어떤 route가 최소한의 변환인지
- 요청을 만족하는 최소 target과 asset 범위
- Rulesync가 변환 대상 source를 발견하는지
- 결과에 compatibility gap이 있는지
- 결과를 신뢰하기 위해 어떤 validation evidence가 필요한지

Reuse는 target의 native contract/documentation, project configuration, 또는 직접 validation과
같은 근거가 있을 때만 선택한다. 경로나 파일 형식이 비슷하다는 이유만으로 호환성을
추정하지 않는다.

## What The Skill Does Not Decide

다음은 caller 또는 repository가 소유한다.

- repository의 장기적인 source-of-truth 정책을 변경할지 여부
- `.rulesync/` 중심 architecture로 migration할지 여부
- source asset의 위치나 naming convention을 바꿀지 여부
- user-global configuration을 변경할지 여부
- simulation이나 의미 손실을 제품 수준에서 허용할지 여부

이 Skill은 변환 편의를 위해 이러한 결정을 암묵적으로 수행하지 않는다.

## What To Expect

호출 결과에서는 최소한 다음을 구분할 수 있어야 한다.

- 어떤 route를 사용했는가
- 무엇을 authoritative source로 유지했는가
- 어떤 target과 asset category를 다뤘는가
- 실제 생성된 결과가 무엇인가, 또는 reuse라서 생성하지 않았는가
- 어떤 compatibility gap을 발견했는가
- 실제로 어떤 validation과 evidence를 얻었는가

파일 생성 성공은 모든 harness의 runtime 의미가 같다는 뜻이 아니다. 지원되지 않거나
근사·simulation된 동작과 검증하지 못한 부분은 별도 gap으로 보고되는 것이 이 Skill의
계약이다.

## Compatibility

Reuse 경로에는 Rulesync가 필요하지 않을 수 있다. 실제 format translation이 필요한
canonical fan-out 또는 native bridge에는 `rulesync` CLI가 PATH에 있어야 한다.

지원 source/target, discovery path와 feature support는 설치된 Rulesync version에 따라
달라질 수 있다. Skill은 일반 변환 작업의 부수 효과로 Rulesync를 설치하거나 upgrade하지
않는다.
