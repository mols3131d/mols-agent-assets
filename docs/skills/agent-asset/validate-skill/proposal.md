# Validate Skill

## 기획

### 목적

`validate-skills`는 Agent Skills 형식에 맞게 작성되었는지 검증하는 전용 스킬이다.
기존 `create-skills`가 스킬을 생성하고 고도화하는 역할이라면, 이 스킬은 생성된 스킬이
표준 구조와 포맷을 지켰는지 확인하는 품질 게이트 역할을 맡는다.

핵심 관심사는 "좋은 스킬인가"보다 먼저 "스킬로 로딩될 수 있는 올바른 형식인가"이다.
따라서 검증 기준은 주관적 평가보다 구조, frontmatter, 파일 참조, 리소스 배치, 스크립트
인터페이스처럼 기계적으로 확인 가능한 항목을 우선한다.

### 배경

Agent Skills는 최소 `SKILL.md` 하나로 동작하지만, 실제로는 다음 이유로 형식 오류가 자주 생긴다.

- `name`과 폴더명이 다르다.
- frontmatter가 YAML로 파싱되지 않는다.
- `description`이 너무 짧거나 사용 시점을 설명하지 않는다.
- `references/` 파일은 있지만 `SKILL.md`에서 연결하지 않는다.
- placeholder 파일이나 TODO가 남아 있다.
- 스크립트가 interactive input을 요구하거나 `--help`가 없다.
- 특정 클라이언트 전용 설정을 범용 Agent Skills 필수 요소처럼 작성한다.

이런 오류는 스킬 사용 시점에 늦게 발견된다. 검증 스킬은 생성 직후 또는 배포 전에 빠르게
실행할 수 있는 표준 검증 절차를 제공해야 한다.

### 사용자 시나리오

- 사용자가 새 스킬 폴더를 만든 뒤 "이 스킬 형식 맞는지 검증해줘"라고 요청한다.
- `create-skills`로 생성한 스킬을 배포하기 전에 검증한다.
- 기존 스킬을 Agent Skills 표준에 맞게 이식하면서 형식 위반을 찾는다.
- 여러 스킬 폴더를 대상으로 CI 또는 로컬 스크립트에서 반복 검증한다.
- 스킬 검증 결과를 `error`, `warning`, `info`로 나누어 수정 우선순위를 정한다.

### 범위

검증한다:

- 스킬 루트와 `SKILL.md` 존재 여부
- YAML frontmatter 구조와 허용 필드
- `name`, `description`, `compatibility`, `metadata`, `allowed-tools` 형식
- Markdown body 존재 여부와 과도한 길이
- `references/`, `scripts/`, `assets/` 리소스 사용 방식
- `SKILL.md`의 상대 경로 참조가 실제 파일과 일치하는지
- placeholder, TODO, 불필요한 보조 문서 잔존 여부
- 스크립트의 기본 실행성, `--help`, 비대화형 인터페이스

검증하지 않는다:

- 스킬이 실제 업무에서 좋은 결과를 내는지에 대한 정성 평가
- 특정 LLM이나 클라이언트의 활성화 확률을 정확히 예측하는 일
- 외부 API, MCP, 비밀값, 네트워크 연결의 실제 성공 여부
- 스킬의 도메인 지식이 사실인지에 대한 전문 검증

### 성공 기준

- 형식 위반은 `error`로 명확히 보고한다.
- 개선 권고는 `warning`이나 `info`로 분리한다.
- 결과는 사람이 읽기 쉬우면서도 자동화가 가능한 JSON 형태로 받을 수 있다.
- 검증 스크립트는 비대화형으로 실행된다.
- 오류 메시지는 어떤 파일의 어떤 규칙을 고쳐야 하는지 설명한다.
- `create-skills`와 역할이 겹치지 않는다. 생성은 `create-skills`, 검증은 `validate-skills`가 맡는다.

## 설계

### 스킬 이름과 위치

- 이름: `validate-skills`
- 위치: `.agents/skills/validate-skills`
- 역할: Agent Skills 형식 검증 전용

예상 구조:

```text
.agents/skills/validate-skills/
├── SKILL.md
├── references/
│   └── validation-rules.md
└── scripts/
    └── validate_skill.py
```

### SKILL.md 설계

`SKILL.md`는 짧게 유지한다. 매번 필요한 검증 절차와 스크립트 사용법만 담고, 세부 규칙은
`references/validation-rules.md`로 분리한다.

포함할 내용:

- 이 스킬이 검증 전용임을 명시
- 입력으로 받을 수 있는 대상:
  - 단일 스킬 디렉터리
  - 여러 스킬 디렉터리
  - 현재 작업 중인 스킬 경로
- 기본 절차:
  1. 대상 경로 확인
  2. `scripts/validate_skill.py` 실행
  3. 결과를 `error`, `warning`, `info`로 해석
  4. 필요하면 파일을 읽고 원인 설명
  5. 사용자가 요청한 경우 수정안 제시
- `skills-ref validate`가 설치되어 있으면 함께 실행하도록 안내
- 형식 검증과 품질 평가의 경계를 명확히 구분

### 검증 스크립트 설계

스크립트는 가능한 많은 검증을 담당한다. 모델 판단은 스크립트가 잡기 어려운 설명 품질,
과도한 범위, 특정 클라이언트 종속성 해석에만 사용한다.

CLI 예시:

```bash
python3 scripts/validate_skill.py path/to/skill
python3 scripts/validate_skill.py path/to/skill --format json
python3 scripts/validate_skill.py path/to/skill --strict
python3 scripts/validate_skill.py .agents/skills/* --recursive
```

출력 형태:

```json
{
  "status": "fail",
  "summary": {
    "errors": 1,
    "warnings": 2,
    "infos": 1
  },
  "results": [
    {
      "level": "error",
      "code": "name_mismatch",
      "path": "SKILL.md",
      "message": "frontmatter name과 부모 디렉터리명이 다릅니다."
    }
  ]
}
```

### 검증 등급

- `error`: Agent Skills 형식 위반 또는 로딩 실패 가능성이 높은 문제
- `warning`: 로딩은 가능하지만 호환성, 재사용성, 유지보수성에 위험이 있는 문제
- `info`: 참고용 개선 제안

`--strict` 모드에서는 일부 `warning`을 실패 상태로 취급할 수 있다.

### 주요 검증 규칙

필수 구조:

- 대상 경로가 디렉터리인지
- `SKILL.md`가 루트에 있는지
- `SKILL.md`가 비어 있지 않은지
- frontmatter와 body가 분리되어 있는지

Frontmatter:

- YAML 파싱 가능 여부
- 필수 필드 `name`, `description`
- 허용 필드만 사용했는지
- `name` 규칙과 폴더명 일치
- `description` 길이와 placeholder 여부
- `compatibility` 길이
- `metadata` mapping 여부
- `allowed-tools` 문자열 여부

본문:

- body 존재 여부
- TODO placeholder 잔존 여부
- 500줄 초과 여부
- 기본 절차나 완료 기준이 있는지

리소스:

- `references/*.md`가 `SKILL.md`에서 연결되어 있는지
- `SKILL.md`에서 언급한 상대 경로가 존재하는지
- 비어 있는 리소스 디렉터리가 있는지
- 예시 파일이 그대로 남아 있는지

스크립트:

- Python 파일 문법 검사
- 실행 스크립트의 shebang 여부
- `--help` 실행 가능 여부
- interactive input 의심 패턴 검사
- 위험한 명령이나 삭제 작업이 있으면 안전장치 여부 경고

### create-skills와의 분리

`create-skills`에 있는 검증 기능은 최소화한다.

- `create-skills`: 스킬 생성, 구조 설계, 리소스 작성, 고도화
- `validate-skills`: 형식 검증, 규칙 검사, 배포 전 품질 게이트

이후 `create-skills`의 `scripts/validate_skill.py`는 제거하거나 `validate-skills` 스킬의 스크립트를
호출하도록 바꾸는 방향이 좋다.
