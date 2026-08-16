# Chatbot Skills

단일 Markdown 파일만으로 완결되는 **flat chatbot skill**을 둡니다.

## Placement

`skills-chatbot/`은 다음 조건을 모두 만족할 때 사용합니다.

1. skill 전체를 `<skill-name>.skill.md` **한 파일**로 표현할 수 있습니다.
1. 배포되는 단일 skill 파일이 **4,000 tokens 미만**입니다.
1. references, assets, schemas, scripts 같은 bundled files가 필요하지 않습니다.

다음 중 하나라도 해당하면 `../skills-chatbot-runtime/` profile을 사용합니다.

- 단일 skill 파일이 **4,000 tokens 이상**이라 내용을 여러 Markdown 파일로 나눠야 합니다.
- Markdown 한 파일만으로 capability를 완결할 수 없습니다.
- references, assets, schemas, scripts, images 또는 host runtime 기능이 필요합니다.
- progressive loading으로 필요한 context만 선택적으로 읽는 편이 더 적합합니다.

로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile도 검토합니다.

## Target Variants

같은 capability가 `../skills/`, `skills-chatbot/`, `../skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.

flat variant는 외부 bundle 없이 **한 파일만 전달되는 harness에서 독립적으로 동작하도록 최적화**합니다. 다른 profile의 구조를 그대로 복제하기보다 flat target에서 가장 효율적인 형태를 우선합니다.
