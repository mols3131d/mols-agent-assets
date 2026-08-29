# Local-Reasoning Structure

Status: **strong candidate**

## Idea

Code를 변경할 때 가능한 한 좁은 context만으로 해당 변경을 이해하고 검증할 수 있는 구조를 선호할 수 있습니다.

핵심은 file이나 module을 작게 만드는 것이 아닙니다. **한 부분을 이해하거나 바꾸기 위해 서로 무관한 책임, 먼 dependency, hidden convention까지 함께 읽어야 하는 범위를 줄이는 것**이 중심입니다.

## Why It May Be a Pattern

최신 coding agent는 큰 context를 읽을 수 있지만, context가 커질수록 관련 정보와 주변 잡음이 함께 늘어납니다. Human developer에게도 같은 문제가 있습니다. 따라서 LOC 자체보다 다음과 같은 질문이 더 오래가는 판단축일 수 있습니다.

- 이 behavior를 수정하려면 몇 개의 unrelated area까지 따라가야 하는가?
- public interface만으로 충분한가, 아니면 implementation detail을 여러 곳에서 알아야 하는가?
- local change가 예상 밖의 distant effect를 만들기 쉬운가?
- 관련 코드가 가까이 있어서 찾기 쉬운가, 아니면 shared abstraction을 따라 repository 전체를 이동해야 하는가?

## Typical Signals

다음은 구조를 다시 볼 만한 신호가 될 수 있습니다.

- 하나의 file이나 module에 서로 다른 change reason이 반복해서 섞입니다.
- 작은 behavior 수정에도 여러 unrelated file을 항상 함께 열어야 합니다.
- private implementation detail이 다른 영역의 판단에 자주 필요합니다.
- local helper를 지나치게 shared하게 만들어 작은 변경도 넓은 blast radius를 가집니다.
- directory나 module boundary는 존재하지만 실제 dependency가 이를 계속 가로지릅니다.

반대로 file이 길거나 module이 크다는 사실만으로는 충분한 신호가 아닙니다. 큰 파일 하나가 하나의 coherent abstraction을 제공하고 변경 범위도 예측 가능하다면 억지로 split할 이유가 약할 수 있습니다.

## Possible Responses

상황에 따라 다음을 고려할 수 있습니다.

- 관련 behavior와 data를 더 가까운 boundary에 모읍니다.
- implementation detail을 감추고 더 안정적인 interface를 둡니다.
- 서로 다른 change reason이 반복해서 충돌한다면 responsibility를 나눕니다.
- 작은 local helper가 실제로 재사용되지 않는다면 shared abstraction으로 올리는 비용을 다시 봅니다.
- dependency direction이 불분명하다면 더 명시적인 module boundary나 architecture invariant와 함께 봅니다.

이 대응들은 모두 선택지입니다. locality를 높인다는 이유로 wrapper, directory, abstraction을 추가해 오히려 navigation과 maintenance cost를 높일 수 있으므로 가장 싼 개선부터 비교합니다.

## Relationship to Existing Patterns

`Filesystem-Legible Structure`와는 질문이 다릅니다.

- Filesystem legibility: **어디에 무엇이 있는지 찾기 쉬운가?**
- Local reasoning: **찾은 부분을 바꾸기 위해 얼마나 많은 다른 것을 알아야 하는가?**

`Source-Mirrored Test Structure`는 관련 test를 찾는 navigation cue에 집중하므로, local reasoning의 test-specific specialization으로 단정하지 않습니다. 다만 test behavior가 한 file에 과도하게 섞여 변경 context가 커지는 상황에서는 서로 참고할 수 있습니다.

## Limits

- cross-cutting concern, compiler pipeline, distributed workflow처럼 본질적으로 여러 영역을 함께 봐야 하는 문제는 local reasoning을 완전히 달성하기 어렵습니다.
- abstraction을 늘리면 local interface는 작아져도 전체 indirection은 커질 수 있습니다.
- strict locality를 추구하다가 duplication을 과도하게 허용하면 invariant가 분산될 수 있습니다.
- framework나 language가 이미 강한 module boundary를 제공한다면 별도 구조를 만들 필요가 없을 수 있습니다.

## Promotion Questions

- `cohesion`, `encapsulation`, `SRP`를 단순 재서술하는 수준을 넘는가?
- agentic coding의 context cost를 포함하되 특정 모델의 context window에 의존하지 않고 설명할 수 있는가?
- file size discussion을 LOC rule 없이 충분히 흡수할 수 있는가?
- `Filesystem-Legible Structure`와 책임 경계가 실제 사례에서도 분명한가?

## Research Notes

- OpenAI의 agent-first repository 경험은 context를 scarce resource로 보고, repository를 agent가 탐색하고 추론하기 쉬운 구조로 만드는 것을 강조합니다.
- 전통적인 modularity와 encapsulation의 local reasoning 관점도 이 후보의 더 오래된 이론적 grounding이 될 수 있습니다.
