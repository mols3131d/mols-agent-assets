# Decisions

## 확정

### 현재 구조와 실행 흐름을 설명한다

- 핵심 진입점부터 저장소·외부 시스템·최종 출력까지 추적하고 사실과 추론을 구분한다.
- **Reason:** 독자의 코드 이해 시간을 줄인다.
- **Impact:** 평가와 개선 권고는 기본 report에서 제외한다.

### 필요한 경우에만 탐색을 위임한다

- 기본 조사는 단일 agent가 수행하고, 범위가 넓으며 독립 실행 경로가 2개 이상일 때만 경로별 탐색을 sub-agent에 위임한다.
- **Reason:** 작은 범위의 위임 비용을 피하고 큰 저장소의 독립 탐색만 병렬화한다.
- **Impact:** sub-agent는 읽기 전용 근거를 반환하고 main agent가 교차 경계 검증과 최종 작성을 소유한다.

### 여섯 workflow를 router로 선택한다

- `help`, `initialize`, `configurator`, `create-dir`, `write-summary`, `write-detail`을 `workflows/INDEX.csv`에서 의미 기반으로 선택한다.
- **Reason:** 사용 안내, config 초기화·수정, directory 생성, summary 작성, detail 작성은 입력과 결과가 독립적이다.
- **Impact:** `SKILL.md`에는 공통 경계와 routing만 두고 선택한 workflow만 읽는다.

### Help는 점진적 양방향 사용 안내다

- `help`는 CLI의 root·subcommand `--help`처럼 Commander와 Executor를 capability, workflow, detail 순서로 안내하며 작업은 실행하지 않는다.
- **Reason:** 필요한 정보만 단계적으로 공개해 선택을 돕고 과도한 정보 출력을 막는다.
- **Impact:** 한 응답은 한 단계만 다루고 끝에 다음 탐색 선택지를 제시하며, “전부” 요청도 capability 요약부터 시작한다.

### 기본 저장 root는 `reports/`다

- 기본 저장 root는 `reports/`이며 상대 경로만 허용한다.
- **Reason:** 생성물을 source와 분리해 예측 가능한 위치에 둔다.
- **Impact:** `output_path`가 없으면 `reports/` 아래에 생성한다.

### 출력 경로를 기계적으로 생성한다

- `default_output_format`은 `%Y-%m%d/%H%M-{title_slug}`이며 `strftime` 처리 후 `{title_slug}`를 치환하고 `/`을 directory 경계로 사용한다.
- **Reason:** 날짜·시각·제목 기반 경로를 결정적으로 생성한다.
- **Impact:** 기본 상대 경로는 `2026-0722/1630-login-api` 형태다.

### 생성 시각에 IANA timezone을 사용한다

- 출력 경로와 frontmatter `datetime`은 config의 IANA `timezone`을 사용하며 기본값은 `Asia/Seoul`이다.
- **Reason:** 실행 환경에 따른 시각 차이를 막는다.
- **Impact:** 경로와 문서 metadata가 같은 기준시를 사용한다.

### Summary frontmatter에 `datetime`을 사용한다

- Summary frontmatter는 `date` 대신 `datetime: 'yyyy-MM-dd HH:mm'`을 사용한다.
- **Reason:** 문서 metadata에 분 단위 생성 시각을 기록한다.
- **Impact:** 소비 도구는 `datetime` 필드를 읽어야 한다.

### Summary와 component template을 분리한다

- Summary는 overview, system map, component mapping, walkthrough, reading guide, understanding notes로 구성하고 component는 responsibility, execution flow, boundaries, evidence로 구성한다.
- **Reason:** 요약부터 근거까지 단계적으로 공개한다.
- **Impact:** 기본은 summary 하나를 생성하고 별도 component 문서는 요청받은 경우에만 `{{domain}}-{{component}}.md`로 추가한다.

### Report 생성을 세 단계로 분리한다

- `create-dir`가 report directory를 만들고, `write-summary`가 `__summary__.md`를 작성하며, `write-detail`이 명시된 component 문서를 추가한다.
- **Reason:** filesystem 준비, 핵심 분석, 선택적 상세화를 독립적으로 실행하고 검증한다.
- **Impact:** 기본 report 요청은 `create-dir`와 `write-summary`를 순서대로 실행하고 detail은 명시 요청 때만 실행한다.

### Config 기반 directory 생성을 script로 고정한다

- `create_report_dir.py`가 config 탐색, timezone 적용, format 치환, slug 검증, project-root 경계 검사, directory 생성을 수행한다.
- **Reason:** Executor별 경로 계산 차이와 project 밖 경로 생성을 막는다.
- **Impact:** `create-dir` workflow는 script command와 반환 경로 확인만 수행한다.

### 생성된 report를 script로 검증한다

- `validate_report.py`가 frontmatter, 필수 heading, placeholder, instruction comment, local link를 summary와 detail 계약에 따라 검사한다.
- **Reason:** 수동 검토만으로 놓치기 쉬운 기계적 오류를 차단한다.
- **Impact:** `write-summary`와 `write-detail`은 완료 전에 validator exit code `0`을 요구한다.

### 인증 시스템 example을 사용한다

- Example은 login endpoint, authentication service, user repository, token issuer로 구성한다.
- **Reason:** 주요 section과 component link 사용법을 한 흐름에서 보여준다.
- **Impact:** example은 template의 기준 구현을 제공한다.

### Configurator가 config를 관리한다

- `scripts/configurator.py`가 config를 관리하며 `DEFAULT_CONFIG`를 기본값의 단일 기준으로 사용한다.
- **Reason:** 생성과 검증을 반복 가능한 코드로 고정한다.
- **Impact:** `initialize_config()`, `check_config()`, `update_config()`와 `init`, `show`, `set` 명령을 제공한다.

### Config는 우선순위에 따라 하나만 읽는다

- `<project-configs-directory>`, `.configs`, project agent skills, global agent skills 순서에서 처음 존재하는 `iceberg-code-report/user_data/config.json` 하나를 읽고 병합하지 않는다.
- **Reason:** project override와 global fallback을 함께 지원한다.
- **Impact:** 상위 config가 아래 config를 대체하며 신규 초기화는 명시한 project configs directory 또는 `.configs`에 생성한다.
