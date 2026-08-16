# Chatbot Skills

자연어 지침만으로 동작하는 flat chatbot skill을 둡니다.

- 각 skill은 `<skill-name>.skill.md` 단일 파일로 둡니다.
- bundled references, assets, scripts 또는 provider runtime이 필요하면 `../skills-chatbot-runtime/` profile을 사용합니다.
- 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile을 사용합니다.
- 같은 capability가 `../skills/`, `skills-chatbot/`, `../skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.
- flat variant는 단일 파일만 제공하는 harness에서도 독립적으로 동작하도록 최적화합니다. 다른 profile의 구조를 그대로 복제하기보다 flat target에서 가장 효율적인 형태를 우선합니다.
