# Render Workflow

Bundled renderer를 사용하거나 렌더 결과를 검증할 때만 읽는다.

## Run

스킬 루트에서 실행한다.

```bash
python scripts/render_dashboard.py render dashboard.yml -o dashboard.md
```

`uv` 환경에서는 다음도 가능하다.

```bash
uv run python scripts/render_dashboard.py render dashboard.yml -o dashboard.md
```

기존 Markdown이 현재 YAML과 같은 projection인지 검증할 때는 다음을 사용한다.

```bash
python scripts/render_dashboard.py validate dashboard.yml --markdown dashboard.md
```

## Renderer Boundary

Renderer는 다음만 담당한다.

- YAML parse와 schema validation
- progress와 aggregate 계산
- gap 번호 생성
- Jinja2 `StrictUndefined` Markdown rendering
- 생성 Markdown 구조 검증
- 기존 Markdown과 현재 YAML render의 drift 검증
- 성공한 결과의 atomic write

Requirement 해석, 상태 판단, evidence freshness 판단은 에이전트 책임이다.

## Result Check

- semantic validation이 성공했는가
- Jinja2 rendering이 undefined variable 없이 성공했는가
- 합계가 item의 numerator/denominator 합과 일치하는가
- gap 번호가 item별로 1부터 시작하는가
- 사용하지 않는 optional section이 생성되지 않았는가
- `validate --markdown`을 사용했다면 기존 Markdown이 같은 template 설정으로 다시 렌더한 결과와 정확히 일치하는가

Renderer나 검증 도구를 실행하지 못했으면 실행한 것으로 기록하지 않는다.
