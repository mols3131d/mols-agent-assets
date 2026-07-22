# Git Commit VCS Skill Document

`git-commit-vcs` 스킬 사용 가이드 문서입니다.

## 기능 개요

프로젝트의 고유 커밋 컨벤션을 탐색하고 이에 맞춰 Git 커밋 메시지를 생성합니다.
특별한 커밋 규칙이 정의되어 있지 않을 경우 Conventional Commits 1.0.0 명세를 적용합니다.

## 컨벤션 탐색 순서

1. **설정 파일 검사**: `.gitmessage`, `.github/commit_template.md`, `CONTRIBUTING.md`, `CONVENTIONS.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules` 등
2. **커밋 히스토리 검사**: `git log -n 20 --oneline` 분석 (언어, 프리픽스 패턴, 대소문자 규칙 파악)
3. **기본 규격 Fallback**: `references/conventional-commits.md` 참조

## 디렉터리 구조

```text
src/skills/git-commit-vcs/
├── SKILL.md
└── references/
    └── conventional-commits.md
```
