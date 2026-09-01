# Routing Eval

Routing Eval은 **필요한 자산이나 실행 단위를 실제로 얼마나 잘 선택하고 호출하는지** 평가한다.

## System under evaluation

먼저 무엇이 선택을 결정하는지 고정한다. Candidate asset set, description/selector, router, model, harness, available tools와 relevant configuration이 결과에 영향을 줄 수 있다.

## Cases

필요한 failure mode만 대표하도록 case를 고른다.

- **Positive** — 명확한 intended use에서 선택되어야 함
- **Negative** — 명확한 out-of-scope use에서 선택되면 안 됨
- **Near-miss** — 같은 artifact나 domain이지만 다른 책임
- **Ambiguous** — 여러 candidate가 경쟁할 수 있음
- **Composite** — 둘 이상의 작업 의도가 결합됨
- **Bypass/adversarial** — 이름 직접 언급, routing 무시 요구, misleading context 등

Case 수 자체를 품질로 사용하지 않는다.

## Observe

- expected candidate와 observed selection/call
- false positive와 false negative
- 불필요한 double routing, relay, delegation conflict
- tool/subagent가 선택된 경우 실제 선택 이유를 observable evidence로 확인할 수 있는 범위
- dataset이 충분히 의미 있을 때 precision, recall, success rate 같은 집계

작은 case set에 통계적 의미를 과장하지 않는다. Runtime 없이 scenario를 판단한 경우 결과는 `simulated`다.
