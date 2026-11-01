---
title: rumdl
description: rumdl의 Markdown 설정 정본, 기본값과 다른 문서 표현 규칙 및 버전 갱신 시 확인할 예외를 찾을 때 사용합니다.
---

# rumdl

rumdl은 Markdown format·lint를 맡습니다. 설정은 [`.rumdl.toml`](../../.rumdl.toml), 실행 버전은 [`mise.toml`](../../mise.toml)과 [`mise.lock`](../../mise.lock)이 소유합니다. 기본 실행 경로는 [Formatting](../development/formatting.md)을 따릅니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 기본 규칙을 우선하고 최신 안정 버전을 검토하되, formatter·lint 출력의 일관성을 위해 검증된 exact pin으로 실행합니다. 패치 릴리스도 출력 변화가 없다고 가정하지 않습니다.

- GFM을 사용하며 Markdown prose는 고정 열 너비로 hard-wrap하지 않습니다. 줄 길이 규칙 `MD013`을 끄는 설정과 [문서 작성 지침](../documentation/principles.md)을 함께 따릅니다.
- heading·목록·fence·강조·table 표현은 native 설정으로 통일합니다. 현재 ATX heading, 원본의 `1.` 번호 목록, backtick fence, asterisk 강조와 compact table을 사용합니다.
- 문서·자산의 표현을 위해 일부 규칙을 끄고 추가 규칙을 켭니다. 전체 선택은 설정 파일이 정본이며 개별 문서에서 임의로 다른 표준을 만들지 않습니다.
- 생성물·임시 디렉터리는 설정의 exclude를 따릅니다. 기본 작업은 `format-changed`이며 전체 format은 명시적인 저장소 정리에 한정합니다.

버전·보안 수정 후보를 검토할 때는 설정 규칙 지원 여부와 변경 파일의 `rumdl check --no-cache <paths...>` 결과, 포맷 diff를 확인합니다. 출력 변화가 있는 minor/major 전환은 별도 검토하며, 오래된 전역 rumdl의 경고를 기준으로 프로젝트 설정을 삭제하지 않습니다.

## 권장 버전 정책

**Patch**(초기 전환 후보 `0.3`)를 권장합니다. `0.2`에서 `0.3`으로 최초 전환할 때는 별도 호환성 검토가 필요하며, 이후 패치 갱신에서도 Markdown 규칙·포맷 diff를 확인합니다. 새 버전의 보안 수정이 있는 경우 현재 pin을 유지한다는 이유로 대응을 지연하지 않습니다.

## Official Sources

- [rumdl repository and documentation](https://github.com/rvben/rumdl)
- [Releases](https://github.com/rvben/rumdl/releases)
