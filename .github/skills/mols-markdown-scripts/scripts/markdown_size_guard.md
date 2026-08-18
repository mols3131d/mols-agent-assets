# Markdown Validator v3

## 1. 주요 결정들

- 문서 크기를 **유효 본문**, **제외 콘텐츠**, **원본 파일 용량**으로 나눠 검사한다.
- 프론트 매터, 코드 블록, 표, 콜아웃은 옵션에 따라 유효 본문에서 제외한다.
- 우회 방지를 위해 제외된 코드 블록·표·콜아웃의 총 글자 수와 줄 수를 별도 제한한다.
- 프론트 매터는 제외 콘텐츠 제한에는 포함하지 않고 원본 파일 용량에는 포함한다.
- 언어 미지정 또는 `markdown`, `md`, `text`, `plaintext`, `rst`, `asciidoc` 코드 블록은 기본적으로 본문으로 계산한다.
- 제외 비율, 개별 블록 크기, 최소 본문 크기는 검사하지 않는다.
- Python API 기본 반환은 `bool`, 상세 모드는 `dict`다.
- 여러 파일과 glob을 지원하며 중복 파일은 한 번만 검사한다.
- CLI는 전체 통과 시 `True`만 출력하고, 실패 시 탭 구분 파일 결과를 출력한다.
- 디버그 로그는 `--debug`에서만 `stderr`로 출력한다.

## 2. 요구사항들

### 의존성

```toml
dependencies = ["pyromark>=0.9.13", "pyyaml>=6.0.2"]
```

### 입력

- 단일·복수 Markdown 파일
- `*`, `?`, `[]`, `**` glob 패턴
- 지원 확장자: `.md`, `.markdown`
- 중복 제거 후 경로순 정렬

### 기본 제한

| 항목 | 기본값 |
| --- | ---: |
| 유효 본문 글자 | 4,000 |
| 유효 본문 줄 | 100 |
| 제외 콘텐츠 글자 | 1,500 |
| 제외 콘텐츠 줄 | 40 |
| 원본 파일 용량 | 32,768 bytes |

### 제외 옵션

기본값은 모두 `True`다.

- `exclude_front_matter`
- `exclude_code_blocks`
- `exclude_tables`
- `exclude_callouts`
- `count_document_code_blocks`

### 처리 규칙

- `pyromark` 이벤트와 UTF-8 바이트 범위로 구조를 판별한다.
- 제외 범위는 줄 경계까지 확장하고 겹치는 범위는 병합한다.
- 프론트 매터는 `yaml.safe_load()`로 검증한다.
- GFM 테이블과 GFM·`[!TYPE]` 콜아웃을 지원한다.
- 파일 용량은 제외 전 원본 바이트 수로 계산한다.

## 3. 스펙

### Python API

```python
check_markdown(
    paths,
    *,
    max_chars=4000,
    max_lines=100,
    max_excluded_chars=1500,
    max_excluded_lines=40,
    max_file_bytes=32768,
    exclude_front_matter=True,
    exclude_code_blocks=True,
    exclude_tables=True,
    exclude_callouts=True,
    count_document_code_blocks=True,
    return_details=False,
) -> bool | dict
```

보조 API:

- `inspect_file()`: 단일 파일 상세 검사
- `analyze_markdown()`: Markdown 문자열 구조 분석

### 실패 조건

```python
failed = any((
    effective_chars > max_chars,
    effective_lines > max_lines,
    excluded_chars > max_excluded_chars,
    excluded_lines > max_excluded_lines,
    file_bytes > max_file_bytes,
))
```

### 상세 결과

```python
{
    "passed": bool,
    "summary": {...},
    "limits": {...},
    "files": [{
        "path": str,
        "passed": bool,
        "error": dict | None,
        "checks": {
            "effective_chars": {"passed": bool, "actual": int, "limit": int, "exceeded_by": int},
            "effective_lines": {...},
            "excluded_chars": {...},
            "excluded_lines": {...},
            "file_bytes": {...},
        },
        "excluded": {
            "front_matter": {"blocks": int, "chars": int, "lines": int},
            "code_blocks": {...}, "tables": {...}, "callouts": {...},
        },
    }],
    "errors": [],
}
```

### CLI

```bash
python check_markdown_v3.py README.md "docs/**/*.md"
```

- 전체 통과: `True`
- 실패 존재: `Result\tFile` 헤더와 실패 파일 결과
- 출력 모드: `table`(기본), `boolean`, `json`
- 용량 단위: `B`, `KB`, `MB`, `KiB`, `MiB`
- 종료 코드: `0` 통과, `1` 제한 초과, `2` 입력·파일·파싱 오류
