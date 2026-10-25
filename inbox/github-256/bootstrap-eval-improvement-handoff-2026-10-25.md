---
description: PR 256의 간결한 Eval 개선 작업을 이어받을 때 현재 상태, 검증 근거와 남은 작업을 확인합니다.
---

# Eval 개선 인계

**계획 실행·검토·결과 기록 완료, 모델/채점 품질 미달.** 기준 commit은 `b381dbd`; 작업 branch는 `agents/pr-256-assignment-progress`, PR head는 `mols/feat/dev-environment-bootstrap`다. 사용자 변경 없이 시작했으며 최종 반영 상태는 [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256)의 head/checks를 확인한다.

## 먼저 읽기

- [준비·범위](bootstrap-eval-improvement-prepare-2026-10-25.md)
- [계획 v3](bootstrap-eval-improvement-plan-2026-10-25.md)
- [검토와 계획 변경 근거](bootstrap-eval-improvement-review-2026-10-25.md)
- [결과·재현 명령·원문 판정](bootstrap-eval-improvement-results-2026-10-25.md)

## 확보한 근거

- 기존 grader: 정상/오답 3쌍 모두 PASS, 사례 기대 판정 3/6 일치.
- 요청 맥락·기준별 판정 후에도 오판이 남았다. Temperature=0 고정 조건의 criterion 일치는 Qwen 10/18, Nemotron 13/18. 두 모델 모두 자동 승인용으로 신뢰할 수 없으며 결과를 숨기지 않는다.
- Nemotron structured JSON의 빈 content는 이전 Skill + `think=false` 통제 요청에서 정상 JSON으로 바뀌었다. 전체 모델 행동 개선을 뜻하지 않는다.
- 공통 adapter와 source 참조·label 비노출·오류 보존·thinking override 회귀 테스트를 추가했다. 공식 전체 테스트 **279 passed**.
- 최종 포맷·frontmatter·index/route·Rulesync 구조·diff 검증을 통과했고 평가 당시 source hash가 유지됐다. 반영 전 fetch에서 로컬과 원격 head는 동일했다. Commit·PR CI의 최신 결과는 위 PR을 확인한다.

## 실행 결과·다음 작업

- Native Promptfoo로 두 모델의 최신 12건을 각 1회 실행했다. Nemotron target에만 `PROMPTFOO_RUNTIME_THINK=false`, 두 실행의 grader는 `ollama:chat:nemotron-3-nano:4b`이며 native temperature=0이다.
- 로컬 export: `.tmp/promptfoo/pr256-improved-nemotron-12.json`, `pr256-improved-qwen-12.json`. Nemotron trigger는 5 PASS/1 envelope ERROR, Qwen은 3 PASS/3 FAIL이다. 두 모델 모두 원문 기준 behavior 0/6이며 각각 7/18 기준만 충족했다.
- Nemotron의 package near-miss envelope 오류는 동일 조건 재시도에서도 재현됐다. 빈 JSON 문제와 구분하며 강제 보정하지 않았다. Grader의 자동 PASS·잘못된 FAIL 사유도 결과 문서에 남겼다.
- 모델·grader·Skill·case 수가 이전과 달라 aggregate 점수를 순수 Skill 개선 효과로 해석하지 않는다. Draft를 유지하며 merge하지 않는다.
- 다음 과제는 기존 보정 표본의 판정 재검토와 실제 사용 대상으로 정한 모델의 제한적 검증이다. 현재 두 소형 모델로 자동 판정 신뢰성을 확보했다고 주장하지 않는다. 새 계정·모델 설치 없이 실행·진단까지는 가능했지만 높은 품질을 보장할 수는 없다.

Run accounting: `loops_used=5/6`, Main Loop의 계획 작업·검토를 마치고 Finalize에서 bounded 검증·반영한다. 보정 효과와 남은 신뢰성 한계를 구분하는 것이 완료 조건이며, 모든 모델의 전 사례 PASS는 조건이 아니다. OS/IDE·유료 모델·새 설치·전역 설정 변경은 범위 밖이다.
