import re
from typing import Final

from core.schema import FrontmatterField

ALLOWED_RESOURCES: Final[set[str]] = {
    "scripts",
    "references",
    "assets",
    "prompts",
    "configs",
    "workflows",
}

NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

COMMON_NAME_FIELD: Final[FrontmatterField] = FrontmatterField(
    "name",
    is_required=True,
    max_length=64,
    regex_pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    regex_message="name은 소문자 영문, 숫자, 단일 하이픈만 사용할 수 있습니다.",
)

COMMON_DESCRIPTION_FIELD: Final[FrontmatterField] = FrontmatterField(
    "description",
    is_required=True,
    max_length=1024,
)

DEFAULT_AGENT_DESCRIPTION: Final[str] = (
    "TODO: Describe the persona, goal, and responsibilities of this agent. Use to "
    "instantiate specialized sub-agents or define main orchestrators."
)

DEFAULT_RULE_DESCRIPTION: Final[str] = (
    "TODO: Describe what this rule restricts, enforces, or guides. Use when the agent "
    "needs to adhere to specific protocols, coding styles, or behavior limits."
)

DEFAULT_SKILL_DESCRIPTION: Final[str] = (
    "TODO: Describe what this skill does and when to use it. Use when the user "
    "asks for tasks, workflows, files, or domain work covered by this skill."
)
