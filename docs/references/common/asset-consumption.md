---
title: Using Assets from This Repository
description: 이 저장소가 관리하는 Agent Asset을 외부 repository나 runtime에서 발견하고 직접 사용하거나 Rulesync로 설치하는 방법
---

# 이 저장소의 자산 사용하기

이 저장소는 Agent Asset의 **upstream library**입니다. Consumer는 필요한 자산만 선택해 사용하고, project나 runtime에 맞춘 변경은 consumer가 소유합니다.

## 어떤 방식으로 가져올까?

| 목적 | 권장 방식 |
| --- | --- |
| 한 번 읽거나 시험한다 | canonical source URL을 직접 사용 |
| 웹을 읽을 수 있는 agent가 필요한 Skill을 찾게 한다 | [`route/ROUTE.md`](../../../route/ROUTE.md)에서 discovery 시작 |
| project에서 Skill을 지속적으로 사용한다 | Rulesync declarative source로 설치 |
| 자산을 수정해서 자기 project 전용으로 쓴다 | 필요한 source만 복사하고 downstream adaptation으로 관리 |
| Subagent를 가져온다 | canonical source를 consumer의 Rulesync 또는 vendor-native 위치로 복사 |

전체 repository나 generated output을 통째로 복제하는 것보다 **필요한 자산만 선택**하는 것을 기본으로 합니다.

## 자산 찾기

Reusable authored source는 [`src/rulesync/.rulesync/`](../../../src/rulesync/.rulesync/)에 있습니다.

- Skills: [`src/rulesync/.rulesync/skills/`](../../../src/rulesync/.rulesync/skills/)
- Subagents: [`src/rulesync/.rulesync/subagents/`](../../../src/rulesync/.rulesync/subagents/)
- Skill discovery metadata: [`route/skills.jsonl`](../../../route/skills.jsonl)

`route/`는 빠른 discovery를 위한 derived surface입니다. 자산 본문의 authority는 `src/`의 canonical source에 있습니다.

## 일회성으로 Skill 사용하기

Runtime이 URL을 읽을 수 있다면 설치 없이 필요한 `SKILL.md`를 직접 제공할 수 있습니다.

```text
https://raw.githubusercontent.com/mols3131d/mols-agent-assets/refs/heads/main/src/rulesync/.rulesync/skills/<skill-name>/SKILL.md
```

Skill에 `references/`, `scripts/` 같은 supporting files가 있으면 `SKILL.md`만으로 충분하다고 가정하지 않습니다. Agent가 필요할 때 같은 Skill directory의 참조 자산도 읽을 수 있어야 합니다.

최신 상태를 따라가려면 `main` URL을 사용하고, 특정 상태를 고정해야 하면 branch 이름 대신 commit SHA를 URL에 사용합니다.

## Rulesync로 Skill 설치하기

지속적으로 사용할 Skill은 consumer repository의 Rulesync source로 선언하는 것을 권장합니다. Consumer에 `rulesync.jsonc`가 없다면 먼저 `rulesync init`으로 workspace를 준비합니다.

```bash
rulesync add mols3131d/mols-agent-assets --ref main --path src/rulesync/.rulesync/skills --skills <skill-name>
```

여러 Skill은 `--skills`에 comma-separated name으로 선택합니다. `rulesync add`는 source declaration과 lock state를 만들고 선택한 Skill을 설치합니다.

그다음 consumer가 사용하는 target에 맞게 projection합니다.

```bash
rulesync install --frozen
rulesync generate
```

재현 가능한 설치가 필요하면 consumer repository가 `rulesync.jsonc`와 `rulesync.lock`을 함께 관리합니다. 새 upstream 상태를 받아들이려면 `rulesync install --update`로 lock을 갱신하고 변경 내용을 검토합니다.

Rulesync의 현재 CLI, target과 declarative source semantics는 이 저장소의 [Rulesync reference](../tooling/rulesync.md)와 upstream official documentation을 기준으로 확인합니다.

## Subagent 또는 직접 수정할 자산 가져오기

현재 Rulesync declarative source 설치는 Rules와 Skills를 대상으로 합니다. 이 저장소의 Subagent나 consumer가 직접 수정해야 하는 자산은 필요한 canonical source만 복사해 downstream에서 소유합니다.

Rulesync를 사용하는 consumer라면 Subagent source를 `.rulesync/subagents/`에 두고 자신의 target으로 generate할 수 있습니다. Rulesync를 사용하지 않는다면 해당 runtime이 정의한 vendor-native project path를 따릅니다.

Skill을 직접 복사할 때는 `SKILL.md` 하나가 아니라 **Skill directory 전체**를 복사해 supporting files를 보존합니다. Upstream notice, attribution 또는 license 정보가 자산에 포함되어 있으면 함께 보존합니다.

## 가져오지 말아야 할 것

- root `.rulesync/`와 root `rulesync.jsonc`는 **이 repository 자체의 consumer configuration**이므로 다른 project의 template이 아닙니다.
- generated vendor projection은 canonical source가 아닙니다.
- `route/`의 derived metadata를 자산 본문 대신 fork하지 않습니다.
- consumer-specific 변경을 이 repository의 upstream source와 이중 authority로 관리하지 않습니다.

필요한 자산을 가져온 뒤에는 consumer가 자신의 runtime support, target path, generation policy와 검증을 소유합니다.

> [!IMPORTANT]
> 이 repository는 현재 root `LICENSE`를 선언하지 않습니다. 위 내용은 기술적인 사용 경로를 설명하며, 제3자의 복사·수정·재배포 권한은 별도 license 또는 permission이 선언되기 전까지 자동으로 부여된다고 가정하지 않습니다.
