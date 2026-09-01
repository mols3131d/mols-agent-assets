# Entrypoint

README, 디렉터리·문서 번들의 진입점, 온보딩 첫 화면처럼 독자가 어떤 범위에 처음 들어왔을 때 **무엇인지 파악하고 다음 행동을 선택하게 하는 문서**에 적용한다.

이 reference는 entrypoint의 역할만 다룬다. 일반 문서의 정보 구조·신뢰성·ownership 원칙은 상위 `SKILL.md`가 소유하고, Markdown 표현은 `markdown.md`가 소유한다.

## Create only when needed

Entrypoint 문서는 다음 중 하나 이상이 실제 문제일 때 만든다.

- 범위의 목적이나 역할을 파일·디렉터리 이름만으로 알기 어렵다.
- 독자가 여러 하위 문서·파일 중 무엇부터 봐야 하는지 선택해야 한다.
- 첫 실행, 첫 사용, 첫 탐색에 필요한 prerequisite나 경계가 있다.
- 상세 정보의 canonical owner가 여러 곳에 있어 첫 navigation이 필요하다.
- 이 범위에서 하지 말아야 할 것 또는 다른 owner로 넘어가야 할 것이 중요하다.

파일이나 디렉터리가 존재한다는 이유만으로 entrypoint 문서를 만들지 않는다. 이미 상위 entrypoint가 같은 범위를 충분히 설명하면 새 문서를 추가하지 않는다.

## Core questions

Entrypoint는 가능한 한 빠르게 다음 질문에 답한다.

1. 이 범위는 무엇인가?
1. 언제 여기서 시작해야 하는가?
1. 처음 무엇을 읽거나 실행하거나 선택해야 하는가?
1. 중요한 경계나 prerequisite는 무엇인가?
1. 자세한 정보의 canonical owner는 어디인가?

모든 질문이 항상 별도 섹션을 필요로 하지는 않는다. 독자가 실제로 필요로 하는 것만 남긴다.

## Recommended flow

기본 흐름은 다음처럼 단순하게 유지한다.

`범위 소개 → 첫 행동 → 자세한 정보`

필요하면 prerequisite, 선택 기준, 경계나 troubleshooting으로 확장한다. source tree를 그대로 설명하는 목차로 만들지 않는다.

## First action

- 가능한 경우 가장 일반적인 첫 경로 하나를 먼저 제시한다.
- 여러 선택지가 있으면 독자가 선택할 수 있는 기준을 함께 제공한다.
- quick start는 실제로 따라 할 수 있는 최소 단위여야 한다.
- 예시는 핵심 경로를 이해하는 데 필요한 만큼만 둔다.
- 상세 절차가 다른 canonical 문서에 있으면 반복하지 않고 연결한다.

## Navigation

- 하위 파일이나 문서를 전부 나열하지 않는다.
- 독자가 다음 결정을 내리는 데 필요한 링크만 둔다.
- 링크 이름만 보고 목적을 추측하기 어렵다면 짧은 맥락을 붙인다.
- 수동으로 유지해야 하는 파일 목록이나 상태 목록은 실제 탐색 이득이 유지비용보다 클 때만 둔다.

## README

README는 가장 흔한 entrypoint 형식이지만 특별한 catch-all 문서가 아니다.

- repository, directory, package, document bundle의 첫 화면 역할이 실제로 필요할 때 사용한다.
- 모든 정책, 설계, 사용법, 이력과 상태를 README 하나에 모으지 않는다.
- 상세 책임은 해당 canonical 문서로 넘기고 README에는 첫 이해와 첫 행동에 필요한 맥락만 둔다.
- 상위 README의 구조를 하위 README마다 기계적으로 반복하지 않는다.

## Restraint

다음은 실제 효용이 없으면 추가하지 않는다.

- 내용 없는 소개 문단
- 자동 생성되지 않는 장황한 파일 목록
- 짧은 문서의 목차
- 의미 없는 badge나 status decoration
- 모든 하위 문서를 복제하는 navigation
- canonical 문서의 요약본을 여러 곳에 반복하는 구조

## Review

완성 후 다음을 확인한다.

- 처음 온 독자가 이 범위의 역할을 빠르게 알 수 있는가?
- 가장 일반적인 다음 행동이 명확한가?
- 선택지가 있다면 선택 기준이 보이는가?
- 상세 정보가 canonical owner에 연결되는가?
- entrypoint 자체가 새로운 유지보수 허브나 중복 source가 되지 않았는가?
- README라는 형식 때문에 필요 이상의 내용을 담고 있지 않은가?
