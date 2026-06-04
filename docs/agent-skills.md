# Agent Skills Management Guide

이 문서는 에이전트 스킬(Agent Skills)이 증가함에 따라 관리 복잡도를 완화하고 아키텍처를 단순화하기 위한 설계 및 구조화 가이드를 제공합니다.

## 배경 (Background)
에이전트가 사용하는 스킬들은 기본적으로 [.agents/skills](file:///m:/workspaces/mols-agent/.agents/skills) 디렉터리 내에 위치하며, 평탄한(Flat) 폴더 구조를 유지해야 합니다. 스킬의 개수가 증가하면 다음과 같은 문제가 발생할 수 있습니다.
- 스킬 디렉터리의 시각적 복잡도 증가
- 기능적 결합도가 높은 스킬 간의 중복 코드 발생
- 형상 관리(Git) 시 스킬 변경 추적의 어려움

---

## 스킬 관리 전략 (Management Strategies)

### 1. 스킬 병합 및 모듈화 (Skill Consolidation & Modularization)
서로 연관성이 높거나 동일한 도메인 영역을 다루는 스킬들은 하나의 스킬로 병합하고, 내부에서 모듈 단위로 기능을 분기하여 실행하도록 설계하십시오.

#### 구현 패턴 (Implementation Pattern)
- **대상 스킬 묶기**: `caveman`, `caveman-commit`, `caveman-compress` 등 유사한 목적의 스킬들을 하나의 디렉터리로 통합합니다.
- **구조 예시**:
  ```text
  .agents/skills/caveman-suite/
  ├── SKILL.md (전체 스킬 명세 및 공통 진입점 정의)
  └── scripts/ (개별 동작을 수행하는 세부 스크립트 배치)
      ├── commit-helper.js
      ├── compress-helper.js
      └── review-helper.js
  ```
- **권장 사항**: `SKILL.md`에서 사용자 입력 키워드 또는 인자(Arguments)를 기반으로 `scripts/` 내의 특정 서브스크립트를 호출하도록 라우팅을 명세하십시오.

### 2. 게이트웨이 / 허브 아키텍처 (Gateway / Hub Architecture)
에이전트 스킬 디렉터리([.agents/skills](file:///m:/workspaces/mols-agent/.agents/skills))에는 인터페이스 역할을 수행하는 단일 스킬만 노출하고, 실제 세부 로직 및 라이브러리들은 프로젝트 소스 디렉터리 내의 계층 구조 폴더에 분리 배치하여 로드하는 방식입니다.

#### 구현 패턴 (Implementation Pattern)
- **구조 예시**:
  ```text
  # 에이전트 스킬 진입점 (Flat 구조 유지)
  .agents/skills/
  └── mols-hub/
      └── SKILL.md (프로젝트 소스 내의 Dispatcher 스크립트 실행)

  # 실제 비즈니스 로직 및 스크립트 관리 (프로젝트 계층 구조 활용)
  src/skills/
  ├── comms/
  │   ├── caveman/
  │   └── cavecrew/
  └── dev-tools/
      └── create-skills/
  ```
- **권장 사항**: `mols-hub` 스킬이 실행되면 `src/skills/` 내부의 모듈들을 동적으로 로드하거나 파라미터에 따라 프로세스를 분기 실행하도록 구성하십시오. 이를 통해 에이전트 스킬 탐색 경로를 단순하게 유지하면서 계층적인 코드 관리가 가능해집니다.

---

## 신규 스킬 추가 체크리스트 (New Skill Checklist)
새로운 에이전트 기능이 필요할 때 다음 단계를 통해 추가 방식을 결정하십시오.

1. **도메인 분석**: 신규 기능이 기존에 존재하는 스킬 도메인(예: caveman, cavecrew 등)에 포함되는지 검토하십시오.
2. **스킬 분할 여부 결정**:
   - 기존 도메인에 해당할 경우: 신규 스킬 폴더를 생성하지 않고, 기존 스킬의 서브 모듈이나 파라미터 옵션으로 기능을 통합하십시오.
   - 새로운 독립 도메인일 경우: 단일 스킬 폴더로 추가하거나 [create-skills](file:///m:/workspaces/mols-agent/.agents/skills/create-skills/SKILL.md) 템플릿을 사용하여 표준 구조를 생성하십시오.
3. **인터페이스 최소화**: 스킬 디렉터리 내의 `SKILL.md`는 에이전트 인터페이스(Prompt 및 YAML Metadata) 정의에만 집중하고, 로직 코드는 최대한 별도의 스크립트 파일로 격리하십시오.
