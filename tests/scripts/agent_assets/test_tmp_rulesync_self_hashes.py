from __future__ import annotations

from scripts.agent_assets import routes_distribution_generate as distribution
from scripts.agent_assets import routes_repository_generate as repository


def test_emit_generated_routes() -> None:
    distribution_outputs = distribution.generate()
    print("DISTRIBUTION_SKILLS_BEGIN")
    print(distribution_outputs[distribution.DISTRIBUTION_SKILL_ROUTE], end="")
    print("DISTRIBUTION_SKILLS_END")

    repository_outputs = repository.generate()
    for path, content in sorted(repository_outputs.items(), key=lambda item: str(item[0])):
        print(f"REPOSITORY_ROUTE_BEGIN {path.name}")
        print(content, end="")
        print(f"REPOSITORY_ROUTE_END {path.name}")

    raise AssertionError("generated route diagnostic")
