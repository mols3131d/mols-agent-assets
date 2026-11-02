---
description: OpenAI ChatGPT의 Chat 모드에서 사용하는 전용 Agent Asset 작성 원본을 찾을 때 확인합니다.
---

# ChatGPT Chat Assets

이 숨김 디렉터리에는 **OpenAI의 ChatGPT Chat 모드**를 대상으로 설계한 Agent Asset의 작성 원본을 둡니다. 현재 Chat 세션에 노출된 플러그인·연결 앱·첨부/프로젝트 파일·분석 도구와 승인된 권한을 기준으로 하며, Codex 또는 ChatGPT Work의 실행 기능을 기본 전제로 삼지 않습니다.

이곳에 보관된 자산은 **관리 대상**이지 자동 설치·활성화된 자산이 아닙니다. GitHub 원본을 Python 샌드박스나 Chat에 자동으로 마운트한다고 가정하지 않습니다. Chat 모드에서 사용하려면 실제 지원되는 Skill 직접 생성·업로드·설치, 플러그인 배포 또는 승인된 지침 로딩 경로를 별도로 구성하고 확인해야 합니다. 구체적인 패키징과 지원 범위는 [OpenAI의 Skill 문서](https://learn.chatgpt.com/docs/build-skills)를 따릅니다.

## Assets

- [OpenSpec CLI Compatibility](skills/mols-openspec-cli-compat/SKILL.md) — OpenSpec의 공식 워크플로를 Chat 도구로 최대한 수행하고 CLI 의존 단계의 실행 충실도·검증·인계 경계를 판단하는 Skill.

실행 지침은 각 Skill의 `SKILL.md`가 소유하며, 유지보수 맥락은 [Skill maintainer guide](../../docs/skills/mols-openspec-cli-compat/README.md)를 참고합니다.
