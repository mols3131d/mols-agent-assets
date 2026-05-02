---
name: private
description: Private rules for the project.
tags: ["private", "security"]
---

# Private Rules

개인 에이전트 협업 프로젝트 준수 사항

## Private Scope

- `--private/`: 개인 디렉토리
  - `--private/adr/`, `--private/spec/`, `--private/kanban/`: 개인 문서
- `.frontmatter`, `frontmatter.json`: 개인 도구 설정
- `.agents/rules/`, `.agents/skills/`: 개인 에이전트 규칙 및 스킬
- `.gemini/antigravity/brain/`: 개인 에이전트 Artifacts (개인용 작업 기록 및 노트)
- Logs: `stdout`, `stderr` 및 실행 이력 (내부 파일 경로 포함 주의)

## Guidelines

### 1. Privacy & Security

- **내부 정보**: Public 영역(VCS, Code)에 문서 ID(KBN, SPEC, ADR), 명세 참조, `--private/` 경로 노출 금지.
- **절대 경로**: 로그 및 VCS 메시지에 로컬 절대 경로(`m:\workspaces\...`) 누출 금지.
- **네트워크**: 서버 주소, API 엔드포인트, 토큰 등 식별 가능한 URL 노출 금지.

### 2. Language Policy

- **Public**: 소스 코드, 주석, 커밋 메시지는 **English** 필수.
- **Private**: Artifacts 및 작업 노트는 **Korean** 허용.
- **표준화**: 프로젝트 공통 용어 및 도구 명칭 준수.

## Example

VCS message:

- ❌ Bad: `feat(sync): KBN-028 tasks.json 동기화 지원 구현`
- ✅ Good: `feat(sync): implement tasks.json file synchronization support`

---

code file:

- ❌ Bad:

  ```typescript
  /**
   * @description KBN-010 과업에 따라 확장 프로그램 설치 로직 구현.
   * 상세 내용은 SPEC-extension-sync.md 문서의 3.2절을 참고할 것.
   *
   * // TODO: KBN-017에서 지적된 리소스 해제 문제 해결 필요
   */
  export async function installMissingExtensions(ids: string[]): Promise<void> {
    // KBN-010 명세에 따라 VS Code 내장 커맨드 호출
    await vscode.commands.executeCommand(
      "workbench.extensions.installExtension",
      ids[0],
    );
  }
  ```

- ✅ Good:

  ```typescript
  /**
   * @description Synchronizes extensions by comparing the local list with the profile data.
   * Automatically installs extensions that are missing from the current environment.
   *
   * @param ids List of extension identifiers to install.
   */
  export async function installMissingExtensions(ids: string[]): Promise<void> {
    // Invoke VS Code's internal command to perform the installation
    // We handle this sequentially to avoid rate limiting or UI blocks
    await vscode.commands.executeCommand(
      "workbench.extensions.installExtension",
      ids[0],
    );
  }
  ```
