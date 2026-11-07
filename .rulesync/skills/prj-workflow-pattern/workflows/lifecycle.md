# Pattern Document Lifecycle

패턴 문서는 `catalog/patterns/`의 재사용 가능한 **선택적 설계 capsule**이다. 상태는 작업을 판단하기 위한 개념이며 별도 registry나 고정 순서를 요구하지 않는다.

## States

1. **Candidate** — 재사용할 가치와 기존 owner를 검토한다. 부적합한 제안은 패턴으로 만들지 않고, 일회성 조사·인계는 `.inbox/`에 둔다.
2. **Canonical capsule** — primary problem과 category를 정하고 작성한 문서 원본이다. 작업 중 draft·PR은 Git 작업 상태이지 패턴의 새로운 정본이 아니다.
3. **Discoverable** — 위치·description·생성 인덱스를 통해 선택할 수 있다. 등재가 외부 설치·적용 또는 프로젝트 정책 채택을 뜻하지는 않는다.
4. **Maintained / restructured** — 개선·검토·검증을 반복하거나 근거 갱신, 이동·재분류·통합·분리·대체를 수행한다. 현재 문서로 충분하면 유지한다.
5. **Retired or removed** — 더는 권장하지 않는 판단과 원본을 삭제하는 행위는 다르다. 필요한 지식·참조의 처리 여부와 권한을 먼저 판단한다.

## Transitions

[Create](create.md) → [Review](review.md)·[Validate](validate.md) → [Publish](publish.md)는 대표적인 흐름일 뿐 필수 직렬 절차가 아니다. 검토·검증·[Improve](improve.md)는 언제든 반복할 수 있다. [Maintain](maintain.md)·[Restructure](restructure.md)는 필요할 때만 선택하며, [Retire](retire.md)는 자동으로 [Delete](delete.md)를 실행하지 않는다.

문서의 의미와 분류·작성 규칙은 [Patterns](../../../../catalog/patterns/README.md)가 소유한다. 문서 일반 정책은 `docs/documentation/`, Git·권한·생성물 검증은 저장소의 각 owner가 소유한다. 생성된 `catalog/INDEX.tsv`는 정본이나 상태 레지스트리가 아니다.
