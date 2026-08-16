# Chatbot Runtime Skills

업체가 제공하는 hosted chatbot runtime에서 bundle과 runtime 기능을 활용하는 skill을 둡니다.

- `SKILL.md` 외에 references, assets, schemas, scripts 등 bundled files를 사용할 수 있습니다.
- runtime script 실행은 허용되지만 사용자의 workspace authority는 전제하지 않습니다.
- 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/`에 둡니다.
- 같은 capability가 target별 배포를 위해 `skills-chatbot/`의 flat variant와 함께 존재할 수 있습니다. 의미가 겹친다는 이유만으로 어느 한쪽을 제거하지 않습니다.
- runtime variant는 해당 host에서 실제로 사용할 수 있는 references, scripts, tools, progressive loading을 활용하되 sibling flat variant의 독립 배포 목적을 침해하지 않습니다.
