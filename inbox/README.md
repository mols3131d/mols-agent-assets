# Inbox

`inbox/`는 사람, chat runtime, coding agent와 automation이 공통으로 사용할 수 있는 **platform-independent artifact workspace**입니다.

## Paths

- current artifact → `inbox/YYYY-MM-DD/<artifact>`
- archived artifact → `inbox/archive/YYYY-MM-DD/<artifact>`

날짜 directory는 실제 artifact가 생길 때만 만듭니다. 빈 directory나 placeholder를 유지하지 않습니다.

Artifact의 생성·승격·보존·삭제 기준과 Git history의 역할은 [Knowledge Lifecycle](../docs/documentation/lifecycle.md)이 소유합니다.

## Boundary

`inbox`는 directory convention이지 별도 branch, vendor feature 또는 workflow engine이 아닙니다. 특정 IDE, agent, chatbot, Notion 또는 GitHub 기능에 의존하지 않습니다.

Artifact 형식은 특정 플랫폼 metadata에 종속시키지 않습니다.
