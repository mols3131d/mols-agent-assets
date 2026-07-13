#!/usr/bin/env python3
import argparse
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze a git diff and suggest appropriate reviewer sub-skills."
    )
    parser.add_argument(
        "--diff-file",
        help="Path to a file containing git diff output. If not provided, reads from stdin.",
    )
    parser.add_argument(
        "--git",
        nargs="?",
        const="HEAD",
        help="Run 'git diff' on the specified ref (defaults to HEAD).",
    )
    return parser.parse_args()


def get_diff_content(args):
    if args.git:
        import subprocess

        try:
            cmd = ["git", "diff", args.git]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {e}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: 'git' command not found in PATH.", file=sys.stderr)
            sys.exit(1)
    elif args.diff_file:
        try:
            with open(args.diff_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading diff file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print(
                "No input provided. Pipe a diff to stdin or use --git / --diff-file.",
                file=sys.stderr,
            )
            sys.exit(1)
        return sys.stdin.read()


def analyze_diff(diff_text):
    # Regex to capture file paths in git diff
    # Format: a/path/to/file b/path/to/file or rename from/to
    file_headers = re.findall(r"^diff --git a/(.*?) b/(.*?)$", diff_text, re.MULTILINE)

    modified_files = []
    for a_path, b_path in file_headers:
        if b_path not in modified_files:
            modified_files.append(b_path)

    # Check for renamed/deleted/added files in the diff headers
    new_files = re.findall(
        r"^new file mode \d+\nindex .*?\n--- /dev/null\n\+\+\+ b/(.*?)$",
        diff_text,
        re.MULTILINE,
    )
    deleted_files = re.findall(
        r"^deleted file mode \d+\nindex .*?\n--- a/(.*?)\n\+\+\+ /dev/null$",
        diff_text,
        re.MULTILINE,
    )

    categories = {
        "audit-architecture": {"files": [], "reasons": []},
        "audit-implementation": {"files": [], "reasons": []},
        "audit-performance": {"files": [], "reasons": []},
        "audit-security": {"files": [], "reasons": []},
        "audit-tests": {"files": [], "reasons": []},
    }

    # Analyze file paths
    for f in modified_files:
        # Architecture detection: folder changes, structural configurations, or naming conventions
        # e.g., router configuration, project layout configs, directory addition
        f_lower = f.lower()

        # Test detection: test files or spec files
        if any(
            term in f_lower for term in ["test", "spec", "mock"]
        ) or f_lower.endswith("_test.go"):
            categories["audit-tests"]["files"].append(f)
            if "Test file modified/added" not in categories["audit-tests"]["reasons"]:
                categories["audit-tests"]["reasons"].append("Test file modified/added")
            continue

        # Otherwise, classify implementation
        categories["audit-implementation"]["files"].append(f)
        if (
            "Implementation file modified/added"
            not in categories["audit-implementation"]["reasons"]
        ):
            categories["audit-implementation"]["reasons"].append(
                "Implementation file modified/added"
            )

        # Check path for architecture patterns
        if "/" not in f:
            categories["audit-architecture"]["files"].append(f)
            categories["audit-architecture"]["reasons"].append(
                f"Root file modified: {f}"
            )
        elif any(
            part in f_lower.split("/")
            for part in [
                "router",
                "handler",
                "controller",
                "repository",
                "service",
                "infrastructure",
            ]
        ):
            categories["audit-architecture"]["files"].append(f)
            categories["audit-architecture"]["reasons"].append(
                f"Architectural component modified in path: {f}"
            )

    # Parse individual diff lines for keywords
    current_file = None
    line_number = 0

    # Simple regexes for scanning added lines
    sec_keywords = [
        (
            re.compile(
                r"\b(password|passwd|secret|token|api[-_]?key|private[-_]?key|credential)\b",
                re.IGNORECASE,
            ),
            "Potential credential/secret leak",
        ),
        (
            re.compile(r"\b(eval|exec|system|popen)\b"),
            "Unsafe command execution function",
        ),
        (
            re.compile(r"\b(unsafe|innerHTML|dangerouslySetInnerHTML)\b"),
            "Potential unsafe execution or XSS risk",
        ),
    ]

    perf_keywords = [
        (
            re.compile(
                r"\b(select\s+\*|insert\s+into|update\s+|delete\s+from)\b",
                re.IGNORECASE,
            ),
            "SQL Query found (verify index and N+1 query safety)",
        ),
        (
            re.compile(
                r"\b(while\s*\(true\)|for\s+.*\b(in|of)\b.*inside\s+loop|nested\s+loops)\b",
                re.IGNORECASE,
            ),
            "Potential loop efficiency check needed",
        ),
    ]

    lines = diff_text.splitlines()
    for line in lines:
        if line.startswith("+++ b/"):
            current_file = line[6:]
            line_number = 0
            continue
        elif line.startswith("@@"):
            # Try to get starting line number
            match = re.search(r"\+(\d+)", line)
            if match:
                line_number = int(match.group(1)) - 1
            continue

        # If we have a file context and it's an added line
        if current_file and line.startswith("+") and not line.startswith("+++"):
            line_number += 1
            content = line[1:]

            # Check security keywords
            for pattern, desc in sec_keywords:
                if pattern.search(content):
                    categories["audit-security"]["files"].append(current_file)
                    categories["audit-security"]["reasons"].append(
                        f"{desc} in {current_file}:{line_number}"
                    )

            # Check performance keywords
            for pattern, desc in perf_keywords:
                if pattern.search(content):
                    categories["audit-performance"]["files"].append(current_file)
                    categories["audit-performance"]["reasons"].append(
                        f"{desc} in {current_file}:{line_number}"
                    )

    # Post process duplicates
    for cat in categories:
        categories[cat]["files"] = sorted(list(set(categories[cat]["files"])))
        categories[cat]["reasons"] = sorted(list(set(categories[cat]["reasons"])))

    return categories, new_files, deleted_files


def main():
    args = parse_args()
    diff_text = get_diff_content(args)

    if not diff_text.strip():
        print("Diff is empty.")
        return

    categories, new_files, deleted_files = analyze_diff(diff_text)

    print("# Diff Analysis Summary")
    print(f"\n- **New files**: {len(new_files)}")
    for nf in new_files:
        print(f"  - `{nf}`")
    print(f"- **Deleted files**: {len(deleted_files)}")
    for df in deleted_files:
        print(f"  - `{df}`")

    print("\n## Recommended Review Sub-Skills")

    recommended_any = False
    for cat, info in categories.items():
        if info["files"]:
            recommended_any = True
            print(f"\n### 🎯 `{cat}`")
            print("**Reasons / Triggers detected**:")
            for r in info["reasons"]:
                print(f"- {r}")
            print("**Files to inspect**:")
            for f in info["files"][:5]:  # Limit to top 5
                print(f"- `{f}`")
            if len(info["files"]) > 5:
                print(f"- ... and {len(info['files']) - 5} more files.")

    if not recommended_any:
        print(
            "\nNo specific triggers matched. Standard `audit-implementation` suggested for general sanity check."
        )


if __name__ == "__main__":
    main()
