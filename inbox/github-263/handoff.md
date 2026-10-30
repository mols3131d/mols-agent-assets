# PR #263 — Check Dependencies 이식 인계

## 현재 상태

- PR: https://github.com/mols3131d/mols-agent-assets/pull/263 (Draft)
- 브랜치: `mols/feat/check-dependencies-skill`
- 입력: 대화 첨부 `check-dependencies-skill.zip` (6 files)
- canonical source: `src/rulesync/.rulesync/skills/check-dependencies/`

스킬 본문, 표준 라이브러리 Python 스크립트, 테스트, Markdown 템플릿, README, 유지보수 사양서를 이식했다. Python 스크립트·테스트·보고서 템플릿은 ZIP 원본과 Git blob SHA가 동일하며, SKILL metadata 및 문서 실행 경로만 이 저장소 구조에 맞게 수정했다. 기존 privacy gate(offline default, online opt-in)와 범위 제한을 유지한다.

## 검증 근거

- ✅ ZIP으로부터 격리 추출한 원본에서 `python -m unittest discover` 9개 통과.
- ✅ 스크립트·테스트·템플릿의 Git blob SHA 원본 일치.
- ⚪ 아직 로컬 repository checkout에서 `npm run rulesync:validate`, `mise run generated-sync`, `mise run test` 및 실제 설치 경로 실행을 수행하지 못했다.
- ⚪ 외부 npm/PyPI/OSV 조회는 수행하지 않았다(명시적 승인 필요). 독립적인 Agent routing/behavior eval도 미실시.

## 최소 후속 작업

1. 저장소의 정상 개발 환경에서 `mise run generated-sync`를 실행해 필요한 generated discovery/projection을 동기화한다. 생성물은 직접 편집하지 않는다.
2. `npm run rulesync:validate` 및 `python -m unittest discover -s src/rulesync/.rulesync/skills/check-dependencies/tests -v`를 실행한다.
3. 생성물과 CI 결과를 검토한다. 부족한 부분이 실제로 드러날 경우에만 좁은 수정으로 대응한다.
4. 현재 스크립트의 탐지 범위는 root `package-lock.json`/`package.json` 및 단순 `requirements.txt`만이다. `uv.lock`, `pyproject.toml`, `pnpm-lock.yaml` 등 지원 확대는 **이 PR에서 하지 않는다**.

## 주의

- 이 PR은 이식 초안이다. PR 존재 또는 mock 기반 테스트 결과를 보안 진단 완전성·온라인 검증·merge readiness로 해석하지 않는다.
- 실제 공개 조회 전에 private registry/configuration, package origin 및 이름 노출 가능성을 검토하고 사용자 승인을 얻어야 한다.
- Python 실행 및 이식 파일에 명시적으로 필요하지 않은 도구, workflow, installer, validation layer는 추가하지 않는다.
