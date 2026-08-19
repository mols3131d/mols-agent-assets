---
title: Rule Projections
description: 이 저장소에서 portable agent Rule의 canonical source와 target projection 책임 경계
---

# Rule Projections

이 저장소는 portable agent Rule의 canonical source를 `src/rulesync/.rulesync/rules/`에 보관한다. `src/rulesync/` 자체가 격리된 native Rulesync workspace이므로 별도 shape 변환은 필요하지 않는다.

```text
src/rulesync/.rulesync/rules/
  → Rulesync from src/rulesync/
  → temporary target-native Rule files for write-producing validation
```

`src/rulesync/rulesync.jsonc`가 projection target과 feature를 선택한다. Rulesync가 생성한 target file은 derived artifact이며 source authority가 아니고 이 repository에는 commit하지 않는다.

## Portable Agent Rules

- repository-wide Rule source는 `src/rulesync/.rulesync/rules/overview.md`를 canonical root로 사용한다.
- 추가 Rule은 `src/rulesync/.rulesync/rules/*.md`에 두고 Rulesync-compatible front matter로 scope/trigger를 표현한다.
- target별 path, filename, glob representation과 embedded/native 차이는 temporary workspace copy에서 projection을 생성해 검증한다.
- target이 canonical capability를 완전히 표현하지 못하면 해당 차이를 숨기거나 full parity로 주장하지 않는다.
- generated target Rule을 source authority로 유지하지 않는다.

현재 Tier A projection target은 `src/rulesync/rulesync.jsonc`이 선언한 GitHub Copilot과 Google Antigravity IDE다. 다른 target을 추가할 때는 Rulesync capability와 실제 generated result를 temporary workspace copy에서 검증한 뒤 승격한다.

## Repository Runtime Boundary

Repository root의 `.rulesync/`, `rulesync.jsonc`, 또는 harness-native Rule/Skill/Agent directory를 distribution source나 generated evidence로 commit하지 않는다. Canonical `.rulesync/`는 오직 격리된 `src/rulesync/` workspace 아래에 둔다. 이 경계는 이 asset-library repository가 보관한 자산을 자기 runtime configuration으로 자동 인식하는 것을 방지한다.

## Chat Runtime Compatibility Boundary

`CHATBOT.md`는 Rule projection이나 별도 Rule authority가 아니다. repository-aware chat runtime이 path-scoped Rule을 자동 discovery/load하지 못할 때 **누락된 harness behavior를 보정하는 compatibility entry**다.

세부 contract는 [CHATBOT Runtime Compatibility Layer](../common/standards/chatbot-repository-bootstrap.md)이 소유한다.

역할을 다음처럼 분리한다.

- Rule source 또는 active target Rule surface가 policy, selector, precedence를 소유한다.
- `CHATBOT.md`는 known target path와 selector가 일치하는 Rule을 discovery/load하도록 연결한다.
- Rule body, full Rule catalog, glob table을 `CHATBOT.md`에 복제하지 않는다.
- active runtime이 같은 Rule discovery/loading을 이미 제공하면 compatibility layer가 중복 수행하지 않는다.

Chat runtime의 tool capability가 coding-oriented harness와 다르더라도 Rule taxonomy를 별도로 만들지 않는다. 동일한 policy를 공유할 수 있으면 기존 Rule authority를 사용하고 target이 해당 semantics를 표현할 수 없는 실제 차이만 명시적 exception으로 남긴다.

## Boundary

- canonical Rule과 chat-runtime compatibility entry를 독립 policy authority로 유지하지 않는다.
- canonical Rule과 temporary generated target output을 독립 authority로 유지하지 않는다.
- Rulesync가 지원하지 않는 semantics가 실제로 필요한 target에는 명시적 exception을 둘 수 있지만 그 exception을 portable source처럼 일반화하지 않는다.
