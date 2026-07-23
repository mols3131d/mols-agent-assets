# Agent Instructions Specification

Agent Instructions는 프로젝트 전체에 전역적으로(Always-on) 적용되는 기본 에이전트 지침 문서입니다.

---

## 1. 파일 위치 및 표준 명칭

| 스코프 | 파일 경로 | 비고 |
| :--- | :--- | :--- |
| **Workspace (권장)** | `AGENTS.md` (루트) 또는 `.github/copilot-instructions.md` | `AGENTS.md` 우선 권장 |
| **User Profile** | `{{VSCODE_USER_PROMPTS_FOLDER}}/copilot-instructions.md` | 사용자 전체 공유 |

---

## 2. 규격 사양

Agent Instructions는 별도의 YAML 프론트매터가 필요 없으며 마크다운 본문으로만 구성됩니다.
