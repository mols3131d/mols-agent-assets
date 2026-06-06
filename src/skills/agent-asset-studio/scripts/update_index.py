#!/usr/bin/env python3
"""Routing Skill의 INDEX.csv 관리 스크립트."""

import csv
from pathlib import Path

HEADERS = ["name", "overview", "keywords", "trigger", "exclusion"]


def init_index(path: Path) -> None:
    """INDEX.csv 파일이 없으면 헤더와 함께 초기화한다."""
    if not path.exists():
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def valid_index(path: Path) -> bool:
    """INDEX.csv 파일의 유효성(존재 여부 및 헤더 일치)을 검증한다."""
    if not path.exists():
        return False
    
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers != HEADERS:
                return False
    except (csv.Error, IOError):
        return False
        
    return True


def update_index(path: Path, data: dict[str, str]) -> None:
    """INDEX.csv에 새로운 행을 추가하거나 기존 행(name 기준)을 업데이트한다."""
    if not valid_index(path):
        init_index(path)
        
    rows = []
    updated = False
    
    # 기존 행 읽기
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("name") == data.get("name"):
                # 기존 행 업데이트
                for key in HEADERS:
                    if key in data:
                        row[key] = data[key]
                updated = True
            rows.append(row)
            
    # 업데이트되지 않았다면 새로 추가
    if not updated:
        new_row = {key: data.get(key, "") for key in HEADERS}
        rows.append(new_row)
        
    # 변경사항 다시 쓰기
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    pass
