# Agent Asset Studio - 스크립트 도구 (Scripts)

`agent-asset-studio`는 에이전트 자산의 기계적 검증 및 초기 구조 생성을 안전하게 자동화하기 위해, `scripts/` 디렉토리에 Python 기반 CLI 도구들을 포함하고 있습니다. 에이전트는 LLM의 임의 추론에 의존하기에 앞서 이 스크립트들을 우선 실행해야 합니다.

---

## 1. init_asset.py (자산 초기화)

새로운 에이전트 스킬이나 규칙 자산을 생성할 때, 규칙에 맞는 기본 템플릿과 디렉토리 구조(Scaffold)를 자동 생성해 줍니다.

- **사용법**:

  ```bash
  python3 scripts/init_asset.py <자산이름> --type <skill|rule> --path <생성경로>
  ```

- **라우팅 스킬 지원**:
  하위 스킬을 가질 수 있는 라우팅 스킬 구조로 초기화하고자 하는 경우 `--routing-skill` 플래그를 추가합니다.

  ```bash
  python3 scripts/init_asset.py <자산이름> --type skill --path <생성경로> --routing-skill
  ```

---

## 2. validate_asset.py (자산 검증)

생성되거나 수정된 에이전트 자산이 프로젝트 표준 규칙 및 마크다운 규격을 준수하는지 자동으로 정적 분석을 수행합니다.

- **사용법**:

  ```bash
  python3 scripts/validate_asset.py <자산디렉토리> --type <skill|rule>
  ```

- **검증 항목**:
  - YAML Frontmatter 규격 및 필수 항목 (`name`, `description` 등)
  - 파일 및 폴더 이름의 네이밍 컨벤션 준수 여부
  - 스킬 파일 본문 라인 수 체크 (과도한 윈도우 점유 방지)

---

## 3. update_index.py (인덱스 갱신)

라우팅 스킬이 새로 추가되거나 하위 스킬 구조가 변경되었을 때, `INDEX.csv` 파일의 메타데이터를 수집하여 자동으로 인덱스 정보를 최신화합니다.

- **사용법**:

  ```bash
  python3 scripts/update_index.py <라우팅스킬디렉토리>
  ```

---

## 4. routerize_skills.py (스킬 라우터 변환)

여러 개의 개별 스킬들을 하나의 마스터 라우팅 스킬 아래로 통합하고 `INDEX.csv`와 `sub-skills/` 구조로 변환하는 작업을 자동화합니다.

- **사용법**:

  ```bash
  python3 scripts/routerize_skills.py --source <스킬경로들> --target <타겟라우터경로>
  ```

---

### 관련 링크

- [README로 돌아가기](README.md)
- [하위 스킬 세부 설명](sub-skills.md)
