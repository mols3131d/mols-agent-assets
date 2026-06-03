---
name: create-skills
description: >
  Agent Skills 표준에 맞는 범용 스킬 생성 및 개선 워크플로. 사용자가 새 스킬을
  만들거나 기존 스킬을 고도화하라고 요청할 때 사용한다. SKILL.md frontmatter,
  description 트리거 최적화, progressive disclosure, scripts/references/assets 설계,
  평가와 검증 루프를 포함한다. Use when: "create skill", "make agent skill",
  "스킬 생성", "스킬 만들기", "스킬 고도화", "create-skills", "/create-skills".
---

# Create Skills

목표: Agent Skills 호환 클라이언트가 재사용할 수 있는 작고 강한 스킬을 만든다.
스킬은 설명서가 아니라 작업 절차, 판단 기준, 반복 검증 도구를 담은 실행 지침이다.

## 기본 원칙

- `SKILL.md`는 필수이며 YAML frontmatter와 Markdown 본문을 포함한다.
- 필수 frontmatter는 `name`, `description`이다. 필요한 경우만 `license`, `compatibility`, `metadata`, `allowed-tools`를 추가한다.
- `description`은 활성화 판정에 직접 쓰인다. 스킬의 기능과 사용 시점을 1024자 이내로 구체적으로 쓴다.
- 본문은 500줄, 5000토큰 미만을 목표로 한다. 매번 필요하지 않은 세부 정보는 `references/`로 분리한다.
- 스크립트는 self-contained, 비대화형, 명확한 `--help`, 의미 있는 exit code, 구조화된 출력을 갖추게 한다.
- 산출물은 최소 파일 수로 유지한다. 범용 Agent Skills에 필요하지 않은 클라이언트 전용 설정은 사용자가 요구할 때만 둔다.

## 생성 절차

1. 요청을 스킬 명세로 바꾼다.
   - 스킬 이름: 소문자 kebab-case.
   - 사용 시점: 어떤 자연어 요청에서 활성화되어야 하는지.
   - 산출 범위: `SKILL.md`, `scripts/`, `references/`, `assets/`, optional frontmatter.
   - 실패 조건: 질문이 필요한 상황, 금지해야 할 작업, 위험한 자동화.

2. 기존 환경을 읽는다.
   - 대상 경로의 기존 파일을 확인한다.
   - 가까운 스킬의 `SKILL.md`만 읽어 형식과 톤을 맞춘다.
   - 저장소 정책이 있으면 언어, 로깅, 타입 힌트, 문서 규칙을 반영한다.
   - 범용 배포가 목표이면 특정 클라이언트 전용 파일은 기본 생성하지 않는다.

3. 구조를 정한다.
   - 항상 `SKILL.md`를 만든다.
   - 필요한 경우만 `references/*.md`를 만든다.
   - 결정적 검사가 필요할 때만 `scripts/*.py` 또는 `scripts/*.sh`를 만든다.
   - 출력에 재사용할 실제 파일이 있을 때만 `assets/`를 만든다.
   - 새 스킬을 scaffold할 때는 `python3 scripts/init_skill.py <name> --path <dir>`를 사용할 수 있다.

4. `SKILL.md`를 작성한다.
   - YAML frontmatter: `name`, `description`을 필수로 둔다.
   - 첫 단락: 이 스킬의 목표와 산출 기준.
   - 핵심 절차: 실행 순서 중심으로 작성한다.
   - 판단 기준: 언제 참조 파일을 읽고, 언제 질문하며, 언제 중단하는지.
   - 검증: 완료 전 확인해야 할 명령과 수동 점검을 적는다.

5. 품질 게이트를 통과시킨다.
   - 가능하면 `skills-ref validate <skill-dir>`를 실행한다.
   - 로컬 보조 검사로 `python3 scripts/validate_skill.py <skill-dir>`를 실행한다.
   - 상세 기준이 필요하면 `references/quality-gate.md`를 읽는다.
   - 실패 항목은 스킬을 고친 뒤 다시 검증한다.

## 프론트매터 작성 규칙

`name`:

- 1-64자.
- 소문자 영문, 숫자, 하이픈만 사용한다.
- 하이픈으로 시작하거나 끝나면 안 된다.
- 연속 하이픈을 쓰지 않는다.
- 부모 디렉터리 이름과 일치해야 한다.

`description`:

- 1-1024자.
- 기능과 사용 시점을 모두 담는다.
- 사용자가 실제로 말할 법한 키워드와 파일 형식, 업무 맥락을 포함한다.
- 너무 넓어져 오탐이 생기지 않게 제외 범위를 짧게 둔다.

Optional fields:

- `license`: 라이선스 이름 또는 번들 라이선스 파일 참조.
- `compatibility`: 특정 클라이언트, 시스템 패키지, 런타임, 네트워크 요구사항이 있을 때만 500자 이내로 작성.
- `metadata`: 클라이언트가 읽을 임의 key-value.
- `allowed-tools`: 실험적 필드다. 클라이언트 지원 여부가 불확실하면 사용하지 않는다.

## Progressive Disclosure

`SKILL.md`에는 매번 필요한 절차만 둔다. 다음 내용은 참조 파일로 분리한다.

- 긴 예시 3개 이상
- 프레임워크별 차이
- 정책 전문, 스키마, API 명세
- 드물게 필요한 심화 체크리스트

참조 파일을 만들면 `SKILL.md`에서 언제 읽어야 하는지 명시한다. "필요하면 참고"처럼
모호하게 쓰지 말고, "보안 자동화를 포함하면 `references/security.md`를 읽는다"처럼 쓴다.
파일 참조는 스킬 루트 기준 상대 경로를 사용하고, 깊은 참조 체인은 피한다.

## 스크립트 판단

이 스킬은 다음 보조 스크립트를 제공한다.

- `scripts/init_skill.py`: Agent Skills 표준 `SKILL.md` 기반 스킬 디렉터리를 초기화한다.
- `scripts/validate_skill.py`: 생성된 스킬의 frontmatter, 이름, 길이, 참조 연결을 검증한다.

스크립트를 만든다:

- 같은 검사를 여러 스킬에 반복 적용해야 한다.
- 정규식, 파일 구조, 링크 검증처럼 사람이 놓치기 쉬운 규칙이 있다.
- 실패 결과가 명확한 JSON 또는 목록으로 표현될 수 있다.
- 명령이 복잡해 `SKILL.md`에 직접 쓰면 재현성이 떨어진다.

스크립트를 만들지 않는다:

- 한 번 읽고 판단하면 되는 내용이다.
- 모델의 도메인 판단이 핵심이다.
- 외부 설치나 네트워크 없이는 실행하기 어렵다.

스크립트 인터페이스:

- 비대화형이어야 한다. 입력은 flag, 환경 변수, stdin으로 받는다.
- `--help`에 사용법, 주요 옵션, 예시, exit code를 적는다.
- 데이터는 stdout에 구조화해서 쓰고, 진단 메시지는 stderr로 보낸다.
- 상태 변경 작업은 idempotent하게 만들고, 위험한 작업은 `--dry-run`, `--confirm` 같은 안전장치를 둔다.

## 완료 기준

- 대상 스킬 폴더에 `SKILL.md`가 있다.
- 프론트매터 `name`이 폴더명과 일치한다.
- `description`에 명확한 트리거 표현이 있다.
- 참조 파일은 `SKILL.md`에서 조건부로 연결된다.
- 범용 스킬에 불필요한 클라이언트 전용 파일이 없다.
- 검증 스크립트가 있으면 실행 결과가 통과한다.
