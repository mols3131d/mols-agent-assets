# GitHub 파일 동기화

lockfile에 등록된 원격 파일을 로컬 경로로 동기화하는 Python CLI입니다. 마지막으로
동기화한 SHA-256 해시를 기준으로 원격 변경, 로컬 수정, 충돌을 구분하며 로컬 변경을
기본적으로 보호합니다.

## 실행

저장소 루트에서 실행합니다.

```bash
python -m src.scripts.sync_github_files
```

기본 lockfile은 현재 디렉터리의 `my-assets-lock.json`입니다. 다른 파일을 사용하려면
경로를 지정합니다.

```bash
python -m src.scripts.sync_github_files --lockfile path/to/assets-lock.json
```

## Lockfile

```json
{
    "version": 1,
    "assets": {
        "sample-rule": {
            "sourceUrl": "https://github.com/owner/repo/blob/main/rules/sample.md",
            "destPath": ".agents/rules/",
            "computedHash": ""
        }
    }
}
```

- `version`: 현재 지원 버전인 `1`을 사용합니다.
- `assets`: 자산 이름을 키로 사용하는 객체입니다.
- `sourceUrl`: 다운로드할 URL입니다. GitHub의 `blob` URL은 raw URL로 자동 변환됩니다.
- `destPath`: 저장할 파일 또는 디렉터리 경로입니다. `/`로 끝나면 URL의 파일명을
  붙이고, 그렇지 않으면 지정한 경로를 파일 경로로 사용합니다.
- `computedHash`: 마지막으로 동기화한 내용의 SHA-256 해시입니다. 최초 등록 시 빈
  문자열을 사용할 수 있으며, 정상 동기화 후 자동 갱신됩니다.

상대 `destPath`는 실행한 현재 디렉터리를 기준으로 해석합니다. 필요한 상위
디렉터리는 자동 생성됩니다.

## 옵션

| 옵션 | 동작 |
| --- | --- |
| `--lockfile PATH` | 사용할 lockfile을 지정합니다. |
| `--dry-run` | 파일과 lockfile을 변경하지 않고 예정 작업만 출력합니다. |
| `--check` | 변경·충돌·로컬 수정이 있으면 종료 코드 `1`을 반환합니다. |
| `--force` | 로컬 수정이나 충돌을 원격 내용으로 덮어씁니다. |

`--dry-run`과 `--check`는 함께 사용할 수 없습니다. `--force`를 `--dry-run` 또는
`--check`와 함께 사용하면 실제로 덮어쓰지 않고 예정된 강제 변경만 보고합니다.

## 상태별 동작

| 상태 | 의미 | 기본 동작 |
| --- | --- | --- |
| `missing` | 로컬 파일이 없음 | 원격 파일 설치 |
| `adopted` | 해시는 비어 있지만 로컬과 원격이 같음 | 현재 해시를 lockfile에 기록 |
| `unchanged` | 원격과 로컬 모두 마지막 동기화 상태와 같음 | 변경 없음 |
| `remote-changed` | 원격만 변경됨 | 로컬 파일 업데이트 |
| `local-modified` | 로컬만 변경됨 | 로컬 파일 보존; `--force` 안내 |
| `untracked-local` | 해시는 비어 있고 로컬과 원격이 다름 | 로컬 파일 보존; `--force` 안내 |
| `conflict` | 원격과 로컬이 모두 변경됨 | 로컬을 보존하고 `<파일>.remote` 생성 |

충돌을 수동으로 해결하거나 원격 버전으로 교체해도 되는 경우 `--force`로 다시
실행합니다. 쓰기는 임시 파일을 만든 뒤 대상 경로로 교체하는 방식으로 수행됩니다.

## 종료 코드

- `0`: 정상 실행. 기본 실행에서는 로컬 수정이나 충돌을 보존하고 건너뛴 경우도
  포함합니다.
- `1`: `--check`에서 작업이 필요하거나, 실행 중 오류가 발생했습니다.
- `2`: CLI 인자가 잘못되었거나 `--dry-run`과 `--check`를 함께 사용했습니다.

## 주의 사항

lockfile의 URL에서 네트워크를 통해 파일을 내려받고 `destPath`에 기록합니다. 신뢰할
수 있는 lockfile만 사용하고, `--dry-run` 또는 `--check`로 변경 범위를 먼저
확인하세요.
