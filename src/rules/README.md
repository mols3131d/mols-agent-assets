# Rules

`rules/`에는 여러 task에 지속 적용되는 policy와 constraint의 source를 둡니다.

Rule은 이 저장소의 설계 개념입니다. 아래 projection과 discovery 규칙은 **repository-local, non-standard convention**이며 범용 Agent 표준이 아닙니다.

## Projections

### Directory scope

루트와 하위 디렉터리의 `AGENTS.md`로 directory subtree에 적용되는 Rule을 배포할 수 있습니다.

- root `AGENTS.md`: repository-wide 기본 Rule
- nested `AGENTS.md`: 해당 디렉터리와 하위 경로의 더 좁은 Rule
- target path에서는 root부터 target까지 applicable chain을 함께 고려

### Glob scope

여러 위치에 공통으로 적용되는 하위 디렉터리, 파일군, 확장자 지침은 glob selector 기반 Rule로 배포할 수 있습니다.

예:

```text
**/*.md
**/*.py
**/tests/**
```

Glob의 파일 형식, metadata field, discovery path는 target harness에 따라 달라질 수 있습니다. 특정 harness의 표현을 Rule 자체의 표준 schema로 간주하지 않습니다.

### Chatbot scope

`CHATBOT.md`는 **텍스트 입출력 중심의 chatbot surface**를 위한 비표준 Rule projection입니다. 웹 검색이나 서비스 plugin/tool을 사용할 수 있는 일반 chatbot에서도 사용할 수 있습니다.

Chatbot이 repository instruction을 찾을 때 이 저장소에서는 다음 fallback chain을 사용합니다.

```text
CHATBOT.md
  ↓ 없으면
AGENTS.md
  ↓ 없으면
README.md
```

- applicable `CHATBOT.md`가 있으면 chatbot-specific Rule source로 우선합니다.
- `CHATBOT.md`가 없으면 applicable `AGENTS.md`를 따릅니다.
- 둘 다 없으면 applicable `README.md`를 마지막 fallback instruction source로 사용합니다.
- 이 chain에서 `README.md`를 사용하는 것은 repository-local fallback일 뿐, README를 일반적인 Rule 형식이나 universal instruction source로 승격하지 않습니다.
- 다른 harness가 더 높은 system/user/platform authority를 정의하면 그 authority를 침범하지 않습니다.

Directory, glob, chatbot projection은 필요에 따라 함께 적용될 수 있습니다. 충돌과 precedence는 repository가 명시한 convention과 target harness의 실제 authority semantics를 따릅니다.

## Boundary

- 상황에 따라 모델이 선택적으로 로드해야 하는 context는 Rule보다 Skill을 우선 검토합니다.
- 한 task의 긴 workflow는 Rule에 넣지 않습니다.
- 동일한 공통 path/file-type Rule을 여러 `AGENTS.md`에 반복 복사하지 않습니다.
- `CHATBOT.md → AGENTS.md → README.md` fallback을 외부 표준처럼 설명하지 않습니다.
