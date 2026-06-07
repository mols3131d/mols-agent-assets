# Document Studio - 스크립트 도구 (Scripts)

`document-studio`는 기계적인 규칙 준수와 문서의 일관성을 확보하고, 수작업 시의 오류를 줄이기 위해 `scripts/` 디렉토리에 Python 기반 CLI 자동화 도구들을 포함하고 있습니다.

---

## 1. init_document.py (문서 템플릿 생성)
표준 템플릿에 맞추어 새 문서를 자동으로 생성하고 frontmatter를 채웁니다.

- **사용법**:
  ```bash
  python3 scripts/init_document.py --type <adr|prd|spec|design|tasks|kanban> --title "문서 제목" --path <생성할경로>
  ```
- **역할**: 각 문서 유형에 할당된 마크다운 템플릿을 복사하여 작성자, 날짜, 초기 상태 등 메타데이터를 즉시 셋업합니다.

---

## 2. update_index.py (로컬 인덱스 갱신)
지정된 디렉토리 내에 들어 있는 마크다운 문서들의 Frontmatter 정보를 자동으로 긁어 모아 로컬 `INDEX.csv` 파일로 리빌딩합니다.

- **사용법**:
  ```bash
  python3 scripts/update_index.py <대상디렉토리>
  ```
- **역할**: 마크다운 파일들의 메타데이터가 변경되었을 때 인덱스 싱크를 신속하게 맞춰줍니다.

---

## 3. sort_index.py (인덱스 정렬)
`INDEX.csv`에 나열된 리소스들을 정렬 기준에 맞춰 재배열합니다.

- **사용법**:
  ```bash
  python3 scripts/sort_index.py <대상INDEX.csv경로>
  ```

---

## 4. kanban.py (칸반 카드 관리)
칸반 보드 파일 내에서 카드의 위치(상태 열)를 CLI 상에서 안전하게 이동시키고 상태를 제어합니다.

- **사용법**:
  ```bash
  python3 scripts/kanban.py <칸반보드경로> --move <카드명> --to <To Do|In Progress|In Review|Done>
  ```

---

### 관련 링크
- [README로 돌아가기](README.md)
- [문서 유형 세부 가이드](document-types.md)
