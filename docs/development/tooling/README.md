---
description: 외부 tooling과 specification의 authority routing, integration knowledge와 중복 경계를 찾을 때 사용하는 directory entrypoint입니다.
---

# Tooling References

`docs/development/tooling/`는 외부 tool과 specification을 사용할 때 반복해서 필요한 **authority routing과 integration knowledge**를 보관합니다.

## Ownership

- 같은 external authority나 integration concern을 둘 이상의 tooling reference가 함께 소유하지 않습니다.
- Tooling reference는 upstream behavior를 local truth처럼 재정의하지 않고, 가능한 한 authoritative source로 route합니다.
- Repository에 필요한 local integration delta가 있으면 upstream fact와 구분해 이 surface가 소유할 수 있습니다.
- 다른 documentation surface에서 같은 tooling knowledge가 필요하면 원문을 복제하기보다 authoritative tooling reference를 link합니다.

## Boundary

- 이 프로젝트에서 사용하는 도구의 기본 설정·버전 선택·예외와 운영 안내는 [Tools](../../tools/README.md)가 소유합니다. 이곳의 공식 source routing과 integration reference를 프로젝트 설정 목록으로 복제하지 않습니다.
- 이 repository에만 적용되는 development workflow와 operational rule은 상위 [Development](../README.md)의 해당 정책이 소유합니다.
- 여러 repository에서 재사용할 설계 pattern은 [`catalog/patterns/`](../../../catalog/patterns/)가 소유합니다.
- Agent Asset 자체의 설계 지식은 [Agent Assets](../agent-assets/README.md)가 소유합니다.

이 README는 tool inventory를 복제하지 않습니다. Filesystem과 search로 찾을 수 있는 목록보다 이 directory의 책임과 ownership boundary만 소유합니다.
