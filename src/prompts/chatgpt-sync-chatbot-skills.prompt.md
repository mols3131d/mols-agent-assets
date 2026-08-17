# ChatGPT Chatbot Skill Sync

GitHub 저장소 `mols3131d/mols-agent-assets`의 최신 `main`을 source of truth로 사용해 ChatGPT용 Skill을 현재 설치 상태와 동기화하라.

대상은 다음 두 repository-local target profile이다.

- `src/skills-chatbot/` — 단일 `*.skill.md`로 완결되는 flat chatbot Skill
- `src/skills-chatbot-runtime/` — `SKILL.md`와 필요한 references, scripts, assets 등으로 구성된 runtime chatbot Skill package

목표는 모든 파일을 무조건 설치하는 것이 아니다. Repository의 capability와 현재 ChatGPT에 설치된 Skill을 비교해 **신규 설치, 업데이트, rename migration, sibling 선택, 충돌 보고**를 안전하게 결정한다.

## Core Contract

- Repository의 최신 `main`을 canonical source로 사용한다.
- 같은 capability의 flat/runtime sibling은 ChatGPT에 동시에 설치하지 않는다.
- 설치된 Skill과 repository Skill의 identity를 이름만으로 판단하지 않는다.
- 같은 Skill이면 중복 설치하지 말고 업데이트한다.
- 이름이 달라도 같은 Skill의 rename이면 가능한 한 기존 installation을 migration한다.
- 이름이 같아도 다른 Skill이면 자동 overwrite하지 않는다.
- identity가 불확실한 destructive action은 수행하지 않고 사용자에게 선택지를 제시한다.
- repository에서 대응되지 않는 기존 installed Skill은 자동 삭제하지 않는다.
- 현재 ChatGPT가 설치된 Skill을 조회하거나 수정할 수 없다면 중복을 추측해 설치하지 말고, 수행할 수 없는 reconciliation 단계를 명확히 보고한다.

## Capability Identity

Skill 이름은 identity의 강한 signal이지만 identity 자체는 아니다.

같은 capability인지 판단할 때 가능한 근거를 다음 순서로 사용한다.

1. stable identity, provenance, 이전 이름 등 명시적 metadata
1. Git history의 rename, move, replacement 기록
1. 주책임과 intended outcome
1. activation intent와 negative boundary
1. 핵심 behavioral contract와 invariants
1. 주요 workflow와 decision rules
1. runtime resource와 dependency 관계
1. name과 description

다음이 실질적으로 이어지면 이름이 달라도 같은 Skill의 revision 또는 rename일 수 있다.

- 해결하려는 문제가 같다.
- activation 상황이 같다.
- responsibility와 outcome이 같다.
- 핵심 behavioral contract가 연속된다.
- 새 버전이 기존 버전의 자연스러운 후속 revision으로 설명된다.

반대로 이름이 같더라도 activation, responsibility, outcome 또는 핵심 contract가 다르면 다른 Skill로 취급한다.

단순히 이름이 비슷하거나 같은 broad domain에 속한다는 이유로 identity를 합치지 않는다.

## Repository Sibling Selection

먼저 `skills-chatbot`과 `skills-chatbot-runtime` 사이에서 같은 capability의 target-specific sibling을 식별한다.

같은 capability의 sibling은 최종 설치 상태에서 하나만 남긴다.

ChatGPT가 runtime package의 resources와 dependencies를 완전히 지원하고, 그것들이 capability fidelity나 실제 동작을 의미 있게 개선하면 runtime variant를 선택한다.

다음 중 하나면 flat variant를 선택한다.

- runtime dependency가 현재 ChatGPT에서 완전히 지원되지 않는다.
- bundled resource가 실제 동작에 기여하지 않는다.
- flat variant만으로 같은 capability를 충분히 제공한다.
- runtime variant가 불필요한 복잡성만 늘린다.

디렉터리 이름, 파일 수, 문서 길이만으로 runtime variant를 우선하지 않는다.

선택되지 않은 sibling은 별도 Skill로 설치하지 않는다.

## Installed Skill Reconciliation

Repository에서 선택한 각 capability마다 현재 installed Skills에서 대응 후보를 찾고 다음 규칙을 적용한다.

### Same Name, Same Identity

이름과 capability identity가 모두 같으면 기존 Skill을 **update**한다.

- 새 Skill을 추가 설치하지 않는다.
- 가능한 경우 기존 installation identity와 사용자 설정을 유지한다.
- repository의 최신 canonical content와 runtime resources로 갱신한다.
- activation, responsibility, behavioral contract, guardrail이 의도치 않게 약화되지 않았는지 확인한다.

이미 최신이면 변경하지 않는다.

### Same Name, Different Identity

이름은 같지만 capability identity가 다르면 **name collision**이다.

자동 overwrite, 삭제, 병합하지 않는다.

사용자에게 다음 선택지를 제시하고 결정 전에는 충돌 상태로 남긴다.

- **Override** — 기존 installed Skill을 repository Skill로 교체
- **Install separately** — repository Skill의 canonical identity를 유지하면서 충돌하지 않는 새 이름으로 별도 설치
- **Skip** — repository Skill 설치를 보류하고 기존 Skill 유지

경고에는 최소한 다음 차이를 보여준다.

- activation
- responsibility
- intended outcome
- 핵심 behavioral contract

새 이름이 필요하더라도 임의 suffix를 확정하지 말고 사용자가 식별 가능한 이름을 선택할 수 있게 한다.

### Different Name, Same Identity

이름은 다르지만 같은 capability이고 rename 근거가 충분하면 **신규 설치가 아니라 update + rename migration**으로 처리한다.

가능하면 다음 상태를 만든다.

```text
old-name → new-canonical-name
```

- 기존 installation identity를 유지한다.
- repository의 현재 canonical name으로 rename한다.
- content와 resources를 최신 version으로 업데이트한다.
- old/new Skill을 동시에 활성 상태로 남기지 않는다.

Git history, metadata, provenance, responsibility continuity 등에서 rename이 충분히 확인되지 않으면 자동 migration하지 않는다.

이 경우 사용자에게 다음 선택지를 제시한다.

- 기존 Skill을 새 canonical Skill로 migration
- 기존 Skill 유지 + repository Skill 별도 설치
- repository Skill 설치 보류

### Repository Only

설치된 대응 Skill이 없으면 신규 설치한다.

단, repository sibling selection을 먼저 완료한 뒤 선택된 variant만 설치한다.

### Installed Only

현재 설치되어 있지만 repository에서 대응 capability를 확인하지 못한 Skill은 자동 삭제하지 않는다.

다음 중 하나로만 분류해 보고한다.

- repository 관리 대상이 아닌 사용자 Skill
- repository에서 제거된 과거 Skill 후보
- rename 추적에 실패한 orphan candidate

삭제나 migration은 별도의 사용자 결정 없이는 수행하지 않는다.

## Rename Detection

Rename은 보수적으로 판정한다.

강한 근거:

- Git history의 실제 rename 또는 move
- metadata의 이전 이름, stable ID, provenance
- old capability가 사라지고 new capability가 동일한 책임을 승계한 기록
- activation, responsibility, outcome, contract의 강한 연속성

약한 근거만으로 rename을 확정하지 않는다.

- 이름이 비슷함
- description 일부가 비슷함
- 같은 broad domain
- 일부 규칙이나 문장이 겹침

Rename 여부가 불확실하면 중복보다 destructive misclassification을 더 위험하게 취급하고 사용자에게 확인한다.

## Update Fidelity

같은 Skill을 업데이트할 때 repository version을 canonical source로 사용하되 단순 텍스트 교체로 취급하지 않는다.

다음을 비교한다.

- activation intent
- negative boundary
- responsibility
- intended outcome
- behavioral contract와 invariants
- workflow와 decision rules
- guardrails
- validation과 failure behavior
- output contract
- runtime resource 관계

현재 installed version에 repository에 없는 내용이 있으면 먼저 출처를 구분한다.

- 과거 repository version에서 남은 stale content → canonical version으로 갱신
- 사용자 고유 customization → 보존 대상 또는 conflict candidate

사용자 customization이 새 canonical contract와 충돌하면 자동으로 제거하지 않고 충돌을 보고한다.

## Runtime Package Handling

`src/skills-chatbot-runtime/<skill>/`을 선택한 경우 package 전체를 하나의 Skill로 취급한다.

- `SKILL.md`를 중심으로 실제 runtime-required resources를 식별한다.
- references, scripts, assets 등 실행에 필요한 파일 관계를 보존한다.
- maintainer-only docs, evals, tests 또는 package에 포함될 필요가 없는 파일은 설치하지 않는다.
- ChatGPT에서 지원되지 않는 dependency 때문에 capability가 조용히 축소되지 않게 한다.
- 핵심 runtime capability를 보존할 수 없으면 호환 가능한 flat sibling을 선택하거나 설치를 보류한다.

## Safety Boundary

충분한 identity 근거 없이 다음을 수행하지 않는다.

- 기존 Skill overwrite
- 기존 Skill 삭제
- 기존 Skill rename
- 두 installed Skills 병합
- 사용자 customization 제거
- same-name collision 자동 해소

반대로 같은 capability임이 충분히 확인된 sibling이나 rename 관계는 중복 설치하지 않는다.

명확한 update, install, sibling selection은 Skill마다 반복 확인을 요구하지 말고 일괄 처리한다. 사용자 결정은 실제 충돌이나 destructive ambiguity가 있는 경우에만 요청한다.

## Decision Flow

```text
repository capability
    │
    ├─ flat/runtime sibling?
    │    ├─ yes → ChatGPT에 적합한 variant 하나 선택
    │    └─ no  → 그대로 진행
    │
    └─ installed Skill과 비교
         │
         ├─ same name + same identity
         │    → update
         │
         ├─ same name + different identity
         │    → conflict: override / install separately / skip
         │
         ├─ different name + same identity + rename confirmed
         │    → update + rename migration
         │
         ├─ different name + probable same identity, uncertain
         │    → conflict: migrate / install separately / skip
         │
         └─ no corresponding Skill
              → install
```

## Execution

현재 ChatGPT가 제공하는 공식 Skill inspection, creation, update, rename, installation capability를 사용한다.

가능한 작업은 실제로 수행하고, 지원되지 않는 mutation을 수행했다고 가정하거나 보고하지 않는다.

현재 환경이 installed Skills 조회를 지원하지 않으면 신규 설치 전에 그 제한을 명시하고, duplicate/collision/rename reconciliation을 수행할 수 없는 상태에서 무조건 일괄 설치하지 않는다.

## Final State Invariants

동기화가 완료된 범위에서는 다음을 만족해야 한다.

- 동일 capability의 flat/runtime sibling이 동시에 설치되어 있지 않다.
- rename된 동일 Skill의 old/new name이 동시에 설치되어 있지 않다.
- same-name different-identity Skill을 임의 overwrite하지 않았다.
- repository canonical version과 installed version 사이에 확인 가능한 의미 drift가 남아 있지 않다.
- 사용자 고유 Skill이나 customization을 근거 없이 삭제하지 않았다.
- 수행하지 못한 reconciliation이나 mutation을 완료했다고 표현하지 않았다.

## Report

완료 후 장황한 내부 reasoning이나 파일별 작업 로그 대신 다음 상태만 간단히 보고한다.

### Installed

새로 설치한 Skill.

### Updated

같은 identity로 확인하여 갱신한 Skill.

### Renamed / Migrated

기존 Skill을 새 canonical name으로 migration한 항목을 `old-name → new-name`으로 표시한다.

### Skipped

이미 최신이거나 sibling selection에서 제외한 Skill.

### Conflicts

자동 처리하지 않은 충돌. 각 항목에 repository Skill, installed Skill, 충돌 이유, 가능한 사용자 선택을 표시한다.

### Orphan Candidates

현재 설치되어 있지만 repository에서 대응 capability를 확인하지 못한 Skill.

### Limitations

현재 ChatGPT 환경의 기능 제한 때문에 확인하거나 수행하지 못한 단계가 있을 때만 표시한다.
