# Documentation Layout

`docs/`는 문서의 책임과 portability에 따라 다음 surface로 나눕니다.

| Path | Responsibility |
| --- | --- |
| [`development/`](development/) | 이 repository의 개발 규칙과 관행 |
| [`document/`](document/) | 이 repository의 문서 규칙과 관행 |
| [`references/`](references/) | 이 repository 또는 다른 프로젝트에서 참고할 문서 |
| [`presets/`](presets/) | 다른 project에 바로 가져가거나 최소 수정해 적용할 reusable policy/profile |
| `<asset-type>/<asset>/` | 한 자산에 대한 portable maintainer documentation capsule |

구체적인 문서 배치와 중복 경계는 [Documentation](document/README.md)이 소유합니다.
