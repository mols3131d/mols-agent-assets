import os
import sys
from datetime import datetime

LOG_FILE = ".agents/brain/evolution.md"
MAX_ENTRIES = 10

def suggest(candidate, priority):
    date_str = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"| {date_str} | {candidate} | {priority} |"
    
    lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    # Header check
    if not lines or "| 날짜" not in lines[0]:
        lines = [
            "| 날짜       | 지침 (Candidate)                   | 편입 추천  |\n",
            "| :--------- | :--------------------------------- | :--------- |\n"
        ]
    
    # Add new entry
    lines.append(new_entry + "\n")
    
    # FIFO Cleanup: keep header (2 lines) + last MAX_ENTRIES
    header = lines[:2]
    data = lines[2:]
    if len(data) > MAX_ENTRIES:
        data = data[-MAX_ENTRIES:]
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(header + data)
    
    print(f"Success: Added candidate to {LOG_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python suggest_evolution.py \"candidate description\" [상|중|하]")
    else:
        suggest(sys.argv[1], sys.argv[2])
