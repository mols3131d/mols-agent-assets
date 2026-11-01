---
title: Biome
description: Biome의 기본 권장 규칙, 저장소 포맷 예외와 CLI·schema 버전 호환성을 확인할 때 사용합니다.
---

# Biome

Biome은 JSON·JSONC·JavaScript·TypeScript 계열의 format·lint를 맡습니다. 설정은 [`biome.json`](../../biome.json), CLI 버전은 [`mise.toml`](../../mise.toml)과 [`mise.lock`](../../mise.lock)이 정본입니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 권장 lint preset과 최신 안정 릴리스를 우선 검토합니다. 현재는 출력 일관성과 config 호환성을 검증한 exact pin으로 실행합니다.

- lint는 recommended preset을 사용하며 개별 규칙을 불필요하게 나열하지 않습니다.
- format은 space 2칸과 LF를 명시해 저장소 파일의 표현을 통일합니다.
- VCS 연동과 Git ignore를 사용합니다. 별도 wrapper에 같은 ignore 정책을 복제하지 않습니다.
- `$schema`와 실제 CLI 버전을 함께 검토합니다. schema URL만 최신으로 바꾸거나, 새 formatter를 검증 없이 기존 pin 대신 실행하지 않습니다.

버전 갱신 시 `biome.json`의 `$schema`와 CLI pin을 함께 갱신하고, `mise run check` 및 [Formatting](../development/formatting.md)의 changed-only 경로에서 출력 diff를 검토합니다. 일상 작업에서 최신화를 이유로 저장소 전체를 다시 포맷하지 않습니다.

## Official Sources

- [Configuration](https://biomejs.dev/reference/configuration/)
- [CLI](https://biomejs.dev/reference/cli/)
