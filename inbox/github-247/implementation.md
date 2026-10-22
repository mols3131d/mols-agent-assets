# PR #247 구현 검증 기록

2026-10-22 기준으로 독립형 `github-pr-review` Skill을 구현했다. 실제 ChatGPT host에서의 설치·자동 선택·도구 실행 평가는 아직 수행하지 않았으므로 Draft를 유지한다.

## 구현과 소비 경로

- 실행 계약: [single-file Skill](../../src/rulesync/.rulesync/skills/github-pr-review/SKILL.md). Rulesync를 유일한 작성 원본으로 선택했으며 다른 자산을 요구하지 않는다.
- 사용·유지보수: [안내](../../docs/skills/github-pr-review/README.md). Native loader와 지정 SHA 원본의 명시적 대화 로드를 구분한다.
- 평가 계약: [19개 case](../../evals/skills/github-pr-review/cases.json). Trigger 5개, behavior 14개이며 assertions는 target에게 제공하지 않는다.

## 현재 런타임에서 관찰한 도구

환경은 Windows의 Codex IDE agent와 연결된 GitHub Plugin이다. ChatGPT 제품의 실행 환경으로 일반화하지 않는다. 작업 기준은 `base=c93ba9306851c3a278f498ee0b04573c18401f14`, 기존 `head=56ce40799794d1b30da14d677af0d4bbbd82eb3b`였다.

| 기능 | 관찰 |
| --- | --- |
| PR·파일 목록 | PR 메타데이터와 변경 파일 2개를 실제 조회. 파일 목록 도구 계약은 모든 page의 경로 반환을 명시 |
| 개별 patch | 목록에서 확인한 `inbox/github-247/plan.md`의 patch 조회 성공. 없는 path의 null과 PR 접근 실패의 404는 계약상 구분 |
| 지정 ref 파일 | 기존 head SHA에서 commit validator 원본 조회 성공. ref 생략 시 기본 브랜치라는 계약 확인 |
| CI·리뷰 | 기존 head의 PR Gate success와 미해결 스레드 없음 확인. workflow 조회는 PR trigger·첫 page만 다루므로 전체 CI로 해석하지 않음 |
| 게시 | 도구 schema의 review event·commit·line/side와 계정 선택 조건만 확인. Review/comment/Approve/Request changes 게시를 실행하지 않음 |

GitHub CLI는 인증되지 않았으므로 메타데이터와 본문 갱신에는 연결된 Plugin을 사용한다. 원본 Skill에는 이 환경의 tool name이나 account ID를 넣지 않았다.

## 검증 근거

- ✅ Pass — repository test task: 236 tests passed. Agent 행동이나 ChatGPT 호환성을 증명하는 결과는 아니다.
- ✅ Pass — Rulesync `config`와 `configured-projection`, documentation frontmatter, docs/distribution/repository generated projection 검증.
- ✅ Pass — 기존 evaluator의 fixture 생성: trigger 5개, behavior 14개. 실제 model 평가를 실행한 결과는 아니다.
- ✅ Pass — rumdl의 cache 없는 Markdown·상대 링크 검증, Biome 2.5.6의 평가 JSON 포맷.
- ✅ Pass — 원본 스크립트 로컬 복사 실행: 정상 subject는 exit 0, 형식 오류와 72자 초과는 각각 exit 1.
- ✅ Pass — 계획 대비 정적 의미 검토: 필수 자산 의존성 없음, SHA·fork·부분 diff·CI 범위 구분, native/복사/미실행 검증, 사용자 게시 권한과 pending write 처리를 원본에서 확인. Runtime 성공을 뜻하지 않는다.
- ⚪ Not Verified — 새 head의 PR Gate와 Branch Check. 기존 head의 성공은 새 commit으로 승계하지 않는다.

`mise run format-changed`의 Python subprocess는 Windows 실행 경로에서 Biome 2.3.11을 선택해 실패했다. 저장소 설정은 바꾸지 않고 설치된 2.5.6 바이너리를 직접 호출해 JSON을 포맷했으며, Markdown은 지정 rumdl로 별도 검증했다. 이 결과를 wrapper task 자체의 성공으로 표기하지 않는다.

## 실행 대체의 범위

안전성을 확인한 원본은 [기존 head의 commit validator](https://github.com/mols3131d/mols-agent-assets/blob/56ce40799794d1b30da14d677af0d4bbbd82eb3b/scripts/commit_message_validate.py), blob `e1abb76eda561d6e6bd6acae0fd2dc4a725d4ee3`다. Import는 `re`, `sys`, `pathlib`; CLI는 지정된 message file만 읽고 네트워크·외부 명령·원격 쓰기를 하지 않는다.

Plugin으로 가져온 원본을 임시 디렉터리에 수정 없이 복사했고 `git hash-object --no-filters`로 blob 일치를 확인했다. Python 3.13.11의 `-I` 실행에서 `runpy`로 로드하고 임시 message file을 `main`에 전달했다. Adapter는 이 입출력 harness뿐이며 validator 로직은 바꾸지 않았다. 정상·형식 오류·길이 초과 3건의 exit code가 각각 0·1·1이었다. Python `-I`는 OS 격리를 증명하지 않는다. 이 실험은 실제 shell 없는 ChatGPT 실행이나 프로젝트 전체 test 통과의 근거가 아니다.

의존성·격리·권한을 재현할 수 없는 production 연동 스크립트는 실행하지 않는 시나리오로 fixture에 남겼다. Stub 성공을 원래 integration check의 통과로 간주하지 않는다.

## 남은 수용 검증

실제 ChatGPT 계정에서 package 로드·명시적 호출·자동 선택을 확인하고, 외부 프로젝트의 단독 실행과 Plugin-only·제한된 executor 조건을 평가해야 한다. 대형 diff, revision 이동, 악의적 PR 입력, 게시·pending review 경계도 실제 tool trajectory로 확인해야 한다. 현재 fixture와 정적 의미 검토는 이 행동 평가를 대신하지 않는다. 독립 subagent 검토와 원격 게시 side effect도 미수행이다.

[OpenAI 공식 안내](https://learn.chatgpt.com/docs/build-skills)는 Skill metadata 기반 선택과 본문 로드를 설명하지만 이 package의 실제 계정 호환성을 증명하지 않는다. 별도 plugin 배포와 merge는 이번 구현에서 수행하지 않는다.
