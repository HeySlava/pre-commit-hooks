from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    ret = 0
    for filename in args.filenames:
        path = Path(filename)
        if path.name != '__init__.py':
            continue
        if path.read_text(encoding='utf-8').strip():
            print(f'{filename}: __init__.py must be empty')
            ret = 1
    return ret


if __name__ == '__main__':
    sys.exit(main())
