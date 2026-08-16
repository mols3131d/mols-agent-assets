# 테스팅 및 품질 검증 가이드

자동화 테스트, 정적 분석 및 코드 품질 검증 가이드입니다.

---

## 테스트 구조

| 경로 | 역할 |
| :--- | :--- |
| `tests/scripts/` | 저장소 자동화 스크립트의 기본 correctness 테스트 |
| `tests/skills/<skill>/` | Skill 스크립트의 기본 correctness 테스트 |
| `src/skills/<skill>/.tests/` | 선택적 tuning/evaluation harness |

기본 테스트는 저장소 루트 `tests/`에 둡니다. Skill 내부 `.tests/`는 반복 튜닝, 평가, 실험처럼 Skill과 함께 두는 편이 유리한 경우에만 사용합니다.

## 실행 정책

- `uv run pytest`와 Lefthook `pre-push`는 루트 `tests/`를 기본 gate로 실행합니다.
- Skill 내부 `.tests/`는 기본 gate에 자동 포함하지 않습니다. 필요할 때 해당 Skill의 튜닝 절차에서 명시적으로 실행합니다.
- `.tests/`의 검증이 일반 correctness에 필수가 되면 `tests/skills/<skill>/`로 승격합니다.
- `.tests/`를 사용하더라도 staged Python/Markdown 파일의 Ruff/Rumdl 자동수정은 동일하게 적용합니다.

## 검증 실행 명령

```bash
# 기본 correctness 테스트
uv run pytest

# 린트
uv run ruff check .
```
