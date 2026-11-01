---
title: Front Matter CMS
description: Front Matter CMS의 기본 설정 우선 원칙, 문서 metadata 편집과 비활성화한 CMS 기능의 예외를 확인할 때 사용합니다.
---

# Front Matter CMS

Front Matter CMS는 VS Code에서 문서 metadata를 편집하는 선택적 연동입니다. 설정은 [`frontmatter.json`](../../frontmatter.json), Markdown metadata의 의미는 [Frontmatter](../documentation/frontmatter.md)가 소유합니다. 문서 작성·검증에 확장 설치가 필수인 것은 아닙니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 공식 설정과 최신 안정 확장을 우선하며, editor 확장 버전을 CLI lock으로 관리하지 않습니다.

- 이 저장소는 게시 사이트가 아니므로 framework를 `other`로 두고 `docs/`를 편집 범위로 설정합니다. baseline은 제외하며 필수 `description`은 native content type에 선언합니다.
- metadata validation은 사용하되 content health는 끕니다. 파일·폴더 탐색과 설명 metadata 관리에 필요한 범위로 사용합니다.
- slug 최적화·preview·사이트 열기·서버 시작/종료 등의 CMS action은 비활성화합니다. 없는 사이트나 서버 운영 절차를 문서 저장소에 추가하지 않습니다.
- 확장을 쓰지 않아도 repository frontmatter validator와 index generator로 같은 저장소 계약을 확인합니다. 확장의 성공 표시가 CI 검증을 대신하지 않습니다.

새 설정이 필요하면 공식 schema·기본값을 먼저 확인하고 프로젝트에 필요한 차이만 추가합니다. 공식 옵션 탐색은 [Front Matter CMS reference](../development/tooling/front-matter-cms.md)를 따릅니다.

## 권장 버전 정책

**Latest**를 편집기 확장 관리 기능에 위임합니다. 프로젝트가 확장 버전을 `mise.toml`에 중복 선언하지 않으며, 새 확장에서 `frontmatter.json` 설정·metadata 편집이 변경되는지만 확인합니다. 확장이 없어도 저장소의 문서 검증 경로는 독립적으로 유지됩니다.

## Official Sources

- [Settings](https://frontmatter.codes/docs/settings)
- [Configuration schema](https://frontmatter.codes/frontmatter.schema.json)
