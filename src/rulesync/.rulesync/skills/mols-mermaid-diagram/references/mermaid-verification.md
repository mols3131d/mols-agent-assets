# Mermaid Verification

Source syntax, renderer support와 rendered image를 서로 다른 단계로 검증한다.

## Baseline

- Example의 minimum version은 feature gate이며 dependency pin 권장이 아니다.
- target renderer, embedded Mermaid와 documentation version을 구분한다.
- renderer가 없으면 render 성공을 주장하지 않는다.
- version 변경 후에는 대표 example을 다시 render한다.

## Level 1: Source Review

항상 수행한다.

- declaration과 type별 arrow·relationship syntax를 확인한다.
- participant, node ID, class와 subgraph reference가 선언됐는지 확인한다.
- fragment, state block, class body와 note가 닫혔는지 확인한다.
- special character가 있는 label을 quote한다.
- experimental type, frontmatter, animation과 icon pack의 renderer 지원을 확인한다.
- relative link와 output filename이 실제 위치와 일치하는지 확인한다.

## Level 2: Renderer Validation

`.mmd` 또는 rendered artifact를 만들거나 renderer가 사용 가능할 때 수행한다.

### Local Mermaid CLI

`mmdc --version` 성공만으로 export 환경이 완전하다고 판단하지 않는다. Node package와 headless browser가 모두 필요하다.

```bash
mmdc -i diagram.mmd -o /tmp/diagram-check.svg
```

```bash
mmdc -i diagram.mmd -o diagram.png -w 2048 --backgroundColor white
mmdc -i diagram.mmd -o diagram.svg
mmdc -i diagram.mmd -o diagram.pdf
```

Chrome/Puppeteer 오류는 environment setup failure다. 올바른 source를 임의로 수정하지 않는다. CLI theme은 설치된 version의 지원 목록을 확인한다.

### Kroki Fallback

Network access가 허용되고 private content가 아닐 때만 사용한다.

```bash
curl -fSs -X POST \
  -H "Content-Type: text/plain" \
  --data-binary @diagram.mmd \
  https://kroki.io/mermaid/svg \
  -o diagram.svg
```

Type이 지원되지 않으면 core type 또는 text/table fallback으로 전환한다.

## Level 3: Visual Review

| Check | Signal | Minimal Fix |
| --- | --- | --- |
| Label clipping | text가 잘리거나 줄이 비정상 | label 축약 또는 `<br/>` |
| Excess density | node와 edge가 한곳에 몰림 | direction, grouping, detail 분리 |
| Wrong aspect | 지나치게 넓거나 높음 | direction 변경 또는 detail 분리 |
| Edge spaghetti | 경로 추적이 어려움 | 선언 순서, boundary, diagram 분리 |
| Wrong type | 정보 구조와 type이 맞지 않음 | 더 직접적인 type으로 교체 |
| Low contrast | text와 fill 구분이 어려움 | custom style 축소 또는 theme 변경 |

수정 후 renderer validation을 다시 수행한다. 반복해도 해결되지 않으면 제약을 명시한다.

## Editing Existing Work

- label 변경은 해당 text만 수정한다.
- node·edge 추가/삭제는 관련 declaration과 relationship만 수정한다.
- direction·grouping·color 변경은 요청 범위에 필요한 최소 source만 수정한다.
- 사용자 피드백을 이유로 source 전체를 재작성하지 않는다.

## Failure Reporting

- **Syntax failure**: error location과 수정한 source를 보고한다.
- **Renderer setup failure**: missing CLI/browser/network를 보고하고 source-only 결과를 제공한다.
- **Unsupported type**: core type 또는 text/table fallback으로 전환한다.
- **Visual limitation**: 남은 readability 문제와 분할 지점을 명시한다.
