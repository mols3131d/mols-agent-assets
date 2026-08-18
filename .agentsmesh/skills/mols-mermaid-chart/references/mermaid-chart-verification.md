# Mermaid Chart Verification

Data, source syntax, renderer support와 rendered image를 서로 다른 단계로 검증한다.

## Baseline

- Example의 minimum version은 feature gate이며 dependency pin 권장이 아니다.
- target renderer, embedded Mermaid와 documentation version을 구분한다.
- renderer가 없으면 render 성공을 주장하지 않는다.
- version 변경 후에는 대표 example을 다시 render한다.

## Level 1: Data And Source Review

항상 수행한다.

- source 값, 단위, sign, 순서, 누락값과 기준 시점을 대조한다.
- declaration과 type별 syntax를 확인한다.
- XY category 수와 series value 수가 일치하는지 확인한다.
- Pie가 같은 전체를 구성하고 category가 중복되지 않는지 확인한다.
- Sankey row가 `source,target,value`이고 value가 수치인지 확인한다.
- Radar axis와 curve value 수, scale 방향을 확인한다.
- Quadrant 좌표와 축 정의의 근거를 확인한다.
- `-beta`, frontmatter와 선택 type의 renderer 지원을 확인한다.
- Mermaid가 직접 지원하지 않는 chart를 억지로 근사하지 않는다.

## Level 2: Renderer Validation

`.mmd` 또는 rendered artifact를 만들거나 renderer가 사용 가능할 때 수행한다.

### Local Mermaid CLI

`mmdc --version` 성공만으로 export 환경이 완전하다고 판단하지 않는다. Node package와 headless browser가 모두 필요하다.

```bash
mmdc -i chart.mmd -o /tmp/chart-check.svg
```

```bash
mmdc -i chart.mmd -o chart.png -w 2048 --backgroundColor white
mmdc -i chart.mmd -o chart.svg
mmdc -i chart.mmd -o chart.pdf
```

Chrome/Puppeteer 오류는 environment setup failure다. 올바른 source나 data를 임의로 바꾸지 않는다. CLI theme은 설치된 version의 지원 목록을 확인한다.

### Kroki Fallback

Network access가 허용되고 private data가 아닐 때만 사용한다.

```bash
curl -fSs -X POST \
  -H "Content-Type: text/plain" \
  --data-binary @chart.mmd \
  https://kroki.io/mermaid/svg \
  -o chart.svg
```

Type이 지원되지 않으면 table, portable chart 또는 전문 chart 도구로 전환한다.

## Level 3: Visual And Scale Review

| Check | Signal | Minimal Fix |
| --- | --- | --- |
| Label clipping | category·axis·legend text가 잘림 | label 축약, chart 분할, larger output |
| Misleading scale | 범위가 차이를 과장하거나 단위가 불명확 | axis·unit 명시 또는 table 병기 |
| Excess density | category·series가 과다 | top-N, detail chart 또는 table |
| Wrong ordering | time/category 순서가 질문과 다름 | source 순서 복원 또는 명시적 정렬 |
| Wrong type | 질문과 chart type이 맞지 않음 | 더 직접적인 type으로 교체 |
| False precision | 근거보다 세밀한 좌표·소수점 | precision 축소 또는 근거 명시 |

수정 후 data review와 renderer validation을 다시 수행한다. 반복해도 해결되지 않으면 제약을 명시한다.

## Failure Reporting

- **Data mismatch**: source와 다른 값·순서·단위·누락을 보고하고 수정한다.
- **Syntax failure**: error location과 수정한 source를 보고한다.
- **Renderer setup failure**: missing CLI/browser/network를 보고하고 source-only 결과를 제공한다.
- **Unsupported type**: portable chart, table 또는 전문 chart tool로 전환한다.
- **Visual limitation**: 남은 readability·scale 문제와 분할 지점을 명시한다.
