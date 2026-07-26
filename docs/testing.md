# 테스팅 및 품질 검증 가이드

자동화 테스트, 정적 분석 및 코드 품질 검증 가이드입니다.

---

## 테스트 구조

| 경로 | 목적 |
| :--- | :--- |
| `tests/scripts/` | 저장소 자동화 스크립트 테스트 |
| `tests/skills/` | 에이전트 스킬 검증용 테스트 및 피스처 |

## 검증 실행 명령

```bash
# 단위 테스트 실행
uv run pytest

# 정적 타입 검사 및 린트
uv run ty check
uv run ruff check .
```
