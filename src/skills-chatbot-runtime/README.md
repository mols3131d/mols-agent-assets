# Chatbot Runtime Skills

업체가 제공하는 hosted chatbot runtime에서 bundle과 runtime 기능을 활용하는 skill을 둡니다.

- `SKILL.md` 외에 references, assets, schemas, scripts 등 bundled files를 사용할 수 있습니다.
- runtime script 실행은 허용되지만 사용자의 workspace authority는 전제하지 않습니다.
- 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile을 사용합니다.
- 같은 capability가 `../skills/`, `../skills-chatbot/`, `skills-chatbot-runtime/` 중 둘 이상에 함께 존재할 수 있습니다. target profile이 다르면 의미가 겹친다는 이유만으로 제거하지 않습니다.
- runtime variant는 해당 host가 실제로 지원하는 references, scripts, tools, progressive loading을 최대한 활용해 context와 실행 비용을 최적화합니다. 다른 profile의 제약을 그대로 가져와 runtime 이점을 포기하지 않습니다.
