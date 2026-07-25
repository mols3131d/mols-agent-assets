import importlib.metadata

import check_dependencies


def test_check_dependencies_passes_when_requirements_are_available(monkeypatch):
    monkeypatch.setattr(
        check_dependencies.tomllib,
        "load",
        lambda _: {
            "project": {"requires-python": ">=3.0", "dependencies": ["demo>=1"]}
        },
    )
    monkeypatch.setattr(check_dependencies.importlib.metadata, "version", lambda _: "1")
    monkeypatch.setattr(check_dependencies.shutil, "which", lambda _: "/bin/tool")

    assert check_dependencies.main() == 0


def test_check_dependencies_reports_missing_package_and_tool(monkeypatch, capsys):
    monkeypatch.setattr(
        check_dependencies.tomllib,
        "load",
        lambda _: {
            "project": {
                "requires-python": ">=3.0",
                "dependencies": ["missing>=1"],
            }
        },
    )
    monkeypatch.setattr(
        check_dependencies.importlib.metadata,
        "version",
        lambda _: (_ for _ in ()).throw(importlib.metadata.PackageNotFoundError),
    )
    monkeypatch.setattr(check_dependencies.shutil, "which", lambda _: None)

    assert check_dependencies.main() == 1
    assert "Missing dependency: missing" in capsys.readouterr().err
