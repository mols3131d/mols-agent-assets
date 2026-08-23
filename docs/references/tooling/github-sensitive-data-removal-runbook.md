---
description: GitHub repository에 노출된 회전·폐기 불가능한 민감정보를 Git history rewrite, GitHub 저장면 정리, fork/clone 대응과 Support purge까지 최대한 제거할 때 사용하는 재사용 런북입니다.
---

# GitHub에 노출된 회전 불가능한 민감정보 최대 제거 런북

> **검증 기준:** GitHub.com 및 `git-filter-repo` 공식 문서, 2026-08-23 확인
>
> **목적:** GitHub repository에 실수로 올라간 **회전·폐기할 수 없는 민감정보**를 가능한 범위에서 최대한 제거한다.
>
> 이 런북은 새 commit에서 파일을 지우는 수준이 아니라 **확산 중단 → Git history rewrite → GitHub ref 교체 → 별도 저장면 정리 → fork/clone 대응 → 필요 시 GitHub Support purge**까지 다룬다.

## 먼저 결론

회전할 수 없는 민감정보라면 **`git-filter-repo`로 history를 다시 쓰고 원격 ref를 교체하는 것이 최소선**이다. 하지만 이것만으로 GitHub에서 완전히 사라졌다고 볼 수는 없다.

GitHub는 history rewrite 후에도 민감 commit이 다음 위치에 남을 수 있다고 설명한다.[^gh-remove]

- 다른 clone
- fork
- 과거 commit SHA를 통한 cached view
- Pull Request가 보존하는 internal ref

따라서 완료 상태는 두 단계로 구분한다.

| 목표 | 완료 기준 |
| --- | --- |
| **Owner-controlled cleanup** | 내가 통제할 수 있는 Git ref, GitHub 저장면, known fork/clone을 정리한다. |
| **GitHub-side purge** | non-PR ref와 fork reference를 먼저 정리한 뒤, GitHub Support가 지원 대상으로 판단하면 affected PR ref, cached view, server-side object, 필요 시 orphaned LFS object까지 정리한다.[^gh-remove] |

> [!IMPORTANT]
> GitHub Support는 non-sensitive data를 제거하지 않으며, **affected credential을 회전하는 것만으로 위험을 완화할 수 없다고 판단한 sensitive data**에 한해 제거를 지원한다.[^gh-remove]
> 이 런북은 회전·폐기할 수 없는 민감정보를 대상으로 하므로 이 조건과 직접 관련되지만, Support의 처리 여부와 범위는 GitHub가 결정한다.
>
> Support를 이용하지 않는 선택은 가능하다. 다만 그 상태를 **“GitHub에서 완전히 삭제됨”**이라고 표현하면 안 된다.

---

## 바로 실행할 순서

급하면 아래 순서부터 따른다.

1. **push / merge / 자동 push를 멈춘다.**
1. public repository라면 **private 전환을 containment 수단으로 검토**한다.
1. 최초 visibility, 접근자, fork, clone, PR/Actions/Pages/Release 등 **복제면을 분류**한다.
1. **fresh clone**에서 `git-filter-repo >= 2.47`로 history를 rewrite한다.
1. `changed-refs`, affected PR, First Changed Commit(s), LFS 상태를 확인한다.
1. force push를 막는 Ruleset/Branch Protection만 잠시 조정한다.
1. `git push --force --mirror origin`으로 원격 ref를 교체한다.
1. `refs/pull/*` 외의 ref가 정상 갱신됐는지 확인하고 **보호 설정을 즉시 복구**한다.
1. Actions, Pages, Releases, PR/Issue text, fork, 기존 clone을 별도로 정리한다.
1. PR internal ref나 cached view까지 제거해야 하면 **GitHub Support purge**를 요청한다.

> [!CAUTION]
> cleanup 과정에서 민감정보 원문을 shell command, Issue/PR, 문서, Support ticket에 불필요하게 다시 복사하지 않는다.

---

## 1. 먼저 사고 범위를 판정한다

현재 visibility 하나만 보면 부족하다. 다음 네 축을 각각 확인한다.

| 축 | 낮은 확산 가능성 | 높은 확산 가능성 |
| --- | --- | --- |
| **Visibility history** | 생성 이후 계속 private | 현재 또는 과거 어느 시점이든 public |
| **GitHub access** | owner only | collaborator, team, outside collaborator 등 존재 |
| **Fork** | 없음 | private fork 또는 과거 public fork 존재 |
| **Clone** | 내가 통제하는 clone만 존재 | 다른 사람, CI runner, VM, 장기 workspace 등에 존재 |

같은 private repository라도 collaborator가 clone을 받아갔다면 **GitHub 밖 사본은 이미 존재한다.**

### 케이스별 대응 강도

| 케이스 | 핵심 위험 | 기본 대응 |
| --- | --- | --- |
| **A. 처음부터 private + owner only + fork 없음 + 내 clone만 있음** | 외부 확산 가능성이 가장 낮음 | history rewrite + 원격 교체 + 내 clone/별도 저장면 정리 |
| **B. 처음부터 private + collaborator 접근 있음** | 접근자의 local clone | A + 과거/현재 접근자와 clone 추적 |
| **C. 처음부터 private + private fork 있음** | 별도 Git repository copy | upstream + fork + fork owner clone 정리 |
| **D. 과거 public → 현재 private** | unknown clone/download + 과거 public fork | public 노출을 전제로 대응 |
| **E. public 상태에서 fork 존재** | 원본 cleanup 후에도 fork에서 접근 가능 | 원본 + 모든 known fork 정리 |
| **F. private지만 여러 clone/CI workspace 존재** | GitHub 밖 object database | 모든 known clone/workspace 정리 |
| **G. private지만 PR/Actions/Pages/Release에 복제됨** | Git history 밖 별도 저장면 | 각 저장면을 별도로 정리 |

### Case A는 언제 Support 없이 끝내기 쉬운가

다음이 모두 맞으면 owner-controlled cleanup에서 종료하는 선택이 비교적 합리적이다.

- repository가 생성 이후 계속 private이었다.
- 다른 사용자나 team에게 접근 권한을 준 적이 없다.
- fork가 없다.
- 다른 사람이 clone한 적이 없다.
- Actions/Pages/Releases/PR 등 별도 복제면을 확인했다.
- GitHub cached view나 PR internal ref까지 서버 측에서 제거해야 한다는 요구가 없다.

Private repository는 기본적으로 허가된 사용자만 접근할 수 있으므로, 이런 경우 public repository보다 외부 확산 가능성이 낮다.[^gh-repo-visibility]

다만 **private이었다는 사실은 history cleanup을 생략해도 된다는 뜻이 아니다.**

### Case B/C에서 중요한 점

Private repository의 접근 권한을 제거해도 **이미 만들어진 local clone은 사라지지 않는다.** Private fork는 접근권한 변화에 따라 삭제될 수 있지만 local clone은 별도다.[^gh-forks]

즉:

```text
GitHub access 제거
≠
상대방 PC의 clone 삭제
```

### Case D/E에서 중요한 점

현재 private이라도 **한 번이라도 public이었다면 public 노출 이력이 더 중요하다.**

GitHub는 public repository를 private으로 전환할 때 기존 public fork를 upstream에서 분리해 public repository network로 남길 수 있다고 설명한다.[^gh-visibility-change]

따라서:

```text
public → private
≠
과거 공개 사본 회수
```

Known fork가 없어도 public 기간 동안의 unknown clone/download 가능성은 잔존 위험으로 남긴다.

### 빠른 의사결정

```text
처음부터 private?
├─ Yes
│  ├─ owner only?
│  │  ├─ Yes
│  │  │  ├─ fork/외부 clone/별도 저장면 없음 → Case A
│  │  │  └─ 하나라도 있음 → Case C/F/G 추가
│  │  └─ No → Case B
│  └─ private fork 있음 → Case C
└─ No: 한 번이라도 public
   ├─ known fork 있음 → Case E
   └─ known fork 없음 → Case D
```

---

## 2. 추가 확산을 먼저 멈춘다

History rewrite 전에 repository를 가능한 한 정지 상태로 만든다.

- 새 push와 merge 중단
- 자동 commit/push를 수행하는 bot/workflow 일시 중단
- 협업자에게 cleanup 완료 전까지 기존 clone에서 push하지 않도록 알림
- 가능하면 open PR을 먼저 merge 또는 close
- public repository라면 private 전환을 containment 수단으로 검토

GitHub는 history rewrite가 commit SHA를 바꾸기 때문에 open PR의 diff와 review가 깨지거나 혼란을 줄 수 있어, 가능하면 먼저 정리할 것을 권장한다.[^gh-remove]

### Public → Private는 containment이다

Private 전환은 **추가 노출을 줄이는 수단**이지 기존 흔적을 지우는 수단이 아니다.

Public fork, clone, cached view는 별도로 다뤄야 한다.[^gh-visibility-change]

### Repository 삭제 후 재생성도 purge가 아니다

Repository 삭제 역시 완전 삭제 수단으로 보지 않는다.

GitHub의 삭제된 repository는 조건에 따라 복구할 수 있고, public repository를 삭제해도 public fork가 자동 삭제되는 것은 아니다.[^gh-restore][^gh-delete]

---

## 3. 민감정보가 어디에 복제됐는지 분류한다

Git file content만 확인하면 부족하다.

| 노출 위치 | 예 | 주 제거 수단 |
| --- | --- | --- |
| Git blob | 파일 본문 | `--invert-paths`, `--replace-text` |
| Git path | filename / directory name | `--path-rename`, `--paths-from-file` |
| Commit / tag message | commit message의 민감 문자열 | `--replace-message` |
| Author / committer metadata | name, email | `--mailmap` 또는 callback |
| Git LFS | LFS object | history rewrite + local orphan cleanup + 필요 시 GitHub remote LFS purge |
| Branch / tag / ref | 과거 commit을 가리키는 ref | 전체 ref rewrite + mirror push |
| Pull Request internal ref | `refs/pull/*` | 일반 push로 제거 불가 |
| GitHub cached view | 과거 SHA 직접 접근 | Support 영역 |
| Fork | 다른 repository copy | fork cleanup/delete |
| Clone | PC, VM, runner workspace | 폐기/re-clone 또는 별도 cleanup |
| Actions log / summary | CI 출력 | log/run 삭제 |
| Actions artifact | 업로드된 파일 | artifact/run 삭제 |
| Actions cache | build/cache copy | cache 삭제 |
| GitHub Pages | publish된 정적 사이트 | unpublish/delete + source cleanup |
| Release asset | 배포 파일 | asset/release 삭제 |
| PR / Issue text | body/comment에 붙여넣은 값 | 직접 편집/삭제 |

---

## 4. Fresh clone과 도구를 준비한다

GitHub는 `--sensitive-data-removal`을 지원하는 **`git-filter-repo >= 2.47`**을 요구한다.[^gh-remove]

`git-filter-repo` upstream의 현재 요구사항은 **Git >= 2.36.0, Python >= 3.6**이다.[^filter-repo-readme]

확인:

```bash
git --version
python3 --version
git filter-repo --version
```

`uv`를 사용한다면 upstream이 안내하는 설치 방식 중 하나는 다음과 같다.[^filter-repo-install]

```bash
uv tool install git-filter-repo
```

### 반드시 fresh clone에서 시작한다

```bash
git clone https://github.com/OWNER/REPOSITORY.git cleanup-repository
cd cleanup-repository
```

`git-filter-repo`는 파괴적인 history rewrite를 보호하기 위해 fresh-clone safety check를 사용한다.[^filter-repo-manual]

> [!CAUTION]
> 특별한 이유 없이 `--force`로 fresh-clone check를 우회하지 않는다.

과거 path와 rename 범위가 불명확하면 rewrite 전에 선택적으로 분석한다.

```bash
git filter-repo --analyze
```

`--analyze`는 과거 path, rename과 object size 보고서를 만들어 filter 범위를 정하는 데 도움을 준다. 분석 자체를 필수 의식으로 만들지는 않는다.[^filter-repo-manual]

### `--sensitive-data-removal`을 기본으로 사용한다

이 모드는 단순 표시용 flag가 아니다. `git-filter-repo`는 민감정보 제거에 필요한 추가 정보를 수집한다.[^filter-repo-manual]

- origin의 여러 ref 확보
- First Changed Commit(s) 추적
- orphaned LFS object 추적
- 다른 copy cleanup에 필요한 정보 생성

Rewrite 후 `.git/filter-repo/`의 다음 파일을 cleanup evidence로 보존한다.[^filter-repo-manual]

```text
changed-refs
first-changed-commits  # original → rewritten mapping
orphaned_lfs_objects   # LFS orphan이 있을 때
```

### 최대 제거 목적이면 `--no-fetch`를 피한다

`--no-fetch`를 사용하면 필요한 ref를 확보하지 못할 수 있다.

Upstream은 ref coverage가 불완전한 상태에서 `--mirror`를 사용하면 예상하지 않은 server ref를 삭제하거나, 반대로 민감 history를 가진 ref를 놓칠 수 있다고 경고한다.[^filter-repo-manual]

---

## 5. 노출 유형에 맞게 history를 rewrite한다

### 파일 전체를 제거

파일 자체가 필요 없다면 가장 단순하다.

```bash
git filter-repo \
  --sensitive-data-removal \
  --invert-paths \
  --path path/to/sensitive-file
```

과거에 rename/move된 적이 있다면 **모든 과거 경로를 명시**한다.

```bash
git filter-repo \
  --sensitive-data-removal \
  --invert-paths \
  --path old/path/private.json \
  --path new/path/private.json
```

`git-filter-repo`가 rename history를 자동으로 추적해 모든 과거 이름을 제거해주는 것으로 가정하면 안 된다.[^filter-repo-manual]

> [!WARNING]
> `--invert-paths`는 과거 버전뿐 아니라 현재 history에서도 해당 파일을 제거한다. Sanitized 버전이 필요하면 rewrite 후 깨끗한 파일을 다시 추가한다.

### 파일은 유지하고 일부 내용만 제거

Replacement file은 repository **밖**에 둔다.

```text
../sensitive-values.txt
```

```bash
git filter-repo \
  --sensitive-data-removal \
  --replace-text ../sensitive-values.txt
```

`--replace-text`는 literal, `regex:`, `glob:` 표현을 지원한다.[^filter-repo-manual]

개념 예:

```text
literal:VALUE_TO_REMOVE
regex:PATTERN_TO_REMOVE==>REDACTED
```

민감값 자체를 shell argument에 직접 넣지 않는 편이 안전하다.

### Commit / tag message에 들어간 경우

```bash
git filter-repo \
  --sensitive-data-removal \
  --replace-message ../sensitive-messages.txt
```

`--replace-message`는 `--replace-text`와 같은 expression file 문법을 사용한다.[^filter-repo-manual]

### Filename / directory path 자체가 민감한 경우

```bash
git filter-repo \
  --sensitive-data-removal \
  --path-rename old/private-path/:safe-path/
```

민감 path를 shell history에 남기지 않으려면 repository 밖의 파일과 `--paths-from-file`을 사용할 수 있다.

```text
literal:old/private-path/==>safe-path/
```

```bash
git filter-repo \
  --sensitive-data-removal \
  --paths-from-file ../path-rewrites.txt
```

### Author / committer / tagger metadata가 민감한 경우

`--mailmap`, `--name-callback`, `--email-callback` 등으로 metadata를 rewrite할 수 있다.[^filter-repo-manual]

이 경우 영향 범위가 넓어질 수 있으므로 별도 fresh clone에서 먼저 실험하고, 예상한 identity만 바뀌는지 확인한 뒤 원격에 반영한다.

### Git LFS가 있다면

`--sensitive-data-removal`은 rewrite 전후 LFS reference를 비교해 orphaned object가 생겼는지 기록한다.[^filter-repo-manual]

다음 메시지가 보이면 기록한다.

```text
NOTE: There were LFS Objects Orphaned by this rewrite
```

Local clone에 해당 orphaned LFS object가 남아 있다면 `.git/lfs/objects/`에서도 제거한다.[^filter-repo-manual]

> [!IMPORTANT]
> Git history에서 LFS reference를 제거해도 **GitHub remote LFS object는 그대로 남을 수 있다.** GitHub는 repository 삭제·재생성 또는 Support 문의를 remote LFS object 제거 경로로 안내한다.[^gh-lfs-remove]
> 이 런북에서는 repository 전체 삭제를 일반 purge 수단으로 취급하지 않으므로, 유지할 repository의 orphaned LFS purge는 Support에 요청하는 것을 우선한다.

Support를 이용할 경우 orphaned LFS 정보를 함께 제공한다.[^gh-remove]

---

## 6. Force push 전에 검증한다

여기까지는 문제가 있으면 cleanup clone을 버리고 다시 시작하기 쉽다.

### 제거 대상 확인

```bash
git log --all --name-status -- path/to/sensitive-file
```

과거 경로가 있었다면 각각 확인한다.

현재 tree도 확인한다.

```bash
git status
git ls-files
```

Project의 deterministic test가 있다면 현재 tree에 대해 실행한다.

### 변경된 ref와 affected PR 확인

```bash
cat .git/filter-repo/changed-refs
```

Affected PR 개수:

```bash
grep -c '^refs/pull/.*/head$' .git/filter-repo/changed-refs
```

Affected PR 목록:

```bash
grep '^refs/pull/.*/head$' .git/filter-repo/changed-refs
```

예상보다 영향 범위가 크면 **아직 push하지 않는다.**

### First Changed Commit(s)를 기록한다

GitHub Support는 `git-filter-repo`가 `NOTE: First Changed Commit(s)`로 보고한 **원래 commit SHA**를 요구한다.[^gh-remove] 해당 값을 기록하고, 원본 commit과 rewrite 결과의 대응을 보존하는 mapping도 함께 남긴다.[^filter-repo-manual]

```bash
cat .git/filter-repo/first-changed-commits
```

LFS orphan이 보고됐다면 다음 파일도 보존한다.

```bash
cat .git/filter-repo/orphaned_lfs_objects
```

GitHub Support에 LFS orphan을 알리고, `git-filter-repo`가 지목한 이 파일을 ticket에 첨부한다.[^gh-remove]

### 옛 object가 남았는지 확인한다

```bash
git cat-file -t OLD_FIRST_CHANGED_COMMIT_SHA
```

정상적으로 제거됐다면 해당 object를 찾지 못하는 fatal error가 나와야 한다.[^filter-repo-manual]

`commit`이 반환되면 **아직 제거되지 않은 것**으로 취급하고 push하지 않는다. Reflog 정리와 garbage collection을 수행한 상태라면 다음 명령으로 old commit을 붙잡고 있는 branch/ref를 찾을 수 있다.[^filter-repo-manual]

```bash
git for-each-ref --contains OLD_FIRST_CHANGED_COMMIT_SHA
```

First Changed Commit이 여러 개면 각각 `git cat-file -t`가 fatal error를 반환해야 한다.

---

## 7. GitHub 보호를 최소 범위로 잠시 조정한다

Force push를 막는 Ruleset/Branch Protection이 있다면 rewrite를 반영하는 동안만 최소 범위로 조정한다.[^gh-remove]

예를 들어:

```json
{
  "type": "non_fast_forward"
}
```

는 force push를 막는다.

원칙:

1. 현재 보호 설정을 기록한다.
1. cleanup push를 막는 규칙만 임시 조정한다.
1. 일반 개발 작업은 계속 중단한다.
1. 원격 history를 교체한다.
1. 즉시 보호 설정을 복구한다.

여러 Ruleset이나 branch protection이 겹칠 수 있으므로 한 규칙만 바꿨는데 계속 막히면 다른 active rule도 확인한다.

---

## 8. Rewritten history를 GitHub에 반영한다

먼저 remote를 확인한다.

```bash
git remote -v
```

`git-filter-repo`는 old/new history가 실수로 섞이는 것을 막기 위해 `origin`을 제거할 수 있다.[^filter-repo-manual]

`origin`이 없다면 **정확한 원래 repository인지 다시 확인한 뒤** 추가한다.

```bash
git remote add origin https://github.com/OWNER/REPOSITORY.git
```

그다음:

```bash
git push --force --mirror origin
```

GitHub와 `git-filter-repo` upstream 모두 sensitive-data removal에서 전체 ref를 갱신하기 위해 이 방식을 안내한다.[^gh-remove][^filter-repo-manual]

> [!CAUTION]
> `--mirror`는 branch와 tag 등 server ref를 강제로 맞추는 강한 작업이다. Cleanup 시작 이후 다른 사람이 올린 변경이 있다면 덮어쓸 수 있다.

### 성공 판정

GitHub의 `refs/pull/*`은 read-only이므로 해당 ref의 push 실패는 예상될 수 있다.[^gh-remove]

이상적인 상태:

```text
일반 branch/tag/ref → 업데이트 성공
refs/pull/*        → read-only로 실패
```

`refs/pull/*` 외의 ref도 실패한다면 Ruleset, branch protection, 권한, ref restriction을 확인한다.

---

## 9. GitHub 보호를 즉시 복구한다

Force push 직후 다음을 되돌린다.

- `non_fast_forward`
- PR requirement
- required status checks
- 임시 bypass
- cleanup 때문에 낮춘 다른 repository protection

Cleanup 완료와 보호 복구는 하나의 작업으로 취급한다.

---

## 10. Git history 밖의 GitHub 저장면을 정리한다

History rewrite는 GitHub의 다른 저장면을 자동으로 정리하지 않는다.

### Actions logs / job summary

Workflow가 민감정보를 stdout/stderr에 출력했을 가능성을 확인한다.

특히:

- debug output
- `cat` / `print`
- test failure
- generated summary
- path/value echo

GitHub는 workflow run log를 별도로 삭제할 수 있다.[^gh-actions-logs]

이미 업로드된 Job summary는 이후 step에서 수정할 수 없다. 민감정보가 들어간 summary를 제거해야 한다면 **workflow run 전체를 삭제**한다.[^gh-actions-summary]

### Workflow artifacts

Affected run이 파일을 artifact로 업로드했다면 별도로 삭제한다.

Workflow run 자체를 삭제하면 그 run의 artifact도 함께 정리할 수 있다.[^gh-actions-artifacts]

### Actions cache

Build/cache에 repository content가 들어갔을 가능성이 있다면 Actions의 cache 목록에서 관련 entry를 확인하고 삭제한다. Cache는 workflow run 삭제와 별도로 관리한다.[^gh-actions-cache]

### GitHub Pages

Pages가 있었다면 repository visibility와 별도로 본다.

민감정보가 publish됐을 가능성이 있다면:

1. site unpublish
1. source/history cleanup
1. 필요 시 Pages site 삭제
1. custom domain과 외부 cache 확인

Unpublish는 현재 deployment를 내리는 것이며 site 자체의 모든 흔적을 지우는 것과는 다르다.[^gh-pages-unpublish]

### Release / Release asset

Release asset은 Git object와 별도 저장면이다. 민감 파일이 올라갔다면 asset 또는 release를 별도로 삭제한다.[^gh-release-assets]

### PR / Issue text

민감정보가 PR description, Issue body, review comment 등에 복사됐다면 history rewrite가 건드리지 않는다. 해당 text를 직접 편집/삭제한다.

---

## 11. Fork와 clone을 별도로 정리한다

### Fork

민감 commit이 fork에 남으면 원본 repository를 정리해도 그 fork에서 계속 접근할 수 있다.[^gh-remove]

#### Private fork

Private repository의 fork owner가 아직 접근권한을 가지고 있다면:

```text
upstream cleanup
→ fork history cleanup 또는 fork 삭제
→ fork owner local clone cleanup
```

개인의 private repository 접근권한을 제거하면 그 사용자의 해당 private fork는 삭제되지만, **local clone은 유지된다.** Team access를 제거한 경우에도 사용자가 다른 경로로 접근권한을 갖지 않으면 private fork가 삭제된다.[^gh-forks]

#### Public fork

Repository가 한 번이라도 public이었다면 기존 public fork를 조사한다.

Public → Private 전환은 기존 public fork를 회수하지 않는다.[^gh-visibility-change]

Known fork가 민감 commit을 보존하면 fork owner에게 history cleanup 또는 삭제를 요청한다.

GitHub Support의 server-side cleanup도 **민감 commit을 참조하는 fork가 남아 있지 않은 상태**를 전제로 한다.[^gh-remove]

### Clone

가장 단순하고 안전한 방법은:

```text
기존 clone 폐기
→ cleanup된 repository를 새로 clone
```

이다.[^filter-repo-manual]

대상에는 다음이 포함될 수 있다.

- 데스크톱 / 노트북
- WSL의 별도 clone
- 개발 VM
- self-hosted runner workspace
- persistent CI volume
- collaborator PC

기존 clone을 유지해야 한다면 **같은 `git-filter-repo` 명령을 각 clone에서 다시 실행하는 방식도 기본값으로 삼지 않는다.** 같은 filter라도 서로 다른 rewritten hash가 생길 수 있다.[^filter-repo-manual]

Upstream이 안내하는 clone cleanup의 핵심은 다음과 같다.[^filter-repo-manual]

1. 기존 tag를 삭제하고 `git fetch --prune --tags`로 cleaned server 상태를 다시 받는다.
1. 보존해야 할 local branch/ref 변경은 **새 history 위로 rebase**한다. Old history와 merge하지 않는다.
1. 필요하면 stash까지 포함한 reflog가 사라진다는 영향을 이해한 뒤 `git reflog expire --expire=now --all`과 `git gc --prune=now`로 pre-rewrite object를 정리한다.
1. 모든 First Changed Commit에 대해 다음 검증이 fatal error를 반환하는지 확인한다.

```bash
git cat-file -t OLD_FIRST_CHANGED_COMMIT_SHA
```

옛 clone에서 단순 `git pull && git push`하거나 old history를 merge하면 제거한 history가 다시 들어올 수 있다.[^gh-remove][^filter-repo-manual]

---

## 12. Support 없이 어디까지 끝냈다고 볼 수 있는가

다음이 모두 끝났다면 repository owner가 직접 할 수 있는 범위에서는 강한 cleanup이다.

- 모든 일반 branch/tag/ref rewrite 완료
- 현재 tree에서 민감정보 제거 확인
- old First Changed Commit object 제거 확인
- Ruleset/Branch Protection 복구
- Actions/Pages/Releases/PR/Issue text 확인
- known fork 정리
- known clone 재오염 방지

하지만 다음은 여전히 남을 수 있다.

```text
refs/pull/*
GitHub cached commit views
GitHub server-side unreachable objects
제3자가 이미 보유한 clone/download
외부 archive/cache
```

따라서 Support를 이용하지 않았다면 최종 상태는 다음처럼 기록하는 것이 정확하다.

> **Owner-controlled cleanup complete — 알려진 일반 ref와 직접 통제 가능한 복제면을 정리했으나 GitHub server-side purge는 수행하지 않음.**

---

## 13. GitHub Support를 사용할 기준

> [!IMPORTANT]
> GitHub Support는 non-sensitive data를 제거하지 않으며, credential rotation으로 위험을 완화할 수 없다고 판단한 sensitive data에 한해 제거를 지원한다.[^gh-remove]
> Support가 server-side purge를 진행하려면 **PR을 제외한 ref가 정리되어 있고, 어떤 fork도 민감정보를 참조하지 않아야 한다.**[^gh-remove]

다음 중 하나라면 Support 요청 가치가 높다.

- 정보가 회전·폐기 불가능하다.
- 개인 식별정보처럼 장기적인 위험이 있다.
- 과거 SHA URL의 cached view가 계속 보인다.
- affected PR internal ref가 sensitive commit을 보존한다.
- GitHub server storage에서도 최대한 제거해야 한다.
- orphaned LFS object가 있다.

GitHub 공식 절차에서 준비하는 정보:[^gh-remove]

```text
Repository: OWNER/REPOSITORY
Affected PR count: <count>
First Changed Commit(s): <git-filter-repo output>
Orphaned LFS objects: <있다면 .git/filter-repo/orphaned_lfs_objects 파일>
```

GitHub가 조건을 확인한 뒤 수행할 수 있는 작업:[^gh-remove]

- affected PR reference dereference/delete
- server-side garbage collection
- cached view 제거
- orphaned LFS object purge

회전 불가능한 정보라는 사실은 Support 판단에서 중요한 맥락이 될 수 있지만, 최종 처리 범위는 GitHub가 결정한다.

---

## 14. Private Information Removal은 별도 경로다

일반 sensitive-data cleanup Support와 **Private Information Removal Request**는 같은 절차가 아니다.

다음처럼 공개 상태 자체가 구체적인 보안 위험을 만드는 정보라면 별도 경로를 검토한다.[^gh-private-info]

- government identification number
- identity theft 위험을 만드는 개인정보
- 구체적인 physical/network security risk를 만드는 confidential information

GitHub는 request에 대체로 다음과 같은 구체성을 요구한다.[^gh-private-info]

1. 민감정보가 있는 file의 직접 링크
1. 정확한 line number
1. 구체적인 security risk 설명
1. 대리인이라면 대리 권한 설명
1. 긴급한 경우 urgency 설명

Fork가 문제라면 해당 fork도 명시적으로 식별한다.

---

## 15. 하지 말아야 할 것

| 하지 말 것 | 이유 |
| --- | --- |
| 새 commit에서 파일만 삭제 | 과거 Git history에는 그대로 남음 |
| `git revert`로 종료 | 이전 object를 삭제하지 않고 반대 변경을 추가할 뿐임 |
| Private 전환만 하고 종료 | 기존 fork/clone/cache를 제거하지 않음 |
| Repository 삭제 후 재생성을 purge로 간주 | 삭제 repository 복구 가능성과 public fork 잔존 가능성이 있음 |
| 일반 개발 clone에서 `--force`로 fresh-clone check 우회 | 불필요한 local data loss 위험 증가 |
| 최대 cleanup인데 습관적으로 `--no-fetch` 사용 | ref coverage 누락 또는 mirror 부작용 가능 |
| Cleanup 중 다른 사람의 push 허용 | 최종 mirror push가 변경을 덮거나 오염 history가 재유입될 수 있음 |
| 옛 clone history를 merge | 제거한 history를 다시 살릴 수 있음 |
| 민감 원문을 Support ticket에 과도하게 복사 | 새로운 복제면을 만들 수 있음 |

---

## 16. 완료 체크리스트

### Owner-controlled cleanup

- [ ] push / merge / 자동 push를 중단했다.
- [ ] visibility history와 과거 접근자를 확인했다.
- [ ] fork와 known clone을 확인했다.
- [ ] Actions / Pages / Releases / PR 등 별도 저장면을 확인했다.
- [ ] fresh clone에서 작업했다.
- [ ] Git 및 `git-filter-repo` 버전을 확인했다.
- [ ] `--sensitive-data-removal`을 사용했다.
- [ ] 과거 rename path까지 포함해 올바른 rewrite 방식을 적용했다.
- [ ] `changed-refs`, affected PR, First Changed Commit(s), LFS 상태를 확인했다.
- [ ] force push 전 현재 tree와 제거 결과를 검증했다.
- [ ] 필요한 GitHub protection만 임시 조정했다.
- [ ] `git push --force --mirror origin`을 완료했다.
- [ ] `refs/pull/*` 외의 ref update 실패가 없는지 확인했다.
- [ ] Ruleset / Branch Protection을 즉시 복구했다.
- [ ] Actions logs/artifacts/cache를 확인했다.
- [ ] Pages / Release / PR / Issue text를 확인했다.
- [ ] known fork를 정리했다.
- [ ] known clone을 폐기/re-clone하거나 안전하게 cleanup했다.
- [ ] old First Changed Commit SHA가 cleaned clone에 남지 않았는지 확인했다.
- [ ] orphaned LFS가 있다면 통제하는 local clone의 해당 object를 정리했다.

### GitHub-side purge까지 완료

- [ ] Owner-controlled cleanup을 완료했다.
- [ ] PR을 제외한 ref에서 민감 commit reference를 제거했다.
- [ ] 민감 commit을 참조하는 fork가 남아 있지 않다.
- [ ] GitHub Support에 affected PR count를 제공했다.
- [ ] `git-filter-repo`가 보고한 원래 First Changed Commit(s)를 제공했다.
- [ ] orphaned LFS가 있다면 `.git/filter-repo/orphaned_lfs_objects`를 제공했다.
- [ ] affected PR ref 처리 여부를 확인했다.
- [ ] cached view 제거 여부를 확인했다.
- [ ] server-side GC 처리 여부를 확인했다.
- [ ] 필요한 경우 Private Information Removal 경로도 처리했다.

---

## 17. 최종 상태 기록 예시

### Support를 사용하지 않은 경우

```text
Status: owner-controlled cleanup complete

- Git history rewritten
- Normal branches/tags/refs replaced
- Repository protections restored
- GitHub Actions / Pages / Releases checked
- Known forks and clones checked
- No known owner-controlled copy retains the sensitive data

Residual risk:
- GitHub PR internal refs or cached views may still retain historical objects
- Orphaned GitHub remote LFS objects may remain if applicable
- Unknown third-party clones or external caches cannot be revoked
- GitHub server-side purge was not requested
```

### GitHub Support purge까지 끝난 경우

```text
Status: GitHub-side cleanup completed

- Owner-controlled cleanup complete
- Affected PR references handled by GitHub
- GitHub cached views removed
- GitHub server-side garbage collection completed
- LFS purge completed if applicable

Residual risk:
- Copies already downloaded or retained by third parties remain outside GitHub's control
- External archives, mirrors, screenshots, or caches require separate remediation
```

---

## References

[^gh-remove]: GitHub Docs, **Removing sensitive data from a repository**.  
    <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository>

[^gh-repo-visibility]: GitHub Docs, **About repositories**.  
    <https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories>

[^gh-forks]: GitHub Docs, **Forks**.  
    <https://docs.github.com/en/enterprise-cloud@latest/pull-requests/reference/forks>

[^gh-visibility-change]: GitHub Docs, **Setting repository visibility**.  
    <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility>

[^gh-restore]: GitHub Docs, **Restoring a deleted repository**.  
    <https://docs.github.com/en/repositories/creating-and-managing-repositories/restoring-a-deleted-repository>

[^gh-delete]: GitHub Docs, **Deleting a repository**.  
    <https://docs.github.com/en/repositories/creating-and-managing-repositories/deleting-a-repository>

[^filter-repo-readme]: `newren/git-filter-repo`, **README — Prerequisites**.  
    <https://github.com/newren/git-filter-repo>

[^filter-repo-install]: `newren/git-filter-repo`, **INSTALL.md**.  
    <https://github.com/newren/git-filter-repo/blob/main/INSTALL.md>

[^filter-repo-manual]: `newren/git-filter-repo`, **git-filter-repo manual source**.  
    <https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt>

[^gh-lfs-remove]: GitHub Docs, **Removing files from Git Large File Storage**.  
    <https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage>

[^gh-actions-logs]: GitHub Docs, **Using workflow run logs**.  
    <https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs>

[^gh-actions-summary]: GitHub Docs, **Workflow commands for GitHub Actions**.  
    <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands>

[^gh-actions-artifacts]: GitHub Docs, **Removing workflow artifacts** and **Workflow artifacts**.  
    <https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts>  
    <https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts>

[^gh-actions-cache]: GitHub Docs, **Managing caches**.  
    <https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manage-caches>

[^gh-pages-unpublish]: GitHub Docs, **Unpublishing a GitHub Pages site** and **Deleting a GitHub Pages site**.  
    <https://docs.github.com/en/pages/getting-started-with-github-pages/unpublishing-a-github-pages-site>  
    <https://docs.github.com/en/pages/getting-started-with-github-pages/deleting-a-github-pages-site>

[^gh-release-assets]: GitHub Docs, **REST API endpoints for release assets**.  
    <https://docs.github.com/en/rest/releases/assets>

[^gh-private-info]: GitHub Docs, **GitHub Private Information Removal Policy**.  
    <https://docs.github.com/en/site-policy/content-removal-policies/github-private-information-removal-policy>
