# Scripts and Automation

## 종류

| 기능 | 실행 시점 | 적합한 작업 |
| --- | --- | --- |
| Custom content action | 사용자가 panel/dashboard에서 실행 | metadata 일괄 보정, report 생성 |
| Field action | 특정 field에서 실행 | title, slug, summary 생성 |
| Placeholder script | 문서 생성 중 값 계산 | ID, category 질문 |
| `postScript` | 새 문서 생성 직후 | front matter 후처리 |
| Media action | media file/folder에서 실행 | image 변환, metadata 처리 |

## Custom script 설정

```json
{
  "frontMatter.custom.scripts": [
    {
      "id": "normalize-frontmatter",
      "title": "Normalize front matter",
      "script": "./.frontmatter/scripts/normalize.py",
      "command": "python",
      "type": "content",
      "bulk": true,
      "output": "notification",
      "hidden": false,
      "contentTypes": [
        "guide",
        "runbook"
      ]
    }
  ]
}
```

## 주요 속성

| 속성 | 역할 |
| --- | --- |
| `id` | script 식별자 |
| `title` | UI label |
| `script` | script path |
| `command` | `node`, `python`, `bash` 등 |
| `type` | `content`, `mediaFile`, `mediaFolder` |
| `bulk` | 여러 항목 처리 |
| `output` | `notification` 또는 `editor` |
| `outputType` | `text`, `html`, `markdown` |
| `hidden` | UI에서 숨김 |
| `contentTypes` | 적용 content type 제한 |
| `environments` | OS별 script/command override |

## Content type의 postScript

```json
{
  "name": "guide",
  "template": "[[workspace]]/.frontmatter/templates/guide.md",
  "postScript": "normalize-frontmatter",
  "fields": []
}
```

`postScript` 값은 `frontMatter.custom.scripts`의 `id`와 일치해야 한다.

## JavaScript extensibility

공식 package를 사용하는 JavaScript script는 현재 파일의 front matter를 읽거나 갱신할 수 있다.

```js
import { ContentScript } from "@frontmatter/extensibility";

const { frontMatter } = ContentScript.getArguments();

ContentScript.updateFrontMatter({
  ...frontMatter,
  normalized: true,
});
```

Python, Bash, PowerShell 등도 `command`를 지정해 사용할 수 있다.

## OS별 실행

```json
{
  "id": "build-index",
  "title": "Build index",
  "script": "./.frontmatter/scripts/build-index.sh",
  "command": "bash",
  "environments": [
    {
      "type": "windows",
      "script": "./.frontmatter/scripts/build-index.ps1",
      "command": "powershell"
    }
  ]
}
```

## 안전 규칙

- repository script는 실행 코드다. 출처와 diff를 검토한다.
- 외부 입력을 shell command에 그대로 삽입하지 않는다.
- 가능하면 workspace-relative path를 사용한다.
- bulk action은 dry-run 또는 변경 목록 출력을 제공한다.
- script가 수정하는 field를 명시한다.
- 실패 시 부분 수정 상태를 남기지 않도록 설계한다.
- CI와 editor에서 같은 runtime/version을 사용한다.
- agent는 script 존재 여부와 config 연결을 함께 확인한다.

## 언제 script를 쓰지 않는가

다음은 schema나 template로 먼저 해결한다.

- 고정 default 값
- content type 식별자
- 필수 field
- enum 선택
- 단순 folder routing
- 정적 본문 skeleton

script는 계산, 외부 조회, 일괄 변경처럼 선언형 설정으로 해결하기 어려운 작업에만 사용한다.

## 공식 출처

- [Custom actions and scripts](https://frontmatter.codes/docs/custom-actions)
- [Content scripts](https://frontmatter.codes/docs/custom-actions/content-scripts)
- [Field actions](https://frontmatter.codes/docs/content-creation/field-actions)
- [Sample scripts](https://frontmatter.codes/docs/custom-actions/sample-scripts)
