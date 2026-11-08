---
description: "PR #295의 mols-stdd 점진적 공개 구조를 개선할 후속 작업 범위, 로딩 계약, 평가와 인계 기준을 제안합니다."
---

# mols-stdd 점진적 공개 최적화 제안

> **적용 현황 (2026-11-09):** W1–W5의 로딩 계약·평가 경로·유지보수 문서는 PR #295 작업 브랜치에 반영됐다. GitHub Branch Check의 소스 검증·결정적 테스트·로컬 생성물 검증은 통과했다. **Rulesync CLI, Promptfoo 실제 모델 평가와 네이티브 IDE/CLI Agent의 reference 로딩 검증은 미완료**다. 아래는 채택 판단을 위한 원래 제안이며 현재 실행 계약은 `SKILL.md`와 관련 reference가 소유한다.

## 제안과 범위

**제안:** 기존 `mols-stdd`의 Change 모델과 세 reference를 유지하고, 사용자 intent에 따라 필요한 instruction과 작업 맥락만 단계적으로 읽도록 라우팅을 교정한다. 새 Skill·Task 객체·설정 파일·스케줄러를 만들지 않는다.

이 문서는 **후속 작업을 위한 비정본 제안서**다. 현재 실행 계약은 `src/rulesync/.rulesync/skills/mols-stdd/`가, 유지보수 설계 결정은 `docs/skills/mols-stdd/README.md`가 소유한다. 채택한 결론은 해당 정본에 반영하고 이 인박스 문서를 런타임 지침으로 적용하지 않는다.

- 작성 기준: 2026-11-09, `mols3131d/mols-agent-assets`.
- 선행 PR: [#293](https://github.com/mols3131d/mols-agent-assets/pull/293) — Change 분할·상태 정본·복구 계약.
- 대상 PR: [#295](https://github.com/mols3131d/mols-agent-assets/pull/295) — 티켓 발행·Agent Dispatch 지원. 확인 당시 #293·#295 모두 Draft이며, #295의 base는 #293의 작업 브랜치다.
- 검토 대상 ref: `mols/feat/stdd-agent-dispatch`, 확인 head `b6dbdaebb66e9d8131abb05b9d5b4302a38df2bb`. 실행 전 최신 ref·PR·변경 파일·충돌을 다시 확인한다.
- 우선순위: 로딩 누락 및 잘못된 실행 경계(P1) → 불필요한 컨텍스트·중복(P2) → 실제 로딩 평가(P1, 검증 작업으로 병행).

### 기대 결과

1. 이미 도입된 프로젝트에서도 **새 티켓 발행** 시 Bootstrap의 실제 발행 절차가 누락되지 않는다.
2. **백로그 조회·Ready 선택**은 기본 Change 계약만으로 처리하고 Dispatch의 Worker·Claim 세부 지침을 불필요하게 읽지 않는다.
3. **직접 수행**은 Workflow를, **할당·위임**은 Dispatch를 선택하며, 실제 수행·결과 회수에 필요한 경우에만 두 reference를 조합한다.
4. **단계적 작업 컨텍스트**는 백로그 메타데이터 → 선택한 Change → 관련 도메인 정본·테스트·코드 순으로 확대한다.
5. 기존 상태·의존성·정본 소유권·안전한 재개·완료 gate를 보존한다. reference 선택률과 동작 정확성을 별개의 근거로 평가한다.

## 기준 구조와 진단

현재 구조:

```text
src/rulesync/.rulesync/skills/mols-stdd/
├── SKILL.md
└── references/
    ├── bootstrap.md
    ├── default-workflow.md
    └── dispatch.md

docs/skills/mols-stdd/README.md           # 유지보수 결정, 실행 정본 아님
evals/skills/mols-stdd/cases.json          # 행동 평가 기준
evals/promptfoo/mols-stdd.yaml             # 실행 설정
route/skills.jsonl                         # 생성되는 외부 탐색 메타데이터
```

구조 자체는 `description → SKILL.md → 조건부 reference`에 부합한다. 파일 수나 행 수를 줄이는 것이 목적이 아니며 **결정 지점마다 필요한 가장 작은 문맥이 정확히 로드되는지**가 핵심이다.

| 발견 사항 | 우선순위 | 확인 근거와 영향 | 조치 |
| --- | --- | --- | --- |
| Bootstrap의 로딩 조건이 '최초 도입·저장 위치 결정' 위주 | P1 | 실제 새 Change 발행과 중복 방지 절차는 `bootstrap.md`의 First Record에 존재함. 도입 후 티켓 발행에서 조건부 절차를 놓칠 수 있음 | '새 Change 발행'도 Bootstrap 선택 조건으로 명시 |
| 단순 Ready 작업 조회에도 Dispatch 선택이 연결됨 | P2 | `SKILL.md`와 Workflow가 '작업 선택'을 `dispatch.md`로 유도함. Select와 병렬 Claim/위임 지침을 함께 읽을 수 있음 | 선택은 공통 계약에서 처리, Dispatch는 할당·위임·조율 시 로드 |
| 진입점과 reference가 동일 예시·절차를 반복 | P2 | `SKILL.md`와 Bootstrap의 `work.md` 예시, 공통 완료 원칙과 Workflow 세부 단계의 중복 | 공통 invariant만 진입점에, 단계별 예시·방법은 해당 reference로 집중 |
| 작업 기록 읽기 범위가 명시적으로 좁혀지지 않음 | P2 | Change와 도메인 Spec을 분리한 구조는 충분하지만 백로그 전체 내용 및 관련 명세를 무차별 읽는 방지 지침은 약함 | 탐색 → 선택 → 심화의 조회 순서를 도입 |
| reference 선택·로드 검증 공백 | P1 | 현재 `evals/promptfoo/mols-stdd.yaml`은 native provider의 단일 `SKILL.md` 응답 평가. `generate_native_tests`는 reference path/로딩 검사를 지원하지 않음 | 기존 Python provider 경로의 선택 평가를 재사용하고 실제 런타임 관찰과 구분 |

진단은 소스에 대한 **정적 검토**이며 실제 IDE/CLI runtime의 reference 로딩을 관찰한 결과가 아니다. 별도 변경이 들어왔을 수 있으므로 구현자는 최신 기준으로 재검증한다.

## 목표 아키텍처

```text
[Native Skill Discovery 또는 기존 route]
            │ 해당 intent일 때만 선택
            ▼
[SKILL.md: 공통 Change 정본·상태·안전 불변조건]
            │
      ┌─────┼────────────────────┐
      ▼     ▼                    ▼
  Bootstrap Workflow          Dispatch
  초기 설정  수행·검증           할당·위임·인계
  새 티켓    직접 실행             병렬 안전
      │     │                    │
      └─────┴────────┬───────────┘
                     ▼
        [선택한 Change의 work.md]
                     ▼ 필요한 경우만
        [도메인 delta·정본·코드·테스트]
```

Reference는 직접 로드할 조건이 있을 때만 선택한다. 위임된 구현은 Dispatch에서 실행 경계를 확인한 뒤 Workflow의 수행·검증 계약을 활용할 수 있지만, 단순 백로그 조회에 두 reference를 강제하지 않는다.

### 요청별 reference 선택 계약

| 실제 intent | 기본 작업 | 추가 reference | 읽지 말아야 할 것 |
| --- | --- | --- | --- |
| STDD 최초 도입·위치 선택 | 기존 정본·root/ref 확인 | `bootstrap.md` | Dispatch·구현용 Workflow |
| 새 Change 발행만 | 중복 검사·`todo` 발행 후 종료 | `bootstrap.md` | Worker 실행·불필요한 delta·Dispatch |
| 백로그 목록·Ready 조회 | 선택된 work root/ref의 최소 상태·의존 확인 | 기본적으로 없음 | 모든 명세·코드·Dispatch |
| 다음 Change 선택만 | 지정/실제 Ready 후보·진행 중 작업 확인, 선택 결과 제시 | 기본적으로 없음 | Claim·병렬 격리·구현 절차 |
| 담당 역할만 지정 | 실제·예정 담당 구분, 정본 충돌 방지 | `dispatch.md` | Worker 실행·자동 `doing` |
| Change 직접 수행 | 목표·수락 조건·기존 근거 확인 후 작업 | `default-workflow.md` | 위임이 없다면 Dispatch |
| 네이티브 Worker에 위임·결과 회수 | 권한·격리·인계·검증 책임 확인 | `dispatch.md`, 실제 수행·완료에는 Workflow | 불필요한 프로젝트 전체 문서 |
| 중단된 Change 재개 | 상태와 실제 수정·검증 결과 대조 | Workflow, 이전 Worker/새 위임이 관련될 때 Dispatch | 전체 백로그·무관한 도메인 |
| 사소한 조회·작은 변경 | 프로젝트 지침 안에서 최소 수행 | 필요한 경우만 | 자동 Change 생성·전체 루프 |

**주의:** 스킬을 선택하는 것과 reference를 읽는 것, 실제 에이전트를 실행하는 것은 별개다. 요청된 승인·권한이 없으면 위임하지 않으며, `ready`·`assignee`·`doing`은 원자적 Claim으로 취급하지 않는다.

### 작업 데이터의 단계적 탐색

1. **Discover:** 사용자 선택 work root/ref의 실제 Change를 탐색한다. 백로그 규모에 맞춰 파일 이름·상태·`depends_on` 등 후보 판단에 필요한 최소 정보만 확인한다. 정본이 없는 위치나 별도 ref를 추측하지 않는다.
2. **Select:** 특정 Change가 선택되거나 재개 대상이면 해당 `work.md`의 목표·수락 조건·진행 근거·다음 행동을 더 읽는다. 상태·의존 관계가 불명확하면 `unknown`으로 남기고 실행 가능한 것으로 간주하지 않는다.
3. **Deepen:** 행동 계약·구현·Review에 필요한 도메인 delta, 현재 명세 정본, 관련 코드·테스트만 추가로 확인한다. Spec이 불필요한 Change에는 생성·로드를 강제하지 않는다.
4. **Refresh:** 실행 전과 완료 직전에는 상태·revision·권한의 최신성을 재확인한다. 이전에 로드한 정보가 stale이면 선택 영역만 다시 확인한다.

이 구조는 별도 INDEX/manifest/DB 없이 적용 가능하다. 대규모 백로그에서 검색 비용이 커진다는 관찰이 생기기 전까지 인덱싱 엔진을 도입하지 않는다.

## 구현 계획

### W1 — 공통 진입점의 로딩 규칙 정리 (P1)

**대상:** `src/rulesync/.rulesync/skills/mols-stdd/SKILL.md`

- Bootstrap 선택 조건을 **초기 도입·저장 위치 결정·새 Change 발행**으로 확장한다. 이미 도입된 프로젝트에서도 새 티켓 발행 시 누락되지 않아야 한다.
- `description`은 Skill 자체의 선택 조건만 표현한다. reference 읽는 법·실행 단계·세부 절차를 metadata에 복제하지 않는다.
- `Ticket and Agent Dispatch`의 **Ready·상태 해석**은 공통 불변조건으로 유지한다. **단순 선택 요청**에는 Dispatch를 요구하지 않도록 링크 trigger를 좁힌다.
- `work.md`의 최소 스키마·단일 상태 정본 원칙은 진입점에 남긴다. 긴 예제나 반복 절차만 Bootstrap과 Workflow로 이동하는 것이 실제 loading 비용을 줄이는지 검토한다. 의미 손실이 크면 무리한 축약을 하지 않는다.
- 필수 불변조건(정본 소유권, 허용 status, 의존·권한·완료 gate)은 조건부 reference 뒤에만 숨기지 않는다.

**완료 조건:** 새 Change 발행과 일반 Ready 조회가 서로 다른 reference 경로를 선택하며, 기존 `todo | doing | done | cancelled`의 의미·정본 수가 변하지 않는다.

### W2 — Reference 책임과 상호 연결 정리 (P1/P2)

**대상:**
- `src/rulesync/.rulesync/skills/mols-stdd/references/bootstrap.md`
- `src/rulesync/.rulesync/skills/mols-stdd/references/default-workflow.md`
- `src/rulesync/.rulesync/skills/mols-stdd/references/dispatch.md`

**Bootstrap:** 기존 프로젝트 채택과 이후의 단일 Change 발행을 함께 소유하도록 도입부와 섹션을 정리한다. 기존 경로·정본을 존중하고 중복 티켓·추측 delta·사전 실행을 금지한다.

**Workflow:** 선택된 Change의 실제 수행·Review·명세 반영·재개·완료를 소유한다. 문서의 Prepare에서 모든 '선택'을 Dispatch로 보내는 연결은 제거하고, 실제 위임이나 조율이 있을 때만 해당 reference를 호출한다. 단순 직접 실행에 추가 위임 컨텍스트를 강제하지 않는다.

**Dispatch:** 예정 담당·실행 가능 Worker·Claim·격리·결과 회수 계약을 유지한다. 공통 Ready 정의는 SKILL.md를 참조하고 다시 규정하지 않는다. 실제 할당·위임이 없는 조회는 이 reference의 대상이 아님을 명시한다.

**완료 조건:** 같은 규칙이 여러 owner에 충돌하게 정의되지 않고, Bootstrap↔Workflow↔Dispatch의 참조 순환이 모든 요청에서 강제 선로딩을 만들지 않는다.

### W3 — 백로그 탐색의 점진적 공개 (P2)

**대상:** 공통 진입점 또는 필요한 가장 좁은 reference 하나. 독립적인 `backlog.md`는 기본적으로 신설하지 않는다.

- `changes/**/work.md`를 자동으로 전부 읽은 뒤 모든 spec·test까지 따라가는 행동을 피한다.
- `ready`를 계산하려면 필요한 의존 상태를 실제로 확인하되, 파일 규모·도구 제약에 따라 최소 조회 수단을 선택한다. 불충분한 탐색 결과를 완전한 백로그로 표현하지 않는다.
- 우선순위·담당자·작업 단계의 새 필수 필드, 검색 엔진·캐시·인덱스를 추가하지 않는다.

**완료 조건:** '다음 할 일은?' 요청에서 선택 대상과 선행 작업을 판단하는 데 무관한 도메인 정본까지 선로드하지 않는다. 도구의 실제 탐색 제약으로 전체 목록 확인이 불가능하면 범위·미확인 항목을 보고한다.

### W4 — 참조 선택 Eval과 실측 분리 (P1)

**대상:**
- `evals/skills/mols-stdd/cases.json`
- `evals/promptfoo/mols-stdd.yaml` 또는 관련 평가 설정
- 필요할 때만 기존 `scripts/agent_assets/skills_promptfoo.py`의 공통 기능

**현행 확인:** 43개 평가 사례는 Trigger/Behavior를 다룬다. native generator `generate_native_tests`는 `reference_paths`와 `expected_loaded_references`를 지원하지 않는다. 반면 기존 Python provider 경로는 `mols-test-design`에서 `expected_loaded_references`와 `assert_reference_loading`을 사용한다. 먼저 이 경로를 재사용할 수 있는지 확인하고 중복 평가 엔진을 만들지 않는다.

**추가할 reference 선택 시나리오(초안):**

| 시나리오 | 기대 reference |
| --- | --- |
| 프로젝트 최초 설정 | `references/bootstrap.md` |
| 기존 프로젝트에 새 티켓 발행만 | `references/bootstrap.md` |
| 백로그·Ready 조회 | 없음 |
| 특정 Change 선택만 | 없음 |
| Change 직접 수행 | `references/default-workflow.md` |
| 담당 역할만 지정 | `references/dispatch.md` |
| Worker 위임과 구현·검증 | `references/dispatch.md` + 필요 시 `references/default-workflow.md` |
| 기존 Change 직접 재개 | `references/default-workflow.md` |
| Worker 미종료 상태의 재할당 요청 | `references/dispatch.md` |
| trivial one-off 수정 | Skill 미선택(기존 negative activation 보존) |

- reference 선택 결과를 판정할 때 **정해진 집합**뿐 아니라 왜 그 reference가 필요한지와 무관한 파일이 로드되지 않았는지를 본다. 정확한 읽기 순서는 데이터 의존성이 있을 때만 고정한다.
- 기존 Trigger/Behavior 사례를 삭제하지 않고, reference 선택 사례를 목적이 다른 평가로 구분한다.
- Python provider가 기록하는 `loaded_references`는 해당 평가 harness의 관찰값이다. **실제 Codex/Claude/기타 런타임의 파일 읽기 trace를 대신하지 않는다.**
- 실제 사용 환경 검증에서는 런타임이 제공하는 네이티브 reference 사용 trace 또는 관찰 가능한 파일 조회 이벤트로 선택·미선택을 검증한다. 제공하지 않는 경우 '미검증'으로 기록한다.
- 실행 전 runtime provider, grader, 비용과 외부 데이터 전송 여부를 확인한다. 가능한 최소 비용의 fixture/smoke부터 시작하고 원격 유료 호출은 승인 없이 실행하지 않는다.

**완료 조건:** 대표 시나리오에 기대 reference 집합이 있고, 최소 하나의 실행 가능한 평가 경로로 로딩 선택이 관찰·비교된다. 평가 실행 없이 사례 작성만 했다면 '평가 추가'와 '평가 통과'를 명확히 구분한다.

### W5 — 유지보수 문서·검증·통합 (P2)

**대상:** `docs/skills/mols-stdd/README.md`, 필요 시 생성용 `route/skills.jsonl`, 관련 평가 문서.

- 유지보수 README에는 **왜 이러한 로딩 경계를 유지하는지**와 intentional omissions만 남긴다. 실행 규칙·라우팅표의 전체 복제는 하지 않는다.
- 실제 `SKILL.md` description 변경 시 공식 generator로 `route/skills.jsonl`을 동기화한다. 생성물 직접 수정을 정본 변경으로 간주하지 않는다.
- 실행 가능한 환경에서 `mise run format-changed`, `mise run generated sync`, `mise run generated validate`, `mise run rulesync-validate`, 관련 fixture 검사와 평가를 수행한다. 없는 도구는 통과로 보고하지 않고 구체적인 인계 항목으로 남긴다.
- #293과 #295의 부모·자식 PR 관계 및 merge 순서를 다시 확인한다. 사용자가 별도의 구현 PR을 요구한다면 작업의 독립성·기준 SHA를 확인한 전용 브랜치를 사용한다. `main` 직접 수정 금지.
- 최종 셀프 리뷰: activation 누락, reference 과적재, owner 충돌, 기존 상태 모델 회귀, 실행 권한 우회, 테스트가 주장하는 범위의 과장 여부를 검토한다.

**완료 조건:** 변경된 실행 계약과 유지보수 문서가 정합하며, 실제 수행한 검사·미수행 검사·후속 위험이 PR에 명시된다.

## 실패 모드와 회귀 안전 기준

| 위험 | 방지 조건 |
| --- | --- |
| 티켓 발행 요청이 위임·구현으로 확대 | `todo` 생성만 하고 종료, 실행 권한·요청 별도 |
| 일반 Ready 조회에 병렬 Claim/Agent 전체 지침 로드 | 진입점의 선택 규칙만 적용 |
| Work 정본 중복 | 기존 GitHub Issue/외부 Work owner 확인, 임의 상태 복제 금지 |
| `assignee` 또는 `doing`을 lock으로 해석 | 네이티브 원자적 Claim 및 작업 공간 격리 별도 검증 |
| Worker 성공 응답만으로 `done` | 최신 파일·검증 근거·명세 반영 후 One Completion Gate |
| 모든 Change·Spec·코드를 선로드 | 후보 탐색 → 선택 → 관련 근거 심화 |
| reference 사용 평가를 런타임 성공으로 과장 | fixture/모델 평가/실제 Agent trace의 증거 수준 분리 |
| 문서 책임 중복 | `.inbox/` 비정본, Skill 실행 정본, README 유지보수 결정 |
| baseline/ref 변경·권한 부족 | 실제 대상·계정·ref 확인, 임의 계정 전환·기준 변경 금지 |

## 다음 작업자의 실행 순서

1. PR #293·#295의 최신 head/base와 새 커밋을 읽고 이 제안의 각 finding이 아직 유효한지 확인한다.
2. 현재 저장소 하네스(`CHATBOT.md`, `AGENTS.md`, 경로 Rule, 자산 워크플로) 및 `mols-agent-asset`·`mols-documentation`을 작업 범위에 맞게 선택한다. 개선 루프의 외부 제어는 요청된 경우 `mols-loops`에 맡긴다.
3. W1·W2의 로딩 계약을 우선 구현하고 정적 리뷰한다. W3는 실제 모호성이 남는 가장 좁은 owner에 반영한다.
4. W4의 기대 선택 결과를 확정하고 기존 평가 실행 경로를 재사용한다. 모델 비용·권한을 확인해 실행 여부를 결정한다.
5. W5의 문서·projection·검증·리뷰를 마친 뒤 PR 결과를 보고한다. 테스트 미실행은 명시적으로 남긴다.
6. 채택한 결론은 Skill과 유지보수 문서에 반영한다. 작업 종료 후 이 인박스 문서는 `.inbox/README.md`의 7일 보호·삭제 우선 기준에 따라 정리한다.

## 최종 수락 조건

- [ ] 새 Change 발행에서 Bootstrap을 선택하며 코드·Worker를 실행하지 않는다.
- [ ] 단순 백로그 조회·Ready 선택에서 Dispatch를 불필요하게 로드하지 않는다.
- [ ] 직접 수행에 Workflow, 실제 위임에 Dispatch를 필요에 맞게 로드한다.
- [ ] 백로그 목록 단계에서 무관한 Spec·테스트·코드를 선로드하지 않는다.
- [ ] 기존 status, single owner, dependency, resume, completion gate를 보존한다.
- [ ] reference 선택과 실제 실행 동작의 평가 근거를 구분한다.
- [ ] 필요한 유지보수 문서·route projection·기존 regression case를 보존한다.
- [ ] 실제 검증과 미검증, 실행 권한 및 남은 위험을 명확히 인계한다.

**보류:** 별도 Task/티켓 DB, manifest·INDEX, 새로운 status, 필수 assignee, Agent 런타임 adapter, 스케줄러·잠금 엔진, 의미 없는 reference 추가. 관찰된 요구와 비용 대비 효용이 확보된 경우에만 재검토한다.
