---
description: Agent Asset과 family의 유지보수 문서 배치, 이식성, 실행 원본과의 책임 경계를 정할 때 사용합니다.
---

# Asset Maintainer Documentation

유지보수 문서는 **실행 방법의 복제본이 아니라 변경·복구에 필요한 맥락**을 보존한다. 이 저장소에서는 `docs/<asset-type>/<owner>/`에 두며, `<owner>`는 개별 자산 또는 유지보수 책임을 공유하는 family다.

## 책임과 구성

- 개별 자산의 의도·제약·설계 결정·복구 지식은 해당 자산 문서에 둔다. 실행 instruction·reference·script·template의 정본은 runtime package가 소유한다.
- Family에 지속적으로 공유할 책임이 있을 때만 family 문서를 만든다. 공통 내용은 한곳에서 관리하고, `README.md`에서 구성 자산과 책임 경계를 안내한다. Family를 별도 runtime taxonomy·registry로 만들지 않는다.
- 개별 자산의 README 필요성은 [README Authoring](../../../documentation/readme-authoring.md)을 따른다. 자산 수만으로 문서나 family를 늘리지 않는다.
- 자산·family와 문서를 함께 옮겼을 때 핵심 의도와 유지보수 방법을 이해할 수 있어야 한다. 특정 저장소의 숨은 의존성이나 실행 원본의 중복을 만들지 않는다.

## 배치와 탐색

`development/`, `documentation/`, `references/`, `tools/`는 일반 문서 영역이며 asset type이 아니다. 이 저장소의 `docs/INDEX.tsv`에는 자산 유형 디렉터리만 노출하고 하위 개별 유지보수 문서는 열거하지 않는다. `docs/<asset-type>/` 아래에는 별도 자동 `INDEX.tsv`를 만들지 않는다. 내부 탐색은 자산·family README와 검색을 사용한다.

문서 전반의 중복·배치 판단은 [Documentation Principles](../../../documentation/principles.md), 인덱스 선택 기준은 [Document Indexing](../../../documentation/indexing.md)이 소유한다.
