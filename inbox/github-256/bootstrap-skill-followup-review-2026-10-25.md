# PR #256 — 한국어 Skill 셀프 리뷰 후속 개선 루프

> 2026-10-25 · [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256) · 이전 [셀프 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/256#pullrequestreview-5642696791) F1 후속
>
> 적용: `mols-loops` + `mols-agent-asset`의 개선·리뷰·검증 기준. 정적 검토는 실제 모델 평가가 아니다.

## 목표와 작업 경계

**목표:** 한국어 번역에서 빠진 정책 출처의 대체 가능성을 복구하고, 기존 평가에서 재발을 감지할 수 있게 한다.

**범위:** 범용 Skill `SKILL.md`, 기존 평가 사례 한 건, 해당 변경에 대한 재검토. 프로젝트 전용 설치기·환경 파일·OS 설정은 PR #258의 책임이며 이번 루프 대상이 아니다.

## Research → Plan → Work → Review

### 발견 및 계획

이전 셀프 리뷰 Medium F1을 확인했다. 기존 영문 원칙은 프로젝트의 개발환경 문서 **또는 동등한 정책**을 인정했지만, 한국어판은 개발환경 문서만 설치 정책의 소유자로 표현했다. 별도 문서 없이 native 설정·잠금 상태를 정책 근거로 관리하는 프로젝트를 부당하게 배제할 수 있다.

새 지침·문서·테스트 러너 대신, 원본 Skill 한 문장을 고치고 기존 behavior 사례의 입력과 평가 기준을 갱신하기로 했다.

### Work

- **Skill:** 설치 정책의 출처를 “프로젝트 개발환경 문서 **또는 동등한 기존 정책**”으로 복구하고, 허용·확정 버전은 해당 프로젝트의 기존 설정·잠금 상태를 따르도록 정리했다. [커밋 `b8ef49d`](https://github.com/mols3131d/mols-agent-assets/commit/b8ef49d4622d135861aa07d42508baf446b45998)
- **기존 Eval:** `portable-owner-and-update-handoff`의 Volta/pnpm 사례에 “별도 개발환경 문서 없음”을 추가하고, 기존 설정과 lock을 정책 근거로 활용하되 새 setup 문서를 요구하지 않는지 검사하도록 했다. [커밋 `a425d61`](https://github.com/mols3131d/mols-agent-assets/commit/a425d61ec20d0ffe94d14dd3da480ff0f5840354)
- **추가하지 않음:** 환경변수, 새 Skill, 신규 검증 스크립트, fixture 수 증가, 전역 환경 변경.

### Review 및 재검토

- **F1 처분: 반영/정적 해결.** `SKILL.md`에 문서 또는 대등한 기존 정책의 선택지가 복구됐다. 평가 사례에도 문서 없는 프로젝트를 추가해 원래 취지를 표현했다.
- **책임·안전:** 설치 실행은 여전히 Skill 외부의 책임이며 사전 승인, 공유 캐시/전역 변경 경계, 호환 자원 재사용과 프로젝트 의존성 격리가 유지된다.
- **경량성:** Skill 45줄 유지, 원본 경로 1개와 기존 평가 case 1개만 수정.
- **정적 구조 확인:** Skill 이름과 생성 배포 route의 `description` 일치, fixture JSON 11건·고유 ID 11건(positive 3, near-miss 3, behavior 5)을 GitHub 파일에서 확인.
- **미검증:** 한국어 Skill 및 11개 최신 Eval의 **실제 Ollama/Promptfoo 모델 행동**. GitHub CI나 파일 검토의 통과는 모델 선택률·설계 품질·실제 설치 안전성을 증명하지 않는다.

## 종료 판단 및 다음 작업

이번 후속 루프는 **F1 수정과 정적 확인**을 완료했으므로 수렴한다. 새 문제 근거 없이 문구·평가 개수·구성을 늘리지 않는다. PR #256의 Draft 해제와 실제 모델 성능 판단은 기존 로컬 평가 entrypoint의 결과 및 최종 리뷰 후 별도로 결정한다. 실제 설치 구현은 [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)에서 다룬다.
