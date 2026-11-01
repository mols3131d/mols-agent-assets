# PR #256 — Bootstrap 설계 Skill 정리·리뷰·개선 루프

> 2026-10-25 · [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256) · 범용 Skill만 대상. 구현 실행기와 호스트 환경은 [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)의 별도 책임.
>
> `mols-loops`의 Prepare → RPI Main Loop → Finalize를 적용해 **실질적인 Review 2회(`loops_used=2`)**로 수렴했다. 정적 리뷰 및 GitHub 원본 대조 근거이며, 실제 모델 실행 평가가 아니다.

## 목표·경계

- 목표: 요청 범위에 맞는 가벼운 **설계·리뷰 전용** Skill. 기존 도구의 기본값, 프로젝트 문서·설정, 호환되는 전역 자원을 적극 재사용한다.
- 고위험 변경은 자동 설치·복구로 편입하지 않고 위험과 안전한 기존 도구/수동 경로를 **제안**한다. 설치 실행은 해당 프로젝트와 사용자의 승인 계약을 따른다.
- 구현 설계는 CLI/API/native task 우선. 신규 resolver, installer, cache manager, configuration framework와 과도한 환경변수·옵션은 만들지 않는다.
- 범위 제외: 이 저장소의 `mise.toml`, 부트스트랩 스크립트, 실제 사용자/전역 환경, PR #258, 새로운 평가 러너 또는 전체 OS 매트릭스.

## Loop 1 — 정리 → 리뷰 → 개선

**정리:** 기존 47줄 `SKILL.md`에서 중복되는 권한·격리·Setup/Update·CLI 재사용 조건을 의미별로 대조했다. 전역 자원을 무조건 거부하거나 모든 도구에 Python 전용 격리를 강요하지 않도록 프로젝트 계약을 우선한다.

**리뷰(관점별 순차 검토):**
- 책임: `write only the smallest glue`는 설계 전용 Skill이 구현을 직접 수행하는 것으로 읽힐 수 있다. **수용**.
- 안전: `separately authorized path`만 언급하면 승인 자체가 위험을 정당화한다고 읽힐 수 있다. **수용**.
- 이식성: 보편적인 user-scoped native tool 설치까지 전면 금지하는 표현이 다른 생태계와 충돌할 수 있다. **수용**. 단 프로젝트 의존성의 격리와 사용자 승인 경계는 유지.
- 효율: 새 문서·sub-Skill·approval engine은 별도 실익이 없으므로 **기각**.

**개선:** 기존 본문만 갱신했다([커밋 `a21cbaf`](https://github.com/mols3131d/mols-agent-assets/commit/a21cbafce1b09011e99cd2ec47f1338c08f022f7)).
- 설치 승인과 위험 작업의 안전성 판단을 구분하고, HOME/hook·전역 변경 등은 기본 자동화에서 제외.
- `write` 대신 `propose` 사용; 실제 구현은 호출자의 엔지니어링 워크플로에 맡김.
- native CLI/API/tasks 및 기존 도구·인터프리터·설정·캐시 재사용 조건을 유지.
- Setup에서 암묵적 버전·lock 변경 방지, Update에서 별도 승인 없는 pin·floating ref 이동 금지.

## Loop 2 — 반례 리뷰 → 보강 → 재검토

**반례:**
1. 잠금 파일이 없는 프로젝트에서도 native manager가 재현 가능한 상태를 제공할 수 있다. 무조건 새 lock/schema/framework를 만드는 것은 이식성과 간결성에 반한다.
2. 네이티브 도구만으로 정확한 상태를 재현할 수 없는 경우에도 자체 resolver를 작성하라는 뜻이 되어서는 안 된다.
3. 단일 Git 설치 요청에 `bootstrap 설계는 필요 없어`라는 힌트가 있는 negative fixture는 실제 근접 요청에 대한 선택력을 과대평가할 수 있다.

**개선:** `SKILL.md`는 재현성 불가 시 한계와 최소 수정안을 제안하도록 보강했다([커밋 `c881567`](https://github.com/mols3131d/mols-agent-assets/commit/c8815678501e81600b48c0eb5d186221ecce7a4e)). 기존 평가 11건을 늘리지 않고 Git 단일 설치 near-miss의 명시적 부정 힌트만 제거했다([커밋 `5ccf1d0`](https://github.com/mols3131d/mols-agent-assets/commit/5ccf1d0edfb494759bdef5beab0f3aba349f783d)).

**재검토(정적):** 47줄 유지, Skill 이름/description과 생성 route 일치, JSON 파싱 성공, 11건 ID 중복 없음(activation 3 / negative 3 / behavior 5), 실제 설치 승인의 선행성·프로젝트 격리·작업 범위·사실 보고 조건이 본문에 남아 있음을 GitHub에서 직접 확인했다.

## Finalize — 결과와 한계

- **정리·개선:** 완료. source `SKILL.md`, 기존 `cases.json`만 수정했다. 생성 route의 metadata 수정이나 새 코드·환경변수·프레임워크 추가는 없다.
- **직접 확인한 근거(`verified`):** GitHub 원본/route/fixture 정적 구조 및 문구 대조. 관련 커밋과 변경 파일은 위 링크 참조.
- **정적 의미 판단(`inferred`):** 리뷰·설계 경계, 위험 변경의 제안 전용 처리 및 과잉 설정 유도 위험을 줄였다. 실제 target 모델의 준수나 안정성까지 입증하지는 않는다.
- **미검증(`unknown`):** 최신 11-case Promptfoo/Ollama 런타임 평가, native discovery/activation, 사용자 시스템 설치 승인 준수, Windows/macOS/Linux 등 실제 bootstrap 동작. 별도 PR #258의 구현 결과는 이 Skill 평가 근거가 아니다.
- **종료 이유:** 2회 실질 검토 후 추가 수정의 예상 가치보다 새 규칙·case·문서 유지비가 커져 중단. 남은 검증은 기존 평가 entrypoint에서 수행하면 되며, 새로운 테스트 체계를 만들지 않는다.
- **Run 게이트:** 정적 Skill 정리·개선 목표 **COMPLETE**. 모델 행동 전체 검증·PR 병합 준비 완료를 뜻하지 않는다. Draft 유지 및 현재 HEAD의 CI 확인은 별도 검증 상태로 판단한다.
