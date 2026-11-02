# Handoff — `mols-project-task-command-design` 준비 PR

> 상태: **정식 Skill 구현·정적 검증 및 PR Gate 통과 / 실제 런타임 평가 미수행**. 이 문서는 비정본 참고 자료이며 실행 지침이 아니다.

## 목표와 기준

프로젝트의 개발·검증·자동화 task/command 진입점을 **최소 복잡성으로 설계·검토·리팩터링**하는 재사용 가능한 Skill을 신설한다. 특정 mise/Make/just/npm 버전에 종속되는 매뉴얼이나 이슈 관리 Skill로 만들지 않는다.

- 준비 PR: [#278](https://github.com/mols3131d/mols-agent-assets/pull/278) (Draft), 브랜치: `mols/feat/project-task-command-design`
- 준비 당시 base `main`: `f0ef1221259d19a70e91a5e9d742f4553df78ed4`
- 정식 Skill 원본 후보: `src/rulesync/.rulesync/skills/mols-project-task-command-design/SKILL.md`
- 설계 근거: [조사 문서](mols-project-task-command-design-research.md)
- 실행 사례: [PR #275](https://github.com/mols3131d/mols-agent-assets/pull/275). **별도 PR이므로 병합 전에는 main에 존재한다고 가정하지 않는다.**

## 준비 완료 / 미완료

**준비 완료:** 이름·설계 책임, 인접 Skill 소유권, task 존치/제거 판단, native 도구 우선, 인수/CLI 통합, CI·hook 소비자와 write boundary 보존, realistic positive/near-miss 사례.

**후속 상태:** 정본 `SKILL.md` 및 유지보수 안내가 생성되었고, 제공용 `route/skills.jsonl`도 정본 메타데이터에 맞춰 갱신한다. 실제 프로젝트 내 설치·선택, 모델 행동 평가, 별도 리뷰 및 Merge는 검증 근거에 따라 구분한다.

## 구현 순서

1. **현재 ref 재확인.** 대상 PR, base/head, #275 병합 여부, 실제 source/소비 경로, 하네스/경로 규칙 확인. 다른 작업의 변경을 자동으로 가져오거나 삭제하지 않는다.
2. **설계 프로세스 적용.** `mols-agent-asset`과 그 `references/common/design.md`, `references/skill/design.md`를 활용. 하나의 선택 가능한 capability로 책임과 activation을 먼저 정한다. `mols-dev-env-bootstrap-design`(설치/업데이트), `mols-ci-design`(CI 정책), `mols-code-comprehension-refactor`(일반 코드 가독성)와 겹치는 부분을 제한한다.
3. **최소 package 작성.** `src/rulesync/.rulesync/skills/mols-project-task-command-design/SKILL.md` 하나로 시작. metadata의 trigger·near-miss를 명확히 하고, 본문에는 **사용처·진입점 inventory → native 대비 판단 → 보존할 계약 → 최소 구조 제안/필요시 구현 인계 → 검증**을 기술한다. `Task`는 runner가 실행하는 프로젝트 명령이며 agent todo와 구별한다.
4. **기존 계약 보존.** 제안 대상의 실제 task/CLI가 소비되는 CI·hook·IDE·문서, PATH·cwd·환경·lock/group, 인수, 실패, 읽기/쓰기·staging·비용 경계를 점검하도록 한다. 새 wrapper/설치기/모델 호출을 기본안으로 만들지 않는다.
5. **Skill 검토·검증.** `mols-agent-asset`의 common/skill review와 validation reference를 활용하고, 기존 repo-native frontmatter/route/generated/drift 및 PR Gate 검사 경로에 맞춘다. generated route·lock을 작성 원본으로 직접 편집하지 않는다.
6. **인계에서 정본으로.** 확정된 원칙만 Skill 원본에 반영. 필요성 확인 전에는 maintainer 문서, 여러 reference, custom script, CI/eval framework를 늘리지 않는다. 실제 runtime eval 수행 여부를 별도로 기록한다.
7. **PR 마무리.** diff/현재 head/base를 재확인하고 PR provenance SHA·검증 증거 갱신. Ready 여부는 구현·검증 결과를 본 후 결정; Merge는 별도 승인 필요.

## 수용 기준

| ID | 시나리오 | 기대 행동 |
| --- | --- | --- |
| AC-01 | `mise run test` 한 줄에 lock/group·공식 호출 계약 | 줄 수만으로 삭제하지 않음 |
| AC-02 | native `mise outdated` 그대로 감싼 alias | 고유 계약이 없으면 직접 호출 제안 |
| AC-03 | suite/config별 반복 npm/mise/Promptfoo 별칭 | native 인수 전달과 비용·cache/write 정책 확인 후 통합 |
| AC-04 | `generated sync`는 생성/stage, `validate`는 read-only | CLI 통합 시에도 부작용·exit 의미 분리 |
| AC-05 | 기존 호출자에 CI·Git hook·문서·OS별 shell 존재 | 변경 전 소비자 탐색과 동시 이관/검증 제시 |
| AC-06 | `mise doctor project`를 구버전 런타임에 제안 | 최소 지원 버전 확인, 호환 가능한 대안 또는 차단 |
| AC-07 | setup/update가 사용자 공유 환경·잠금 안전 계약 보유 | 단순화 때문에 기존 권한·격리 경계 훼손하지 않음 |
| AC-08 | “내가 할 작업(Task) 정리”, “CI Gate만 설계” | Skill 활성화하지 않고 owner 구분 |
| AC-09 | 하나의 CLI에서 여러 모드를 task 이름으로 복제 | 실질적인 옵션/서브커맨드 통합이 적절한지 평가 |
| AC-10 | “Node 버전 하나만 알려줘” | 명령 체계 설계 의도가 없으면 Skill 비적용 |

## 검증 범위

- **준비 문서:** main 기준 작성 원본 및 기존 Skill owner 확인. Skill의 실제 routing/행동은 **미검증**이다.
- **구현 후 필수:** Skill 구조·metadata·링크·native source·derived route 정합성, positive/near-miss 설계 사례 리뷰. 실제 runner 명령을 제안할 때 해당 버전 contract를 확인한다.
- **선택적:** 실제 agent 선택·행동 평가는 목적과 비용을 보고 소규모로 실시. 시뮬레이션/정적 분석을 runtime 실증으로 표시하지 않는다.
- **범위 밖:** #275 코드 수정/병합, 전체 저장소 task 개편, 새로운 범용 도구 설치기·CI 정책·외부 자동화.

정본 Skill의 정적 검증과 CI는 완료했으며, **실제 자동 선택·행동 평가 및 독립 리뷰는 수행하지 않았다**. PR은 리뷰를 위한 상태로 전환할 수 있으나 병합에는 별도 승인이 필요하다.

## 구현 인계 갱신 (2026-11-02)

- 신규 정본: `src/rulesync/.rulesync/skills/mols-project-task-command-design/SKILL.md` (단일 실행 파일), `docs/skills/mols-project-task-command-design/README.md` (유지보수 판단).
- 배포용 derived route `route/skills.jsonl`은 기존 정본에서 생성된 metadata와 신규 source의 `name`·`description`을 같은 정렬·JSONL 포맷으로 재산출한다. CI의 공식 generated validation이 최종 기준이며, root `.agents/route`는 이 저장소가 사용하는 locked dependency만 취급하므로 신규 source 추가만으로 자체 사용을 주장하지 않는다.
- PR #275는 현재 `main`에 통합됨. 준비 당시 독립 PR이라고 한 부분은 과거 시점 기록이며, 이 변경은 새 `main`을 병합 부모로 보존한다.
- 정적 설계·현재 CI 검증의 합격을 실제 routing/behavior eval이나 모든 target runtime의 설치 성공으로 표현하지 않는다.

## 정식 구현 완료 후 검증 (2026-11-02)

- ✅ Pass — `SKILL.md` 단일 package와 `docs/skills/mols-project-task-command-design/README.md` 유지보수 안내 작성. `route/skills.jsonl`의 정본 frontmatter 기반 generated metadata를 동기화.
- ✅ Pass — [PR Gate #693](https://github.com/mols3131d/mols-agent-assets/actions/runs/41467665398): Rulesync asset validation, generated drift, docs frontmatter, deterministic tests 및 project doctor를 포함한 서버 측 검사 전체 성공.
- ✅ Pass (정적 의미 검토) — 10개 AC를 기준으로 공식 명령 유지, 불필요한 alias 제거, CLI subcommand 통합, 효과·권한 경계, near-miss 비활성화와 기존 owner 경계를 대조. 새 runtime script/framework 없이 재사용 가능한 설계 판단으로 표현했음을 확인.
- ⚪ Not Verified — 실제 agent 자동 선택·행동 routing/eval, 다른 대상 런타임의 설치·실행 호환성, 독립적인 사람/다른 모델의 review. 셀프 검토와 CI 성공을 독립 리뷰 또는 runtime eval로 취급하지 않는다.
- 현재 기준 main에 [PR #275](https://github.com/mols3131d/mols-agent-assets/pull/275)가 병합됐고, 이 PR은 당시 최신 main commit `452b153ea484d8a32a0400318dd5d1a1e4645603`를 병합 부모로 포함했다. 추가로 main이 이동했다면 별도 동기화 검토 필요.
