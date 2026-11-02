---
description: OpenAI ChatGPT의 Chat 모드에서 사용하는 전용 Agent Asset 작성 원본을 찾을 때 확인합니다.
---

# ChatGPT Chat Assets

이 숨김 디렉터리에는 **OpenAI의 ChatGPT Chat 모드**를 대상으로 설계한 Agent Asset의 작성 원본을 둡니다. 현재 Chat 세션에 노출된 플러그인·연결 앱·첨부/프로젝트 파일·분석 도구와 승인된 권한을 기준으로 하며, Codex 또는 ChatGPT Work의 실행 기능을 기본 전제로 삼지 않습니다.

이곳에 보관된 자산은 **관리 대상**이지 자동 설치·활성화된 자산이 아닙니다. GitHub 원본을 Python 샌드박스나 Chat에 자동으로 마운트한다고 가정하지 않습니다. Chat 모드에서 사용하려면 대상 환경에서 실제 지원하는 Skill 생성·업로드·설치, 플러그인 배포 또는 승인된 지침 로딩 경로를 별도로 구성·확인해야 합니다. 구체적인 패키징과 지원 범위는 [OpenAI의 Skill 문서](https://learn.chatgpt.com/docs/build-skills)를 따릅니다.

## Assets

- [ChatGPT Chat Agent Asset](skills/mols-chatgpt-chat-asset/SKILL.md) — Chat 전용 에이전트 자산 생성·튜닝·관리에서 적합한 소비 표면과 실행·검증 경계를 선택하는 Skill. [Maintainer guide](../../docs/skills/mols-chatgpt-chat-asset/README.md).

- [OpenSpec CLI Compatibility](skills/mols-openspec-cli-compat/SKILL.md) — OpenSpec CLI 실행을 사용할 수 없는 Chat 세션에서 기존 도구로 보존 가능한 작업 범위와 정확한 인계 경계를 판단하는 Skill.

실행 지침은 각 Skill의 `SKILL.md`가 소유하며, 유지보수 맥락은 각 자산의 maintainer guide가 담당합니다.
