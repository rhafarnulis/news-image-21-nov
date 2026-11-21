#!/usr/bin/env python3
"""Entry point for the news-image-20261121 competition.

The front page itself is drawn by draw_frontpage.py and shipped in
this repository as entry.png. This program only copies those exact
bytes to the output directory, so two runs always produce identical
output. Standard library only; no network.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
