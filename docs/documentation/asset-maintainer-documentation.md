---
description: 개별 Agent Asset 또는 family의 유지보수 문서를 어디에 두고, 실행 원본과 family 문서, 저장소 전용 문서의 책임을 어떻게 나눌지 정할 때 사용합니다.
---

# Asset Maintainer Documentation

`docs/<asset-type>/<owner>/**`에는 해당 Agent Asset이나 family를 유지보수하는 데 필요한 문서를 둡니다. 이 문서는 대응하는 자산과 함께 다른 저장소로 옮겨도 계속 쓸 수 있어야 합니다. `<owner>`는 하나의 asset이거나 같은 책임을 공유하는 family일 수 있습니다.

`development`, `documentation`, `references`는 문서 전용 namespace이며 asset type으로 사용하지 않습니다.

## Ownership

- 하나의 asset에만 적용되는 유지보수 지식은 `docs/<asset-type>/<asset>/`에 둡니다.
- 같은 family가 공유하는 유지보수 지식이나 책임 경계는 `docs/<asset-type>/<family>/`에서 한 번만 설명합니다.
- family 문서는 `runtime taxonomy`, `registry`, `metadata schema`가 아닙니다. 실제 실행 진입점과 trigger는 각 asset이 계속 맡습니다.
- family 구성 정보를 별도 registry로 복제하지 않습니다. family 문서의 `README.md`에서 현재 구성 asset과 책임 경계를 사람이 읽을 수 있게 설명합니다.
- 구성 asset 수만으로 family 문서를 만들지 않습니다. family 자체가 지속적인 유지보수 경계일 때만 둡니다.

## Contract

각 유지보수 문서는 대응하는 asset 또는 family와 함께 다른 저장소로 옮겨도 이해·수정·복구할 수 있을 만큼 독립적이어야 합니다.

- 해당 asset 또는 family의 의도, 반드시 지켜야 할 조건, 유지보수·복구 방법, 쉽게 알 수 없는 결정을 이 문서 안에서 이해할 수 있게 합니다.
- 다른 저장소 전용 문서가 없으면 의미를 복원할 수 없는 숨은 의존성을 만들지 않습니다.
- 실행 동작의 정본을 문서에 복제하지 않습니다. 유지보수 문서는 맥락을 보존하기 위한 자료이지 실행 원본을 대신하지 않습니다.
- 실행에 필요한 instruction, reference, script, template 같은 자산은 유지보수 문서가 아니라 대응하는 runtime package가 소유합니다.

이 문서 묶음 안의 중복 경계는 이 문서의 Ownership과 Contract가 정합니다. 저장소 전반의 중복 판단은 [Documentation Principles](principles.md)를 따릅니다.

## Entrypoint

Asset별 문서에 README를 둘지와 진입점 역할은 [README Authoring](readme-authoring.md)을 따릅니다.

family 문서는 구성 asset과 공통 책임 경계를 설명해야 하므로 `README.md`를 진입점으로 둡니다. README도 대응하는 asset 또는 family와 함께 다른 저장소로 옮겨 쓸 수 있어야 합니다.

## Portability Review

유지보수 문서를 검토할 때 다음을 확인합니다.

- 이 디렉터리와 대응하는 asset 또는 family만으로 핵심 의도와 유지보수 경계를 이해할 수 있는가?
- 공통 지식이 각 구성 asset의 문서에 불필요하게 반복되어 있지 않은가?
- 외부 프로젝트 경로, 개인 작업 공간, 특정 플랫폼 UI에 불필요하게 의존하지 않는가?
- 외부 의존성이 꼭 필요하다면 그 이유와 출처가 분명한가?
