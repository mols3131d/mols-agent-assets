# Report (리포트) - 한국어 번역본

> **참고**: 이 문서는 사용자의 이해를 돕기 위한 번역본입니다. 에이전트는 원문(`.agents/workflows/communication/report.md`)을 기준으로 동작합니다.

1. **[WRITE]**: **탐지된 아카이브 디렉토리**에 기술 리포트를 작성합니다 (`convention.md` 준수, 통상: `reports/` 폴더).
   - 파일명 형식: `YYYY-MM-DD-HHMM.md`
   - 내용: 전체 로그, 로직, 안정성 결과 포함.
2. **[CHAT]**: 생성된 리포트 파일의 내용을 고밀도 채팅 메시지로 **요약**하여 전달합니다.
3. **[SYNC]**: 모든 변경 사항이 `handover.md` 및 `Kanban` 보드에 반영되었는지 확인합니다.
