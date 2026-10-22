---
description: GitHub PR 리뷰 Skill의 독립 실행 의도, 원본 소비 경로와 평가 범위를 확인하고 유지보수할 때 사용합니다.
---

# GitHub PR Review

연결된 GitHub 도구로 PR을 검토하고, 실행 환경에 맞는 근거와 검토 범위를 보고하는 독립 Skill이다. [작성 원본](../../../src/rulesync/.rulesync/skills/github-pr-review/SKILL.md) 하나가 실행 계약을 소유한다. `github-context`는 컨텍스트 탐색을, 이 자산은 결함 판정과 검증·보고를 소유하므로 함께 사용해도 되지만 설치 의존성은 없다.

## 사용 경로

Rulesync 작성 원본을 선택했다. 다른 프로젝트에서 사용할 때는 해당 프로젝트의 installer나 native Skill loader로 `github-pr-review/` package를 소비한다. 이 저장소의 root dependency 설정에 새 Skill을 추가할 필요는 없다. 배포 탐색은 생성되는 [Skill route](../../../route/skills.jsonl)를 사용한다.

[OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills)는 standalone Skill과 plugin으로 배포한 Skill의 지원 범위를 구분한다. 실제 설치·발견·명시적 호출 방식은 사용하는 host와 계정에서 확인한다. 이 PR은 별도 plugin을 배포하거나 ChatGPT 계정에 Skill을 설치하지 않는다.

Native discovery가 없는 대화에서는 다음처럼 특정 revision의 원본을 **읽고 이번 리뷰에 적용하도록 명시**할 수 있다. `<full-sha>`와 PR URL은 실제 값으로 치환한다.

```text
연결된 GitHub 도구로 mols3131d/mols-agent-assets의 <full-sha>에서
src/rulesync/.rulesync/skills/github-pr-review/SKILL.md 전체를 읽고
이번 리뷰의 작업 지침으로 적용해줘. 대상은 <PR URL>이며 결과는 채팅에만 작성해줘.
```

이 방식은 원본을 대화에 로드하는 경로다. Native Skill 설치나 자동 선택이 확인됐다는 뜻은 아니다. 실제 로드 여부와 도구 접근을 확인하고 사용할 수 없는 기능은 결과에서 구분한다.

## 평가와 유지보수

[평가 fixture](../../../evals/skills/github-pr-review/cases.json)는 trigger, 타 프로젝트의 단독 실행, 제한된 코드 실행, coverage, revision과 게시 권한을 다룬다. 각 case의 `assertions`는 grader용이며 target 입력에는 `prompt`와 Skill만 제공한다. 실제 tool trajectory와 원격 side effect를 확인하려면 해당 도구가 연결된 host에서 실행해야 한다. 텍스트 응답만 평가하는 runner는 실제 도구 호출을 증명하지 않는다.

- 구조 검증: 저장소의 `npm run rulesync:validate`, frontmatter validation과 generated projection 검증을 재사용한다.
- Fixture 연결: 기존 `scripts.agent_assets.skills_promptfoo.generate_tests`에 `skill=github-pr-review`, `suite=trigger` 또는 `behavior`를 전달할 수 있다. Fixture 생성 성공은 행동 평가가 아니다.
- Runtime 평가: Skill 원본 revision, model/host, capability 조건, case 입력, 실제 응답·도구 기록과 rubric 판정을 함께 남긴다. `activation-negative`는 body를 로드하지 않고 metadata만으로 판정한다.

도구 이름이나 계정 ID를 원본에 고정하지 않는다. 도구 계약이 바뀌면 실제 연결에서 필요한 읽기 경로와 오류·페이지 제한부터 확인한다. 실행 로직을 추가할 때만 package resource를 늘리며, eval과 유지보수 문서는 deployable package 밖에 둔다.
