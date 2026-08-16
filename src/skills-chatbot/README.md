# Chatbot Skills

자연어 지침만으로 동작하는 flat chatbot skill을 둡니다.

- 각 skill은 `<skill-name>.skill.md` 단일 파일로 둡니다.
- bundled references, assets, scripts 또는 provider runtime이 필요하면 `../skills-chatbot-runtime/`에 둡니다.
- 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/`에 둡니다.
- 같은 capability가 runtime별 배포를 위해 `skills-chatbot/`과 `skills-chatbot-runtime/`에 함께 존재할 수 있습니다. 의미가 겹친다는 이유만으로 한쪽을 제거하지 않습니다.
- flat variant는 단일 파일만 제공하는 target에서도 독립적으로 동작해야 하며, runtime variant는 해당 host의 bundle/runtime 이점을 활용할 수 있습니다.
