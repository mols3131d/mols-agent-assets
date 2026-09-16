# Automation

Tach를 CI, local hook, script, wrapper 또는 automated maintenance에 배치하는 작업에만 읽는다.

## Classify the Automation

먼저 automation의 역할을 분리한다.

- **Validation gate** — architecture contract를 바꾸지 않고 위반 여부를 검증한다.
- **Maintenance mutation** — dependency/module configuration을 동기화하거나 편집한다.
- **Inspection** — graph나 현재 상태를 보여 주어 판단 evidence를 제공한다.

세 역할의 성공을 서로 대체하지 않는다. Mutation이나 inspection이 성공했다는 이유만으로 architecture contract가 검증됐다고 판단하지 않는다.

## Validation Gate

- Repository가 이미 Tach validation entrypoint를 소유하면 그것을 재사용한다. 별도 owner가 없으면 `tach check` 같은 native non-mutating validation을 직접 사용하는 쪽을 우선한다.
- External package dependency declaration이 task나 repository contract에 material하면 `tach check-external`을 architecture boundary check와 별도 evidence로 고려한다. 필요하지 않은 검증을 기본 gate에 추가하지 않는다.
- Local hook은 빠른 feedback surface일 수 있지만 merge admission의 owner를 새로 정의하지 않는다. 가능하면 local과 CI가 같은 validation semantics를 공유하게 한다.
- Script나 workflow는 Tach의 exit semantics와 material diagnostics를 숨기지 않는다. Check failure, tool/configuration error, 실행 불가를 같은 결과로 뭉개지 않는다.
- Validation gate 안에서 configuration을 자동으로 고쳐 green 상태를 만들지 않는다.

## Maintenance Mutation

- `tach sync`, `tach mod`처럼 configuration을 바꾸는 작업은 validation gate와 분리한다.
- Automated mutation에는 side effect가 명시되어야 하고, 생성된 diff를 architecture decision으로 review할 surface가 있어야 한다.
- 현재 import graph가 바뀌었다는 이유만으로 반복 실행이 contract를 자동으로 넓히지 않게 한다. 생성된 dependency나 relaxation은 각각 의도를 확인한 뒤 채택한다.
- Commit, PR 생성, write-back 같은 후속 side effect는 repository workflow와 권한이 명시적으로 소유할 때만 추가한다.

## Scripts and Wrappers

- Native Tach command를 그대로 전달하기만 하는 wrapper는 만들지 않는다.
- Wrapper가 필요하다면 environment/bootstrap, repository-specific scope resolution, 여러 validation의 안정적인 composition, cross-platform entrypoint처럼 실제 repository contract를 제공해야 한다.
- Wrapper는 underlying Tach failure를 성공으로 바꾸거나 중요한 diagnostics를 버리지 않는다. Version-sensitive option과 schema를 wrapper에 불필요하게 고정하지 않는다.
- Automation이 특정 module이나 boundary로 checked scope를 좁히면 결과 claim도 같은 범위로 제한한다.

## Inspection

- `tach show` 같은 inspection은 diagnosis와 review를 위한 evidence로 사용할 수 있지만 validation gate를 대신하지 않는다.
- Generated graph나 visualization은 current observation이며 intended architecture의 authority가 아니다.

## Boundary

이 reference는 Tach-specific automation 배치와 mutation boundary만 다룬다. Generic CI architecture, provider-specific workflow authoring, test-selection strategy, dependency installation과 general-purpose scripting methodology는 해당 repository/tooling owner가 소유한다.
