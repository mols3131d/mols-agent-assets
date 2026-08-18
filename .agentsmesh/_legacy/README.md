# AgentsMesh Legacy Staging

이 디렉터리는 Project EXODUS 중 현재 `src/` source tree를 **변형 없이 복제한 임시 migration staging area**다.

## Authority

- 현재 canonical authority는 여전히 원래 `src/`에 있다.
- `.agentsmesh/_legacy/src/`는 migration 작업용 snapshot이며 직접 편집하지 않는다.
- asset을 AgentsMesh-native 형태로 전환할 때 원본과 이 snapshot을 비교 근거로 사용할 수 있다.

## AgentsMesh boundary

AgentsMesh는 `_`로 시작하는 canonical file/directory를 generation에서 제외한다. 따라서 `_legacy/` 내용은 아직 target-native output의 source가 아니다.

`_root.md`는 AgentsMesh의 특별한 예외이므로 이 staging tree에서는 사용하지 않는다.

## Migration

각 asset은 검증 후 필요한 canonical surface로 하나씩 승격한다.

```text
_legacy/src/rules/*     -> ../rules/*
_legacy/src/skills/*    -> ../skills/*
_legacy/src/agents/*    -> ../agents/*
_legacy/src/prompts/*   -> ../commands/* when semantically compatible
```

Hosted chatbot profiles와 AgentsMesh scope 밖의 자산은 억지로 승격하지 않는다.

Cutover가 끝나고 모든 legacy responsibility가 새 owner 또는 명시적 retirement로 매핑되면 `_legacy/`를 제거한다.

## Snapshot

- source branch: `agent/refactor/agentsmesh-migration`
- source commit: `6b9653c1e342ec22db520c62616d7be4a1539d38`
- source tree: `src/` @ `6a678b8ffd3adabb5c232700df50e3fb63225f9f`
