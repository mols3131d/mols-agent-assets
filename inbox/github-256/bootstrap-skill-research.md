# Bootstrap Design Skill — Research

> PR #256 · research artifact · 2026-10-24. 대상은 이 저장소의 신규 **`mols-dev-env-bootstrap-design` Skill** 설계이다. 제품의 설치 정책 정본이나 Skill 실행 계약이 아니다.

## 조사 목표와 범위

초기 설정, 반복 복구, 개발 중 bounded update를 설계하는 Skill이 **독립적인 재사용 능력**을 갖추도록 현재 자산과 외부 도구의 운영 semantics를 조사한다. 새 Skill은 일반 dependency upgrade, OS 전역 installer 구현, CI admission workflow 디자인을 소유하지 않는다.

- 조사 대상 기준 ref: PR #256의 `mols/feat/dev-environment-bootstrap` (`7d66775bfbcb5b35227c70bfe3ae9b3e7ba31050`, 조사 시작 시점).
- 현재 source: [기존 Skill 초안 (조사 시작 시 commit)](https://github.com/mols3131d/mols-agent-assets/blob/7d66775bfbcb5b35227c70bfe3ae9b3e7ba31050/src/rulesync/.rulesync/skills/mols-dev-bootstrap-design/SKILL.md), [부트스트랩 명세](https://github.com/mols3131d/mols-agent-assets/blob/dfa9f45ce7da69673f08d3e53df88f5a7a23fe7d/inbox/github-258/development-environment-bootstrap-spec.md), [mise.toml](../../mise.toml), [mise 가이드](../../docs/references/tooling/mise.md).
- 문서 owner: `docs/skills/<asset>/`는 해당 자산과 함께 이관할 수 있는 maintainer knowledge. 실행 동작은 `SKILL.md`가 소유한다. [Asset Maintainer Documentation](../../docs/documentation/asset-maintainer-documentation.md).
- 설계 루프 방식: **mols-loops: Prepare → Research → Review → 재탐색 → Review → Finalize**. 연구 결과를 구현 사실로 과장하지 않는다.

## Research Loop 1 — 현재 구조 및 설계 선택

**Research.** 기존 Skill 초안은 setup / update, 허용 범위와 lock, 설치 scope, 부분 실패, 복구, 인계를 모두 다루지만 이름의 `env`와 함께 검토할 소유권·검증이 필요하다. 현재 `mise.toml`에는 `setup`만 있고 `update` 전용 task가 없다. 개발 CLI는 모두 exact pin; `uv sync --all-groups`, Rulesync frozen install, projection, external Skill installer, Lefthook install을 순서대로 실행한다. 이 경로가 안전한 부분 복구나 최신 허용 버전 선택을 이미 구현했다고 볼 수 없다.

**핵심 설계 후보 비교.**

| 대안 | 이점 | 비용·위험 | 판단 |
| --- | --- | --- | --- |
| mise/uv 전용 운영 스킬 | 즉시 구체적 | 다른 런타임/프로젝트에 의존 | 기각: portable Skill과 local repo 구현을 분리 |
| 모든 언어/OS installer를 추상화하는 프레임워크 | 공통 API처럼 보임 | 불필요한 schema, 권한 추측, 운영 복잡도 | 기각: native owner 우선 |
| 설계 판단 + 명시적 구현 인계 | 책임이 명확하고 도구 독립 | 현장 구현·검증을 따로 해야 함 | 채택 |
| setup 과 update를 하나의 암묵적 최신화로 통합 | 호출 수 감소 | 비의도적 변경·재현성 상실 | 기각 |

**Review 1.** 단순히 '스킬 이름을 바꾸는' 작업만으로는 다음 사용자에게 효용이 떨어진다. Portable activation, 위험 권한, 실패한 독립 작업의 판정, 스킬 문서의 owner를 지속적으로 설명할 필요가 있다. 다만 Skill 본문에 mise command, npm backend 세부사항을 주입하면 다시 도구 종속 자산이 된다. 이 trade-off는 유지보수 문서에서 rationale로 보존하고 Skill 본문은 최소한으로 유지한다.

## Research Loop 2 — 공식 semantics, 실패모드와 반증

**Research.** 최신 공식 문서 기준으로 repo-specific 제안을 공격적으로 점검한다.

1. **mise 관리 영역도 무조건 안전한 전역 설치는 아니다.** `mise run`은 기본적으로 필요한 도구를 task 전에 자동 설치한다(`task.run_auto_install` 기본 true); `--skip-tools` 또는 task 설정으로 제한할 수 있다. Tool manager cache는 OS package manager와 다르지만 사용자 공유 상태·디스크·네트워크에 영향을 준다. 따라서 'mise-managed 자동 설치 허용' 역시 설치 영역과 명시된 정책을 확인해야 한다. 근거: [mise dev tools](https://mise.jdx.dev/dev-tools/), [mise task run](https://mise.jdx.dev/cli/run.html).
2. **mise.lock은 정책 범위 자체가 아니다.** `mise lock --bump`는 `mise.toml` request가 허용하는 최신으로 lock을 갱신하고 request를 변경하지 않는다. Exact pin은 그대로이며 `mise upgrade --bump`는 request를 바꿀 수 있어 다르다. Locked install은 별도의 실행 단계이고 platform-specific URL/sidecar가 요구될 수 있다. 근거: [mise lockfile](https://mise.jdx.dev/dev-tools/mise-lock.html), [mise lock CLI](https://mise.jdx.dev/cli/lock.html).
3. **uv 기본 sync는 항상 순수 복구가 아니다.** `uv sync`/`uv run`은 lock를 갱신할 수 있고, `--locked`는 out-of-date lock에서 실패한다. `uv sync`는 lock에 없는 extraneous package를 지울 수 있다. `uv lock --upgrade`는 선언된 dependency constraints를 존중한다. 근거: [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).
4. **Python 자동 다운로드도 설치 side effect다.** uv는 필요한 Python을 자동 설치할 수 있으며, managed interpreter와 user PATH 노출 여부를 별개로 구분해야 한다. OS 전역 도구만 신경 쓰면 권한·네트워크 영향이 빠진다. 근거: [uv Python installation](https://docs.astral.sh/uv/guides/install-python/).
5. **Entry-point가 없는 상태는 self-bootstrap 불가능.** mise가 없으면 `mise run setup`이 실행되지 않는다. OS별 공식 설치 안내를 preflight 문서가 제공하고, 추가 wrapper가 실제로 이 문제를 줄이는지 입증하지 않는 한 이중 부트스트랩은 도입하지 않는다.
6. **사용자 공유 영역의 native installer는 별도 동의가 필요하다.** 현 `skills_sync.py`는 source-native install script를 호출하므로 단지 저장소 lock이 있다고 무인 실행까지 승인된 것은 아니다.
7. **도구별 source/update 범위가 다르다.** Git floating branch와 SemVer prefix를 같은 '허용 버전 범위'로 취급하면 무단 revision advance가 발생한다. 정해진 update policy가 없는 ref는 이동시키지 않아야 한다.

**Review 2 — 적용 판단.** Skill의 작업은 구체 CLI flag를 암기시키는 것이 아니라 lifecycle, manifest/lock ownership, 설치 권한, dependency graph, 성공/실패 표시를 **프로젝트 상황에서 결정하게 하는 것**이다. 기존 초안은 핵심을 갖췄으나 `mise-managed`의 무조건 자동 설치처럼 읽히지 않도록 portability boundary를 더 명확히 해야 한다. 공식 문서 링크와 도구별 세부 옵션은 이번 maintainer docs 또는 프로젝트 명세에만 두고 Skill에는 이식 가능한 판단 규칙만 남긴다.

## 재사용성 및 Activation 조사

- **Positive:** "새 저장소의 개발환경을 처음 설치하고 이후 지정된 major 범위 안에서 최신 도구를 업데이트하는 bootstrap을 설계해줘".
- **Positive:** "기존 setup script에서 설치되지 않은 Git을 skip하고 나머지를 복구하는 정책을 리뷰해줘".
- **Positive:** "mise가 아닌 asdf / pip / pnpm 환경에서 최초 setup과 update의 lock 경계를 설계해줘".
- **Near miss:** "uv.lock의 패키지 한 개만 올려줘" → 일반 의존성 작업; bootstrap lifecycle 설계 아님.
- **Near miss:** "CI PR Gate 필수 테스트 구성해줘" → CI 설계 owner.
- **Near miss:** "내 컴퓨터에 Node 설치해줘" → 일회 설치 작업; 설계 Skill 선택 불필요.
- **Out of scope:** Script를 실제 실행하지 않고 새로운 vendor-native command가 성공했다고 주장하거나, 권한 없이 system-wide 설치 수행.

## 결정과 잔여 불확실성

**결정.** 새로운 이름을 정확히 `mols-dev-env-bootstrap-design`으로 통일한다. Canonical `SKILL.md` 하나를 유지하고, 유지보수 근거는 `docs/skills/mols-dev-env-bootstrap-design/README.md`에 둔다. 별도 Skill reference는 지금 필요한 conditional loading benefit이 없어 보류한다. `route/skills.jsonl`은 source generator에서 파생되므로 함께 동기화한다. 이름을 남기는 compatibility alias는 필요하지 않다.

**불확실성.** 실제 사용자 PC, OS 별 자동 설치와 다양한 version-manager 동작은 테스트하지 않았다. Mise/uv 공식 문서는 현재 동작을 설명할 뿐 PR의 실제 실행 결과가 아니다. 사전 정의할 도구별 version 범위는 사용자·프로젝트의 후속 결정이며 Skill이 임의로 선택하지 않는다.

**연구 종료 기준.** 소유권, API/업데이트 경계, missing-tool 리스크, portable activation, maintainer docs 위치가 근거와 함께 정리되었다. 구현 순서·검증 방법은 별도의 **Plan Run**으로 인계한다.
