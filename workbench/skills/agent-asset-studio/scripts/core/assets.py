from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Sequence

from configs import agent, rule, skill
from core.base import Asset, AssetInitOptions, Validator
from core.validators import (
    AssetBodyLengthValidator,
    FrontmatterValidator,
    RoutingSkillValidator,
    SkillTriggerValidator,
)
from templates import (
    AGENT_TEMPLATE,
    EXAMPLE_REFERENCE,
    EXAMPLE_SCRIPT,
    ROUTING_SKILL_TEMPLATE,
    RULE_TEMPLATE,
    SKILL_TEMPLATE,
)

EXAMPLE_ASSET = """이 파일은 실제 템플릿, 이미지, 설정 예시 같은 정적 자산으로 교체한다.
사용하지 않으면 `assets/`와 함께 삭제한다.
"""


def write_text(path: Path, content: str, executable: bool = False) -> None:
    """텍스트 파일을 쓰고 필요시 실행 권한을 설정한다."""
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def yaml_quote(value: str) -> str:
    """YAML 스칼라 값을 적절하게 이스케이프한다."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def title_case_name(name: str) -> str:
    """kebab-case 명칭을 가독성 높은 제목으로 변환한다."""
    return " ".join(part.capitalize() for part in name.split("-") if part)


def build_optional_frontmatter(
    license_val: str | None,
    compatibility: str | None,
    metadata: dict[str, str],
    allowed_tools: str | None,
) -> str:
    """공통 Frontmatter YAML 문자열을 조립한다."""
    lines: list[str] = []
    if license_val:
        lines.append(f"license: {yaml_quote(license_val)}")
    if compatibility:
        lines.append(f"compatibility: {yaml_quote(compatibility)}")
    if metadata:
        lines.append("metadata:")
        for key in sorted(metadata):
            lines.append(f"  {key}: {yaml_quote(metadata[key])}")
    if allowed_tools:
        lines.append(f"allowed-tools: {yaml_quote(allowed_tools)}")
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


EXAMPLE_FILES = {
    "scripts": ("example.py", EXAMPLE_SCRIPT, True),
    "references": ("reference.md", EXAMPLE_REFERENCE, False),
    "assets": ("example.txt", EXAMPLE_ASSET, False),
}


def build_resource_notes(resources: Sequence[str], include_examples: bool) -> str:
    """선택한 리소스 사양에 부합하는 가이드 마크다운을 렌더링한다."""
    if not resources:
        return "현재 선택된 리소스 디렉터리는 없다. 필요한 경우에만 추가한다."

    lines: list[str] = []
    if "scripts" in resources:
        lines.append("- `scripts/`: 반복 실행 또는 결정적 처리가 필요한 명령을 둔다.")
        if include_examples:
            lines.append(
                "- `scripts/example.py`: 예시 스크립트다. "
                "실제 로직으로 교체하거나 삭제한다."
            )
    if "references" in resources:
        lines.append("- `references/`: 조건부로 읽을 상세 문서를 둔다.")
        if include_examples:
            lines.append("- 상세 참조가 필요하면 `references/reference.md`를 읽는다.")
    if "assets" in resources:
        lines.append("- `assets/`: 산출물에 복사하거나 삽입할 정적 자산을 둔다.")
        if include_examples:
            lines.append(
                "- `assets/example.txt`: 예시 자산이다. "
                "실제 자산으로 교체하거나 삭제한다."
            )
    if "prompts" in resources:
        lines.append(
            "- `prompts/`: 에이전트 지시에 필요한 세부 프롬프트 템플릿을 보관한다."
        )
    if "configs" in resources:
        lines.append("- `configs/`: 에이전트 기동 설정 및 환경 옵션을 둔다.")
    if "workflows" in resources:
        lines.append("- `workflows/`: INDEX.csv가 가리키는 workflow module을 둔다.")
    return "\n".join(lines)


def create_resource_dirs(
    asset_dir: Path, resources: Sequence[str], include_examples: bool
) -> list[str]:
    """자산 하위에 지정된 리소스 디렉터리와 예제 뼈대 파일을 생성한다."""
    created: list[str] = []
    for resource in resources:
        resource_dir = asset_dir / resource
        resource_dir.mkdir(exist_ok=True)
        created.append(resource_dir.relative_to(asset_dir).as_posix() + "/")

        if not include_examples:
            continue

        example = EXAMPLE_FILES.get(resource)
        if example is None:
            continue

        example_filename, example_content, executable = example
        example_path = resource_dir / example_filename
        write_text(example_path, example_content, executable=executable)
        created.append(example_path.relative_to(asset_dir).as_posix())
    return created


def run_base_initialization(
    asset: Asset,
    options: AssetInitOptions,
) -> dict[str, Any]:
    """모든 자산이 공통으로 사용하는 디렉터리 구성 및 초기화 핵심 메커니즘."""
    filename = asset.get_filename()
    asset_dir = asset.path

    planned_files = [filename]
    resources = list(options.resources)
    if options.routing_skill:
        planned_files.append("INDEX.csv")
        if "workflows" not in resources:
            resources.append("workflows")

    for resource in resources:
        planned_files.append(f"{resource}/")
        example = EXAMPLE_FILES.get(resource)
        if options.include_examples and example is not None:
            planned_files.append(f"{resource}/{example[0]}")

    if options.dry_run:
        return {
            "status": "dry_run",
            "asset_type": asset.asset_type,
            "name": asset.name,
            "asset_dir": str(asset_dir),
            "planned": planned_files,
        }

    if asset_dir.exists():
        raise FileExistsError(f"자산 디렉터리가 이미 있습니다: {asset_dir}")

    asset_dir.mkdir(parents=True, exist_ok=False)

    # 템플릿 마크다운 렌더링
    title = title_case_name(asset.name)
    frontmatter = build_optional_frontmatter(
        options.license_val,
        options.compatibility,
        options.metadata,
        options.allowed_tools,
    )
    resource_notes = build_resource_notes(resources, options.include_examples)

    file_content = asset.select_template(options).format(
        skill_name=asset.name,
        rule_name=asset.name,
        agent_name=asset.name,
        skill_title=title,
        rule_title=title,
        agent_title=title,
        description=yaml_quote(options.description),
        optional_frontmatter=frontmatter,
        resource_notes=resource_notes,
    )

    write_text(asset_dir / filename, file_content)
    created = [filename]
    if options.routing_skill:
        index_content = ",".join(skill.ROUTE_INDEX_FIELDS) + "\n"
        write_text(asset_dir / "INDEX.csv", index_content)
        created.append("INDEX.csv")
    created.extend(create_resource_dirs(asset_dir, resources, options.include_examples))

    return {
        "status": "created",
        "asset_type": asset.asset_type,
        "name": asset.name,
        "asset_dir": str(asset_dir),
        "created": created,
        "next_steps": [
            f"{filename}의 TODO와 본문 내용을 실제 내용으로 채운다.",
            "사용하지 않는 예시 파일과 리소스 디렉터리를 정리한다.",
        ],
    }


class TemplateAsset(Asset):
    """템플릿 기반 자산의 공통 동작."""

    asset_type: ClassVar[str]
    filename: ClassVar[str]
    config: ClassVar[Any]
    template: ClassVar[str]
    validators: ClassVar[Sequence[type[Validator]]]

    def get_filename(self) -> str:
        return self.filename

    def get_validators(self) -> list[Validator]:
        return [validator() for validator in self.validators]

    def initialize(self, options: AssetInitOptions) -> dict[str, Any]:
        return run_base_initialization(self, options)


class SkillAsset(TemplateAsset):
    """에이전트가 호출해 특정 태스크를 완수하는 스킬 자산 클래스."""

    asset_type = "skill"
    filename = "SKILL.md"
    config = skill
    template = SKILL_TEMPLATE
    validators = [
        FrontmatterValidator,
        SkillTriggerValidator,
        AssetBodyLengthValidator,
        RoutingSkillValidator,
    ]

    def select_template(self, options: AssetInitOptions) -> str:
        if options.routing_skill:
            return ROUTING_SKILL_TEMPLATE
        return self.template


class RuleAsset(TemplateAsset):
    """에이전트 준수 기준 및 프로토콜을 통제하는 규칙 자산 클래스."""

    asset_type = "rule"
    filename = "RULE.md"
    config = rule
    template = RULE_TEMPLATE
    validators = [
        FrontmatterValidator,
        AssetBodyLengthValidator,
    ]


class AgentAsset(TemplateAsset):
    """특수 역할과 페르소나를 탑재한 에이전트 자산 클래스."""

    asset_type = "agent"
    filename = "AGENT.md"
    config = agent
    template = AGENT_TEMPLATE
    validators = [
        FrontmatterValidator,
        AssetBodyLengthValidator,
    ]
