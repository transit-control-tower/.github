"""Validate tracked files without importing code or contacting services."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root
    ).decode("utf-8").split("\0")
    failures = []
    checked = 0
    for relative in filter(None, tracked):
        file = root / relative
        suffix = file.suffix.lower()
        if suffix not in {".py", ".json", ".svg"}:
            continue
        try:
            if suffix == ".py":
                ast.parse(file.read_text(encoding="utf-8-sig"), filename=relative)
            elif suffix == ".json":
                json.loads(file.read_text(encoding="utf-8-sig"))
            else:
                ET.parse(file)
            checked += 1
        except (OSError, ValueError, SyntaxError, ET.ParseError) as error:
            # Avoid echoing potentially sensitive source contents.
            failures.append(f"{relative}: {type(error).__name__}")
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"Repository checks: {checked} files passed, {len(failures)} failed")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
