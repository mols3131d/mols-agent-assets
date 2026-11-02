# Common Design

자산 형식보다 책임, 적용 범위, 분리 비용, 권한을 먼저 설계한다. 유형별 세부 판단은 각 `design.md`가 소유한다.

## Responsibility

- 자산이 무엇을 소유하고 왜 변경되는지로 책임을 판단한다.
- 기존 owner가 적절하면 새 owner를 만들지 않는다.
- 새 책임이나 큰 변경은 대표 use case로 추상화가 맞는지 확인한다.
- 인접 자산과 혼동되기 쉬우면 대표 near-miss도 확인한다.
- owner나 asset type이 끝까지 모호하면 추측으로 새 자산을 만들지 않는다.

## Applicability

적용 여부를 가장 직접적으로 표현하는 mechanism을 고른다.

- repository, directory, path, glob 등 구조로 결정 가능 → structural scope
- task intent나 의미적 관련성이 필요 → semantic routing
- specialization, isolation, capability, independent perspective가 필요 → delegation

기존 native mechanism으로 충분하면 새 layer를 만들지 않는다. 항상 적용되어야 하는 authority나 safety boundary를 optional routing에 맡기지 않는다.

## Granularity

파일이나 context surface는 분리 비용보다 독립성이 클 때만 나눈다. 독립성을 판단하는 주요 기준은 applicability, loading, reuse, ownership이다.

거의 항상 함께 적용되고 같은 이유로 바뀌면 함께 둔다. 반대로 불필요한 context가 반복해서 같이 로드되거나 독립 reuse가 분명하면 분리한다.

Filesystem은 탐색을 돕는 단서로 사용하되, 가독성을 위해 framework convention, cohesion, operability, ownership을 왜곡하지 않는다.

## Core and delta

- reusable core 전체를 project/target별로 복제하지 않고 필요한 delta만 둔다.
- customization의 scope와 owner를 분명히 한다.
- 실제로 여러 layer가 겹칠 때만 precedence나 merge rule을 추가한다.

## Portability boundary

재사용 자산은 작성 중인 저장소가 아니라 **적용될 대상 작업**을 기준으로 설계한다. 먼저 호스트 저장소에서만 의미가 있는 경로·명령·자동화·예시를 제거하거나 명확한 local delta로 분리한다.

- 현재 repository에서만 사용되는 자산이 명시적으로 요청되지 않았다면, 다른 저장소 구조와 runtime에서 같은 책임을 수행할 수 있어야 한다.
- Script, template, reference 등 deployable resource는 설치된 자산 패키지를 기준으로 resolve한다. 작성 원본의 checkout path를 consumer path로 가정하지 않는다.
- 특정 GitHub repo, local CI, project task나 개인 계정은 계약의 필수 조건이 아니라면 source citation 또는 검증 사례로만 남긴다.
- 서로 다른 가상의 consumer 상황을 한 번씩 대입해 source-local 전제가 행동 조건으로 승격되지 않았는지 확인한다.

## Authority and precision

권한은 concern별로 구분한다. 사용자와 프로젝트는 outcome과 scope를, source framework는 canonical representation을, target runtime은 target behavior를, repository는 local delta를 소유한다.

여러 접근이 유효하면 outcome·constraint·heuristic 중심으로 두고, 순서·재현성·안전성이 취약할수록 더 강한 구조나 deterministic mechanism을 사용한다. 일반 모델 지식이나 target-specific schema를 포괄성을 위해 복제하지 않는다.

## Write boundary

변경 전에 쓰기 범위를 정한다. 읽었다는 이유로 쓰기 권한이 생기지 않는다. Generated/projection은 별도 계약이 없으면 derived로 취급하고, 외부 자산을 재사용하면 필요한 attribution, license, revision을 보존한다.
