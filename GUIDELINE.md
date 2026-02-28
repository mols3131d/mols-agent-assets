# GUIDELINE

> mols-agent는 개인 프로젝트이며, 이 문서는 워크스페이스의 기술적 명세와 에이전트 운영 표준을 정의합니다.

## 1. 언어 표준 (Language Standard)

인간과 에이전트 간의 효율적인 협업을 위해 언어의 역할을 분리합니다.

- **인터랙션 및 서술 (Interaction/Narrative)**: **한국어 (Korean)**
    - 에이전트와의 대화, 추론 과정 설명, 모든 문서 및 리드미(`README.md`, `*.md`).
    - 사용자와의 의사소통 정확도 및 풍부한 맥락 전달을 목표로 합니다.
- **기술적 자산 (Technical Assets)**: **영어 (English)**
    - 소스 코드, 커밋 메시지, 로그, 내부 변수명, 시스템 아티팩트.
    - LLM 간의 논리적 이식성 확보 및 토큰 효율성을 최적화합니다.

## 2. 마크다운 표준 (Markdown & Schema)

모든 문서는 일관된 구조와 에이전트 인지 최적화를 위해 다음 규약을 준수합니다.

### 링크 프로토콜

- **루트 상대 경로**: 모든 링크는 워크스페이스 루트를 기준으로 하며, 반드시 `/`로 시작해야 합니다.
    - 예: `[이름](/path/to/asset.md)`
- **무결성**: 잘못된 경로는 에이전트의 길찾기(Navigating) 오류를 유발하므로 즉시 수정해야 합니다.

### 프론트매터 (Frontmatter)

모든 `.md` 파일은 Hugo 호환 YAML 형식을 포함해야 합니다.

- `title`, `description`, `categories`, `date`, `lastmod`, `tags`
- **에이전트 제어 필드**: `agent-readable`, `agent-editable`, `agent-moveable`, `agent-deletable` (boolean)

## 3. 에이전트 운영 표준 (AOS)

에이전트는 단순히 명령을 수행하는 것을 넘어, 다음의 '지능 자산 관리' 프로토콜을 따릅니다.

### 자산 라이프사이클 (ACE-Kernel)

1. **RFC (Request for Comments)**: 새로운 로직 제안 시 TAS 페르소나 시스템을 통한 비판적 토론.
2. **ADR (Architecture Decision Record)**: 합의된 결론의 맥락과 결정 사항을 영구히 기록.
3. **REQ (Requirements)**: ADR을 바탕으로 실제 구현(Forge)을 위한 명세 작성.

### TAS 페르소나 시스템

복잡한 의사결정 시 다음 세 하브 에이전트의 논리적 충돌을 활용합니다.

- **Thesis (Leni 💛)**: 창의적 프로토타이핑, 긍정적 시도.
- **Antithesis (Kana 🟥)**: 냉철한 회의론, 맹점 분석 및 비판.
- **Synthesis (Rin 🔵)**: 갈등을 승화시킨 최적의 최종 결론(Main Agent).

## 4. 파일 관리 및 안전 제약

- **소프트 삭제 (Soft Delete)**: 어떠한 경우에도 파일을 영구 삭제하지 않습니다. 모든 삭제 대상은 `/.trash/` 디렉토리로 이동시키며, 파일명 충돌 시 이름을 변경하여 보존합니다.
- **결과물 분리 (NOT_FOR_RESULT)**: `.agents/` 디렉토리는 제어 로직 전용 공간입니다. 실제 프로젝트 결과물은 반드시 `/outputs/` 또는 `/studio/` 내에 저장해야 합니다.
- **미니멀리즘 (Karpathy Principle)**: 최소한의 코드로 문제를 해결하며, 과도한 추상화나 불필요한 기능(Speculative Features)을 배제합니다.
