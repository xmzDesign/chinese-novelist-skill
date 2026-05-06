#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    return subprocess.call([sys.executable, str(root / "scripts" / "novel_runtime_hook.py"), "--mode", "post-tool"])


if __name__ == "__main__":
    raise SystemExit(main())
