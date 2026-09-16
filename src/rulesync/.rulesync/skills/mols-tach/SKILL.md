---
name: mols-tach
description: >-
  Use when Tach materially governs Python module architecture: introducing or changing
  Tach boundaries, diagnosing violations or modeling/configuration problems, visualizing
  or explaining Tach dependency architecture, or designing and implementing Tach-specific
  validation automation, scripts, or hooks. Treat observed imports as evidence rather than
  permission and distinguish implementation violations, Tach modeling/configuration errors,
  and intended contract changes. Do not use for ordinary Python work, Tach package/dependency
  installation, generic CLI lookup, or generic CI/test/diagram design where Tach architecture
  is incidental.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mols Tach

Tach가 관리하는 Python module architecture contract와 observed dependency evidence를 구분해 해석하고, 필요한 경계를 변경·검증하며 architecture evidence를 정확히 설명한다.

## Route

현재 task에 필요한 reference만 읽는다.

| Intent | Load |
| --- | --- |
| Tach 도입, baseline, incremental adoption | `references/adoption.md` |
| CI, hook, script, wrapper, validation orchestration, automated maintenance | `references/automation.md` |
| Dependency graph 생성·해석, Tach architecture 시각화·설명 | `references/visualization.md` |

여러 intent가 실제로 포함되면 해당 reference를 함께 읽는다. 그 외 Tach architecture 작업에는 reference를 선로드하지 않는다. Command option, schema처럼 version-sensitive detail이 판단에 material하면 현재 authoritative Tach source를 확인하고 이 Skill에 full reference를 복제하지 않는다.

## Core Contract

- Tach architecture configuration은 선언된 contract다. 현재 import graph와 Tach가 관찰한 dependency, usage, graph, violation은 evidence이지 permission이 아니다.
- Contract와 implementation이 어긋나면 implementation violation, Tach modeling/configuration error, intended contract change, unclear intent를 먼저 구분한다. Intent가 불분명하면 기존 contract를 임의로 완화하지 않는다.
- `ignore`, unchecked boundary, broad utility·dependency·interface·visibility·exclude 같은 relaxation이나 exception은 명시적인 architecture 결정일 때만 사용한다. Checker를 통과시키기 위한 기본 해결책으로 사용하지 않는다.
- 가장 좁은 잘못된 owner를 수정한다. Code가 contract를 위반하면 code를, Tach가 module/import model을 잘못 해석하면 modeling configuration을, architecture intent가 바뀌었다면 contract를 수정한다.
- Dynamic import, runtime registration, generated behavior, network·event·URL coupling처럼 import graph 밖의 관계는 Tach가 증명하지 않은 것으로 취급한다.

## Diagnose

- 현재 task에 material한 module boundary, dependency direction, layer, public interface, visibility와 exception만 확인한다.
- Modeling error 가능성이 있으면 architecture 판단 전에 source-root resolution과 module boundary가 실제 Python import model을 올바르게 표현하는지 확인한다.
- Boundary 변경이 필요하면 producer·consumer 역할과 허용된 public surface를 필요한 만큼 확인한다.

## Change

- 기존 contract 안에서 implementation을 바로잡을 수 있으면 constraint relaxation보다 그 변경을 먼저 검토한다.
- Contract 변경은 필요한 module, dependency, layer, interface 또는 visibility surface로 제한한다.
- 현재 작업과 무관한 module rule이나 architecture debt를 함께 정리하지 않는다.

## Verification

- 변경 후 repository가 소유한 Tach validation entrypoint를 우선 실행한다. 별도 owner가 없으면 현재 Tach의 native boundary validation을 사용한다.
- Contract를 바꿨다면 의도한 dependency direction과 exposure만 허용되는지 다시 확인한다.
- Passing validation은 실제 checked scope에 대한 evidence다. Unchecked, excluded, ignored 또는 disabled relationship은 검증됐다고 주장하지 않는다.
- Tach validation을 repository 전체 correctness나 runtime behavior correctness로 확대 해석하지 않는다. 필요한 repository-native test나 다른 validation을 대체하지 않는다.
- 실행하지 않은 check나 관찰하지 않은 behavior를 검증했다고 주장하지 않는다.

## Boundary

이 Skill은 Tach-specific architecture contract, evidence 해석, adoption, automation과 visualization 판단을 소유한다. 일반 Python semantics, 일반 software architecture methodology, dependency installation, generic CI architecture, test strategy, generic diagram design과 Tach CLI reference는 소유하지 않는다.
