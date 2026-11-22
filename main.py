#!/usr/bin/env python3
"""news-image-20261122 entry program.

The repository holds the finished front page as entry.png (drawn by
make_image.py from the day's reported news). This program's whole job is
to place that image at the output path the grader expects, byte for byte,
with nothing but the Python 3.13 standard library.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    with open(SOURCE, "rb") as fh:
        head = fh.read(8)
    if head[:4] != b"\x89PNG":
        print("entry.png is missing or not a PNG", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
