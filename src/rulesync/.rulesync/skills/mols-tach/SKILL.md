---
name: mols-tach
description: >-
  Use when working in a Python repository governed by Tach and the task materially
  changes or diagnoses module dependencies, layers, interfaces, visibility, or Tach
  boundary violations. Treat observed imports as evidence rather than permission,
  distinguish implementation violations from intended contract changes, and do not
  weaken constraints merely to make checks pass. Do not use for ordinary Python work
  where Tach boundaries are immaterial, or for Tach installation, CLI lookup, or
  command-reference questions.
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

Tach가 관리하는 Python module architecture contract를 해석하고, 의도된 경계를 보존하거나 변경하며, 그 결과를 검증한다.

## Contract

- `tach.toml`과 repository의 Tach configuration은 현재 import graph의 사본이 아니라 선언된 architecture contract로 취급한다. 실제 코드가 다른 dependency를 사용한다는 사실만으로 contract를 그 상태에 맞추지 않는다.
- Contract와 implementation이 어긋나면 먼저 implementation violation, 의도된 contract change, 의도가 불분명한 상태를 구분한다. 의도가 불분명하면 기존 contract를 임의로 완화하지 않는다.
- Tach가 관찰한 dependency, usage, graph와 violation은 판단을 위한 evidence다. 관찰된 관계나 configuration을 자동으로 추론·갱신하는 결과도 architecture 결정 자체가 아니라 검토할 제안으로 취급한다.
- `ignore`, unchecked boundary, broadly shared utility, 넓은 dependency·interface·visibility·exclude 같은 relaxation은 명시적인 architecture 결정일 때만 사용한다. Checker를 통과시키기 위한 기본 해결책으로 사용하지 않는다.
- 변경은 잘못된 owner를 가장 좁게 수정한다. Code가 contract를 위반하면 code를, architecture 의도가 바뀌었다면 contract를 수정한다. 현재 작업과 무관한 module rule을 함께 정리하지 않는다.
- Tach의 명령, 옵션, schema와 version-sensitive behavior는 현재 Tach contract가 소유한다. 이 Skill에 복제하거나 기억에 의존하지 않는다.

## Diagnose

- 현재 task에 material한 module boundary, dependency direction, layer, public interface, visibility와 exception만 확인한다.
- 선언된 architecture와 실제 dependency evidence를 분리해서 본다. Existing violation을 intended architecture의 증거로 간주하지 않는다.
- Boundary 변경이 필요한 경우 producer와 consumer 양쪽의 역할과 허용된 public surface를 필요한 만큼 확인한 뒤 변경 대상을 정한다.
- Import graph 밖의 dynamic import, runtime registration, generated behavior, network·event·URL 기반 coupling 등은 Tach가 증명하지 않은 것으로 취급한다.

## Change

- 기존 contract 안에서 구현을 바로잡을 수 있으면 architecture constraint를 완화하는 것보다 그 구현 변경을 우선 검토한다.
- Contract 자체를 변경할 때는 필요한 module, dependency, layer, interface 또는 visibility surface만 변경하고 그 의도를 결과에서 설명 가능하게 유지한다.
- 자동으로 발견되거나 제안된 dependency는 각각 필요성을 판단한 뒤 채택한다. 현재 code가 사용한다는 이유만으로 허용하지 않는다.
- 예외가 필요한 경우 일반 규칙을 넓히기보다 실제 예외의 범위를 좁게 유지한다.

## Verification

- 변경 후에는 적용되는 Tach validation을 실제로 실행해 선언된 contract와 implementation이 일치하는지 확인한다.
- Contract를 변경했다면 결과가 의도한 dependency direction과 exposure만 허용하는지 관련 evidence를 다시 확인한다.
- Tach validation 성공을 repository 전체 correctness나 architecture correctness로 확대 해석하지 않는다. Tach가 표현하고 관찰할 수 있는 boundary가 만족됐다는 범위에서만 주장한다.
- 변경된 runtime behavior에 필요한 repository-native test나 다른 validation은 Tach 결과로 대체하지 않는다.
- 실행하지 않은 check나 관찰하지 않은 behavior를 검증했다고 주장하지 않는다.

## Boundary

이 Skill은 Tach-specific architecture contract와 그 evidence의 해석을 소유한다. 일반 Python semantics, 일반적인 software architecture methodology, dependency installation, CI 설계, test strategy 또는 Tach CLI reference를 소유하지 않는다.
