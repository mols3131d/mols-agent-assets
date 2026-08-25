# Catalog

이 디렉토리는 여러 프로젝트에서 자주 재사용하는 외부 Agent Skill source를 기록합니다.

`skills.json`은 설치 상태나 dependency lock이 아니라 **다시 찾고 설치하기 위한 curated catalog**입니다. 실제 설치 방식, target, scope와 update 동작은 사용할 시점의 upstream 및 `skills` CLI contract를 따릅니다.

## Files

- `skills.json` — 자주 재사용하는 외부 Skill source 목록

## Entry

각 항목은 필요한 최소 정보만 가집니다.

- `name` — catalog에서 식별할 이름
- `source` — upstream GitHub repository (`owner/repo`)
- `description` — 선택할 때 참고하는 짧은 설명

고정 revision, 설치 경로, target별 상태와 computed hash 같은 lock 정보는 여기에 두지 않습니다. 특정 repository가 실제 dependency로 사용하는 Skill의 상태는 해당 dependency 관리 surface가 소유합니다.
