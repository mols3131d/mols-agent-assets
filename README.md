# mols-agent-assets

AI 에이전트 자산을 개발, 검증 및 관리하는 저장소입니다.

Rulesync가 표현할 수 있는 Agent Asset은 `src/rulesync/`의 **격리된 native workspace**에서 관리합니다. 설정은 `src/rulesync/rulesync.jsonc`, 정본(canonical) Rule/Skill/Subagent는 `src/rulesync/.rulesync/`에 둡니다. 저장소 루트에는 Rulesync runtime workspace를 만들지 않습니다.

## 자산 유형

| 유형 | 역할 |
| --- | --- |
| Rule | 지속 적용되는 정책과 제약 |
| Skill | 재사용 가능한 기능과 조건부 context |
| Prompt | 현재 호출의 목표와 일회성 context |
| Agent | 독립 역할, 권한, 도구, 위임 |

외부 기준에 가까운 개념은 `docs/references/common/standards/agent-assets-standard-baseline.md`, 이 저장소의 비표준 확장과 실제 운용 기준은 `docs/references/common/standards/agent-assets-standard-personal.md`의 **Personal Agent Asset Standard**가 소유합니다.

## 소스 경계

| 디렉터리 | 역할 |
| --- | --- |
| `src/rulesync/` | 격리된 native Rulesync workspace와 projection 설정 |
| `src/rulesync/.rulesync/` | Rulesync-compatible Rule, Skill, Subagent의 정본 소스 |
| `src/`의 다른 경로 | 실제 요구가 있는 custom/non-standard Agent Asset 소스 |
| `.agents/AGENTS.md` | 이 저장소 자체에 적용되는 저장소 로컬 guard |
| `.agents/skills/` | 명시적으로 repository-local인 runtime Skill만 두는 예외 surface |
| `tests/` | 결정론적 테스트 |
| `evals/` | 행동/model eval과 cross-asset 회귀 계약 |
| `docs/` | 사람용 문서와 레퍼런스 |
| `scripts/` | 자동화·검증·동기화 도구 |

저장소 루트의 `.rulesync/`, `rulesync.jsonc`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/agents/`는 배포 소스로 사용하지 않습니다. `.agents/skills/`도 distribution canonical source가 아니며 현재 명시적 repository-local Skill인 `mols-chatbot-bootstrap`만 예외로 둡니다. Native read-only 검증은 `src/rulesync/`에서 직접 실행하고, generation처럼 파일을 쓰는 검증만 workspace 전체를 임시 디렉터리로 복사해 수행합니다.

Canonical Skill front matter와 target namespace는 current Rulesync schema를 따릅니다. Agent Skills와 vendor/harness 규격은 생성된 target artifact의 contract로 적용하며, 공식 원문은 `docs/references/skills/agent-skills-io/agent-skills-io-specification.md`에서 연결합니다. 이 저장소의 추가 convention은 `docs/references/skills/agent-assets-skills-standard-personal.md`, package shape와 target boundary는 `docs/references/skills/agent-assets-skills-target-profiles.md`가 소유합니다.

## 기본 작업 흐름

```text
src/rulesync/.rulesync 편집
  → Markdown 변경 시 rumdl fmt
  → src/rulesync에서 native doctor / dry-run preview
  → 파일을 쓰는 검증만 임시 workspace 복사본에서 수행
  → repository test / 적용 가능한 eval
  → 정본 소스만 최종 검토
```

핵심 원칙은 단순합니다. **native layout은 보존하되, 저장소 루트의 runtime surface와 배포 소스는 분리합니다.**
