---
description: PR 256의 간결한 Promptfoo 평가 보완 작업을 인계할 때 목표, 범위, 권한과 시작 상태를 확인합니다.
---

# Eval 개선 준비

**READY WITH LIMITS.** 사용자 요청에 따라 준비 → 계획·계획 검토 → 구현·재평가 → 결과·인계를 진행한다. `mols-loops`는 진행·검토를, `mols-agent-asset`은 평가·자산 개선을 담당한다. 검토는 순차적으로 수행하며 독립적인 사람 검수로 표현하지 않는다.

- 시작: `b381dbdbfa91cf8a72517a5286daebc2a753e3f1`, `agents/pr-256-assignment-progress`, clean. 기존 [평가 결과](bootstrap-eval-results-2026-10-25.md)와 로컬 raw export 3개가 있다.
- 목표: 기존 Promptfoo 체계에서 채점 위양성을 보정하고 JSON 오류를 진단한 뒤, 근거가 있는 Skill 개선과 제한적 재평가를 수행한다. 범용 재사용 목표를 유지한다.
- 범위: 공통 evaluator의 최소 수정·회귀 테스트, 소수 보정 입력, 필요한 Skill·fixture 수정, 문서와 인계 기록. 기대 답안을 완화하거나 오류를 의미 성공으로 처리하지 않는다.
- 범위 밖: 새 평가 프레임워크, OS/IDE 실설치 검증, 모든 조합의 호환성 보장, 외부 유료 모델, 모델·패키지 설치, 전역 설정 변경, Draft 해제·merge.
- 자원: 기존 Python·Promptfoo 캐시와 로컬 Ollama 모델을 재확인하여 재사용한다. 로그·원응답은 `.tmp/`에 두고 공개 가능한 요약과 보정 fixture만 보존한다.
- 완료 조건: 보정 전후 판정과 남은 오류를 구분해 보고하고, 필요한 수정·검증 및 모델 평가 근거를 남긴다. 모델의 전 사례 PASS를 완료 조건으로 가정하지 않는다.
- 진행: 핵심 설계 결정을 계획에 기록하고 substantive review 후 갱신한다. Main Loop 상한 6회, 현재 `loops_used=0`. 문제가 남으면 원인·재현 명령·다음 단계를 인계한다.

후속 아티팩트는 같은 디렉터리의 `bootstrap-eval-improvement-*` 이름으로 생성한다.
