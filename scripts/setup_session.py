import shutil
import subprocess
import sys


def check_command(cmd: str) -> bool:
    """명령이 PATH에 있는지 확인합니다."""
    return shutil.which(cmd) is not None


def sync_dependencies():
    """uv로 Python 의존성을 동기화합니다."""
    if not check_command("uv"):
        print("[1/2] Warning: 'uv' command not found. Skipping dependency sync.")
        return
    print("[1/2] Syncing python dependencies with uv...")
    subprocess.run(["uv", "sync"], check=True)


def sync_agent_skills():
    """repository task로 외부 Agent Skill dependency를 동기화합니다."""
    if not check_command("mise"):
        print("[2/2] Warning: 'mise' command not found. Skipping skill sync.")
        return
    print("[2/2] Syncing locked agent skill dependencies...")
    try:
        subprocess.run(["mise", "run", "skills-sync"], check=True)
    except subprocess.CalledProcessError:
        print("Warning: skill sync encountered an issue, skipping.")


def main():
    print("===========================================")
    print("  Initializing Workspace Session Environment")
    print("===========================================")
    try:
        sync_dependencies()
        sync_agent_skills()
    except subprocess.CalledProcessError as error:
        print(
            f"\nError: Initialization failed during subprocess execution: {error}",
            file=sys.stderr,
        )
        sys.exit(1)
    print("===========================================")
    print("  Initialization Complete!")
    print("===========================================")


if __name__ == "__main__":
    main()
