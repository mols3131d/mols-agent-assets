# 자산 개발 가이드

`mols-agent-assets` 저장소에서 AI 에이전트 자산을 신규 생성하고 수정, 최적화 및 승격 배포하는 가이드입니다.

---

## 디렉터리 역할

- `src/`: 자산 생성, 수정, 실험 및 초안 작성을 수행하는 기본 개발 공간.
- `release/`: 검증이 완료된 배포 확정 자산 공간. 직접 수정하지 않습니다.
- `scripts/src_to_release.py`: `src/`에서 검증된 자산을 `release/`로 승격하는 자동화 스크립트.

## 개발 파이프라인

1. **초안 작성 (`src/`)**:
   - 사람용 초안 작성 시 `*.human.ko.md` 확장자를 사용합니다.
   - 자산 변환 완료 시 `.human.ko`를 제거하여 에이전트 자산(`.md`)으로 변경합니다.

2. **최적화 (`agent-asset-studio`)**:
   - `agent-asset-studio` 스킬을 활용하여 컨텍스트 용량 최적화 및 규격 검증을 수행합니다.

3. **릴리즈 승격**:
   - 검증이 끝난 자산을 `release/` 폴더로 승격 배포합니다:

     ```bash
     uv run python scripts/src_to_release.py skills/<skill-name>
     ```
