# PR #258 — 로컬 에이전트 인계

> 대상: `mols3131d/mols-agent-assets` · 브랜치 `mols/feat/repository-dev-bootstrap` · 2026-10-25. **이 문서는 실행할 개선 작업만 정리한 인계 자료이며 정책 정본이 아니다.** 작업 전 PR HEAD와 working tree를 다시 확인한다.

## 목표

[PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)에 남긴 [문서·버전 정책 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258#pullrequestreview-5642776539)와 [스크립트 경량화 리뷰](https://github.com/mols3131d/mols-agent-assets/pull/258#pullrequestreview-5642787295)를 반영한다. **기존 기능·안전성을 지키면서 설정과 자체 구현을 최소화하는 것**이 목표다.

## 작업

1. **개발환경 문서 정리** — `docs/development/development-environment.md`를 일반 개발환경 정책 중심으로 재구성한다. 부트스트랩 고유의 승인·setup/update·실행 경계는 적절한 **부트스트랩 섹션**에 모으고, 도구별 명령·운영 절차는 `docs/references/tooling/mise.md`에 위임한다. 설치 승인·격리 계약은 보존하고 중복 설명은 제거한다.
2. **CLI별 버전 전략 결정** — `mise.toml`의 uv, Node, rumdl, Lefthook, Biome, Rulesync, skills CLI를 **호환성/재현성 우선** 또는 **허용 범위 내 최신 안정 버전 지향**으로 구분한다. 각 판단에 실제 사용처·호환성 근거와 허용 갱신 범위를 붙이고, 가능한 한 mise/native manifest·lock이 정책을 소유하게 한다. `setup`은 검증된 버전을 재현하고, `update`에서만 명시적으로 허용 범위 내 갱신·차이 검토를 수행한다. **모든 도구를 무조건 latest로 바꾸지 않는다.** 잠금 없는 범위 선언이 재현성을 깨면 먼저 native lock 경로를 검증한다.
3. **실행기 경량화** — `scripts/development_bootstrap.py`의 약 500줄을 책임별로 검토한다. 특히 자식 환경에 **7개 지정·6개 제거**, 추가 `PATH` 변경, Git/uv 호출별 제한이 정말 필요한지 각 항목별로 확인한다. `tool_command()`의 npm 메타데이터/실행 경로 검사, 도구 버전 검사, 반복적인 자체 상태 검사도 mise·uv·Git의 native 기능이나 기존 설정으로 대체할 수 있는지 확인한다. **실제 동작과 안전성의 동등성이 입증된 부분만 제거·단순화**하고, 범용 환경변수 필터·추가 옵션·새 추상화는 만들지 않는다.

## 보존할 경계

- 최근 수정한 **F1 Git 대상 저장소/dirty lock 보호, F2 uv 그룹 누락 방어, F3 `.venv`의 system-site-packages 격리**와 대응 테스트를 유지한다.
- 사용자 PATH·프록시·인증·캐시 등 프로젝트 계약과 호환되는 설정을 보존한다. 전역 Python 패키지를 프로젝트 `.venv` 의존성 대신 사용하지 않는다.
- 사용자 머신의 실제 설치·갱신과 HOME/전역 설정 변경은 **[개발환경 정책](../../docs/development/development-environment.md)에 따른 명시적 사전 승인 전에는 실행하지 않는다**. 안전한 테스트 fixture와 실제 설치를 구분한다.
- **PR #256의 범용 Skill**, HOME Skills·Rulesync projection·Git hooks 자동 연동, OS 지원 확대, 별도 설치 프레임워크는 범위 밖이다. 새 도구/추가 환경변수도 근거 없이 도입하지 않는다.

## 검증 및 종료

- 변경 전에 현재 브랜치 상태와 기존 테스트를 확인한다. 기준 참고: [PR Gate 성공](https://github.com/mols3131d/mols-agent-assets/actions/runs/40183907854) 및 이전 [안전성 개선 기록](bootstrap-minimal-improvement-loop-2026-10-25.md). **이전 CI 성공은 이후 변경의 검증 근거가 아니다.**
- 문서 구조, **도구별 버전 결정 및 재현성**, 스크립트에서 제거/유지한 책임·환경변수의 근거를 각각 간결하게 확인한다. 관련 `tests/scripts/test_development_bootstrap.py`를 조정하고 repository-native 테스트 및 PR Gate를 통과시킨다. 실행하지 못한 native/OS 검증은 미검증으로 남긴다.
- 완료 시 PR에 **변경 요약·검증 결과·남은 제한**만 보고한다. 불필요한 연구 문서나 추가 옵션을 만들지 말고, PR은 병합하지 않는다.
