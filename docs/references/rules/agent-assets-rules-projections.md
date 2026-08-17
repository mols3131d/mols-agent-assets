---
title: Rule Projections
description: 이 저장소에서 Rule을 directory, glob, chatbot surface에 배치하는 repository-local convention
---

# Rule Projections

이 문서는 Personal Agent Asset Standard의 **Rule 유형에만 적용되는 비표준 projection**을 소유한다.

## Directory — `AGENTS.md`

루트와 하위 디렉터리의 `AGENTS.md`를 directory subtree Rule로 사용한다.

- root `AGENTS.md` → repository-wide 기본 Rule
- nested `AGENTS.md` → 해당 directory와 하위 경로의 더 좁은 Rule
- target을 다룰 때 applicable ancestor chain을 함께 고려

실제 precedence와 override semantics는 target harness의 규격을 따른다.

## Glob

directory tree 하나로 표현하기 어려운 공통 파일군은 harness가 지원하는 glob selector를 사용한다.

```text
**/*.md
**/*.py
**/tests/**
```

- target path와 selector가 일치할 때만 적용한다.
- 같은 file-type Rule을 여러 `AGENTS.md`에 복제하기보다 glob을 우선 검토한다.
- glob schema와 discovery path는 harness-specific이며 범용 Rule 표준으로 취급하지 않는다.

## Chatbot — `CHATBOT.md`

`CHATBOT.md`는 텍스트 입출력 중심 chatbot surface를 위한 repository-local Rule projection이다.

Repository instruction fallback은 다음과 같다.

```text
CHATBOT.md
  ↓ 없으면
AGENTS.md
  ↓ 없으면
README.md
```

- applicable `CHATBOT.md`가 있으면 chatbot Rule로 우선한다.
- 없으면 applicable `AGENTS.md`를 사용한다.
- 둘 다 없을 때만 `README.md`를 fallback instruction source로 사용한다.
- README 자체를 일반적인 Rule 형식으로 간주하지 않는다.
- platform/system/user/tool authority는 이 fallback보다 우선한다.

## Boundary

Directory, glob, chatbot projection은 scope가 겹치면 함께 적용될 수 있다. 같은 policy의 의미를 여러 projection에서 독립적으로 정의하지 말고, 필요한 최소 로컬 적용만 둔다.

이 문서의 projection은 외부 범용 표준이 아니라 **mols-agent-assets의 Personal Agent Asset Standard 확장**이다.
