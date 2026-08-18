# GitHub to Google Drive Sync (Google Apps Script)

GitHub 저장소의 `src-only` 브랜치에 있는 에이전트 자산들을 구글 드라이브 특정 폴더로 자동 동기화하는 Google Apps Script(GAS) 도구입니다.

## 설정 및 사용법

1. **마커 파일 생성**: 동기화할 대상 구글 드라이브 폴더에 `.github-drive-sync-marker` 라는 이름의 빈 파일을 생성합니다.
2. **스크립트 속성(Script Properties) 설정**: 앱스 스크립트 프로젝트 설정에 아래 항목을 추가합니다:
   - `TARGET_FOLDER_ID`: 대상 구글 드라이브 폴더의 ID
   - `GITHUB_TOKEN`: GitHub Personal Access Token (PAT)
3. **수동 실행**: 앱스 스크립트 편집기에서 `syncGithubToGDrive` 함수를 선택하여 바로 실행(Run)할 수 있습니다.
4. **트리거 등록 (자동 실행)**: `Main.gs` 내 `setupTrigger()` 함수를 최초 1회 실행하면 정기 실행(7일 간격) 트리거가 자동 등록됩니다.
